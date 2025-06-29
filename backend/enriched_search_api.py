"""
Enhanced Search API with Rich Data Integration
Incorporates extracted experience, education, and skills from headlines
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Optional, Generator
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
    title="Happenstance - Yale Network Search API",
    description="AI-powered discovery engine for Yale's network with real-time streaming search",
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
        "message": "Happenstance - Yale Network Search API v3.0",
        "features": [
            "Real-time streaming search results",
            "AI-powered query enhancement with GPT-4o-mini",
            "Massively expanded search conditions",
            "Rich data extraction from LinkedIn headlines",
            "Professional role categorization and scoring"
        ],
        "data_richness": {
            "total_profiles": "14,412",
            "rich_headlines": "1,841",
            "leadership_roles": "91",
            "tech_roles": "173", 
            "academic_roles": "320"
        },
        "endpoints": {
            "streaming_search": "/search-stream?q=query",
            "enriched_search": "/enriched-search?q=query",
            "query_analysis": "/analyze-query?q=query",
            "data_stats": "/data-stats"
        }
    }

@app.get("/search-stream")
async def streaming_search(
    q: str = Query(..., description="Natural language search query"),
    limit: int = Query(20, description="Maximum number of results")
):
    """
    Streaming search that sends results as they're found - ChatGPT style
    """
    def generate_stream():
        try:
            # Step 1: Send initial status
            yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing query with AI...', 'step': 1})}\n\n"
            
            # Generate AI enhancement
            enhancement = query_enhancer.enhance_query(q)
            yield f"data: {json.dumps({'type': 'analysis', 'data': {'traits': enhancement.traits, 'key_phrases': enhancement.key_phrases}})}\n\n"
            
            # Step 2: Database search
            yield f"data: {json.dumps({'type': 'status', 'message': 'Searching Yale database...', 'step': 2})}\n\n"
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fast simple search first for immediate results
            fast_sql = f"""
            SELECT 
                p.uuid_id, p.full_name as name, p.headline, p.location,
                p.summary, p.ai_summary, p.ai_tags, ya.school as yale_school,
                ya.major, ya.class_year, p.profile_url,
                length(p.headline) as headline_length
            FROM people p
            LEFT JOIN yale_affiliations ya ON p.uuid_id = ya.person_uuid
            WHERE {_generate_people_conditions(enhancement.key_phrases)}
            ORDER BY headline_length DESC, p.full_name ASC
            LIMIT {limit * 2};
            """
            
            cursor.execute(fast_sql)
            results = cursor.fetchall()
            
            # Stream results one by one as they're processed
            result_count = 0
            for row in results:
                if result_count >= limit:
                    break
                    
                result = {
                    "uuid_id": str(row['uuid_id']),
                    "name": row['name'],
                    "headline": row['headline'] or '',
                    "location": row['location'] or '',
                    "summary": row['summary'] or '',
                    "ai_summary": row['ai_summary'],
                    "ai_tags": row['ai_tags'] or [],
                    "yale_school": row['yale_school'],
                    "major": row['major'],
                    "class_year": row['class_year'],
                    "profile_url": row['profile_url'],
                    "relevance_score": 85.0 - (result_count * 2)  # Simulate decreasing relevance
                }
                
                # Add enriched data
                if row['headline'] and len(row['headline']) > 30:
                    experiences = data_enricher.extract_experience_from_headline(row['headline'])
                    result['extracted_data'] = {
                        'experiences': experiences,
                        'has_rich_data': True
                    }
                    if experiences:
                        result['current_role_summary'] = f"{experiences[0]['title']} at {experiences[0]['company']}"
                else:
                    result['extracted_data'] = {'experiences': [], 'has_rich_data': False}
                
                yield f"data: {json.dumps({'type': 'result', 'data': result})}\n\n"
                result_count += 1
            
            conn.close()
            
            # Final summary
            yield f"data: {json.dumps({'type': 'complete', 'total': result_count, 'query': q})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_stream(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "*"
        }
    )

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
        WHERE relevance_score >= 5
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
    """Generate massively expanded search conditions like Happenstance"""
    if not key_phrases:
        return "TRUE"  # Return all results if no phrases
    
    # Create a massive expansion of search terms like Happenstance
    expanded_conditions = []
    
    # Always include basic phrase matching first
    for phrase in key_phrases:
        basic_conditions = [
            f"p.headline ILIKE '%{phrase}%'",
            f"p.summary ILIKE '%{phrase}%'", 
            f"p.full_name ILIKE '%{phrase}%'",
            f"p.ai_tags::text ILIKE '%{phrase}%'"
        ]
        expanded_conditions.extend(basic_conditions)
    
    # Then add comprehensive domain-specific expansions
    query_text = ' '.join(key_phrases).lower()
    
    # VENTURE CAPITAL & INVESTMENT (like Happenstance's comprehensive matching)
    if any(term in query_text for term in ['venture', 'capital', 'vc', 'investment', 'investor', 'fund']):
        vc_conditions = [
            "p.headline ~* '(VC|venture capital|venture capitalist|investment|investor|fund|capital|private equity|PE|angel|angel investor|seed|series A|series B|portfolio|LP|limited partner|GP|general partner|investment banking|IB|equity research|M&A|merger|acquisition|buyout|growth equity|asset management|wealth management|hedge fund|mutual fund|financial|finance|banking|securities|trading|analyst|associate|principal|partner|managing director|VP|vice president)'",
            "p.summary ~* '(VC|venture capital|venture capitalist|investment|investor|fund|capital|private equity|PE|angel|angel investor|seed|series A|series B|portfolio|LP|limited partner|GP|general partner|investment banking|IB|equity research|M&A|merger|acquisition|buyout|growth equity|asset management|wealth management|hedge fund|mutual fund|financial|finance|banking|securities|trading|analyst|associate|principal|partner|managing director|VP|vice president)'",
            "p.headline ILIKE '%startup%' OR p.headline ILIKE '%entrepreneur%' OR p.headline ILIKE '%funding%'",
            "p.summary ILIKE '%startup%' OR p.summary ILIKE '%entrepreneur%' OR p.summary ILIKE '%funding%'"
        ]
        expanded_conditions.extend(vc_conditions)
    
    # COMPUTER SCIENCE & TECHNOLOGY (comprehensive tech matching)
    if any(term in query_text for term in ['computer', 'science', 'tech', 'software', 'engineer', 'developer', 'programming']):
        tech_conditions = [
            "p.headline ~* '(CS|computer science|software|programming|tech|technology|engineering|developer|coding|programmer|data science|data scientist|machine learning|ML|AI|artificial intelligence|algorithm|backend|frontend|full stack|fullstack|web development|mobile development|iOS|Android|Python|Java|JavaScript|React|Node|SQL|database|DevOps|cloud|AWS|Google Cloud|Azure|startup|fintech|biotech|edtech|SaaS|API|microservices|blockchain|crypto|cybersecurity|security|infrastructure|platform|product manager|technical|CTO|VP Engineering|software architect|senior developer|lead developer|principal engineer|staff engineer)'",
            "p.summary ~* '(CS|computer science|software|programming|tech|technology|engineering|developer|coding|programmer|data science|data scientist|machine learning|ML|AI|artificial intelligence|algorithm|backend|frontend|full stack|fullstack|web development|mobile development|iOS|Android|Python|Java|JavaScript|React|Node|SQL|database|DevOps|cloud|AWS|Google Cloud|Azure|startup|fintech|biotech|edtech|SaaS|API|microservices|blockchain|crypto|cybersecurity|security|infrastructure|platform|product manager|technical|CTO|VP Engineering|software architect|senior developer|lead developer|principal engineer|staff engineer)'",
            "p.headline ILIKE '%google%' OR p.headline ILIKE '%microsoft%' OR p.headline ILIKE '%apple%' OR p.headline ILIKE '%facebook%' OR p.headline ILIKE '%meta%' OR p.headline ILIKE '%amazon%' OR p.headline ILIKE '%netflix%' OR p.headline ILIKE '%uber%' OR p.headline ILIKE '%airbnb%'",
        ]
        expanded_conditions.extend(tech_conditions)
    
    # BUSINESS & ENTREPRENEURSHIP (founder/startup ecosystem)
    if any(term in query_text for term in ['founder', 'startup', 'entrepreneur', 'business', 'ceo', 'company']):
        business_conditions = [
            "p.headline ~* '(founder|co-founder|cofounder|CEO|entrepreneur|startup|company|business|executive|president|director|VP|vice president|C-suite|leadership|strategy|operations|product|marketing|sales|growth|scaling|unicorn|exit|IPO|acquisition|B2B|B2C|SaaS|marketplace|platform|consulting|advisor|board|investor|angel|venture|raised|funding|seed|series|valuation|revenue|customer|user|market|industry|sector)'",
            "p.summary ~* '(founder|co-founder|cofounder|CEO|entrepreneur|startup|company|business|executive|president|director|VP|vice president|C-suite|leadership|strategy|operations|product|marketing|sales|growth|scaling|unicorn|exit|IPO|acquisition|B2B|B2C|SaaS|marketplace|platform|consulting|advisor|board|investor|angel|venture|raised|funding|seed|series|valuation|revenue|customer|user|market|industry|sector)'",
            "p.headline ILIKE '%YC%' OR p.headline ILIKE '%Y Combinator%' OR p.headline ILIKE '%Techstars%' OR p.headline ILIKE '%500 Startups%'",
        ]
        expanded_conditions.extend(business_conditions)
    
    # MEDICINE & HEALTHCARE 
    if any(term in query_text for term in ['medicine', 'medical', 'health', 'doctor', 'physician', 'clinical']):
        medical_conditions = [
            "p.headline ~* '(MD|doctor|physician|medical|medicine|health|healthcare|clinical|hospital|patient|research|biomedical|biotech|pharma|pharmaceutical|drug|therapy|treatment|diagnosis|surgery|cardiology|neurology|oncology|pediatric|psychiatry|radiology|pathology|emergency|ICU|nurse|nursing|public health|epidemiology|clinical trial|FDA|NIH|resident|fellow|attending|professor|faculty|researcher|scientist)'",
            "p.summary ~* '(MD|doctor|physician|medical|medicine|health|healthcare|clinical|hospital|patient|research|biomedical|biotech|pharma|pharmaceutical|drug|therapy|treatment|diagnosis|surgery|cardiology|neurology|oncology|pediatric|psychiatry|radiology|pathology|emergency|ICU|nurse|nursing|public health|epidemiology|clinical trial|FDA|NIH|resident|fellow|attending|professor|faculty|researcher|scientist)'",
        ]
        expanded_conditions.extend(medical_conditions)
    
    # FINANCE & CONSULTING (broad professional services)
    if any(term in query_text for term in ['consulting', 'finance', 'banking', 'analyst', 'advisor']):
        finance_conditions = [
            "p.headline ~* '(consulting|consultant|advisor|McKinsey|BCG|Bain|Deloitte|PwC|EY|KPMG|Accenture|analyst|associate|manager|senior|principal|partner|director|finance|financial|banking|investment banking|corporate finance|treasury|accounting|audit|tax|risk|compliance|strategy|operations|transformation|implementation|client|project|engagement)'",
            "p.summary ~* '(consulting|consultant|advisor|McKinsey|BCG|Bain|Deloitte|PwC|EY|KPMG|Accenture|analyst|associate|manager|senior|principal|partner|director|finance|financial|banking|investment banking|corporate finance|treasury|accounting|audit|tax|risk|compliance|strategy|operations|transformation|implementation|client|project|engagement)'",
        ]
        expanded_conditions.extend(finance_conditions)
    
    # Combine ALL conditions with OR (cast a wide net like Happenstance)
    final_condition = f"({' OR '.join(expanded_conditions)})"
    
    # Include Yale affiliation OR any mention of Yale
    return f"({final_condition}) AND (ya.person_uuid IS NOT NULL OR p.headline ILIKE '%yale%' OR p.summary ILIKE '%yale%')"

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
    print("🚀 Starting Happenstance - Yale Network Search API v3.0...")
    print("📍 API will be available at: http://localhost:8003")
    print("📖 Documentation at: http://localhost:8003/docs")
    print("🔍 Streaming search: http://localhost:8003/search-stream?q=founders")
    print("🧠 Real-time AI-powered discovery engine for Yale's network")
    
    uvicorn.run(app, host="0.0.0.0", port=8003)