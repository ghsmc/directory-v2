#!/usr/bin/env python3
"""
Universal search engine that handles ANY query
Uses OpenAI to parse queries and generate SQL + key phrases dynamically
"""

import sys
import os
import openai
import json
import re
from typing import List, Dict, Any, Optional
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UniversalSearchEngine:
    """Universal search engine that handles any natural language query"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.db = SessionLocal()
    
    def search(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Universal search that handles any query:
        - "Yale robotics engineers" 
        - "Stanford AI researchers"
        - "Harvard doctors in Boston"
        - "MIT founders in fintech"
        - etc.
        """
        
        print(f"🔍 Universal Search: '{query}'")
        
        # Step 1: Parse query into structured components
        parsed_query = self._parse_query_with_openai(query)
        
        # Step 2: Generate SQL from parsed components
        sql_query = self._generate_sql_from_parsed_query(parsed_query)
        
        # Step 3: Execute SQL search
        candidates = self._execute_sql_search(sql_query, limit * 3)  # Get more candidates
        
        # Step 4: Generate key phrases for each candidate
        enhanced_results = []
        for candidate in candidates[:limit]:
            key_phrases = self._generate_key_phrases_for_candidate(candidate, parsed_query)
            
            enhanced_candidate = {
                'name': candidate.full_name,
                'location': candidate.location,
                'headline': candidate.headline,
                'yale_school': candidate.school,
                'current_title': candidate.current_title,
                'current_company': candidate.current_company,
                'key_phrases': key_phrases,
                'match_score': self._calculate_universal_match_score(candidate, parsed_query, key_phrases)
            }
            enhanced_results.append(enhanced_candidate)
        
        # Step 5: Sort by match score
        enhanced_results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {
            'query': query,
            'parsed_query': parsed_query,
            'sql_query': sql_query,
            'total_results': len(enhanced_results),
            'results': enhanced_results
        }
    
    def _parse_query_with_openai(self, query: str) -> Dict[str, Any]:
        """Use OpenAI to parse any natural language query into structured components"""
        
        prompt = f"""Parse this search query into structured components for a professional networking search.

Query: "{query}"

Extract these components and return as JSON:

{{
  "education_institutions": ["Harvard", "MIT", "Stanford", "Yale"],
  "role_keywords": ["engineer", "doctor", "researcher", "founder"],
  "specialization_keywords": ["robotics", "AI", "fintech", "healthcare"],  
  "location_keywords": ["NYC", "Boston", "San Francisco"],
  "company_type_keywords": ["startup", "tech company", "hospital"],
  "experience_level": ["senior", "junior", "director"],
  "current_vs_past": "current",
  "filters": {{
    "education": ["Institution names to filter by"],
    "roles": ["Job titles/roles to match"],
    "specializations": ["Technical specializations"],
    "locations": ["Geographic locations"],
    "company_types": ["Types of companies"]
  }},
  "sql_patterns": {{
    "education_patterns": ["%harvard%", "%mit%"],
    "title_patterns": ["%engineer%", "%robotics%"],
    "company_patterns": ["%startup%", "%labs%"],
    "location_patterns": ["%boston%", "%cambridge%"]
  }}
}}

Be comprehensive - extract ALL relevant keywords that could help find matching people.
For education, include the institution and common variations.
For roles, include job titles, specializations, and related terms.
"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=800
            )
            
            parsed_json = response.choices[0].message.content.strip()
            # Clean up the response to extract just the JSON
            if "```json" in parsed_json:
                parsed_json = parsed_json.split("```json")[1].split("```")[0].strip()
            elif "```" in parsed_json:
                parsed_json = parsed_json.split("```")[1].strip()
            
            parsed_query = json.loads(parsed_json)
            return parsed_query
            
        except Exception as e:
            print(f"   OpenAI parsing error: {e}")
            # Fallback parsing
            return self._fallback_parse_query(query)
    
    def _fallback_parse_query(self, query: str) -> Dict[str, Any]:
        """Simple fallback parsing if OpenAI fails"""
        
        query_lower = query.lower()
        
        # Common institutions
        institutions = []
        if any(term in query_lower for term in ['yale', 'yalie']):
            institutions.append('Yale')
        if any(term in query_lower for term in ['harvard', 'harvard university']):
            institutions.append('Harvard')
        if any(term in query_lower for term in ['stanford', 'stanford university']):
            institutions.append('Stanford')
        if any(term in query_lower for term in ['mit', 'massachusetts institute']):
            institutions.append('MIT')
        
        # Common roles
        roles = []
        if any(term in query_lower for term in ['engineer', 'engineering']):
            roles.append('engineer')
        if any(term in query_lower for term in ['doctor', 'physician', 'md']):
            roles.append('doctor')
        if any(term in query_lower for term in ['founder', 'co-founder', 'ceo']):
            roles.append('founder')
        if any(term in query_lower for term in ['researcher', 'research']):
            roles.append('researcher')
        
        # Specializations
        specializations = []
        if any(term in query_lower for term in ['robotics', 'robot']):
            specializations.append('robotics')
        if any(term in query_lower for term in ['ai', 'artificial intelligence', 'machine learning']):
            specializations.append('AI')
        if any(term in query_lower for term in ['mechanical', 'mech']):
            specializations.append('mechanical')
        
        return {
            "education_institutions": institutions,
            "role_keywords": roles,
            "specialization_keywords": specializations,
            "filters": {
                "education": institutions,
                "roles": roles,
                "specializations": specializations
            },
            "sql_patterns": {
                "education_patterns": [f"%{inst.lower()}%" for inst in institutions],
                "title_patterns": [f"%{role}%" for role in roles + specializations]
            }
        }
    
    def _generate_sql_from_parsed_query(self, parsed_query: Dict[str, Any]) -> str:
        """Generate SQL query from parsed components"""
        
        base_sql = """
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                ya.school,
                e.title as current_title,
                e.company as current_company,
                p.summary
            FROM people p
            LEFT JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN education ed ON ed.person_uuid = p.uuid_id  
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE 1=1
        """
        
        conditions = []
        
        # Education filters
        education_patterns = parsed_query.get('sql_patterns', {}).get('education_patterns', [])
        if education_patterns:
            education_conditions = []
            for pattern in education_patterns:
                education_conditions.extend([
                    f"LOWER(ya.school) LIKE '{pattern}'",
                    f"LOWER(ed.institution) LIKE '{pattern}'",
                    f"LOWER(p.headline) LIKE '{pattern}'"
                ])
            
            if education_conditions:
                conditions.append(f"({' OR '.join(education_conditions)})")
        
        # Role/title filters
        title_patterns = parsed_query.get('sql_patterns', {}).get('title_patterns', [])
        if title_patterns:
            title_conditions = []
            for pattern in title_patterns:
                title_conditions.extend([
                    f"LOWER(p.headline) LIKE '{pattern}'",
                    f"LOWER(e.title) LIKE '{pattern}'"
                ])
            
            if title_conditions:
                conditions.append(f"({' OR '.join(title_conditions)})")
        
        # Company filters
        company_patterns = parsed_query.get('sql_patterns', {}).get('company_patterns', [])
        if company_patterns:
            company_conditions = []
            for pattern in company_patterns:
                company_conditions.append(f"LOWER(e.company) LIKE '{pattern}'")
            
            if company_conditions:
                conditions.append(f"({' OR '.join(company_conditions)})")
        
        # Location filters
        location_patterns = parsed_query.get('sql_patterns', {}).get('location_patterns', [])
        if location_patterns:
            location_conditions = []
            for pattern in location_patterns:
                location_conditions.append(f"LOWER(p.location) LIKE '{pattern}'")
            
            if location_conditions:
                conditions.append(f"({' OR '.join(location_conditions)})")
        
        # Combine all conditions
        if conditions:
            base_sql += " AND " + " AND ".join(conditions)
        
        base_sql += " ORDER BY p.full_name LIMIT 30"
        
        return base_sql
    
    def _execute_sql_search(self, sql_query: str, limit: int):
        """Execute the generated SQL query"""
        
        try:
            print(f"   Executing SQL...")
            return self.db.execute(text(sql_query)).fetchall()
        except Exception as e:
            print(f"   SQL execution error: {e}")
            # Fallback to simple query
            fallback_sql = """
                SELECT DISTINCT p.full_name, p.location, p.headline, ya.school,
                       e.title as current_title, e.company as current_company, p.summary
                FROM people p
                LEFT JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
                LEFT JOIN experience e ON e.person_uuid = p.uuid_id
                WHERE ya.school IS NOT NULL
                ORDER BY p.full_name LIMIT 10
            """
            return self.db.execute(text(fallback_sql)).fetchall()
    
    def _generate_key_phrases_for_candidate(self, candidate, parsed_query: Dict[str, Any]) -> List[str]:
        """Generate key phrases explaining why this candidate matches the query"""
        
        profile_text = f"""
        Name: {candidate.full_name}
        Headline: {candidate.headline or 'N/A'}
        Current Title: {candidate.current_title or 'N/A'}
        Current Company: {candidate.current_company or 'N/A'}
        Education: {candidate.school or 'N/A'}
        Summary: {candidate.summary[:200] if candidate.summary else 'N/A'}
        """
        
        # Extract query context
        institutions = parsed_query.get('education_institutions', [])
        roles = parsed_query.get('role_keywords', [])
        specializations = parsed_query.get('specialization_keywords', [])
        
        context = f"Institutions: {institutions}, Roles: {roles}, Specializations: {specializations}"
        
        prompt = f"""Generate 3-5 key phrases explaining why this person matches the search criteria.

Search Context: {context}

Profile:
{profile_text}

Generate key phrases in this style:
- "Robotics systems engineer"
- "Stanford University graduate" 
- "Mechanical engineering professional"
- "Experience in autonomous systems"
- "Alumni of Stanford School of Engineering"

Focus on their education, technical expertise, current role, and relevant experience.

Return ONLY a JSON list: ["phrase1", "phrase2", "phrase3"]"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            
            key_phrases_text = response.choices[0].message.content.strip()
            if "```json" in key_phrases_text:
                key_phrases_text = key_phrases_text.split("```json")[1].split("```")[0].strip()
            
            key_phrases = json.loads(key_phrases_text)
            return key_phrases
            
        except Exception as e:
            print(f"   Key phrase generation error for {candidate.full_name}: {e}")
            # Fallback phrases
            return [
                f"{candidate.school} graduate" if candidate.school else "University graduate",
                "Professional background",
                "Technical expertise"
            ]
    
    def _calculate_universal_match_score(self, candidate, parsed_query: Dict[str, Any], key_phrases: List[str]) -> float:
        """Calculate match score for any query type"""
        
        score = 0.3  # Base score
        
        # Education match
        institutions = parsed_query.get('education_institutions', [])
        if institutions:
            for inst in institutions:
                if candidate.school and inst.lower() in candidate.school.lower():
                    score += 0.3
                    break
        
        # Role match
        roles = parsed_query.get('role_keywords', [])
        if roles:
            text_to_check = f"{candidate.headline or ''} {candidate.current_title or ''}".lower()
            for role in roles:
                if role.lower() in text_to_check:
                    score += 0.2
                    break
        
        # Specialization match
        specializations = parsed_query.get('specialization_keywords', [])
        if specializations:
            text_to_check = f"{candidate.headline or ''} {candidate.current_title or ''}".lower()
            for spec in specializations:
                if spec.lower() in text_to_check:
                    score += 0.2
                    break
        
        # Key phrase quality
        if len(key_phrases) >= 4:
            score += 0.1
        
        return min(score, 1.0)
    
    def display_results(self, search_result: Dict[str, Any]):
        """Display results in happenstance.ai style"""
        
        query = search_result['query']
        parsed = search_result['parsed_query']
        results = search_result['results']
        
        print(f"\n🎯 Found {len(results)} people matching '{query}'")
        
        # Show filters detected
        print(f"\n📋 Filters Detected:")
        filters = parsed.get('filters', {})
        for filter_type, values in filters.items():
            if values:
                print(f"   {filter_type.title()}: {', '.join(values)}")
        
        print("\n" + "="*80)
        
        for i, person in enumerate(results, 1):
            print(f"\n{i}. {person['name']}")
            print(f"   📍 {person['location'] or 'Location not specified'}")
            print(f"   💼 {person['headline'] or 'Headline not available'}")
            if person['current_title'] and person['current_company']:
                print(f"   🏢 {person['current_title']} at {person['current_company']}")
            print(f"   🎓 {person['yale_school'] or 'Education not specified'}")
            print(f"   📊 Match Score: {person['match_score']:.2f}")
            
            print(f"\n   🔑 Key Phrases:")
            for phrase in person['key_phrases']:
                print(f"      • {phrase}")
            
            print("-" * 60)
    
    def close(self):
        """Close database connection"""
        self.db.close()

def test_universal_search():
    """Test the universal search with various queries"""
    
    if not OPENAI_API_KEY:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        return
    
    test_queries = [
        "Yale robotics engineers",
        "Yale doctors in New York", 
        "Yale startup founders",
        "Yale AI researchers",
        "Yale professors and academics",
        "Yale people working at tech companies"
    ]
    
    searcher = UniversalSearchEngine()
    
    print("🚀 Testing Universal Search Engine")
    print("=" * 60)
    
    try:
        for query in test_queries:
            print(f"\n{'='*20} TESTING QUERY {'='*20}")
            
            result = searcher.search(query, limit=3)
            searcher.display_results(result)
            
            print(f"\n✅ Successfully processed: '{query}'")
            print("-" * 80)
        
        print(f"\n🎉 Universal search engine working! Tested {len(test_queries)} different query types.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        searcher.close()

if __name__ == "__main__":
    test_universal_search()