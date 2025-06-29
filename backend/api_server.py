#!/usr/bin/env python3
"""Production-ready API server with enhanced search"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import sys
import os

sys.path.append('.')
from enhanced_search import EnhancedYaleSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Yale Network Search API",
    description="AI-powered search for Yale people, inspired by happenstance.ai",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine
search_engine = EnhancedYaleSearch()

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 20

class PersonResult(BaseModel):
    uuid: str
    name: str
    location: Optional[str]
    headline: Optional[str]
    current_position: Optional[Dict[str, str]]
    yale_info: Optional[Dict[str, str]]
    linkedin_url: Optional[str]
    score: float
    match_reasons: List[str]
    matched_terms: Dict[str, List[str]]

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[PersonResult]
    query_analysis: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Yale Network Search API",
        "description": "AI-powered search for Yale people",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "stats": "/stats", 
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        count = search_engine.db.execute("SELECT COUNT(*) FROM people").scalar()
        return {
            "status": "healthy",
            "database": "connected", 
            "total_people": count
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")

@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        stats = {}
        
        # Total people
        stats['total_people'] = search_engine.db.execute(
            "SELECT COUNT(*) FROM people"
        ).scalar()
        
        # Yale people
        stats['yale_people'] = search_engine.db.execute(
            "SELECT COUNT(DISTINCT p.uuid_id) FROM people p JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id"
        ).scalar()
        
        # By affiliation type
        affiliation_stats = search_engine.db.execute("""
            SELECT ya.affiliation_type, COUNT(*) 
            FROM yale_affiliations ya 
            GROUP BY ya.affiliation_type
            ORDER BY COUNT(*) DESC
        """).fetchall()
        
        stats['by_affiliation'] = {row[0]: row[1] for row in affiliation_stats}
        
        # Top locations
        location_stats = search_engine.db.execute("""
            SELECT p.location, COUNT(*) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            WHERE p.location IS NOT NULL AND p.location != ''
            GROUP BY p.location 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """).fetchall()
        
        stats['top_locations'] = {row[0]: row[1] for row in location_stats}
        
        # Top Yale schools
        school_stats = search_engine.db.execute("""
            SELECT ya.school, COUNT(*) 
            FROM yale_affiliations ya 
            WHERE ya.school IS NOT NULL AND ya.school != ''
            GROUP BY ya.school 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """).fetchall()
        
        stats['top_yale_schools'] = {row[0]: row[1] for row in school_stats}
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {e}")

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Enhanced search endpoint"""
    
    if not request.query or len(request.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
    if request.limit and (request.limit < 1 or request.limit > 100):
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    try:
        # Execute search
        results = search_engine.search(request.query, limit=request.limit or 20)
        
        # Parse query for analysis
        parsed = search_engine.parse_query(request.query)
        
        # Convert results to response format
        person_results = []
        for result in results:
            person = result.person
            
            # Current position
            current_position = None
            current_exp = next((e for e in person.experiences if e.is_current), None)
            if current_exp:
                current_position = {
                    "title": current_exp.title,
                    "company": current_exp.company
                }
            
            # Yale info
            yale_info = None
            if person.yale_affiliations:
                yale_aff = person.yale_affiliations[0]
                yale_info = {
                    "school": yale_aff.school,
                    "affiliation_type": yale_aff.affiliation_type,
                    "major": yale_aff.major
                }
            
            person_result = PersonResult(
                uuid=str(person.uuid_id),
                name=person.full_name,
                location=person.location,
                headline=person.headline,
                current_position=current_position,
                yale_info=yale_info,
                linkedin_url=person.linkedin_url,
                score=result.score,
                match_reasons=result.match_reasons,
                matched_terms=result.matched_terms
            )
            person_results.append(person_result)
        
        return SearchResponse(
            query=request.query,
            total_results=len(person_results),
            results=person_results,
            query_analysis=parsed
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

@app.get("/search")
async def search_get(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """GET version of search endpoint for easy testing"""
    request = SearchRequest(query=q, limit=limit)
    return await search(request)

# Example queries endpoint
@app.get("/examples")
async def get_example_queries():
    """Get example search queries"""
    return {
        "examples": [
            "Yale VC investors in NYC",
            "Yale entrepreneurs and founders", 
            "Yale SOM graduates working in finance",
            "Yale people in Connecticut",
            "Yale computer science graduates",
            "Yale professors and academics",
            "Yale alumni working at tech companies",
            "Yale law school graduates",
            "Yale medical school doctors",
            "Yale founders in San Francisco"
        ],
        "tips": [
            "Be specific about location (NYC, San Francisco, Boston)",
            "Include role types (VC, founder, professor, doctor)",
            "Mention Yale schools (SOM, Law School, Medical School)",
            "Use industry terms (tech, finance, healthcare, education)"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🎓 Starting Yale Network Search API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    print("🔍 Example search: http://localhost:8000/search?q=Yale%20people%20in%20Connecticut")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")