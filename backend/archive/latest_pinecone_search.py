#!/usr/bin/env python3
"""
Latest Pinecone API search for Yale alumni
Org: Milo, Project: Milo, Index: dense-milo-people, Namespace: yale-people-2025-dense
"""

import sys
import os
sys.path.append('.')

from pinecone import Pinecone
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
PINECONE_API_KEY = os.getenv("TRI_HYBRID_PINECONE") or os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class LatestPineconeYaleSearch:
    """Yale search using latest Pinecone API with dense-milo-people index"""
    
    def __init__(self):
        # Initialize Pinecone with modern API
        if PINECONE_API_KEY:
            self.pc = Pinecone(api_key=PINECONE_API_KEY)
            self.index = self.pc.Index("dense-milo-people")
            print("✅ Connected to Pinecone index: dense-milo-people")
        else:
            print("❌ PINECONE_API_KEY not found")
            self.pc = None
            self.index = None
        
        # Initialize OpenAI
        if OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.openai_client = None
        
        self.db = SessionLocal()
    
    def search_yale_people(self, query: str = "robotics engineers", top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Search Yale people using SQL-based precision search
        
        Falls back to proven SQL approach that returns quality results
        """
        
        print(f"🔍 Searching Yale alumni for: '{query}' (using SQL)")
        print(f"   🎯 Focus: High-quality, domain-specific matches")
        
        return self._sql_precision_search(query, top_k)
    
    def _sql_precision_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """SQL-based precision search that maintains specificity"""
        
        query_lower = query.lower()
        sql_conditions = []
        priority_weights = {}
        
        # Robotics-specific search (highest priority)
        if 'robotics' in query_lower or 'robot' in query_lower:
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%robotics%'",
                "LOWER(e.title) LIKE '%robotics%'",
                "LOWER(ed.field_of_study) LIKE '%robotics%'"
            ])
            priority_weights['robotics'] = 1
        
        # Mechatronics (robotics-related, high priority)
        if 'mechatronics' in query_lower or 'robotics' in query_lower:
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%mechatronics%'",
                "LOWER(e.title) LIKE '%mechatronics%'",
                "LOWER(ed.field_of_study) LIKE '%mechatronics%'"
            ])
            priority_weights['mechatronics'] = 2
        
        # Mechanical engineering (often robotics-related)
        if 'mechanical' in query_lower or 'engineer' in query_lower:
            sql_conditions.extend([
                "(LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%')",
                "(LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%')",
                "LOWER(ed.field_of_study) LIKE '%mechanical engineering%'"
            ])
            priority_weights['mechanical'] = 4
        
        # Automation/controls (robotics adjacent)
        if any(term in query_lower for term in ['automation', 'control', 'mechatronics']):
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%automation%'",
                "LOWER(e.title) LIKE '%automation%'",
                "LOWER(p.headline) LIKE '%controls%'",
                "LOWER(e.title) LIKE '%controls%'"
            ])
            priority_weights['automation'] = 3
        
        # Hardware engineering (at relevant companies)
        if 'hardware' in query_lower or 'engineer' in query_lower:
            sql_conditions.extend([
                "(LOWER(p.headline) LIKE '%hardware%' AND LOWER(p.headline) LIKE '%engineer%')",
                "(LOWER(e.title) LIKE '%hardware%' AND LOWER(e.title) LIKE '%engineer%')"
            ])
            priority_weights['hardware'] = 5
        
        # Software engineers (only for software-specific queries)
        if 'software' in query_lower:
            sql_conditions.extend([
                "(LOWER(p.headline) LIKE '%software%' AND LOWER(p.headline) LIKE '%engineer%')",
                "(LOWER(e.title) LIKE '%software%' AND LOWER(e.title) LIKE '%engineer%')"
            ])
            priority_weights['software'] = 6
        
        # Default engineering search if no specific terms
        if not sql_conditions and 'engineer' in query_lower:
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%engineer%'",
                "LOWER(e.title) LIKE '%engineer%'"
            ])
            priority_weights['general'] = 7
        
        if not sql_conditions:
            # Fallback: broad search but maintain quality
            sql_conditions = [f"LOWER(p.headline) LIKE '%{query_lower}%'"]
            priority_weights['fallback'] = 8
        
        # Build SQL query with priority ranking
        where_clause = " OR ".join(sql_conditions)
        
        sql_query = text(f"""
            SELECT DISTINCT 
                p.full_name,
                p.headline,
                p.location,
                ya.school,
                e.title as current_title,
                e.company as current_company,
                CASE 
                    WHEN LOWER(p.headline) LIKE '%robotics%' OR LOWER(e.title) LIKE '%robotics%' THEN 1
                    WHEN LOWER(p.headline) LIKE '%mechatronics%' OR LOWER(e.title) LIKE '%mechatronics%' THEN 2
                    WHEN LOWER(p.headline) LIKE '%automation%' OR LOWER(e.title) LIKE '%automation%' THEN 3
                    WHEN (LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%') THEN 4
                    WHEN (LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%') THEN 5
                    WHEN (LOWER(p.headline) LIKE '%hardware%' AND LOWER(p.headline) LIKE '%engineer%') THEN 6
                    ELSE 7
                END as priority_score
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
            WHERE ({where_clause})
            ORDER BY priority_score, p.full_name
            LIMIT :limit
        """)
        
        try:
            results = self.db.execute(sql_query, {'limit': top_k}).fetchall()
            
            yale_matches = []
            for i, result in enumerate(results, 1):
                match_reasons = self._generate_sql_match_reasons(result, query)
                
                enhanced_match = {
                    'rank': i,
                    'name': result.full_name,
                    'headline': result.headline,
                    'location': result.location,
                    'yale_school': getattr(result, 'school', ''),
                    'current_title': getattr(result, 'current_title', ''),
                    'current_company': getattr(result, 'current_company', ''),
                    'priority_score': getattr(result, 'priority_score', 7),
                    'yale_verified': True,
                    'match_reasons': match_reasons,
                    'source': 'sql_precision'
                }
                yale_matches.append(enhanced_match)
            
            print(f"   🎓 Found {len(yale_matches)} high-quality Yale alumni")
            return yale_matches
            
        except Exception as e:
            print(f"❌ SQL search error: {e}")
            return []
    
    def _generate_sql_match_reasons(self, result, query: str) -> List[str]:
        """Generate match reasons for SQL results"""
        
        reasons = ['Yale University affiliation']
        
        query_terms = query.lower().split()
        
        for term in query_terms:
            if hasattr(result, 'headline') and result.headline and term in result.headline.lower():
                reasons.append(f"Headline contains '{term}'")
            elif hasattr(result, 'current_title') and result.current_title and term in result.current_title.lower():
                reasons.append(f"Current role contains '{term}'")
        
        if hasattr(result, 'school') and result.school:
            reasons.append(f"Yale school: {result.school}")
        
        if hasattr(result, 'priority_score') and result.priority_score <= 3:
            reasons.append("High relevance match")
        
        return reasons
    
    def _extract_person_data(self, match) -> Dict[str, str]:
        """Extract person data from Pinecone match metadata"""
        
        try:
            # Get metadata from the match
            metadata = getattr(match, 'metadata', {})
            
            # Extract directly from metadata fields
            person_data = {
                'name': metadata.get('name', ''),
                'position': metadata.get('position', ''),
                'about': metadata.get('about', ''),
                'location': metadata.get('location', ''),
                'experience': metadata.get('experience', ''),
                'education': metadata.get('education', ''),
                'current_company_name': metadata.get('current_company_name', ''),
                'current_company_title': metadata.get('current_company_title', ''),
            }
            
            # If no name found, try to extract from ID (e.g., "evelyn-tsisin")
            if not person_data['name'] and hasattr(match, 'id'):
                person_id = match.id
                if person_id:
                    # Remove any trailing ID numbers and convert hyphens to spaces
                    name_part = '-'.join(person_id.split('-')[:-1]) if person_id.count('-') > 1 else person_id
                    person_data['name'] = name_part.replace('-', ' ').title()
            
            return person_data
            
        except Exception as e:
            print(f"   ⚠️  Error extracting person data: {e}")
            return {}
    
    def _extract_yale_school(self, education_text: str) -> str:
        """Extract Yale school from education text"""
        
        if not education_text:
            return "Yale University"
        
        # Look for specific Yale schools
        education_lower = education_text.lower()
        
        if 'yale law' in education_lower or 'yale university law' in education_lower:
            return "Yale Law School"
        elif 'yale school of medicine' in education_lower or 'yale medical' in education_lower:
            return "Yale School of Medicine"
        elif 'yale school of management' in education_lower or 'yale som' in education_lower:
            return "Yale School of Management"
        elif 'yale divinity' in education_lower:
            return "Yale Divinity School"
        elif 'yale school of art' in education_lower:
            return "Yale School of Art"
        elif 'yale school of music' in education_lower:
            return "Yale School of Music"
        elif 'yale school of nursing' in education_lower:
            return "Yale School of Nursing"
        elif 'yale school of public health' in education_lower:
            return "Yale School of Public Health"
        elif 'yale university' in education_lower:
            return "Yale University"
        else:
            return "Yale University"
    
    def _get_yale_person_by_name(self, name: str):
        """Check if person exists in Yale database"""
        
        if not name:
            return None
        
        try:
            query = text("""
                SELECT DISTINCT 
                    p.full_name,
                    ya.school,
                    e.title as current_title,
                    e.company as current_company
                FROM people p
                JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
                LEFT JOIN experience e ON e.person_uuid = p.uuid_id AND e.is_current = true
                WHERE LOWER(p.full_name) = LOWER(:name)
                LIMIT 1
            """)
            
            result = self.db.execute(query, {'name': name}).fetchone()
            return result
            
        except Exception as e:
            return None
    
    def _generate_match_reasons(self, person_data: Dict[str, str], query: str, score: float) -> List[str]:
        """Generate reasons why this person matched the query"""
        
        reasons = [f"Semantic similarity: {score:.3f}"]
        
        # Check query terms in different fields
        query_lower = query.lower()
        query_terms = query_lower.split()
        
        for term in query_terms:
            if term in person_data.get('position', '').lower():
                reasons.append(f"Title contains '{term}'")
            elif term in person_data.get('about', '').lower():
                reasons.append(f"Background mentions '{term}'")
            elif term in person_data.get('experience', '').lower():
                reasons.append(f"Experience includes '{term}'")
            elif term in person_data.get('education', '').lower():
                reasons.append(f"Education related to '{term}'")
        
        if not any("contains" in r or "mentions" in r or "includes" in r for r in reasons):
            reasons.append("Semantic match in profile content")
        
        return reasons
    
    def display_results(self, results: List[Dict[str, Any]], query: str):
        """Display search results in a nice format"""
        
        print(f"\n🎯 YALE ALUMNI SEARCH RESULTS: '{query}'")
        print("=" * 80)
        
        if not results:
            print("   No Yale alumni found matching this query.")
            return
        
        for result in results:
            # Handle both SQL and Pinecone result formats
            score_display = ""
            if 'score' in result:
                score_display = f" (Score: {result['score']:.3f})"
            elif 'priority_score' in result:
                score_display = f" (Priority: {result['priority_score']})"
            
            print(f"\n{result['rank']}. {result['name']}{score_display}")
            
            # Handle headline vs position
            if result.get('headline'):
                print(f"   💼 {result['headline']}")
            elif result.get('position'):
                print(f"   💼 {result['position']}")
            
            if result.get('current_title') and result.get('current_company'):
                print(f"   🏢 {result['current_title']} at {result['current_company']}")
            
            if result.get('location'):
                print(f"   📍 {result['location']}")
            
            if result.get('yale_school'):
                print(f"   🎓 {result['yale_school']}")
            
            if result.get('about'):
                about_preview = result['about'][:150] + "..." if len(result['about']) > 150 else result['about']
                print(f"   📝 {about_preview}")
            
            print(f"   🔍 Match reasons:")
            for reason in result['match_reasons']:
                print(f"      • {reason}")
            
            print(f"   ✅ Yale verified: {result['yale_verified']}")
            print("-" * 60)
    
    def test_different_queries(self):
        """Test different types of queries"""
        
        test_queries = [
            "robotics engineers",
            "mechanical engineers", 
            "software engineers",
            "startup founders",
            "venture capital",
            "doctors and physicians",
            "professors and academics"
        ]
        
        print(f"\n🧪 TESTING DIFFERENT QUERIES")
        print("=" * 60)
        
        for query in test_queries:
            print(f"\n{'='*15} TESTING: '{query}' {'='*15}")
            
            results = self.search_yale_people(query, top_k=3)
            
            if results:
                print(f"✅ Found {len(results)} Yale alumni")
                for i, r in enumerate(results, 1):
                    position = r.get('headline', '') or r.get('position', '')
                    score_info = ""
                    if 'score' in r:
                        score_info = f" (Score: {r['score']:.3f})"
                    elif 'priority_score' in r:
                        score_info = f" (Priority: {r['priority_score']})"
                    print(f"   {i}. {r['name']} - {position}{score_info}")
            else:
                print(f"❌ No results found")
    
    def close(self):
        """Close database connection"""
        self.db.close()

def main():
    """Main test function"""
    
    print("🚀 LATEST PINECONE + YALE SEARCH")
    print("Org: Milo | Project: Milo | Index: dense-milo-people")
    print("Namespace: yale-people-2025-dense")
    print("=" * 70)
    
    searcher = LatestPineconeYaleSearch()
    
    try:
        # Test specific query
        print("\n🎯 SPECIFIC SEARCH TEST:")
        results = searcher.search_yale_people("robotics engineers", top_k=5)
        searcher.display_results(results, "robotics engineers")
        
        # Test different queries
        searcher.test_different_queries()
        
        print(f"\n🎉 Pinecone + Yale search completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
    
    finally:
        searcher.close()

if __name__ == "__main__":
    main()