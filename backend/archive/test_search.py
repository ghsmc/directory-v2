#!/usr/bin/env python3
"""Test the search functionality with real data"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.search.search_engine import YaleSearchEngine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_search():
    """Test search functionality"""
    
    db_session = SessionLocal()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("OpenAI API key not found in environment")
        return
        
    search_engine = YaleSearchEngine(db_session, openai_api_key)
    
    # Test queries
    test_queries = [
        "Yale alumni in Connecticut",
        "People from Yale University",
        "Yale graduates working as professors",
        "Alumni from New Haven"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Testing query: {query}")
        print(f"{'='*50}")
        
        try:
            results = search_engine.search(query, limit=5, use_semantic_search=False)
            
            print(f"Intent: {results['parsed_query']['intent']}")
            print(f"Filters found: {len(results['parsed_query']['filters'])}")
            for filter in results['parsed_query']['filters']:
                print(f"  - {filter['type']}: {filter['values']}")
                
            print(f"\nResults found: {results['total_results']}")
            
            for i, result in enumerate(results['results'][:3], 1):
                print(f"\n{i}. {result['name']}")
                print(f"   Location: {result['location']}")
                print(f"   Yale: {result.get('yale_info', {}).get('school', 'N/A')}")
                if result.get('current_position'):
                    print(f"   Current: {result['current_position']['title']} at {result['current_position']['company']}")
                print(f"   Score: {result['score']:.2f}")
                if result.get('matched_filters'):
                    print(f"   Matched: {result['matched_filters']}")
                    
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    db_session.close()

if __name__ == "__main__":
    test_search()