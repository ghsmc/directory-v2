#!/usr/bin/env python3
"""
Test broader search strategies to get more Yale results
"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_current_vs_broader_search():
    """Compare current restrictive search vs broader search"""
    
    db = SessionLocal()
    
    print("🔍 Testing: Current vs Broader Search Strategies")
    print("=" * 60)
    
    # Current restrictive search: "Yale engineers"
    print("\n1️⃣ CURRENT RESTRICTIVE: 'Yale engineers'")
    restrictive_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.headline) LIKE '%engineer%'
            OR LOWER(e.title) LIKE '%engineer%'
        )
    """)
    
    restrictive_count = db.execute(restrictive_query).scalar()
    print(f"   Results: {restrictive_count}")
    
    # Broader search: Include related terms
    print("\n2️⃣ BROADER: 'Yale technical people'")
    broader_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.headline) LIKE '%engineer%'
            OR LOWER(p.headline) LIKE '%developer%'
            OR LOWER(p.headline) LIKE '%software%'
            OR LOWER(p.headline) LIKE '%technical%'
            OR LOWER(p.headline) LIKE '%technology%'
            OR LOWER(p.headline) LIKE '%product%'
            OR LOWER(p.headline) LIKE '%data%'
            OR LOWER(p.headline) LIKE '%research%'
            OR LOWER(p.headline) LIKE '%scientist%'
            OR LOWER(p.headline) LIKE '%analyst%'
            OR LOWER(p.headline) LIKE '%consultant%'
            OR LOWER(e.title) LIKE '%engineer%'
            OR LOWER(e.title) LIKE '%developer%'
            OR LOWER(e.title) LIKE '%software%'
            OR LOWER(e.title) LIKE '%technical%'
            OR LOWER(e.title) LIKE '%technology%'
            OR LOWER(e.title) LIKE '%product%'
            OR LOWER(e.title) LIKE '%data%'
            OR LOWER(e.title) LIKE '%research%'
            OR LOWER(e.title) LIKE '%scientist%'
            OR LOWER(e.title) LIKE '%analyst%'
            OR LOWER(e.title) LIKE '%consultant%'
        )
    """)
    
    broader_count = db.execute(broader_query).scalar()
    print(f"   Results: {broader_count}")
    print(f"   📈 Improvement: {broader_count - restrictive_count} more people ({(broader_count/restrictive_count - 1)*100:.0f}% increase)")
    
    # Even broader: Include past experiences
    print("\n3️⃣ BROADEST: 'Yale people with ANY technical background'")
    broadest_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            -- Current or past titles
            LOWER(p.headline) LIKE '%engineer%'
            OR LOWER(p.headline) LIKE '%developer%'
            OR LOWER(p.headline) LIKE '%software%'
            OR LOWER(p.headline) LIKE '%technical%'
            OR LOWER(p.headline) LIKE '%technology%'
            OR LOWER(p.headline) LIKE '%product%'
            OR LOWER(p.headline) LIKE '%data%'
            OR LOWER(p.headline) LIKE '%research%'
            OR LOWER(p.headline) LIKE '%scientist%'
            OR LOWER(p.headline) LIKE '%analyst%'
            OR LOWER(p.headline) LIKE '%consultant%'
            OR LOWER(p.headline) LIKE '%manager%'
            OR LOWER(p.headline) LIKE '%director%'
            OR LOWER(e.title) LIKE '%engineer%'
            OR LOWER(e.title) LIKE '%developer%'
            OR LOWER(e.title) LIKE '%software%'
            OR LOWER(e.title) LIKE '%technical%'
            OR LOWER(e.title) LIKE '%technology%'
            OR LOWER(e.title) LIKE '%product%'
            OR LOWER(e.title) LIKE '%data%'
            OR LOWER(e.title) LIKE '%research%'
            OR LOWER(e.title) LIKE '%scientist%'
            OR LOWER(e.title) LIKE '%analyst%'
            OR LOWER(e.title) LIKE '%consultant%'
            OR LOWER(e.title) LIKE '%manager%'
            OR LOWER(e.title) LIKE '%director%'
            -- Education background
            OR LOWER(ed.field_of_study) LIKE '%engineer%'
            OR LOWER(ed.field_of_study) LIKE '%computer%'
            OR LOWER(ed.field_of_study) LIKE '%science%'
            OR LOWER(ed.field_of_study) LIKE '%technology%'
            OR LOWER(ed.degree) LIKE '%engineering%'
            OR LOWER(ed.degree) LIKE '%science%'
            -- Company indicators
            OR LOWER(e.company) LIKE '%tech%'
            OR LOWER(e.company) LIKE '%software%'
            OR LOWER(e.company) LIKE '%data%'
            OR LOWER(e.company) LIKE '%systems%'
            OR LOWER(e.company) LIKE '%solutions%'
        )
    """)
    
    broadest_count = db.execute(broadest_query).scalar()
    print(f"   Results: {broadest_count}")
    print(f"   📈 Improvement: {broadest_count - restrictive_count} more people ({(broadest_count/restrictive_count - 1)*100:.0f}% increase)")
    
    # All Yale people for context
    print("\n4️⃣ BASELINE: All Yale people in database")
    total_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
    """)
    
    total_count = db.execute(total_query).scalar()
    print(f"   Total Yale people: {total_count}")
    print(f"   📊 Technical coverage: {broadest_count}/{total_count} = {(broadest_count/total_count)*100:.1f}%")
    
    db.close()
    
    return {
        'restrictive': restrictive_count,
        'broader': broader_count, 
        'broadest': broadest_count,
        'total': total_count
    }

def test_search_by_yale_school():
    """Test search results by different Yale schools"""
    
    db = SessionLocal()
    
    print("\n\n🏫 Testing: Search by Yale School")
    print("=" * 60)
    
    # Get school breakdown
    school_query = text("""
        SELECT ya.school, COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        GROUP BY ya.school
        ORDER BY COUNT(DISTINCT p.uuid_id) DESC
    """)
    
    schools = db.execute(school_query).fetchall()
    
    for school in schools:
        print(f"   {school.school}: {school.count} people")
        
        # Test technical people in each school
        tech_in_school_query = text("""
            SELECT COUNT(DISTINCT p.uuid_id) as count
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            WHERE ya.school = :school
            AND (
                LOWER(p.headline) LIKE '%engineer%'
                OR LOWER(p.headline) LIKE '%technical%'
                OR LOWER(p.headline) LIKE '%technology%'
                OR LOWER(p.headline) LIKE '%product%'
                OR LOWER(p.headline) LIKE '%data%'
                OR LOWER(e.title) LIKE '%engineer%'
                OR LOWER(e.title) LIKE '%technical%'
                OR LOWER(e.title) LIKE '%technology%'
                OR LOWER(e.title) LIKE '%product%'
                OR LOWER(e.title) LIKE '%data%'
            )
        """)
        
        tech_count = db.execute(tech_in_school_query, {'school': school.school}).scalar()
        tech_percent = (tech_count / school.count * 100) if school.count > 0 else 0
        
        print(f"      → Technical: {tech_count} ({tech_percent:.1f}%)")
    
    db.close()

def test_search_by_location():
    """Test search results by location"""
    
    db = SessionLocal()
    
    print("\n\n🌍 Testing: Search by Location")
    print("=" * 60)
    
    # Get location breakdown
    location_query = text("""
        SELECT p.location, COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        WHERE p.location IS NOT NULL AND p.location != ''
        GROUP BY p.location
        ORDER BY COUNT(DISTINCT p.uuid_id) DESC
        LIMIT 10
    """)
    
    locations = db.execute(location_query).fetchall()
    
    print("   Top 10 locations:")
    for location in locations:
        print(f"   {location.location}: {location.count} people")
    
    # Test NYC specifically
    print(f"\n   🗽 NEW YORK AREA BREAKDOWN:")
    
    ny_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.location) LIKE '%new york%'
            OR LOWER(p.location) LIKE '%nyc%'
            OR LOWER(p.location) LIKE '%manhattan%'
            OR LOWER(p.location) LIKE '%brooklyn%'
            OR LOWER(p.location) LIKE '%queens%'
        )
    """)
    
    ny_count = db.execute(ny_query).scalar()
    print(f"      Total NY area Yale people: {ny_count}")
    
    # Technical people in NY
    ny_tech_query = text("""
        SELECT COUNT(DISTINCT p.uuid_id) as count
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.location) LIKE '%new york%'
            OR LOWER(p.location) LIKE '%nyc%'
            OR LOWER(p.location) LIKE '%manhattan%'
            OR LOWER(p.location) LIKE '%brooklyn%'
        )
        AND (
            LOWER(p.headline) LIKE '%engineer%'
            OR LOWER(p.headline) LIKE '%technical%'
            OR LOWER(p.headline) LIKE '%technology%'
            OR LOWER(p.headline) LIKE '%product%'
            OR LOWER(p.headline) LIKE '%startup%'
            OR LOWER(p.headline) LIKE '%founder%'
            OR LOWER(e.title) LIKE '%engineer%'
            OR LOWER(e.title) LIKE '%technical%'
            OR LOWER(e.title) LIKE '%technology%'
            OR LOWER(e.title) LIKE '%product%'
            OR LOWER(e.title) LIKE '%startup%'
            OR LOWER(e.title) LIKE '%founder%'
        )
    """)
    
    ny_tech_count = db.execute(ny_tech_query).scalar()
    print(f"      Technical/startup people in NY: {ny_tech_count}")
    
    db.close()

if __name__ == "__main__":
    print("📊 YALE DATABASE OPTIMIZATION ANALYSIS")
    print("How to get WAY more results from Yale alumni")
    print("=" * 80)
    
    # Test 1: Compare search strategies
    results = test_current_vs_broader_search()
    
    # Test 2: Search by school
    test_search_by_yale_school()
    
    # Test 3: Search by location
    test_search_by_location()
    
    print("\n" + "=" * 80)
    print("💡 RECOMMENDATIONS TO GET MORE RESULTS:")
    print("=" * 80)
    
    print(f"1️⃣ BROADEN KEYWORDS: {results['restrictive']} → {results['broader']} results")
    print("   • Include: developer, technical, product, data, research, analyst")
    print("   • Include: consultant, manager, director (technical context)")
    
    print(f"\n2️⃣ INCLUDE PAST EXPERIENCE: {results['broader']} → {results['broadest']} results") 
    print("   • Search experience table for ALL past jobs")
    print("   • Include education field of study")
    print("   • Include company patterns (tech, software, data, systems)")
    
    print(f"\n3️⃣ SEMANTIC SEARCH: Could find {results['total'] - results['broadest']} more")
    print("   • Use embeddings to find semantically similar profiles")
    print("   • Match on skills, interests, and context")
    print("   • Find people who don't use obvious keywords")
    
    print(f"\n4️⃣ RELAXED MATCHING:")
    print("   • Partial word matching (e.g., 'tech' matches 'technology')")
    print("   • Fuzzy matching for typos and variations")
    print("   • Company name variations and synonyms")
    
    total_improvement = results['broadest'] - results['restrictive']
    print(f"\n🎯 TOTAL POTENTIAL: +{total_improvement} more results ({(results['broadest']/results['restrictive']-1)*100:.0f}% increase)")
    print("   This would give you much more comprehensive Yale network coverage!")