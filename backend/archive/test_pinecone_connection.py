#!/usr/bin/env python3
"""
Test Pinecone connection and index information
"""

import os
from dotenv import load_dotenv
import pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

def test_pinecone_connection():
    """Test Pinecone connection and index listing"""
    
    print("🔍 TESTING PINECONE CONNECTION")
    print("=" * 50)
    
    if not PINECONE_API_KEY:
        print("❌ PINECONE_API_KEY not found")
        return
    
    try:
        # Initialize Pinecone
        print(f"🔗 Initializing Pinecone...")
        print(f"   API Key: {PINECONE_API_KEY[:8]}...")
        print(f"   Environment: {PINECONE_ENVIRONMENT}")
        
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        
        # List available indexes
        print(f"\n📋 Available indexes:")
        indexes = pinecone.list_indexes()
        for index_name in indexes:
            print(f"   • {index_name}")
        
        # Try to describe the dense-milo-people index
        if "dense-milo-people" in indexes:
            print(f"\n📊 Index details for 'dense-milo-people':")
            index_stats = pinecone.describe_index("dense-milo-people")
            print(f"   Status: {index_stats.status}")
            print(f"   Dimension: {index_stats.dimension}")
            print(f"   Metric: {index_stats.metric}")
            
            # Connect to index and get stats
            index = pinecone.Index("dense-milo-people")
            stats = index.describe_index_stats()
            print(f"   Total vectors: {stats.total_vector_count}")
            print(f"   Namespaces: {list(stats.namespaces.keys())}")
            
            # Check yale-people-2025-dense namespace specifically
            if "yale-people-2025-dense" in stats.namespaces:
                namespace_stats = stats.namespaces["yale-people-2025-dense"]
                print(f"\n🎓 Yale namespace 'yale-people-2025-dense':")
                print(f"   Vector count: {namespace_stats.vector_count}")
            else:
                print(f"\n❌ Namespace 'yale-people-2025-dense' not found")
                print(f"   Available namespaces: {list(stats.namespaces.keys())}")
        else:
            print(f"\n❌ Index 'dense-milo-people' not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pinecone_connection()