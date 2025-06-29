#!/usr/bin/env python3
"""
AI-Enhanced API Server for Yale Network Search
Includes AI-generated summaries and tags in search results
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import sys
import os

sys.path.append('.')
from search_api import YaleNetworkSearch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Yale Network Search API - AI Enhanced",
    description="AI-powered search for Yale people with AI-generated summaries and tags",
    version="2.0.0"
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
search_engine = YaleNetworkSearch()

class SearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 20

class PersonResult(BaseModel):
    uuid_id: str
    name: str
    headline: Optional[str]
    location: Optional[str]
    summary: Optional[str]
    ai_summary: Optional[str]
    ai_tags: Optional[List[str]]
    ai_processed: Optional[bool]
    yale_school: Optional[str]
    major: Optional[str]
    class_year: Optional[int]
    affiliation_type: Optional[str]
    profile_url: Optional[str]
    relevance_score: float

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[PersonResult]
    filters_detected: Dict[str, Any]
    search_time_ms: int

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Yale Network Search API - AI Enhanced",
        "description": "AI-powered search for Yale people with AI-generated summaries and tags",
        "version": "2.0.0",
        "features": [
            "Natural language query parsing",
            "AI-generated profile summaries", 
            "AI-generated profile tags",
            "Relevance scoring with AI content",
            "14,412+ Yale profiles"
        ],
        "endpoints": {
            "search": "/search (POST) or /search?q=query (GET)",
            "stats": "/stats", 
            "health": "/health",
            "examples": "/examples"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from sqlalchemy import create_engine, text
        from dotenv import load_dotenv
        
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Test database connection
            total_count = conn.execute(text("SELECT COUNT(*) FROM people")).scalar()
            ai_enhanced_count = conn.execute(text("SELECT COUNT(*) FROM people WHERE ai_processed = TRUE")).scalar()
            
        return {
            "status": "healthy",
            "database": "connected", 
            "total_people": total_count,
            "ai_enhanced_profiles": ai_enhanced_count,
            "ai_enhancement_progress": f"{ai_enhanced_count/total_count*100:.1f}%" if total_count > 0 else "0%"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")

@app.get("/stats")
async def get_stats():
    """Get database statistics including AI enhancement progress"""
    try:
        from sqlalchemy import create_engine, text
        from dotenv import load_dotenv
        
        load_dotenv()
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            stats = {}
            
            # Basic stats
            stats['total_people'] = conn.execute(text("SELECT COUNT(*) FROM people")).scalar()
            stats['yale_people'] = conn.execute(text(
                "SELECT COUNT(DISTINCT p.uuid_id) FROM people p JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id"
            )).scalar()
            
            # AI enhancement stats
            stats['ai_enhanced_profiles'] = conn.execute(text(
                "SELECT COUNT(*) FROM people WHERE ai_processed = TRUE"
            )).scalar()
            stats['ai_enhancement_progress'] = f"{stats['ai_enhanced_profiles']/stats['total_people']*100:.1f}%"
            
            # Top Yale schools
            school_stats = conn.execute(text("""
                SELECT ya.school, COUNT(*) 
                FROM yale_affiliations ya 
                WHERE ya.school IS NOT NULL AND ya.school != ''
                GROUP BY ya.school 
                ORDER BY COUNT(*) DESC 
                LIMIT 10
            """)).fetchall()
            stats['top_yale_schools'] = {row[0]: row[1] for row in school_stats}
            
            # AI tag analysis (if any profiles are enhanced)
            if stats['ai_enhanced_profiles'] > 0:
                # Get most common AI tags
                tag_stats = conn.execute(text("""
                    SELECT tag, COUNT(*) as count
                    FROM (
                        SELECT jsonb_array_elements_text(ai_tags) as tag
                        FROM people 
                        WHERE ai_tags IS NOT NULL
                    ) tags
                    GROUP BY tag
                    ORDER BY count DESC
                    LIMIT 10
                """)).fetchall()
                stats['top_ai_tags'] = {row[0]: row[1] for row in tag_stats}
            
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {e}")

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """AI-enhanced search endpoint"""
    
    if not request.query or len(request.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
    if request.limit and (request.limit < 1 or request.limit > 100):
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    try:
        # Execute search using our enhanced search API
        import time
        start_time = time.time()
        
        results = search_engine.search(request.query, limit=request.limit or 20)
        
        search_time_ms = int((time.time() - start_time) * 1000)
        
        # Convert to response format
        person_results = []
        for person_data in results['results']:
            person_result = PersonResult(
                uuid_id=str(person_data['uuid_id']),
                name=person_data['name'],
                headline=person_data['headline'],
                location=person_data['location'],
                summary=person_data['summary'],
                ai_summary=person_data['ai_summary'],
                ai_tags=person_data['ai_tags'],
                ai_processed=person_data['ai_processed'],
                yale_school=person_data['yale_school'],
                major=person_data['major'],
                class_year=person_data['class_year'],
                affiliation_type=person_data['affiliation_type'],
                profile_url=person_data['profile_url'],
                relevance_score=person_data['relevance_score']
            )
            person_results.append(person_result)
        
        return SearchResponse(
            query=request.query,
            total_results=results['total_found'],
            results=person_results,
            filters_detected=results['filters_detected'],
            search_time_ms=search_time_ms
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

@app.get("/examples")
async def get_example_queries():
    """Get example search queries"""
    return {
        "natural_language_examples": [
            "students studying artificial intelligence at Yale",
            "people with data science experience", 
            "computer science majors",
            "Yale School of Medicine students",
            "research fellows at Yale",
            "environmental management students",
            "statistics data science graduates"
        ],
        "simple_examples": [
            "data science",
            "medicine",
            "computer science",
            "research",
            "management",
            "psychology",
            "economics"
        ],
        "tips": [
            "Use natural language: 'students studying AI' works great",
            "Try field-specific terms: 'data science', 'medicine', 'law'",
            "Include Yale schools: 'Yale School of Medicine', 'SOM'",
            "AI summaries and tags enhance search relevance"
        ],
        "ai_features": [
            "AI-generated summaries provide clear, engaging descriptions",
            "AI tags categorize profiles for better discovery",
            "AI content is included in relevance scoring",
            "Enhanced profiles show ai_processed: true"
        ]
    }

@app.post("/enhance-batch")
async def enhance_batch(limit: Optional[int] = 50):
    """Trigger AI enhancement for unprocessed profiles"""
    try:
        from batch_ai_enhancement import BatchAIEnhancer
        
        logger.info(f"Starting batch AI enhancement for {limit} profiles")
        
        enhancer = BatchAIEnhancer(batch_size=10)
        enhancer.run_batch_enhancement(max_profiles=limit)
        
        return {
            "message": f"Successfully enhanced {enhancer.processed_count} profiles",
            "processed": enhancer.processed_count,
            "errors": enhancer.error_count,
            "estimated_cost": f"${enhancer.processed_count * 0.0002:.4f}"
        }
        
    except Exception as e:
        logger.error(f"Batch enhancement error: {e}")
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🎓 Starting Yale Network Search API - AI Enhanced...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    print("🔍 Example search: http://localhost:8000/search?q=data%20science%20students")
    print("🤖 AI Features: Enhanced summaries and tags for better search")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")