"""
Enhanced Search API with Rich Data Integration
Incorporates extracted experience, education, and skills from headlines
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
from ai_query_enhancer import AIQueryEnhancer
from data_enricher import DataEnricher

load_dotenv()

app = FastAPI(
    title="Yale Network Search - Enriched API",
    description="AI-powered search with rich profile data extraction and analysis",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
query_enhancer = AIQueryEnhancer()
data_enricher = DataEnricher()

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

def enrich_search_results(results: List[Dict]) -> List[Dict]:
    """Enrich search results with extracted experience, education, and skills"""
    enriched_results = []
    
    for result in results:
        # Extract rich data from headline
        headline = result.get('headline', '')
        
        if headline and len(headline) > 30:
            # Extract structured data
            experiences = data_enricher.extract_experience_from_headline(headline)
            education = data_enricher.extract_education_from_headline(headline)
            skills = data_enricher.extract_skills_from_headline(headline)
            
            # Add enriched data to result
            result['extracted_data'] = {
                'experiences': experiences,
                'education': education,
                'skills': skills,
                'has_rich_data': True
            }
            
            # Create summary of professional info
            current_roles = [exp for exp in experiences if exp.get('is_current', False)]
            if current_roles:
                result['current_role_summary'] = f"{current_roles[0]['title']} at {current_roles[0]['company']}"
            
            # Add skills summary
            if skills:
                result['skills_summary'] = ', '.join(skills[:3]) + ('...' if len(skills) > 3 else '')
        else:
            result['extracted_data'] = {
                'experiences': [],
                'education': [],
                'skills': [],
                'has_rich_data': False
            }
        
        enriched_results.append(result)
    
    return enriched_results

@app.get("/")
async def root():
    """API information"""
    return {
        "message": "Yale Network Search - Enriched API v3.0",
        "features": [
            "AI-powered query enhancement",
            "Rich data extraction from headlines",
            "Experience and education parsing",
            "Skills identification",
            "Professional role categorization"
        ],
        "data_richness": {
            "total_profiles": "14,412",
            "rich_headlines": "1,841",
            "leadership_roles": "91",
            "tech_roles": "173", 
            "academic_roles": "320"
        },
        "endpoints": {
            "enriched_search": "/enriched-search?q=query",
            "profile_analysis": "/analyze-profile?name=full_name",
            "data_stats": "/data-stats"
        }
    }

@app.get("/enriched-search")
async def enriched_search(
    q: str = Query(..., description="Natural language search query"),
    limit: int = Query(20, description="Maximum number of results"),
    include_analysis: bool = Query(False, description="Include AI query analysis"),
    include_rich_data: bool = Query(True, description="Include extracted experience/education data")
):
    """
    Enhanced search with AI analysis and rich data extraction
    """
    start_time = time.time()
    
    try:
        # Generate AI enhancement
        enhancement = query_enhancer.enhance_query(q)
        
        # Execute enhanced search with focus on headline richness
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Modified SQL to prioritize profiles with rich data
        sql = f"""
        WITH scored_profiles AS (
            SELECT 
                p.uuid_id,
                p.full_name as name,
                p.headline,
                p.location,
                p.summary,
                p.ai_summary,
                p.ai_tags,
                p.ai_processed,
                ya.school as yale_school,
                ya.major,
                ya.class_year,
                ya.affiliation_type,
                p.profile_url,
                -- Enhanced 1-100 relevance scoring
                LEAST(100, GREATEST(0, (
                    -- Exact phrase matches in headline (40 points max)
                    {_generate_weighted_headline_conditions(enhancement.key_phrases)} +
                    -- Summary content matches (25 points max)
                    CASE WHEN p.summary IS NOT NULL AND {_generate_summary_conditions(enhancement.key_phrases)} THEN 25.0 ELSE 0.0 END +
                    -- Professional role relevance (20 points max)
                    {_generate_professional_scoring(enhancement.traits)} +
                    -- AI tags semantic matches (10 points max)
                    CASE WHEN p.ai_tags IS NOT NULL AND {_generate_ai_tags_conditions(enhancement.key_phrases)} THEN 10.0 ELSE 0.0 END +
                    -- Data quality bonus (5 points max)
                    CASE WHEN length(p.headline) > 100 THEN 5.0 
                         WHEN length(p.headline) > 50 THEN 3.0 
                         WHEN length(p.headline) > 20 THEN 1.0 ELSE 0.0 END
                ))) as relevance_score,
                length(p.headline) as headline_length
            FROM people p
            LEFT JOIN yale_affiliations ya ON p.uuid_id = ya.person_uuid
            WHERE (
                {_generate_people_conditions(enhancement.key_phrases)}
            )
        )
        SELECT DISTINCT *
        FROM scored_profiles
        WHERE relevance_score >= 30
        ORDER BY relevance_score DESC, headline_length DESC, name ASC
        LIMIT {limit};
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        # Process and enrich results
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
        
        # Enrich with extracted data if requested
        if include_rich_data:
            processed_results = enrich_search_results(processed_results)
        
        conn.close()
        
        # Build response
        response = {
            "query": q,
            "total_results": len(processed_results),
            "results": processed_results,
            "search_time_ms": round((time.time() - start_time) * 1000),
            "enhanced": True,
            "enriched": include_rich_data
        }
        
        # Include analysis if requested
        if include_analysis:
            response["query_analysis"] = {
                "traits": enhancement.traits,
                "work_filters": enhancement.work_filters,
                "key_phrases": enhancement.key_phrases,
                "company_patterns": enhancement.company_patterns,
                "title_patterns": enhancement.title_patterns,
                "explanation": enhancement.explanation
            }
        
        return response
        
    except Exception as e:
        print(f"Enriched search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/analyze-query")
async def analyze_query(q: str = Query(..., description="Query to analyze")):
    """
    Analyze a search query and return AI-enhanced breakdown
    """
    try:
        # Generate AI enhancement
        enhancement = query_enhancer.enhance_query(q)
        
        return {
            "query": q,
            "analysis": {
                "traits": enhancement.traits,
                "work_filters": enhancement.work_filters,
                "key_phrases": enhancement.key_phrases,
                "company_patterns": enhancement.company_patterns,
                "title_patterns": enhancement.title_patterns,
                "explanation": enhancement.explanation
            },
            "confidence": "high" if len(enhancement.traits) > 3 else "medium"
        }
        
    except Exception as e:
        print(f"Query analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/analyze-profile")
async def analyze_profile(name: str = Query(..., description="Full name of person to analyze")):
    """
    Analyze a specific profile and extract rich data
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT uuid_id, full_name, headline, ai_summary, ai_tags FROM people WHERE full_name ILIKE %s", (f"%{name}%",))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        headline = result['headline'] or ''
        
        # Extract rich data
        enrichment = data_enricher.enrich_profile_data(str(result['uuid_id']), headline)
        
        response = {
            "profile": {
                "uuid_id": str(result['uuid_id']),
                "name": result['full_name'],
                "headline": headline,
                "ai_summary": result['ai_summary'],
                "ai_tags": result['ai_tags']
            },
            "extracted_data": {
                "experiences": enrichment['experiences'],
                "education": enrichment['education'],
                "skills": enrichment['skills']
            },
            "analysis": {
                "data_richness": "high" if len(headline) > 50 else "low",
                "professional_indicators": len(enrichment['experiences']),
                "education_indicators": len(enrichment['education']),
                "skill_indicators": len(enrichment['skills'])
            }
        }
        
        conn.close()
        return response
        
    except Exception as e:
        print(f"Profile analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/data-stats")
async def get_data_stats():
    """Get comprehensive data statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Basic stats
        cursor.execute("SELECT COUNT(*) FROM people")
        total_people = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE length(headline) > 50")
        rich_headlines = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE headline ~* '(founder|CEO|president|director)'")
        leadership = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE headline ~* '(engineer|developer|scientist|researcher)'")
        technical = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE headline ~* '(PhD|professor|academic|researcher)'")
        academic = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM people WHERE ai_processed = true")
        ai_enhanced = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_profiles": total_people,
            "data_richness": {
                "rich_headlines": rich_headlines,
                "rich_percentage": f"{(rich_headlines/total_people*100):.1f}%"
            },
            "professional_categories": {
                "leadership_roles": leadership,
                "technical_roles": technical,
                "academic_roles": academic
            },
            "ai_enhancement": {
                "enhanced_profiles": ai_enhanced,
                "enhancement_rate": f"{(ai_enhanced/total_people*100):.1f}%"
            },
            "extractable_data_estimate": {
                "experience_records": rich_headlines * 0.75,  # Estimated
                "education_records": rich_headlines * 1.2,   # Estimated
                "skills_records": rich_headlines * 1.1       # Estimated
            }
        }
        
    except Exception as e:
        print(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve stats: {str(e)}")

def _generate_headline_conditions(key_phrases: List[str]) -> str:
    """Generate SQL conditions for headline matching"""
    if not key_phrases:
        return "FALSE"
    conditions = [f"p.headline ILIKE '%{phrase}%'" for phrase in key_phrases]
    return f"({' OR '.join(conditions)})"

def _generate_summary_conditions(key_phrases: List[str]) -> str:
    """Generate SQL conditions for summary matching"""
    if not key_phrases:
        return "FALSE"
    conditions = [f"p.summary ILIKE '%{phrase}%'" for phrase in key_phrases]
    return f"({' OR '.join(conditions)})"

def _generate_ai_tags_conditions(key_phrases: List[str]) -> str:
    """Generate SQL conditions for AI tags matching"""
    if not key_phrases:
        return "FALSE"
    conditions = [f"p.ai_tags::text ILIKE '%{phrase}%'" for phrase in key_phrases]
    return f"({' OR '.join(conditions)})"

def _generate_people_conditions(key_phrases: List[str]) -> str:
    """Generate comprehensive conditions for people table"""
    if not key_phrases:
        return "FALSE"
    conditions = [f"(p.headline ILIKE '%{phrase}%' OR p.summary ILIKE '%{phrase}%' OR p.full_name ILIKE '%{phrase}%')" for phrase in key_phrases]
    return f"({' OR '.join(conditions)})"

def _generate_weighted_headline_conditions(key_phrases: List[str]) -> str:
    """Generate weighted scoring for headline matches (0-40 points)"""
    if not key_phrases:
        return "0"
    
    # Weight exact matches higher than partial matches
    conditions = []
    for phrase in key_phrases:
        # Exact phrase match: 40 points
        # Case-insensitive partial match: 20 points
        # Individual word matches: 10 points each
        conditions.append(f"""
            CASE WHEN p.headline ILIKE '{phrase}' THEN 40.0
                 WHEN p.headline ILIKE '%{phrase}%' THEN 20.0
                 WHEN p.headline ~* '\\y{phrase.split()[0] if phrase.split() else phrase}\\y' THEN 10.0
                 ELSE 0.0 END
        """)
    
    return f"GREATEST({', '.join(conditions)})"

def _generate_professional_scoring(traits: List[str]) -> str:
    """Generate professional role relevance scoring (0-20 points)"""
    if not traits:
        return "0"
    
    # Map common professional traits to scoring patterns
    professional_patterns = {
        'venture capitalist': r'(VC|venture capital|investment|investor|fund)',
        'entrepreneur': r'(founder|co-founder|startup|entrepreneur|CEO)',
        'engineer': r'(engineer|developer|software|technical|programming)',
        'researcher': r'(research|scientist|PhD|postdoc|academic)',
        'consultant': r'(consultant|consulting|advisor|advisory)',
        'analyst': r'(analyst|analysis|financial|investment)',
        'manager': r'(manager|management|director|VP|executive)',
        'doctor': r'(MD|doctor|physician|medical|healthcare)',
        'lawyer': r'(JD|lawyer|attorney|legal|law)',
        'professor': r'(professor|faculty|lecturer|instructor|academic)'
    }
    
    scoring_conditions = []
    for trait in traits:
        trait_lower = trait.lower()
        for pattern_key, regex_pattern in professional_patterns.items():
            if pattern_key in trait_lower or any(word in trait_lower for word in pattern_key.split()):
                scoring_conditions.append(f"CASE WHEN p.headline ~* '{regex_pattern}' THEN 20.0 ELSE 0.0 END")
                break
    
    if not scoring_conditions:
        return "0"
    
    return f"GREATEST({', '.join(scoring_conditions)})"

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enriched Yale Network Search API v3.0...")
    print("📍 API will be available at: http://localhost:8003")
    print("📖 Documentation at: http://localhost:8003/docs")
    print("🔍 Enriched search: http://localhost:8003/enriched-search?q=founders")
    print("🧠 Rich data extraction, AI enhancement, professional categorization")
    
    uvicorn.run(app, host="0.0.0.0", port=8003)