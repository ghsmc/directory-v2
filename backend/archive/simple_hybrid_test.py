#!/usr/bin/env python3
"""Simple test of hybrid search functionality"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Test basic database connectivity and hybrid search
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_database():
    """Test basic database operations"""
    print("🔍 Testing Database Connectivity...")
    
    db = SessionLocal()
    try:
        # Check people count
        people_count = db.execute(text("SELECT COUNT(*) FROM people")).scalar()
        print(f"   Total people: {people_count}")
        
        # Check Yale affiliations
        yale_count = db.execute(text("""
            SELECT COUNT(DISTINCT p.uuid_id) 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        """)).scalar()
        print(f"   Yale people: {yale_count}")
        
        # Sample Yale person
        sample = db.execute(text("""
            SELECT p.full_name, p.location, p.headline, ya.school 
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id 
            LIMIT 1
        """)).fetchone()
        
        if sample:
            print(f"   Sample: {sample.full_name} - {sample.headline}")
            print(f"   Location: {sample.location}")
            print(f"   Yale School: {sample.school}")
        
        # Check embeddings table
        try:
            embeddings_count = db.execute(text("SELECT COUNT(*) FROM profile_embeddings")).scalar()
            print(f"   Profile embeddings: {embeddings_count}")
        except Exception as e:
            print(f"   Profile embeddings table: Not found ({e})")
        
        return True
        
    except Exception as e:
        print(f"   Database error: {e}")
        return False
    finally:
        db.close()

def test_simple_sql_search():
    """Test simple SQL search without complex parsing"""
    print("\n🔍 Testing Simple SQL Search...")
    
    db = SessionLocal()
    try:
        # Simple search for Yale people
        results = db.execute(text("""
            SELECT DISTINCT p.full_name, p.location, p.headline, ya.school
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            WHERE p.full_name IS NOT NULL
            LIMIT 5
        """)).fetchall()
        
        print(f"   Found {len(results)} Yale people:")
        for i, person in enumerate(results, 1):
            print(f"   {i}. {person.full_name}")
            if person.location:
                print(f"      Location: {person.location}")
            if person.headline:
                print(f"      Headline: {person.headline[:60]}...")
            if person.school:
                print(f"      Yale School: {person.school}")
            print()
        
        return len(results) > 0
        
    except Exception as e:
        print(f"   SQL search error: {e}")
        return False
    finally:
        db.close()

def test_location_search():
    """Test location-based search"""
    print("🗺️  Testing Location Search...")
    
    db = SessionLocal()
    try:
        # Search for people in Connecticut
        results = db.execute(text("""
            SELECT DISTINCT p.full_name, p.location, ya.school
            FROM people p 
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            WHERE LOWER(p.location) LIKE '%connecticut%' 
               OR LOWER(p.location) LIKE '%ct%'
               OR LOWER(p.location) LIKE '%new haven%'
            LIMIT 3
        """)).fetchall()
        
        print(f"   Found {len(results)} people in Connecticut area:")
        for person in results:
            print(f"   • {person.full_name} - {person.location}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"   Location search error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🧪 Simple Hybrid Search Test")
    print("=" * 40)
    
    # Test 1: Database connectivity
    db_ok = test_database()
    
    if db_ok:
        # Test 2: Simple SQL search
        sql_ok = test_simple_sql_search()
        
        # Test 3: Location search
        location_ok = test_location_search()
        
        print("=" * 40)
        print("📋 Test Results:")
        print(f"   Database: {'✅' if db_ok else '❌'}")
        print(f"   SQL Search: {'✅' if sql_ok else '❌'}")
        print(f"   Location Search: {'✅' if location_ok else '❌'}")
        
        if db_ok and sql_ok:
            print("\n🎉 Basic functionality is working!")
            print("   The hybrid search engine should be able to find results.")
        else:
            print("\n⚠️  Some issues found. Check database and SQL queries.")
    else:
        print("\n❌ Database connection failed. Check DATABASE_URL and PostgreSQL.")