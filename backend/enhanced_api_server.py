"""
Enhanced API Server with AI-Powered Query Enhancement
Provides sophisticated search capabilities using AI-generated filters and SQL queries
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import psycopg2
import psycopg2.extras
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from ai_query_enhancer import AIQueryEnhancer, SearchEnhancement

load_dotenv()

app = FastAPI(
    title="Yale Network Search - Enhanced API",
    description="AI-powered search for Yale community with sophisticated query enhancement",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global enhancer instance
query_enhancer = AIQueryEnhancer()

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/")
async def root():
    """API information and available endpoints"""
    return {
        "message": "Yale Network Search - Enhanced API",
        "version": "2.0.0",
        "features": [
            "AI-powered query enhancement",
            "Comprehensive trait and filter generation",
            "Advanced SQL query optimization",
            "Natural language processing",
            "Yale-specific search capabilities"
        ],
        "endpoints": {
            "enhanced_search": "/enhanced-search?q=your_query",
            "query_analysis": "/analyze-query?q=your_query",
            "basic_search": "/search?q=your_query",
            "stats": "/stats",
            "health": "/health"
        },
        "example_queries": [
            "Software engineers who've worked on growth at Series A-C companies",
            "Product managers at tech startups in NYC",
            "Data scientists with machine learning experience",
            "Investment bankers at bulge bracket firms",
            "Healthcare entrepreneurs and founders"
        ]
    }

@app.get("/enhanced-search")
async def enhanced_search(
    q: str = Query(..., description="Natural language search query"),
    limit: int = Query(20, description="Maximum number of results"),
    include_analysis: bool = Query(False, description="Include AI query analysis in response")
):
    """
    Enhanced search using AI-powered query analysis and optimization
    """
    start_time = time.time()
    
    try:
        # Generate AI enhancement
        enhancement = query_enhancer.enhance_query(q)
        
        # Generate optimized SQL
        sql = query_enhancer.generate_enhanced_sql(enhancement, limit)
        
        # Execute search
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Process results
        processed_results = []
        for row in results:
            result = {
                "uuid_id": str(row['uuid_id']),
                "name": row['name'],
                "headline": row['headline'] or '',
                "location": row['location'] or '',
                "summary": row['summary'] or '',
                "ai_summary": row['ai_summary'],
                "ai_tags": row['ai_tags'] or [],
                "ai_processed": row['ai_processed'] or False,
                "yale_school": row['yale_school'],
                "major": row['major'],
                "class_year": row['class_year'],
                "affiliation_type": row['affiliation_type'],
                "profile_url": row['profile_url'],
                "relevance_score": float(row['relevance_score']) if row['relevance_score'] else 0.0
            }
            processed_results.append(result)
        
        conn.close()
        
        # Build response
        response = {
            "query": q,
            "total_results": len(processed_results),
            "results": processed_results,
            "search_time_ms": round((time.time() - start_time) * 1000),
            "enhanced": True
        }
        
        # Include analysis if requested
        if include_analysis:
            response["query_analysis"] = {
                "traits": enhancement.traits,
                "work_filters": enhancement.work_filters,
                "key_phrases": enhancement.key_phrases,
                "company_patterns": enhancement.company_patterns,
                "title_patterns": enhancement.title_patterns,
                "explanation": enhancement.explanation,
                "sql_conditions": enhancement.sql_conditions
            }
        
        return response
        
    except Exception as e:
        print(f"Enhanced search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/analyze-query")
async def analyze_query(q: str = Query(..., description="Query to analyze")):
    """
    Analyze a query and return AI-generated traits, filters, and search strategy
    """
    try:
        enhancement = query_enhancer.enhance_query(q)
        
        return {
            "original_query": q,
            "analysis": {
                "traits": enhancement.traits,
                "work_filters": enhancement.work_filters,
                "key_phrases": enhancement.key_phrases,
                "company_patterns": enhancement.company_patterns,
                "title_patterns": enhancement.title_patterns,
                "explanation": enhancement.explanation,
                "sql_conditions": enhancement.sql_conditions
            },
            "generated_sql": query_enhancer.generate_enhanced_sql(enhancement, 10)
        }
        
    except Exception as e:
        print(f"Query analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/search")
async def basic_search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, description="Maximum number of results")
):
    """
    Basic search endpoint (backwards compatibility)
    """
    # For now, redirect to enhanced search
    return await enhanced_search(q, limit, include_analysis=False)

@app.get("/stats")
async def get_stats():
    """Database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute("SELECT COUNT(*) FROM people")
        total_people = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE ai_processed = true")
        ai_enhanced = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM experience")
        total_experience = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM education")
        total_education = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM yale_affiliations")
        yale_affiliations = cursor.fetchone()[0]
        
        # Get recent AI enhancements
        cursor.execute("""
            SELECT COUNT(*) FROM people 
            WHERE ai_processed = true 
            AND ai_processed_at >= NOW() - INTERVAL '24 hours'
        """)
        recent_ai_enhancements = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "database_stats": {
                "total_people": total_people,
                "ai_enhanced_profiles": ai_enhanced,
                "ai_enhancement_rate": f"{(ai_enhanced/total_people*100):.1f}%" if total_people > 0 else "0%",
                "total_experience_records": total_experience,
                "total_education_records": total_education,
                "yale_affiliations": yale_affiliations,
                "recent_ai_enhancements_24h": recent_ai_enhancements
            },
            "search_capabilities": {
                "ai_query_enhancement": True,
                "trait_generation": True,
                "filter_optimization": True,
                "advanced_sql_generation": True,
                "relevance_scoring": True
            }
        }
        
    except Exception as e:
        print(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve stats: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        
        # Test AI enhancer
        test_enhancement = query_enhancer.enhance_query("test")
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "ai_enhancer": "operational",
            "version": "2.0.0"
        }
        
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced Yale Network Search API...")
    print("📍 API will be available at: http://localhost:8001")
    print("📖 Documentation at: http://localhost:8001/docs")
    print("🔍 Enhanced search: http://localhost:8001/enhanced-search?q=software%20engineers")
    print("🧠 AI Features: Query enhancement, trait generation, advanced SQL optimization")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)