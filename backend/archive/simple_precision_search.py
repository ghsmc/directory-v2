#!/usr/bin/env python3
"""
Simple precision search to get 10 high-quality robotics engineer results
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

def test_precision_robotics_search():
    """Test precise ways to find robotics engineers"""
    
    db = SessionLocal()
    
    print("🎯 PRECISION ROBOTICS SEARCH")
    print("Finding exactly 10 high-quality robotics-related Yale engineers")
    print("=" * 70)
    
    # Strategy 1: Direct robotics search
    print("\n1️⃣ DIRECT ROBOTICS:")
    direct_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.headline) LIKE '%robotics%'
            OR LOWER(e.title) LIKE '%robotics%'
            OR LOWER(ed.field_of_study) LIKE '%robotics%'
        )
        LIMIT 5
    """)
    
    direct_results = db.execute(direct_query).fetchall()
    print(f"   Found: {len(direct_results)}")
    for r in direct_results:
        print(f"   • {r.full_name}: {r.headline}")
    
    # Strategy 2: Mechanical engineers
    print("\n2️⃣ MECHANICAL ENGINEERS:")
    mech_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            (LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%')
            OR (LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%')
            OR LOWER(ed.field_of_study) LIKE '%mechanical engineering%'
            OR LOWER(ed.field_of_study) LIKE '%mechanical%'
        )
        LIMIT 5
    """)
    
    mech_results = db.execute(mech_query).fetchall()
    print(f"   Found: {len(mech_results)}")
    for r in mech_results:
        print(f"   • {r.full_name}: {r.headline}")
    
    # Strategy 3: Automation/Controls engineers
    print("\n3️⃣ AUTOMATION/CONTROLS:")
    auto_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.headline) LIKE '%automation%'
            OR LOWER(e.title) LIKE '%automation%'
            OR LOWER(p.headline) LIKE '%controls%'
            OR LOWER(e.title) LIKE '%controls%'
            OR LOWER(p.headline) LIKE '%mechatronics%'
            OR LOWER(e.title) LIKE '%mechatronics%'
        )
        LIMIT 5
    """)
    
    auto_results = db.execute(auto_query).fetchall()
    print(f"   Found: {len(auto_results)}")
    for r in auto_results:
        print(f"   • {r.full_name}: {r.headline}")
    
    # Strategy 4: Hardware engineers
    print("\n4️⃣ HARDWARE ENGINEERS:")
    hardware_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            (LOWER(p.headline) LIKE '%hardware%' AND LOWER(p.headline) LIKE '%engineer%')
            OR (LOWER(e.title) LIKE '%hardware%' AND LOWER(e.title) LIKE '%engineer%')
        )
        LIMIT 5
    """)
    
    hardware_results = db.execute(hardware_query).fetchall()
    print(f"   Found: {len(hardware_results)}")
    for r in hardware_results:
        print(f"   • {r.full_name}: {r.headline}")
    
    # Strategy 5: Combined best results
    print("\n5️⃣ COMBINED BEST 10:")
    combined_query = text("""
        SELECT DISTINCT 
            p.full_name, 
            p.headline, 
            e.title, 
            e.company,
            CASE 
                WHEN LOWER(p.headline) LIKE '%robotics%' OR LOWER(e.title) LIKE '%robotics%' THEN 1
                WHEN LOWER(p.headline) LIKE '%mechatronics%' OR LOWER(e.title) LIKE '%mechatronics%' THEN 2
                WHEN LOWER(p.headline) LIKE '%automation%' OR LOWER(e.title) LIKE '%automation%' THEN 3
                WHEN (LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%') THEN 4
                WHEN (LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%') THEN 5
                WHEN (LOWER(p.headline) LIKE '%hardware%' AND LOWER(p.headline) LIKE '%engineer%') THEN 6
                ELSE 7
            END as priority
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            -- Robotics (highest priority)
            LOWER(p.headline) LIKE '%robotics%'
            OR LOWER(e.title) LIKE '%robotics%'
            OR LOWER(ed.field_of_study) LIKE '%robotics%'
            
            -- Mechatronics (very robotics related)
            OR LOWER(p.headline) LIKE '%mechatronics%'
            OR LOWER(e.title) LIKE '%mechatronics%'
            OR LOWER(ed.field_of_study) LIKE '%mechatronics%'
            
            -- Automation/Controls (robotics adjacent)
            OR LOWER(p.headline) LIKE '%automation%'
            OR LOWER(e.title) LIKE '%automation%'
            OR LOWER(p.headline) LIKE '%controls%'
            OR LOWER(e.title) LIKE '%controls%'
            
            -- Mechanical Engineering (often does robotics)
            OR (LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%')
            OR (LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%')
            OR LOWER(ed.field_of_study) LIKE '%mechanical engineering%'
            OR LOWER(ed.field_of_study) LIKE '%mechanical%'
            
            -- Hardware Engineering (could be robotics)
            OR (LOWER(p.headline) LIKE '%hardware%' AND LOWER(p.headline) LIKE '%engineer%')
            OR (LOWER(e.title) LIKE '%hardware%' AND LOWER(e.title) LIKE '%engineer%')
        )
        ORDER BY priority, p.full_name
        LIMIT 10
    """)
    
    combined_results = db.execute(combined_query).fetchall()
    print(f"   Found: {len(combined_results)} (FINAL RESULTS)")
    print()
    
    for i, r in enumerate(combined_results, 1):
        print(f"   {i}. {r.full_name} (Priority: {r.priority})")
        print(f"      💼 {r.headline}")
        if r.title and r.company:
            print(f"      🏢 {r.title} at {r.company}")
        print()
    
    db.close()
    
    return len(combined_results)

def show_keyword_expansion_strategy():
    """Show how to expand keywords while staying specific"""
    
    print("\n" + "=" * 70)
    print("💡 KEYWORD EXPANSION STRATEGY")
    print("=" * 70)
    
    print("""
🎯 FOR 'ROBOTICS ENGINEERS' - Stay Specific:

✅ GOOD EXPANSIONS (robotics-related):
   • robotics → mechatronics, automation, controls
   • engineer → mechanical engineer, hardware engineer
   • Include: systems engineer, design engineer (at robotics companies)

❌ BAD EXPANSIONS (too broad):
   • DON'T add: analyst, researcher, consultant
   • DON'T add: software engineer (unless at robotics company)
   • DON'T add: data scientist, product manager

🔍 SEARCH STRATEGY:
   1. Direct matches: 'robotics engineer'
   2. Domain-specific: 'mechatronics', 'automation', 'controls'  
   3. Adjacent roles: 'mechanical engineer', 'hardware engineer'
   4. Past experience: previous robotics jobs
   5. Education: studied robotics/mechanical engineering
   6. Company context: engineers at robotics companies

📊 PRIORITY RANKING:
   1. Robotics (highest priority)
   2. Mechatronics  
   3. Automation/Controls
   4. Mechanical Engineering
   5. Hardware Engineering (at relevant companies)
   
This keeps results HIGHLY RELEVANT while expanding the pool!
""")

if __name__ == "__main__":
    final_count = test_precision_robotics_search()
    show_keyword_expansion_strategy()
    
    print(f"\n🎯 RESULT: Found {final_count}/10 high-quality robotics-related Yale engineers")
    print("   Strategy: Expand within domain, maintain specificity, prioritize by relevance")