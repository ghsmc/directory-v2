#!/usr/bin/env python3
"""
Create missing search indexes (without CONCURRENT to avoid transaction issues)
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")

def create_missing_indexes():
    """Create missing indexes for search optimization"""
    
    engine = create_engine(DATABASE_URL)
    
    print("🔧 CREATING MISSING SEARCH INDEXES")
    print("=" * 50)
    
    # Create indexes one by one in separate connections to avoid transaction issues
    missing_indexes = [
        # Yale affiliations indexes
        """
        CREATE INDEX IF NOT EXISTS yale_school_gin 
        ON yale_affiliations USING gin(to_tsvector('english', COALESCE(school, '')))
        """,
        
        """
        CREATE INDEX IF NOT EXISTS yale_major_gin 
        ON yale_affiliations USING gin(to_tsvector('english', COALESCE(major, '')))
        """,
        
        """
        CREATE INDEX IF NOT EXISTS yale_school_idx 
        ON yale_affiliations (school)
        """,
        
        """
        CREATE INDEX IF NOT EXISTS yale_class_year_idx 
        ON yale_affiliations (class_year)
        """,
        
        """
        CREATE INDEX IF NOT EXISTS yale_major_idx 
        ON yale_affiliations (major)
        """,
        
        # People additional indexes
        """
        CREATE INDEX IF NOT EXISTS people_headline_gin 
        ON people USING gin(to_tsvector('english', COALESCE(headline, '')))
        """,
    ]
    
    for i, index_sql in enumerate(missing_indexes, 1):
        try:
            # Create new connection for each index to avoid transaction issues
            with engine.connect() as conn:
                print(f"  Creating index {i}/{len(missing_indexes)}...")
                conn.execute(text(index_sql))
                conn.commit()
                print(f"  ✅ Index {i} created successfully")
        except Exception as e:
            if "already exists" in str(e):
                print(f"  ℹ️  Index {i} already exists")
            else:
                print(f"  ❌ Error creating index {i}: {e}")
    
    print("\n✅ Missing indexes creation complete!")

if __name__ == "__main__":
    create_missing_indexes()