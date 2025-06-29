#!/usr/bin/env python3
"""
Set up optimized database indexes for fast searching
Creates indexes on key searchable fields for Yale Network Search
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")

def setup_search_indexes():
    """Create optimized indexes for search performance"""
    
    engine = create_engine(DATABASE_URL)
    
    print("🔧 SETTING UP SEARCH INDEXES")
    print("=" * 50)
    
    with engine.connect() as conn:
        
        # Full-text search indexes for people table
        print("📝 Creating full-text search indexes...")
        
        search_indexes = [
            # People table - main search fields
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS people_name_gin 
            ON people USING gin(to_tsvector('english', full_name))
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS people_headline_gin 
            ON people USING gin(to_tsvector('english', headline))
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS people_location_gin 
            ON people USING gin(to_tsvector('english', location))
            """,
            
            # Combined search index for people
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS people_search_combined_gin 
            ON people USING gin(to_tsvector('english', 
                COALESCE(full_name, '') || ' ' || 
                COALESCE(headline, '') || ' ' || 
                COALESCE(location, '') || ' ' ||
                COALESCE(about, '')
            ))
            """,
            
            # Yale affiliations - searchable fields
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_school_gin 
            ON yale_affiliations USING gin(to_tsvector('english', school))
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_major_gin 
            ON yale_affiliations USING gin(to_tsvector('english', major))
            """,
            
            # Regular indexes for exact matches and sorting
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS people_location_idx 
            ON people (location)
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_school_idx 
            ON yale_affiliations (school)
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_class_year_idx 
            ON yale_affiliations (class_year)
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_major_idx 
            ON yale_affiliations (major)
            """,
            
            # Foreign key indexes for fast joins
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS yale_person_uuid_idx 
            ON yale_affiliations (person_uuid)
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS experience_person_uuid_idx 
            ON experience (person_uuid)
            """,
            
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS education_person_uuid_idx 
            ON education (person_uuid)
            """,
        ]
        
        # Create each index with error handling
        for i, index_sql in enumerate(search_indexes, 1):
            try:
                print(f"  Creating index {i}/{len(search_indexes)}...")
                conn.execute(text(index_sql))
                conn.commit()
                print(f"  ✅ Index {i} created")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"  ℹ️  Index {i} already exists")
                else:
                    print(f"  ❌ Error creating index {i}: {e}")
                conn.rollback()
        
        print("\n🧮 ANALYZING TABLES FOR OPTIMAL PERFORMANCE...")
        
        # Analyze tables to update statistics for query planner
        tables_to_analyze = ['people', 'yale_affiliations', 'experience', 'education']
        
        for table in tables_to_analyze:
            try:
                conn.execute(text(f"ANALYZE {table}"))
                print(f"  ✅ Analyzed {table}")
            except Exception as e:
                print(f"  ❌ Error analyzing {table}: {e}")
        
        conn.commit()
        
        print("\n📊 FINAL INDEX STATUS:")
        print("=" * 50)
        
        # Check all indexes
        indexes = conn.execute(text("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename IN ('people', 'yale_affiliations', 'experience', 'education')
            ORDER BY tablename, indexname
        """)).fetchall()
        
        current_table = None
        for idx in indexes:
            if idx.tablename != current_table:
                print(f"\n{idx.tablename}:")
                current_table = idx.tablename
            
            index_type = "GIN" if "gin" in idx.indexdef else "BTREE"
            print(f"  • {idx.indexname} ({index_type})")
        
        print(f"\n✅ Search optimization complete! Created {len(search_indexes)} indexes.")

if __name__ == "__main__":
    setup_search_indexes()