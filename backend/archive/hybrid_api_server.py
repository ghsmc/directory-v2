#!/usr/bin/env python3
"""
Hybrid API server with advanced query architecture
Implements the complete happenstance.ai style search pipeline
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

sys.path.append('.')
from app.search.hybrid_search_engine import HybridSearchEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Yale Network Hybrid Search API",
    description="Advanced AI-powered search with vector + structured + graph capabilities",
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

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request/Response Models
class HybridSearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    limit: Optional[int] = Field(20, ge=1, le=100, description="Number of results")
    user_id: Optional[str] = Field(None, description="User ID for graph constraints")
    include_explanation: Optional[bool] = Field(True, description="Include score breakdown")
    ranking_mode: Optional[str] = Field("auto", description="Ranking strategy: auto, semantic, structured, yale, network")

class PersonResult(BaseModel):
    person_id: str
    name: str
    location: Optional[str]
    headline: Optional[str] 
    summary: Optional[str]
    linkedin_url: Optional[str]
    score: float
    match_reasons: List[str]
    matched_filters: Dict[str, List[str]]
    score_breakdown: Optional[Dict[str, float]] = None

class HybridSearchResponse(BaseModel):
    query: str
    total_results: int
    execution_time_ms: float
    results: List[PersonResult]
    query_analysis: Dict[str, Any]
    ranking_weights: Dict[str, float]
    debug_info: Optional[Dict[str, Any]] = None

class QueryAnalysisRequest(BaseModel):
    query: str = Field(..., description="Query to analyze")

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Yale Network Hybrid Search API",
        "description": "Advanced search combining vector similarity, structured filters, and graph traversal",
        "version": "2.0.0",
        "features": [
            "Natural language parsing",
            "Vector semantic search", 
            "Structured SQL filtering",
            "Graph traversal constraints",
            "Multi-factor ranking",
            "Explainable results"
        ],
        "endpoints": {
            "hybrid_search": "/search/hybrid",
            "analyze_query": "/search/analyze", 
            "classic_search": "/search",
            "stats": "/stats",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Enhanced health check"""
    try:
        # Test database connection
        count = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        yale_count = db.execute(text("""
            SELECT COUNT(DISTINCT p.uuid_id) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        """)).scalar()
        
        # Test vector extension
        vector_enabled = False
        try:
            db.execute(text("SELECT vector_dims('[1,2,3]'::vector)")).scalar()
            vector_enabled = True
        except:
            pass
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_people": count,
            "yale_people": yale_count,
            "vector_search": "enabled" if vector_enabled else "disabled",
            "openai_configured": bool(OPENAI_API_KEY)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")

@app.post("/search/hybrid", response_model=HybridSearchResponse)
async def hybrid_search(request: HybridSearchRequest, db: Session = Depends(get_db)):
    """
    Advanced hybrid search endpoint
    
    Combines vector similarity, structured filters, graph constraints, and multi-factor ranking
    
    Example queries:
    - "Fintech PMs in NYC who went to Stanford"
    - "Yale SOM alumni working in venture capital" 
    - "Connecticut entrepreneurs in healthcare"
    - "Yale professors and researchers in AI"
    """
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    if not request.query or len(request.query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    try:
        # Initialize hybrid search engine
        search_engine = HybridSearchEngine(db, OPENAI_API_KEY)
        
        # Prepare user context
        user_context = {}
        if request.user_id:
            user_context["user_id"] = request.user_id
        
        # Execute hybrid search
        result = search_engine.search(
            raw_query=request.query,
            user_context=user_context,
            limit=request.limit
        )
        
        # Convert results to response format
        person_results = []
        for candidate in result.get_top_results(request.limit):
            person_result = PersonResult(
                person_id=candidate.person_id,
                name=candidate.person_data.get('name', ''),
                location=candidate.person_data.get('location'),
                headline=candidate.person_data.get('headline'),
                summary=candidate.person_data.get('summary'),
                linkedin_url=candidate.person_data.get('linkedin_url'),
                score=candidate.final_score,
                match_reasons=candidate.match_reasons,
                matched_filters=candidate.matched_filters,
                score_breakdown=candidate.score_breakdown if request.include_explanation else None
            )
            person_results.append(person_result)
        
        return HybridSearchResponse(
            query=request.query,
            total_results=result.total_results,
            execution_time_ms=result.execution_time_ms,
            results=person_results,
            query_analysis={
                "intent": result.query.intent,
                "confidence": result.query.confidence,
                "parsed_entities": result.query.parsed_entities,
                "filter_count": len(result.query.filters),
                "has_embedding": result.query.embedding is not None,
                "has_graph_constraints": result.query.graph_constraints is not None
            },
            ranking_weights={
                "embedding_similarity": result.query.ranking_weights.embedding_similarity,
                "filter_match": result.query.ranking_weights.filter_match,
                "graph_proximity": result.query.ranking_weights.graph_proximity,
                "yale_affinity": result.query.ranking_weights.yale_affinity
            },
            debug_info=result.debug_info if request.include_explanation else None
        )
        
    except Exception as e:
        logger.error(f"Hybrid search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")

@app.get("/search/hybrid")
async def hybrid_search_get(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    user_id: Optional[str] = Query(None, description="User ID for graph constraints"),
    explain: bool = Query(True, description="Include explanations"),
    db: Session = Depends(get_db)
):
    """GET version of hybrid search for easy testing"""
    request = HybridSearchRequest(
        query=q,
        limit=limit,
        user_id=user_id,
        include_explanation=explain
    )
    return await hybrid_search(request, db)

@app.post("/search/analyze")
async def analyze_query(request: QueryAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze query parsing without executing search
    
    Shows how a natural language query gets broken down into:
    - Intent detection
    - Entity extraction  
    - Filter generation
    - Ranking optimization
    """
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        search_engine = HybridSearchEngine(db, OPENAI_API_KEY)
        
        # Parse query without executing search
        query = search_engine.query_parser.parse_query(request.query)
        
        # Generate explanation
        explanation = search_engine.query_parser.explain_query_parsing(query)
        
        return {
            "query": request.query,
            "parsing_explanation": explanation,
            "hybrid_query_structure": query.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Query analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.get("/search")
async def classic_search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Fallback to classic search for compatibility"""
    # This could call the existing enhanced_search.py for comparison
    try:
        from enhanced_search import EnhancedYaleSearch
        
        search_engine = EnhancedYaleSearch()
        results = search_engine.search(q, limit=limit)
        
        return {
            "query": q,
            "total_results": len(results),
            "search_type": "classic",
            "results": [
                {
                    "person_id": str(result.person.uuid_id),
                    "name": result.person.full_name,
                    "location": result.person.location,
                    "headline": result.person.headline,
                    "score": result.score,
                    "match_reasons": result.match_reasons
                }
                for result in results
            ]
        }
        
    except Exception as e:
        logger.error(f"Classic search error: {e}")
        raise HTTPException(status_code=500, detail=f"Classic search failed: {e}")

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Enhanced database statistics"""
    try:
        stats = {}
        
        # Basic counts
        stats['total_people'] = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        stats['yale_people'] = db.execute(text("""
            SELECT COUNT(DISTINCT p.uuid_id) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        """)).scalar()
        
        # Profile completeness
        try:
            stats['with_embeddings'] = db.execute(text("""
                SELECT COUNT(*) FROM profile_embeddings
            """)).scalar()
        except:
            stats['with_embeddings'] = 0
        
        stats['with_linkedin'] = db.execute(text("""
            SELECT COUNT(*) FROM people WHERE linkedin_url IS NOT NULL
        """)).scalar()
        
        # Yale affiliations
        affiliation_stats = db.execute("""
            SELECT ya.affiliation_type, COUNT(*) 
            FROM yale_affiliations ya 
            GROUP BY ya.affiliation_type
            ORDER BY COUNT(*) DESC
        """).fetchall()
        stats['by_affiliation'] = {row[0]: row[1] for row in affiliation_stats}
        
        # Top Yale schools
        school_stats = db.execute("""
            SELECT ya.school, COUNT(*) 
            FROM yale_affiliations ya 
            WHERE ya.school IS NOT NULL AND ya.school != ''
            GROUP BY ya.school 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """).fetchall()
        stats['top_yale_schools'] = {row[0]: row[1] for row in school_stats}
        
        # Top locations
        location_stats = db.execute("""
            SELECT p.location, COUNT(*) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            WHERE p.location IS NOT NULL AND p.location != ''
            GROUP BY p.location 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """).fetchall()
        stats['top_locations'] = {row[0]: row[1] for row in location_stats}
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {e}")

@app.get("/examples")
async def get_example_queries():
    """Example queries showcasing hybrid search capabilities"""
    return {
        "hybrid_search_examples": [
            {
                "query": "Fintech PMs in NYC who went to Stanford",
                "description": "Combines industry, role, location, and education filters",
                "features": ["title_matching", "location_filtering", "education_filtering"]
            },
            {
                "query": "Yale SOM alumni working in venture capital",
                "description": "Yale-specific search with industry filtering",
                "features": ["yale_affiliation", "industry_matching", "structured_filters"]
            },
            {
                "query": "Connecticut entrepreneurs in healthcare within 2 hops",
                "description": "Geographic + industry + graph constraints", 
                "features": ["location_filtering", "graph_traversal", "industry_matching"]
            },
            {
                "query": "Yale professors and researchers in AI",
                "description": "Academic roles with technology focus",
                "features": ["title_matching", "yale_affiliation", "semantic_search"]
            },
            {
                "query": "Yale College class of 2015-2020 founders",
                "description": "Specific Yale school, graduation years, and role",
                "features": ["yale_school", "class_year_range", "title_matching"]
            }
        ],
        "search_tips": [
            "Be specific about location (NYC, San Francisco, Boston)",
            "Include role types (VC, founder, professor, engineer)",
            "Mention Yale schools (SOM, Law School, Medical School)", 
            "Use industry terms (fintech, healthcare, edtech)",
            "Specify connection constraints (within 2 hops)",
            "Combine multiple filters for precise results"
        ],
        "ranking_modes": {
            "auto": "Automatically optimizes based on query type",
            "semantic": "Prioritizes semantic similarity",
            "structured": "Prioritizes exact filter matches",
            "yale": "Prioritizes Yale connections and affiliations",
            "network": "Prioritizes graph proximity and connections"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Yale Network Hybrid Search API...")
    print("📍 API available at: http://localhost:8002")
    print("📖 Documentation at: http://localhost:8002/docs") 
    print("🔍 Hybrid search: http://localhost:8002/search/hybrid?q=Yale%20people%20in%20NYC")
    print("🧠 Query analysis: http://localhost:8002/search/analyze")
    
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")