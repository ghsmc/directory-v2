#!/usr/bin/env python3
"""
Test precise search strategies that maintain specificity but get more results
Focus on getting exactly 10 high-quality matches
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

def test_precision_strategies():
    """Test different precision strategies to get exactly 10 good results"""
    
    db = SessionLocal()
    
    print("🎯 PRECISION SEARCH TESTING")
    print("Goal: Get exactly 10 high-quality matches, not random broad results")
    print("=" * 70)
    
    # Strategy 1: Too restrictive (current problem)
    print("\n1️⃣ TOO RESTRICTIVE: Exact 'robotics engineer'")
    restrictive_query = text("""
        SELECT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            LOWER(p.headline) LIKE '%robotics engineer%'
            OR LOWER(e.title) LIKE '%robotics engineer%'
        )
        LIMIT 10
    """)
    
    restrictive_results = db.execute(restrictive_query).fetchall()
    print(f"   Results: {len(restrictive_results)}")
    for r in restrictive_results:
        print(f"   • {r.full_name}: {r.headline}")
    
    # Strategy 2: Smart expansion within domain
    print("\n2️⃣ SMART EXPANSION: Robotics + related engineering")
    smart_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            -- Direct robotics matches
            LOWER(p.headline) LIKE '%robotics%'
            OR LOWER(e.title) LIKE '%robotics%'
            OR LOWER(ed.field_of_study) LIKE '%robotics%'
            
            -- Mechanical engineering (robotics adjacent)
            OR (
                (LOWER(p.headline) LIKE '%mechanical%' OR LOWER(e.title) LIKE '%mechanical%')
                AND (LOWER(p.headline) LIKE '%engineer%' OR LOWER(e.title) LIKE '%engineer%')
            )
            
            -- Automation/controls (robotics adjacent)
            OR LOWER(p.headline) LIKE '%automation%'
            OR LOWER(e.title) LIKE '%automation%'
            OR LOWER(p.headline) LIKE '%controls%'
            OR LOWER(e.title) LIKE '%controls%'
            
            -- Hardware engineering (could be robotics)
            OR (
                (LOWER(p.headline) LIKE '%hardware%' OR LOWER(e.title) LIKE '%hardware%')
                AND (LOWER(p.headline) LIKE '%engineer%' OR LOWER(e.title) LIKE '%engineer%')
            )
            
            -- Mechatronics (definitely robotics related)
            OR LOWER(p.headline) LIKE '%mechatronics%'
            OR LOWER(e.title) LIKE '%mechatronics%'
            OR LOWER(ed.field_of_study) LIKE '%mechatronics%'
        )
        ORDER BY 
            CASE 
                WHEN LOWER(p.headline) LIKE '%robotics%' OR LOWER(e.title) LIKE '%robotics%' THEN 1
                WHEN LOWER(p.headline) LIKE '%mechatronics%' OR LOWER(e.title) LIKE '%mechatronics%' THEN 2
                WHEN LOWER(p.headline) LIKE '%automation%' OR LOWER(e.title) LIKE '%automation%' THEN 3
                ELSE 4
            END,
            p.full_name
        LIMIT 10
    """)
    
    smart_results = db.execute(smart_query).fetchall()
    print(f"   Results: {len(smart_results)}")
    for r in smart_results:
        print(f"   • {r.full_name}: {r.headline}")
        if r.title and r.company:
            print(f"     → {r.title} at {r.company}")
    
    # Strategy 3: Include past experience (people who USED to do robotics)
    print("\n3️⃣ INCLUDE PAST EXPERIENCE: Former robotics people")
    past_exp_query = text("""
        SELECT DISTINCT p.full_name, p.headline, 
               e.title as current_title, e.company as current_company,
               e_past.title as past_title, e_past.company as past_company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id AND e.is_current = true
        LEFT JOIN experience e_past ON e_past.person_uuid = p.uuid_id
        WHERE (
            -- Past robotics experience
            LOWER(e_past.title) LIKE '%robotics%'
            OR LOWER(e_past.title) LIKE '%mechanical engineer%'
            OR LOWER(e_past.title) LIKE '%automation%'
            OR LOWER(e_past.title) LIKE '%mechatronics%'
            OR LOWER(e_past.company) LIKE '%robotics%'
            OR LOWER(e_past.company) LIKE '%automation%'
        )
        ORDER BY p.full_name
        LIMIT 10
    """)
    
    past_results = db.execute(past_exp_query).fetchall()
    print(f"   Results: {len(past_results)}")
    for r in past_results:
        print(f"   • {r.full_name}: {r.headline}")
        if r.past_title and r.past_company:
            print(f"     → Past: {r.past_title} at {r.past_company}")
    
    # Strategy 4: Company-based (people at robotics companies)
    print("\n4️⃣ COMPANY-BASED: Engineers at robotics companies")
    company_query = text("""
        SELECT DISTINCT p.full_name, p.headline, e.title, e.company
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN experience e ON e.person_uuid = p.uuid_id
        WHERE (
            -- Engineers at robotics/automation companies
            (
                (LOWER(p.headline) LIKE '%engineer%' OR LOWER(e.title) LIKE '%engineer%')
                AND (
                    LOWER(e.company) LIKE '%robotics%'
                    OR LOWER(e.company) LIKE '%automation%'
                    OR LOWER(e.company) LIKE '%mechanical%'
                    OR LOWER(e.company) LIKE '%systems%'
                    OR LOWER(e.company) LIKE '%controls%'
                    OR LOWER(e.company) LIKE '%tesla%'
                    OR LOWER(e.company) LIKE '%spacex%'
                    OR LOWER(e.company) LIKE '%boeing%'
                    OR LOWER(e.company) LIKE '%lockheed%'
                    OR LOWER(e.company) LIKE '%general electric%'
                    OR LOWER(e.company) LIKE '%ford%'
                    OR LOWER(e.company) LIKE '%toyota%'
                )
            )
        )
        ORDER BY 
            CASE 
                WHEN LOWER(e.company) LIKE '%robotics%' THEN 1
                WHEN LOWER(e.company) LIKE '%automation%' THEN 2
                WHEN LOWER(e.company) LIKE '%tesla%' OR LOWER(e.company) LIKE '%spacex%' THEN 3
                ELSE 4
            END,
            p.full_name
        LIMIT 10
    """)
    
    company_results = db.execute(company_query).fetchall()
    print(f"   Results: {len(company_results)}")
    for r in company_results:
        print(f"   • {r.full_name}: {r.headline}")
        if r.title and r.company:
            print(f"     → {r.title} at {r.company}")
    
    # Strategy 5: Education-based (studied robotics/mechanical)
    print("\n5️⃣ EDUCATION-BASED: Studied robotics/mechanical engineering")
    education_query = text("""
        SELECT DISTINCT p.full_name, p.headline, ed.degree, ed.field_of_study
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
        WHERE (
            LOWER(ed.field_of_study) LIKE '%robotics%'
            OR LOWER(ed.field_of_study) LIKE '%mechanical engineering%'
            OR LOWER(ed.field_of_study) LIKE '%mechanical%'
            OR LOWER(ed.field_of_study) LIKE '%mechatronics%'
            OR LOWER(ed.field_of_study) LIKE '%automation%'
            OR LOWER(ed.degree) LIKE '%mechanical%'
            OR LOWER(ed.degree) LIKE '%robotics%'
            OR (
                LOWER(ed.field_of_study) LIKE '%engineering%'
                AND (
                    LOWER(p.headline) LIKE '%robotics%'
                    OR LOWER(p.headline) LIKE '%mechanical%'
                )
            )
        )
        ORDER BY 
            CASE 
                WHEN LOWER(ed.field_of_study) LIKE '%robotics%' THEN 1
                WHEN LOWER(ed.field_of_study) LIKE '%mechatronics%' THEN 2
                WHEN LOWER(ed.field_of_study) LIKE '%mechanical%' THEN 3
                ELSE 4
            END,
            p.full_name
        LIMIT 10
    """)
    
    education_results = db.execute(education_query).fetchall()
    print(f"   Results: {len(education_results)}")
    for r in education_results:
        print(f"   • {r.full_name}: {r.headline}")
        if r.field_of_study:
            print(f"     → Studied: {r.field_of_study}")
    
    db.close()
    
    return {
        'restrictive': len(restrictive_results),
        'smart': len(smart_results),
        'past': len(past_results),
        'company': len(company_results),
        'education': len(education_results)
    }

def combined_precision_search():
    """Combine all strategies for optimal 10 results"""
    
    db = SessionLocal()
    
    print("\n\n🎯 COMBINED PRECISION SEARCH")
    print("Combining all strategies with ranking to get best 10 results")
    print("=" * 70)
    
    combined_query = text("""
        WITH ranked_candidates AS (
            SELECT DISTINCT 
                p.full_name,
                p.headline,
                e.title as current_title,
                e.company as current_company,
                ed.field_of_study,
                CASE 
                    -- Highest priority: Direct robotics mentions
                    WHEN LOWER(p.headline) LIKE '%robotics%' OR LOWER(e.title) LIKE '%robotics%' THEN 1
                    WHEN LOWER(ed.field_of_study) LIKE '%robotics%' THEN 2
                    
                    -- High priority: Mechatronics (definitely robotics related)
                    WHEN LOWER(p.headline) LIKE '%mechatronics%' OR LOWER(e.title) LIKE '%mechatronics%' THEN 3
                    WHEN LOWER(ed.field_of_study) LIKE '%mechatronics%' THEN 4
                    
                    -- Medium priority: Mechanical engineers (often do robotics)
                    WHEN (LOWER(p.headline) LIKE '%mechanical%' AND LOWER(p.headline) LIKE '%engineer%') THEN 5
                    WHEN (LOWER(e.title) LIKE '%mechanical%' AND LOWER(e.title) LIKE '%engineer%') THEN 6
                    WHEN LOWER(ed.field_of_study) LIKE '%mechanical engineering%' THEN 7
                    
                    -- Medium priority: Automation/controls (robotics adjacent)
                    WHEN LOWER(p.headline) LIKE '%automation%' OR LOWER(e.title) LIKE '%automation%' THEN 8
                    WHEN LOWER(p.headline) LIKE '%controls%' OR LOWER(e.title) LIKE '%controls%' THEN 9
                    
                    -- Lower priority: Hardware engineers at relevant companies
                    WHEN (
                        (LOWER(p.headline) LIKE '%hardware%' OR LOWER(e.title) LIKE '%hardware%')
                        AND (LOWER(e.company) LIKE '%robotics%' OR LOWER(e.company) LIKE '%automation%')
                    ) THEN 10
                    
                    ELSE 11
                END as priority_score
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id
            LEFT JOIN education ed ON ed.person_uuid = p.uuid_id
            WHERE (
                -- Direct robotics
                LOWER(p.headline) LIKE '%robotics%'
                OR LOWER(e.title) LIKE '%robotics%'
                OR LOWER(ed.field_of_study) LIKE '%robotics%'
                
                -- Mechatronics
                OR LOWER(p.headline) LIKE '%mechatronics%'
                OR LOWER(e.title) LIKE '%mechatronics%'
                OR LOWER(ed.field_of_study) LIKE '%mechatronics%'
                
                -- Mechanical engineering
                OR (
                    (LOWER(p.headline) LIKE '%mechanical%' OR LOWER(e.title) LIKE '%mechanical%')
                    AND (LOWER(p.headline) LIKE '%engineer%' OR LOWER(e.title) LIKE '%engineer%')
                )
                OR LOWER(ed.field_of_study) LIKE '%mechanical engineering%'
                OR LOWER(ed.field_of_study) LIKE '%mechanical%'
                
                -- Automation/controls
                OR LOWER(p.headline) LIKE '%automation%'
                OR LOWER(e.title) LIKE '%automation%'
                OR LOWER(p.headline) LIKE '%controls%'
                OR LOWER(e.title) LIKE '%controls%'
                
                -- Hardware at robotics companies
                OR (
                    (LOWER(p.headline) LIKE '%hardware%' OR LOWER(e.title) LIKE '%hardware%')
                    AND (
                        LOWER(e.company) LIKE '%robotics%'
                        OR LOWER(e.company) LIKE '%automation%'
                        OR LOWER(e.company) LIKE '%tesla%'
                        OR LOWER(e.company) LIKE '%spacex%'
                    )
                )
            )
        )
        SELECT full_name, headline, current_title, current_company, field_of_study, priority_score
        FROM ranked_candidates
        ORDER BY priority_score, full_name
        LIMIT 10
    """)
    
    results = db.execute(combined_query).fetchall()
    
    print(f"🎯 FINAL RESULTS: {len(results)} precision matches")
    print()
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.full_name} (Priority: {r.priority_score})")
        print(f"   💼 {r.headline}")
        if r.current_title and r.current_company:
            print(f"   🏢 {r.current_title} at {r.current_company}")
        if r.field_of_study:
            print(f"   🎓 Studied: {r.field_of_study}")
        print()
    
    db.close()
    
    return len(results)

if __name__ == "__main__":
    # Test individual strategies
    results = test_precision_strategies()
    
    # Test combined approach
    final_count = combined_precision_search()
    
    print("=" * 70)
    print("💡 PRECISION SEARCH STRATEGY SUMMARY")
    print("=" * 70)
    
    print(f"Individual strategy results:")
    for strategy, count in results.items():
        print(f"   {strategy}: {count} results")
    
    print(f"\nCombined precision search: {final_count} results")
    
    print(f"\n🎯 KEY INSIGHT:")
    print(f"   Instead of broadening to random 'analysts' and 'researchers',")
    print(f"   we stay SPECIFIC to robotics/mechanical/mechatronics/automation")
    print(f"   but search across headlines, job titles, past experience, education, and companies")
    print(f"   This gives us {final_count} relevant results without diluting quality!")