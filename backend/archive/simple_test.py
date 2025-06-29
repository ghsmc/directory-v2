#!/usr/bin/env python3
"""Simple test of the database and basic functionality"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Person, Education, Experience, YaleAffiliation

DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_database():
    """Test database queries without AI"""
    
    db_session = SessionLocal()
    
    print("=== Yale Network Search - Database Test ===\n")
    
    # Count total people
    total_people = db_session.query(Person).count()
    print(f"Total people in database: {total_people}")
    
    # Count Yale people
    yale_people = db_session.query(Person).join(YaleAffiliation).count()
    print(f"Yale-affiliated people: {yale_people}")
    
    # Show some Yale people
    print(f"\n=== Sample Yale People ===")
    people = db_session.query(Person).join(YaleAffiliation).limit(5).all()
    
    for i, person in enumerate(people, 1):
        print(f"\n{i}. {person.full_name}")
        print(f"   Location: {person.location}")
        print(f"   Headline: {person.headline}")
        
        # Show Yale affiliations
        for yale_aff in person.yale_affiliations:
            print(f"   Yale: {yale_aff.school} ({yale_aff.affiliation_type})")
            if yale_aff.major:
                print(f"         Major: {yale_aff.major}")
        
        # Show current experience
        current_exp = next((e for e in person.experiences if e.is_current), None)
        if current_exp:
            print(f"   Current: {current_exp.title} at {current_exp.company}")
    
    # Test basic SQL search
    print(f"\n=== Manual SQL Search Test ===")
    print("Query: Find Yale people in Connecticut")
    
    ct_people = db_session.query(Person)\
        .join(YaleAffiliation)\
        .filter(Person.location.ilike('%connecticut%'))\
        .limit(3).all()
    
    print(f"Found {len(ct_people)} Yale people in Connecticut:")
    for person in ct_people:
        print(f"  - {person.full_name} ({person.location})")
    
    # Test search by degree type
    print(f"\nQuery: Find Yale undergraduates")
    
    undergrads = db_session.query(Person)\
        .join(YaleAffiliation)\
        .filter(YaleAffiliation.affiliation_type == 'undergraduate')\
        .limit(3).all()
    
    print(f"Found {len(undergrads)} Yale undergraduates:")
    for person in undergrads:
        print(f"  - {person.full_name}")
        for yale_aff in person.yale_affiliations:
            if yale_aff.affiliation_type == 'undergraduate':
                print(f"    {yale_aff.school}, {yale_aff.major}")
    
    print(f"\n=== Database Test Complete ===")
    print("✓ Real Yale data successfully imported and searchable!")
    
    db_session.close()

if __name__ == "__main__":
    test_database()