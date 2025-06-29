#!/usr/bin/env python3
"""
Test what methods are available on Pinecone Index
"""

import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("TRI_HYBRID_PINECONE") or os.getenv("PINECONE_API_KEY")

def test_pinecone_methods():
    """Test Pinecone Index methods"""
    
    if not PINECONE_API_KEY:
        print("❌ No Pinecone API key found")
        return
    
    try:
        print("🔍 Testing Pinecone Index methods")
        print(f"API Key: {PINECONE_API_KEY[:8]}...")
        
        pc = Pinecone(api_key=PINECONE_API_KEY)
        print("✅ Pinecone client initialized")
        
        # Try to get the index
        index = pc.Index("dense-milo-people")
        print("✅ Index object created")
        
        # List all methods
        methods = [m for m in dir(index) if not m.startswith('_')]
        print(f"📋 Available methods: {methods}")
        
        # Try a simple query with vector
        print("🔍 Testing vector query...")
        dummy_vector = [0.1] * 1536  # OpenAI embedding size
        
        vector_result = index.query(
            namespace="yale-people-2025-dense",
            vector=dummy_vector,
            top_k=1,
            include_metadata=True
        )
        
        print(f"✅ Vector query successful! Found {len(vector_result.matches)} matches")
        if vector_result.matches:
            print(f"   Sample match ID: {vector_result.matches[0].id}")
            print(f"   Sample score: {vector_result.matches[0].score}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pinecone_methods()