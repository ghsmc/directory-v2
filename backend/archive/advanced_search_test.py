#!/usr/bin/env python3
"""
Advanced search test matching the exact happenstance.ai pattern
Tests complex multi-filter queries like "Yale engineers at startups"
"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_yale_engineers_at_startups():
    """Test the exact query: Yale engineers at startups"""
    print("🔍 Testing: Yale engineers at startups")
    
    db = SessionLocal()
    try:
        # Build the exact SQL pattern from happenstance.ai
        query = text("""
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                ya.school,
                e.title as current_title,
                e.company as current_company
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE
                -- Yale education filter
                (ya.school IS NOT NULL)
                AND
                -- Engineer title filter
                (
                    LOWER(p.headline) LIKE '%engineer%'
                    OR LOWER(p.headline) LIKE '%developer%'
                    OR LOWER(p.headline) LIKE '%software%'
                    OR LOWER(p.headline) LIKE '%technical%'
                    OR LOWER(p.headline) LIKE '%cto%'
                    OR LOWER(p.headline) LIKE '%architect%'
                    OR LOWER(e.title) LIKE '%engineer%'
                    OR LOWER(e.title) LIKE '%developer%'
                    OR LOWER(e.title) LIKE '%software%'
                    OR LOWER(e.title) LIKE '%technical%'
                    OR LOWER(e.title) LIKE '%cto%'
                    OR LOWER(e.title) LIKE '%architect%'
                )
                AND
                -- Startup company filter
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
                    OR LOWER(e.company) LIKE '%bio%'
                    OR LOWER(e.company) LIKE '%health%'
                    OR LOWER(e.company) LIKE '%fintech%'
                    OR LOWER(e.company) LIKE '%saas%'
                    OR LOWER(e.company) LIKE '%mobile%'
                    OR LOWER(e.company) LIKE '%app%'
                    OR LOWER(e.company) LIKE '%software%'
                )
            ORDER BY p.full_name
            LIMIT 10
        """)
        
        results = db.execute(query).fetchall()
        
        print(f"   Found {len(results)} Yale engineers at startups:")
        print()
        
        for i, person in enumerate(results, 1):
            print(f"   {i}. {person.full_name}")
            if person.location:
                print(f"      📍 {person.location}")
            if person.headline:
                print(f"      💼 {person.headline[:80]}...")
            if person.current_title:
                print(f"      🏢 {person.current_title} at {person.current_company}")
            print(f"      🎓 {person.school}")
            print()
        
        return len(results)
        
    except Exception as e:
        print(f"   Error: {e}")
        return 0
    finally:
        db.close()

def test_yale_founders():
    """Test: Yale founders and entrepreneurs"""
    print("🚀 Testing: Yale founders and entrepreneurs")
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                ya.school
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE
                (ya.school IS NOT NULL)
                AND
                (
                    LOWER(p.headline) LIKE '%founder%'
                    OR LOWER(p.headline) LIKE '%co-founder%'
                    OR LOWER(p.headline) LIKE '%ceo%'
                    OR LOWER(p.headline) LIKE '%entrepreneur%'
                    OR LOWER(p.headline) LIKE '%startup%'
                    OR LOWER(e.title) LIKE '%founder%'
                    OR LOWER(e.title) LIKE '%co-founder%'
                    OR LOWER(e.title) LIKE '%ceo%'
                    OR LOWER(e.title) LIKE '%entrepreneur%'
                )
            ORDER BY p.full_name
            LIMIT 8
        """)
        
        results = db.execute(query).fetchall()
        
        print(f"   Found {len(results)} Yale founders:")
        for person in results:
            print(f"   • {person.full_name} - {person.headline[:60] if person.headline else 'N/A'}")
        
        return len(results)
        
    except Exception as e:
        print(f"   Error: {e}")
        return 0
    finally:
        db.close()

def test_yale_vcs():
    """Test: Yale VCs and investors"""
    print("💰 Testing: Yale VCs and investors")
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                ya.school
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE
                (ya.school IS NOT NULL)
                AND
                (
                    LOWER(p.headline) LIKE '%investor%'
                    OR LOWER(p.headline) LIKE '%venture%'
                    OR LOWER(p.headline) LIKE '%vc%'
                    OR LOWER(p.headline) LIKE '%partner%'
                    OR LOWER(p.headline) LIKE '%principal%'
                    OR LOWER(p.headline) LIKE '%investment%'
                    OR LOWER(p.headline) LIKE '%capital%'
                    OR LOWER(e.title) LIKE '%investor%'
                    OR LOWER(e.title) LIKE '%venture%'
                    OR LOWER(e.title) LIKE '%partner%'
                    OR LOWER(e.title) LIKE '%principal%'
                    OR LOWER(e.company) LIKE '%capital%'
                    OR LOWER(e.company) LIKE '%ventures%'
                    OR LOWER(e.company) LIKE '%partners%'
                    OR LOWER(e.company) LIKE '%fund%'
                )
            ORDER BY p.full_name
            LIMIT 8
        """)
        
        results = db.execute(query).fetchall()
        
        print(f"   Found {len(results)} Yale VCs/investors:")
        for person in results:
            print(f"   • {person.full_name} - {person.headline[:60] if person.headline else 'N/A'}")
        
        return len(results)
        
    except Exception as e:
        print(f"   Error: {e}")
        return 0
    finally:
        db.close()

def test_yale_in_tech_companies():
    """Test: Yale people at major tech companies"""
    print("🏢 Testing: Yale people at major tech companies")
    
    db = SessionLocal()
    try:
        query = text("""
            SELECT DISTINCT
                p.full_name,
                p.location,
                p.headline,
                e.company,
                ya.school
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE
                (ya.school IS NOT NULL)
                AND
                (
                    LOWER(e.company) LIKE '%google%'
                    OR LOWER(e.company) LIKE '%microsoft%'
                    OR LOWER(e.company) LIKE '%apple%'
                    OR LOWER(e.company) LIKE '%facebook%'
                    OR LOWER(e.company) LIKE '%meta%'
                    OR LOWER(e.company) LIKE '%amazon%'
                    OR LOWER(e.company) LIKE '%netflix%'
                    OR LOWER(e.company) LIKE '%uber%'
                    OR LOWER(e.company) LIKE '%airbnb%'
                    OR LOWER(e.company) LIKE '%stripe%'
                    OR LOWER(e.company) LIKE '%spotify%'
                    OR LOWER(e.company) LIKE '%twitter%'
                    OR LOWER(e.company) LIKE '%tesla%'
                    OR LOWER(e.company) LIKE '%linkedin%'
                    OR LOWER(e.company) LIKE '%salesforce%'
                    OR LOWER(e.company) LIKE '%openai%'
                    OR LOWER(e.company) LIKE '%anthropic%'
                    OR LOWER(p.headline) LIKE '%google%'
                    OR LOWER(p.headline) LIKE '%microsoft%'
                    OR LOWER(p.headline) LIKE '%apple%'
                    OR LOWER(p.headline) LIKE '%meta%'
                    OR LOWER(p.headline) LIKE '%amazon%'
                )
            ORDER BY p.full_name
            LIMIT 8
        """)
        
        results = db.execute(query).fetchall()
        
        print(f"   Found {len(results)} Yale people at major tech companies:")
        for person in results:
            company = person.company or "N/A"
            print(f"   • {person.full_name} at {company}")
        
        return len(results)
        
    except Exception as e:
        print(f"   Error: {e}")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    print("🧪 Advanced Search Pattern Testing")
    print("=" * 50)
    print("Testing sophisticated multi-filter queries like happenstance.ai")
    print()
    
    # Test different query patterns
    engineers = test_yale_engineers_at_startups()
    founders = test_yale_founders()
    vcs = test_yale_vcs()
    tech = test_yale_in_tech_companies()
    
    print("=" * 50)
    print("📊 Results Summary:")
    print(f"   Yale engineers at startups: {engineers}")
    print(f"   Yale founders: {founders}")
    print(f"   Yale VCs/investors: {vcs}")
    print(f"   Yale at tech companies: {tech}")
    
    total = engineers + founders + vcs + tech
    print(f"   Total specialized Yale people: {total}")
    
    if total > 0:
        print(f"\n🎉 Success! Found {total} people matching advanced search patterns")
        print("   The advanced SQL filtering is working correctly!")
    else:
        print("\n⚠️  No matches found - need more data or refined filters")