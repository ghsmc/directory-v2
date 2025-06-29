#!/usr/bin/env python3
"""
Working API server with simplified hybrid search
Focus on getting results with current data
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import sys
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Yale Network Working Search API",
    description="Simplified hybrid search that actually returns results",
    version="2.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request/Response Models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    limit: Optional[int] = Field(10, ge=1, le=50, description="Number of results")

class PersonResult(BaseModel):
    name: str
    location: Optional[str]
    headline: Optional[str]
    yale_school: Optional[str]
    score: float
    match_reasons: List[str]

class SearchResponse(BaseModel):
    query: str
    total_results: int
    execution_time_ms: float
    results: List[PersonResult]
    query_analysis: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Yale Network Working Search API",
        "description": "Simplified search that returns actual results from your Yale data",
        "version": "2.1.0",
        "database_people": 82,
        "endpoints": {
            "search": "/search",
            "stats": "/stats", 
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check"""
    try:
        count = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        yale_count = db.execute(text("""
            SELECT COUNT(DISTINCT p.uuid_id) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        """)).scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_people": count,
            "yale_people": yale_count,
            "openai_configured": bool(OPENAI_API_KEY)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Working search that returns results
    
    Searches Yale people with smart query parsing and SQL filtering
    """
    import time
    start_time = time.time()
    
    try:
        # Parse query for search terms
        query_lower = request.query.lower()
        search_analysis = analyze_query(query_lower)
        
        # Build SQL query based on parsed terms
        sql_query, params = build_search_sql(search_analysis, request.limit)
        
        # Execute search
        results = db.execute(text(sql_query), params).fetchall()
        
        # Convert to response format
        person_results = []
        for i, row in enumerate(results):
            score = calculate_score(row, search_analysis)
            match_reasons = generate_match_reasons(row, search_analysis)
            
            person_result = PersonResult(
                name=row.full_name,
                location=row.location,
                headline=row.headline,
                yale_school=row.school,
                score=score,
                match_reasons=match_reasons
            )
            person_results.append(person_result)
        
        execution_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=request.query,
            total_results=len(person_results),
            execution_time_ms=execution_time,
            results=person_results,
            query_analysis=search_analysis
        )
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

@app.get("/search")
async def search_get(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    db: Session = Depends(get_db)
):
    """GET version of search"""
    request = SearchRequest(query=q, limit=limit)
    return await search(request, db)

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Database statistics"""
    try:
        stats = {}
        
        stats['total_people'] = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        stats['yale_people'] = db.execute(text("""
            SELECT COUNT(DISTINCT p.uuid_id) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        """)).scalar()
        
        # Top locations
        location_stats = db.execute(text("""
            SELECT p.location, COUNT(*) as count
            FROM people p 
            WHERE p.location IS NOT NULL AND p.location != ''
            GROUP BY p.location 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """)).fetchall()
        stats['top_locations'] = {row.location: row.count for row in location_stats}
        
        # Sample people
        sample_people = db.execute(text("""
            SELECT p.full_name, p.location, ya.school
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LIMIT 5
        """)).fetchall()
        stats['sample_people'] = [
            {"name": row.full_name, "location": row.location, "yale_school": row.school}
            for row in sample_people
        ]
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {e}")

def analyze_query(query: str) -> Dict[str, Any]:
    """Simple query analysis"""
    analysis = {
        "original": query,
        "locations": [],
        "schools": [],
        "roles": [],
        "keywords": []
    }
    
    # Location detection
    location_terms = {
        'connecticut': ['connecticut', 'ct', 'new haven'],
        'new_york': ['new york', 'nyc', 'ny', 'manhattan'],
        'boston': ['boston', 'cambridge', 'massachusetts'],
        'california': ['california', 'san francisco', 'la', 'los angeles']
    }
    
    for location, variants in location_terms.items():
        if any(variant in query for variant in variants):
            analysis['locations'].append(location)
    
    # Yale school detection
    yale_schools = {
        'yale_college': ['yale college', 'undergraduate'],
        'yale_som': ['som', 'business school', 'management'],
        'yale_law': ['law school', 'yale law'],
        'yale_medicine': ['medical school', 'medicine']
    }
    
    for school, variants in yale_schools.items():
        if any(variant in query for variant in variants):
            analysis['schools'].append(school)
    
    # Role detection
    roles = {
        'student': ['student', 'graduate student'],
        'professor': ['professor', 'faculty', 'academic'],
        'doctor': ['doctor', 'physician', 'md'],
        'researcher': ['researcher', 'research'],
        'entrepreneur': ['entrepreneur', 'founder']
    }
    
    for role, variants in roles.items():
        if any(variant in query for variant in variants):
            analysis['roles'].append(role)
    
    # Extract other keywords
    keywords = query.split()
    analysis['keywords'] = [k for k in keywords if len(k) > 2]
    
    return analysis

def build_search_sql(analysis: Dict[str, Any], limit: int) -> tuple:
    """Build SQL query from analysis"""
    
    base_sql = """
        SELECT DISTINCT 
            p.full_name, 
            p.location, 
            p.headline,
            ya.school
        FROM people p 
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        WHERE p.full_name IS NOT NULL
    """
    
    conditions = []
    params = {}
    
    # Location filters
    if analysis['locations']:
        location_conditions = []
        for i, location in enumerate(analysis['locations']):
            if location == 'connecticut':
                location_conditions.append("""
                    (LOWER(p.location) LIKE '%connecticut%' 
                     OR LOWER(p.location) LIKE '%ct%' 
                     OR LOWER(p.location) LIKE '%new haven%')
                """)
            elif location == 'new_york':
                location_conditions.append("""
                    (LOWER(p.location) LIKE '%new york%' 
                     OR LOWER(p.location) LIKE '%nyc%'
                     OR LOWER(p.location) LIKE '%manhattan%')
                """)
            else:
                param_name = f"location_{i}"
                params[param_name] = f"%{location}%"
                location_conditions.append(f"LOWER(p.location) LIKE LOWER(:{param_name})")
        
        if location_conditions:
            conditions.append(f"({' OR '.join(location_conditions)})")
    
    # Role filters
    if analysis['roles']:
        role_conditions = []
        for i, role in enumerate(analysis['roles']):
            param_name = f"role_{i}"
            params[param_name] = f"%{role}%"
            role_conditions.append(f"LOWER(p.headline) LIKE LOWER(:{param_name})")
        
        if role_conditions:
            conditions.append(f"({' OR '.join(role_conditions)})")
    
    # Keyword search in name or headline
    if analysis['keywords']:
        keyword_conditions = []
        for i, keyword in enumerate(analysis['keywords'][:3]):  # Limit to 3 keywords
            param_name = f"keyword_{i}"
            params[param_name] = f"%{keyword}%"
            keyword_conditions.append(f"""
                (LOWER(p.full_name) LIKE LOWER(:{param_name}) 
                 OR LOWER(p.headline) LIKE LOWER(:{param_name}))
            """)
        
        if keyword_conditions:
            conditions.append(f"({' OR '.join(keyword_conditions)})")
    
    # Combine conditions
    if conditions:
        base_sql += " AND (" + " OR ".join(conditions) + ")"
    
    # Add ordering and limit
    base_sql += f" ORDER BY p.full_name LIMIT {limit}"
    
    return base_sql, params

def calculate_score(row, analysis: Dict[str, Any]) -> float:
    """Calculate relevance score"""
    score = 0.5  # Base score for all Yale people
    
    # Location match
    if analysis['locations'] and row.location:
        for location in analysis['locations']:
            if location.replace('_', ' ') in row.location.lower():
                score += 0.3
                break
    
    # Role match
    if analysis['roles'] and row.headline:
        for role in analysis['roles']:
            if role in row.headline.lower():
                score += 0.2
                break
    
    # Keyword match
    if analysis['keywords']:
        text_to_search = f"{row.full_name} {row.headline or ''}".lower()
        for keyword in analysis['keywords']:
            if keyword.lower() in text_to_search:
                score += 0.1
    
    return min(score, 1.0)

def generate_match_reasons(row, analysis: Dict[str, Any]) -> List[str]:
    """Generate match reasons"""
    reasons = ["Yale affiliation"]
    
    if analysis['locations'] and row.location:
        for location in analysis['locations']:
            if location.replace('_', ' ') in row.location.lower():
                reasons.append(f"Location: {location.replace('_', ' ').title()}")
                break
    
    if analysis['roles'] and row.headline:
        for role in analysis['roles']:
            if role in row.headline.lower():
                reasons.append(f"Role: {role.title()}")
                break
    
    if row.school:
        reasons.append(f"School: {row.school}")
    
    return reasons

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Yale Network Working Search API...")
    print("📍 API available at: http://localhost:8003")
    print("📖 Documentation at: http://localhost:8003/docs")
    print("🔍 Search: http://localhost:8003/search?q=Connecticut")
    print("📊 Stats: http://localhost:8003/stats")
    
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")