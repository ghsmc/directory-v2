#!/usr/bin/env python3
"""
OpenAI-enhanced search that generates semantic key phrases
Matches the happenstance.ai pattern with AI-generated explanations
"""

import sys
import os
import openai
import json
from typing import List, Dict, Any
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class OpenAIEnhancedSearch:
    """Search engine with OpenAI-powered semantic analysis"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.db = SessionLocal()
    
    def search_yale_engineers_at_startups(self, limit: int = 10):
        """Enhanced search with OpenAI semantic analysis"""
        
        print("🔍 Searching: Yale engineers at startups (with OpenAI analysis)")
        
        # Step 1: SQL search for candidates
        candidates = self._get_sql_candidates()
        
        # Step 2: Generate key phrases for each candidate
        enhanced_results = []
        for candidate in candidates[:limit]:
            key_phrases = self._generate_key_phrases(candidate)
            
            enhanced_candidate = {
                'name': candidate.full_name,
                'location': candidate.location,
                'headline': candidate.headline,
                'yale_school': candidate.school,
                'current_title': candidate.current_title,
                'current_company': candidate.current_company,
                'key_phrases': key_phrases,
                'match_score': self._calculate_match_score(candidate, key_phrases)
            }
            enhanced_results.append(enhanced_candidate)
        
        # Step 3: Sort by match score
        enhanced_results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return enhanced_results
    
    def _get_sql_candidates(self):
        """Get SQL candidates using advanced filtering"""
        
        query = text("""
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                ya.school,
                e.title as current_title,
                e.company as current_company,
                p.summary
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE
                -- Yale education filter
                (ya.school IS NOT NULL)
                AND
                -- Engineer title filter (broad)
                (
                    LOWER(p.headline) LIKE '%engineer%'
                    OR LOWER(p.headline) LIKE '%developer%'
                    OR LOWER(p.headline) LIKE '%software%'
                    OR LOWER(p.headline) LIKE '%technical%'
                    OR LOWER(p.headline) LIKE '%cto%'
                    OR LOWER(p.headline) LIKE '%architect%'
                    OR LOWER(p.headline) LIKE '%product%'
                    OR LOWER(p.headline) LIKE '%technology%'
                    OR LOWER(e.title) LIKE '%engineer%'
                    OR LOWER(e.title) LIKE '%developer%'
                    OR LOWER(e.title) LIKE '%software%'
                    OR LOWER(e.title) LIKE '%technical%'
                    OR LOWER(e.title) LIKE '%cto%'
                    OR LOWER(e.title) LIKE '%architect%'
                    OR LOWER(e.title) LIKE '%product%'
                )
                AND
                -- Startup/tech company filter (broad)
                (
                    LOWER(p.headline) LIKE '%startup%'
                    OR LOWER(p.headline) LIKE '%founder%'
                    OR LOWER(p.headline) LIKE '%co-founder%'
                    OR LOWER(e.company) LIKE '%startup%'
                    OR LOWER(e.company) LIKE '%labs%'
                    OR LOWER(e.company) LIKE '%technologies%'
                    OR LOWER(e.company) LIKE '%systems%'
                    OR LOWER(e.company) LIKE '%solutions%'
                    OR LOWER(e.company) LIKE '%platform%'
                    OR LOWER(e.company) LIKE '%inc%'
                    OR LOWER(e.company) LIKE '%ai%'
                    OR LOWER(e.company) LIKE '%tech%'
                    OR LOWER(e.company) LIKE '%innovation%'
                    OR LOWER(e.company) LIKE '%digital%'
                    OR LOWER(e.company) LIKE '%data%'
                    OR LOWER(e.company) LIKE '%software%'
                    OR LOWER(e.company) LIKE '%app%'
                    OR LOWER(e.company) LIKE '%network%'
                    OR LOWER(e.company) LIKE '%consulting%'
                    OR LOWER(e.company) LIKE '%services%'
                )
            ORDER BY p.full_name
            LIMIT 20
        """)
        
        return self.db.execute(query).fetchall()
    
    def _generate_key_phrases(self, candidate) -> List[str]:
        """Use OpenAI to generate semantic key phrases explaining the match"""
        
        # Build context about the person
        profile_text = f"""
        Name: {candidate.full_name}
        Headline: {candidate.headline or 'N/A'}
        Current Title: {candidate.current_title or 'N/A'}
        Current Company: {candidate.current_company or 'N/A'}
        Yale School: {candidate.school}
        Summary: {candidate.summary[:200] if candidate.summary else 'N/A'}
        """
        
        prompt = f"""You are analyzing a person's profile to explain why they match the search "Yale engineers at startups".

Profile:
{profile_text}

Generate 3-5 key phrases that explain why this person matches "Yale engineers at startups". Use the exact style from this example:

Example key phrases:
- "Engineering professional"  
- "Mechanical engineer by training"
- "Product developer with a technical background"
- "Yale University graduate"
- "Alumni of Yale College"
- "Earned a degree from Yale"
- "Startup team member"
- "Early-stage company employee"
- "Building products at a venture-backed startup"

Focus on:
1. Their engineering/technical background
2. Their Yale education/affiliation
3. Their startup/entrepreneurial experience
4. Their specific expertise areas

Return ONLY a JSON list of key phrases, no other text:
["phrase1", "phrase2", "phrase3", ...]"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse the JSON response
            key_phrases_text = response.choices[0].message.content.strip()
            key_phrases = json.loads(key_phrases_text)
            
            return key_phrases
            
        except Exception as e:
            print(f"   OpenAI error for {candidate.full_name}: {e}")
            # Fallback key phrases
            return [
                "Yale University graduate",
                "Technical professional",
                "Engineering background"
            ]
    
    def _calculate_match_score(self, candidate, key_phrases: List[str]) -> float:
        """Calculate match score based on profile and key phrases"""
        
        score = 0.5  # Base score for Yale affiliation
        
        # Boost for engineering keywords
        text_to_check = f"{candidate.headline or ''} {candidate.current_title or ''}".lower()
        
        eng_keywords = ['engineer', 'developer', 'software', 'technical', 'cto', 'architect', 'product']
        for keyword in eng_keywords:
            if keyword in text_to_check:
                score += 0.15
                break
        
        # Boost for startup keywords  
        startup_keywords = ['startup', 'founder', 'co-founder', 'ceo', 'entrepreneur']
        for keyword in startup_keywords:
            if keyword in text_to_check:
                score += 0.15
                break
        
        # Boost for company indicators
        company_text = (candidate.current_company or '').lower()
        company_keywords = ['tech', 'labs', 'systems', 'solutions', 'platform', 'ai', 'software']
        for keyword in company_keywords:
            if keyword in company_text:
                score += 0.1
                break
        
        # Boost for key phrase quality
        if len(key_phrases) >= 4:
            score += 0.1
        
        return min(score, 1.0)
    
    def display_results(self, results: List[Dict]):
        """Display results in happenstance.ai style"""
        
        print(f"\n🎯 Found {len(results)} Yale engineers at startups")
        print("\n" + "="*80)
        
        for i, person in enumerate(results, 1):
            print(f"\n{i}. {person['name']}")
            print(f"   📍 {person['location'] or 'Location not specified'}")
            print(f"   💼 {person['headline'] or 'Headline not available'}")
            if person['current_title'] and person['current_company']:
                print(f"   🏢 {person['current_title']} at {person['current_company']}")
            print(f"   🎓 {person['yale_school']}")
            print(f"   📊 Match Score: {person['match_score']:.2f}")
            
            print(f"\n   🔑 Key Phrases:")
            for phrase in person['key_phrases']:
                print(f"      • {phrase}")
            
            print("-" * 60)
    
    def close(self):
        """Close database connection"""
        self.db.close()

def test_openai_enhanced_search():
    """Test the OpenAI-enhanced search functionality"""
    
    if not OPENAI_API_KEY:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        return
    
    print("🚀 Testing OpenAI-Enhanced Yale Engineer Search")
    print("=" * 60)
    
    searcher = OpenAIEnhancedSearch()
    
    try:
        # Run the enhanced search
        results = searcher.search_yale_engineers_at_startups(limit=5)
        
        # Display results
        searcher.display_results(results)
        
        print(f"\n🎉 Success! Generated semantic key phrases for {len(results)} candidates")
        print("   This matches the happenstance.ai style with AI-powered explanations!")
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
    
    finally:
        searcher.close()

if __name__ == "__main__":
    test_openai_enhanced_search()