#!/usr/bin/env python3
"""
Pinecone-enhanced search for Yale alumni
Combines semantic search with SQL filtering for perfect results
"""

import sys
import os
sys.path.append('.')

from pinecone import Pinecone, ServerlessSpec
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class PineconeYaleSearch:
    """Advanced search combining Pinecone semantic search with Yale SQL filtering"""
    
    def __init__(self):
        # Initialize Pinecone
        if PINECONE_API_KEY:
            self.pc = Pinecone(api_key=PINECONE_API_KEY)
            self.index = self.pc.Index("dense-milo-people")
        else:
            print("⚠️  PINECONE_API_KEY not found - falling back to SQL only")
            self.pc = None
            self.index = None
        
        # Initialize OpenAI for embedding generation
        if OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.openai_client = None
        
        self.db = SessionLocal()
    
    def search_yale_engineers(self, query: str = "robotics engineers", top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Advanced search combining Pinecone + Yale database
        
        1. Search Pinecone for semantic matches
        2. Filter to only Yale people in our database
        3. Return top 10 results with explanations
        """
        
        print(f"🔍 Searching Yale alumni for: '{query}'")
        
        # Step 1: Get semantic matches from Pinecone
        if self.index:
            pinecone_results = self._search_pinecone(query, top_k=100)  # Get more candidates
            print(f"   📊 Pinecone found {len(pinecone_results)} semantic matches")
        else:
            pinecone_results = []
            print("   ⚠️  Pinecone not available - using SQL only")
        
        # Step 2: Filter to Yale people and enrich with our data
        yale_matches = self._filter_to_yale_alumni(pinecone_results)
        print(f"   🎓 {len(yale_matches)} are Yale alumni in our database")
        
        # Step 3: If we don't have enough from Pinecone, supplement with SQL
        if len(yale_matches) < top_k:
            sql_supplements = self._get_sql_supplements(query, top_k - len(yale_matches))
            yale_matches.extend(sql_supplements)
            print(f"   🔍 Added {len(sql_supplements)} from SQL search")
        
        # Step 4: Generate explanations and scores
        final_results = []
        for i, match in enumerate(yale_matches[:top_k]):
            explained_match = self._add_explanations(match, query, i+1)
            final_results.append(explained_match)
        
        print(f"   ✅ Returning {len(final_results)} final results")
        
        return final_results
    
    def _search_pinecone(self, query: str, top_k: int = 100) -> List[Dict[str, Any]]:
        """Search Pinecone for semantic matches"""
        
        if not self.index:
            return []
        
        try:
            # Query the yale-people namespace
            results = self.index.query(
                namespace="yale-people-2025-dense",
                vector=None,  # Let Pinecone generate the embedding
                query_text=query,
                top_k=top_k,
                include_metadata=True
            )
            
            pinecone_matches = []
            for match in results.matches:
                pinecone_matches.append({
                    'id': match.id,
                    'score': match.score,
                    'metadata': match.metadata,
                    'source': 'pinecone'
                })
            
            return pinecone_matches
            
        except Exception as e:
            print(f"   ⚠️  Pinecone search error: {e}")
            return []
    
    def _filter_to_yale_alumni(self, pinecone_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter Pinecone results to only Yale alumni in our database"""
        
        if not pinecone_results:
            return []
        
        yale_matches = []
        
        for pinecone_match in pinecone_results:
            # Extract name from Pinecone ID or metadata
            name = self._extract_name_from_pinecone(pinecone_match)
            
            if name:
                # Check if this person is in our Yale database
                yale_person = self._get_yale_person_by_name(name)
                
                if yale_person:
                    # Combine Pinecone data with Yale database data
                    combined_match = {
                        'name': yale_person.full_name,
                        'headline': yale_person.headline,
                        'location': yale_person.location,
                        'yale_school': yale_person.school,
                        'current_title': yale_person.current_title,
                        'current_company': yale_person.current_company,
                        'pinecone_score': pinecone_match['score'],
                        'pinecone_metadata': pinecone_match.get('metadata', {}),
                        'source': 'yale_database'
                    }
                    yale_matches.append(combined_match)
        
        return yale_matches
    
    def _extract_name_from_pinecone(self, pinecone_match: Dict[str, Any]) -> str:
        """Extract person name from Pinecone ID or metadata"""
        
        # Try to get name from metadata first
        metadata = pinecone_match.get('metadata', {})
        if 'chunk_text' in metadata:
            chunk_text = metadata['chunk_text']
            # Parse "name: John Doe" from chunk_text
            if 'name:' in chunk_text:
                name_part = chunk_text.split('name:')[1].split('position:')[0].strip()
                return name_part
        
        # Fallback: parse from ID (e.g., "fazlur-rahman-khan-5a8769210" -> "Fazlur Rahman Khan")
        person_id = pinecone_match.get('id', '')
        if person_id:
            # Remove the trailing ID part and convert hyphens to spaces
            name_part = '-'.join(person_id.split('-')[:-1])  # Remove last part (ID)
            name = name_part.replace('-', ' ').title()
            return name
        
        return None
    
    def _get_yale_person_by_name(self, name: str):
        """Get Yale person from database by name"""
        
        try:
            query = text("""
                SELECT DISTINCT 
                    p.full_name,
                    p.headline,
                    p.location,
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
            print(f"   ⚠️  Database lookup error for {name}: {e}")
            return None
    
    def _get_sql_supplements(self, query: str, needed_count: int) -> List[Dict[str, Any]]:
        """Get additional results from SQL to supplement Pinecone results"""
        
        # Parse query to understand what we're looking for
        query_lower = query.lower()
        
        sql_conditions = []
        
        # Robotics-specific search
        if 'robotics' in query_lower or 'robot' in query_lower:
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%robotics%'",
                "LOWER(e.title) LIKE '%robotics%'",
                "LOWER(ed.field_of_study) LIKE '%robotics%'"
            ])
        
        # Mechanical engineering
        if 'mechanical' in query_lower or 'engineer' in query_lower:
            sql_conditions.extend([
                "(LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%')",
                "(LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%')",
                "LOWER(ed.field_of_study) LIKE '%mechanical engineering%'"
            ])
        
        # Automation/controls
        if any(term in query_lower for term in ['automation', 'control', 'mechatronics']):
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%automation%'",
                "LOWER(e.title) LIKE '%automation%'",
                "LOWER(p.headline) LIKE '%mechatronics%'",
                "LOWER(e.title) LIKE '%mechatronics%'"
            ])
        
        # Default engineering search if no specific terms
        if not sql_conditions:
            sql_conditions.extend([
                "LOWER(p.headline) LIKE '%engineer%'",
                "LOWER(e.title) LIKE '%engineer%'"
            ])
        
        # Build SQL query
        where_clause = " OR ".join(sql_conditions)
        
        sql_query = text(f"""
            SELECT DISTINCT 
                p.full_name,
                p.headline,
                p.location,
                ya.school,
                e.title as current_title,
                e.company as current_company
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
            WHERE ({where_clause})
            ORDER BY p.full_name
            LIMIT :limit
        """)
        
        try:
            results = self.db.execute(sql_query, {'limit': needed_count}).fetchall()
            
            sql_matches = []
            for result in results:
                sql_match = {
                    'name': result.full_name,
                    'headline': result.headline,
                    'location': result.location,
                    'yale_school': result.school,
                    'current_title': result.current_title,
                    'current_company': result.current_company,
                    'pinecone_score': 0.0,  # No Pinecone score for SQL results
                    'source': 'sql_supplement'
                }
                sql_matches.append(sql_match)
            
            return sql_matches
            
        except Exception as e:
            print(f"   ⚠️  SQL supplement error: {e}")
            return []
    
    def _add_explanations(self, match: Dict[str, Any], query: str, rank: int) -> Dict[str, Any]:
        """Add explanations and enhanced scoring to each match"""
        
        # Calculate final score
        final_score = match.get('pinecone_score', 0.0)
        
        # Boost score for Yale affiliation
        if match.get('yale_school'):
            final_score += 0.2
        
        # Generate match reasons
        match_reasons = ['Yale University affiliation']
        
        if match.get('pinecone_score', 0) > 0:
            match_reasons.append(f"Semantic similarity: {match['pinecone_score']:.3f}")
        
        if match.get('current_title'):
            match_reasons.append(f"Current role: {match['current_title']}")
        
        if match.get('yale_school'):
            match_reasons.append(f"Yale school: {match['yale_school']}")
        
        # Enhanced match data
        enhanced_match = {
            'rank': rank,
            'name': match['name'],
            'headline': match.get('headline', ''),
            'location': match.get('location', ''),
            'yale_school': match.get('yale_school', ''),
            'current_title': match.get('current_title', ''),
            'current_company': match.get('current_company', ''),
            'final_score': final_score,
            'pinecone_score': match.get('pinecone_score', 0.0),
            'match_reasons': match_reasons,
            'source': match.get('source', 'unknown')
        }
        
        return enhanced_match
    
    def display_results(self, results: List[Dict[str, Any]], query: str):
        """Display results in a nice format"""
        
        print(f"\n🎯 FINAL RESULTS: Yale alumni matching '{query}'")
        print("=" * 80)
        
        for result in results:
            print(f"\n{result['rank']}. {result['name']} (Score: {result['final_score']:.3f})")
            print(f"   💼 {result['headline']}")
            if result['current_title'] and result['current_company']:
                print(f"   🏢 {result['current_title']} at {result['current_company']}")
            print(f"   🎓 {result['yale_school']}")
            print(f"   📍 {result['location']}")
            print(f"   🔍 Source: {result['source']}")
            
            print(f"   ✨ Match reasons:")
            for reason in result['match_reasons']:
                print(f"      • {reason}")
            
            print("-" * 60)
    
    def close(self):
        """Close database connection"""
        self.db.close()

def test_pinecone_yale_search():
    """Test the combined Pinecone + Yale search"""
    
    print("🚀 TESTING PINECONE + YALE ENHANCED SEARCH")
    print("=" * 70)
    
    searcher = PineconeYaleSearch()
    
    try:
        # Test different queries
        test_queries = [
            "robotics engineers",
            "mechanical engineers", 
            "automation engineers",
            "Yale founders",
            "engineers at startups"
        ]
        
        for query in test_queries:
            print(f"\n{'='*20} TESTING: '{query}' {'='*20}")
            
            results = searcher.search_yale_engineers(query, top_k=5)
            searcher.display_results(results, query)
            
            if not results:
                print(f"   ⚠️  No results found for '{query}'")
        
        print(f"\n🎉 Pinecone + Yale search testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        searcher.close()

if __name__ == "__main__":
    test_pinecone_yale_search()