#!/usr/bin/env python3
"""
Debug Pinecone connection issues
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def debug_pinecone():
    """Debug Pinecone connection"""
    
    print("🔍 DEBUGGING PINECONE CONNECTION")
    print("=" * 50)
    
    if not PINECONE_API_KEY:
        print("❌ PINECONE_API_KEY not found")
        return
    
    # Test API connectivity with direct REST call
    headers = {
        'Api-Key': PINECONE_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        print("🌐 Testing Pinecone REST API...")
        
        # Try to list indexes via REST API
        response = requests.get(
            'https://api.pinecone.io/indexes',
            headers=headers,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            indexes = response.json()
            print(f"   ✅ Success! Found {len(indexes)} indexes:")
            
            for index in indexes:
                index_name = index.get('name', 'unknown')
                status = index.get('status', {}).get('ready', False)
                host = index.get('host', 'unknown')
                
                print(f"      • {index_name}")
                print(f"        Status: {'Ready' if status else 'Not Ready'}")
                print(f"        Host: {host}")
                
                if index_name == "dense-milo-people":
                    print(f"        🎯 Found target index!")
                    
                    # Test a simple query to this index
                    print(f"        🔍 Testing index connection...")
                    try:
                        query_url = f"https://{host}/query"
                        query_data = {
                            "namespace": "yale-people-2025-dense",
                            "topK": 1,
                            "vector": [0.0] * 1536,  # Dummy vector
                            "includeMetadata": True
                        }
                        
                        query_response = requests.post(
                            query_url,
                            headers=headers,
                            json=query_data,
                            timeout=10
                        )
                        
                        print(f"        Query Status: {query_response.status_code}")
                        if query_response.status_code == 200:
                            result = query_response.json()
                            print(f"        ✅ Index query successful!")
                            print(f"        Namespace exists: {'yale-people-2025-dense' in str(result)}")
                        else:
                            print(f"        ❌ Query failed: {query_response.text}")
                            
                    except Exception as e:
                        print(f"        ❌ Query error: {e}")
                        
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    debug_pinecone()