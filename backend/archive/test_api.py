#!/usr/bin/env python3
"""Test the API endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Test API endpoints"""
    
    # Test health endpoint
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API server not running. Please start with: python api_server.py")
        return
    
    # Test stats endpoint
    print("\nTesting /stats endpoint...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Stats: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Total Yale people: {stats.get('yale_people')}")
        print(f"Top locations: {list(stats.get('top_locations', {}).keys())[:5]}")
    
    # Test search endpoint
    print("\nTesting /search endpoint...")
    test_queries = [
        "Yale people in Connecticut",
        "Yale professors",
        "Yale founders"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = requests.get(f"{BASE_URL}/search", params={"q": query, "limit": 3})
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Results found: {data['total_results']}")
            
            for i, result in enumerate(data['results'][:2], 1):
                print(f"  {i}. {result['name']} - {result.get('location', 'No location')}")
                if result.get('match_reasons'):
                    print(f"     Match: {', '.join(result['match_reasons'][:2])}")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    test_api()