#!/usr/bin/env python3
"""
Data Explorer for Yale Network Search
Comprehensive analysis of the 14,412+ Yale profiles
"""

import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from collections import Counter
import re

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")

class YaleDataExplorer:
    """Explore and analyze Yale Network data"""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    def overview(self):
        """Get basic data overview"""
        print("📊 YALE NETWORK DATA OVERVIEW")
        print("=" * 60)
        
        with self.engine.connect() as conn:
            # Basic counts
            total_people = conn.execute(text("SELECT COUNT(*) FROM people")).scalar()
            yale_affiliations = conn.execute(text("SELECT COUNT(*) FROM yale_affiliations")).scalar()
            ai_enhanced = conn.execute(text("SELECT COUNT(*) FROM people WHERE ai_processed = TRUE")).scalar()
            
            print(f"Total People: {total_people:,}")
            print(f"Yale Affiliations: {yale_affiliations:,}")
            print(f"AI Enhanced: {ai_enhanced:,} ({ai_enhanced/total_people*100:.1f}%)")
    
    def analyze_schools(self):
        """Analyze Yale schools distribution"""
        print("\n🏫 YALE SCHOOLS BREAKDOWN:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            schools = conn.execute(text("""
                SELECT school, COUNT(*) as count
                FROM yale_affiliations 
                WHERE school IS NOT NULL AND LENGTH(school) > 0
                GROUP BY school 
                ORDER BY count DESC
                LIMIT 20
            """)).fetchall()
            
            for school in schools:
                print(f"{school.count:>6,} | {school.school}")
    
    def analyze_locations(self):
        """Analyze geographic distribution"""
        print("\n📍 GEOGRAPHIC DISTRIBUTION:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            # Get all locations
            locations = conn.execute(text("""
                SELECT location, COUNT(*) as count
                FROM people 
                WHERE location IS NOT NULL AND LENGTH(location) > 0
                GROUP BY location 
                ORDER BY count DESC 
                LIMIT 20
            """)).fetchall()
            
            print("Top Locations:")
            for loc in locations:
                print(f"{loc.count:>6,} | {loc.location}")
            
            # No location data
            no_location = conn.execute(text("""
                SELECT COUNT(*) FROM people 
                WHERE location IS NULL OR LENGTH(location) = 0
            """)).scalar()
            
            print(f"\n{no_location:>6,} | [No Location Data]")
    
    def analyze_headlines(self):
        """Analyze headline patterns and roles"""
        print("\n💼 ROLE ANALYSIS FROM HEADLINES:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            # Get all headlines
            headlines = conn.execute(text("""
                SELECT headline, COUNT(*) as count
                FROM people 
                WHERE headline IS NOT NULL AND LENGTH(headline) > 0
                GROUP BY headline 
                ORDER BY count DESC
                LIMIT 20
            """)).fetchall()
            
            print("Most Common Headlines:")
            for hl in headlines:
                print(f"{hl.count:>6,} | {hl.headline[:80]}...")
            
            # Role categorization
            print(f"\n📊 ROLE CATEGORIES:")
            role_patterns = {
                'Students': r'student',
                'Faculty/Professors': r'professor|faculty|lecturer',
                'Researchers': r'research|fellow|postdoc',
                'Medical': r'doctor|physician|md|medical',
                'Business/CEO': r'ceo|founder|entrepreneur|president',
                'Consultants': r'consultant|consulting',
                'Engineers': r'engineer|developer|software',
                'Lawyers': r'attorney|lawyer|legal',
                'Analysts': r'analyst|analysis'
            }
            
            for category, pattern in role_patterns.items():
                count = conn.execute(text(f"""
                    SELECT COUNT(*) FROM people 
                    WHERE headline IS NOT NULL 
                    AND headline ~* '{pattern}'
                """)).scalar()
                
                if count > 0:
                    print(f"{count:>6,} | {category}")
    
    def analyze_majors(self):
        """Analyze academic majors/fields"""
        print("\n🎓 ACADEMIC MAJORS/FIELDS:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            majors = conn.execute(text("""
                SELECT major, COUNT(*) as count
                FROM yale_affiliations 
                WHERE major IS NOT NULL AND LENGTH(major) > 0
                GROUP BY major 
                ORDER BY count DESC 
                LIMIT 20
            """)).fetchall()
            
            for major in majors:
                print(f"{major.count:>6,} | {major.major}")
    
    def analyze_class_years(self):
        """Analyze graduation years"""
        print("\n📅 CLASS YEARS DISTRIBUTION:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            years = conn.execute(text("""
                SELECT class_year, COUNT(*) as count
                FROM yale_affiliations 
                WHERE class_year IS NOT NULL 
                GROUP BY class_year 
                ORDER BY class_year DESC 
                LIMIT 30
            """)).fetchall()
            
            if years:
                print("Recent Years:")
                for year in years:
                    print(f"{year.count:>6,} | Class of {year.class_year}")
            else:
                print("No class year data available")
    
    def analyze_ai_tags(self):
        """Analyze AI-generated tags"""
        print("\n🤖 AI TAGS ANALYSIS:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            # Check if we have AI tags
            ai_count = conn.execute(text("""
                SELECT COUNT(*) FROM people 
                WHERE ai_tags IS NOT NULL
            """)).scalar()
            
            if ai_count > 0:
                # Get all tags
                tags = conn.execute(text("""
                    SELECT tag, COUNT(*) as count
                    FROM (
                        SELECT jsonb_array_elements_text(ai_tags) as tag
                        FROM people 
                        WHERE ai_tags IS NOT NULL
                    ) tags
                    GROUP BY tag
                    ORDER BY count DESC
                    LIMIT 15
                """)).fetchall()
                
                print(f"AI Enhanced Profiles: {ai_count:,}")
                print("Most Common AI Tags:")
                for tag in tags:
                    print(f"{tag.count:>6,} | {tag.tag}")
            else:
                print("No AI tags found yet. Run batch AI enhancement to generate tags.")
    
    def sample_profiles(self, limit=10):
        """Show sample interesting profiles"""
        print(f"\n👥 SAMPLE PROFILES ({limit} examples):")
        print("-" * 60)
        
        with self.engine.connect() as conn:
            # Get diverse sample
            profiles = conn.execute(text(f"""
                SELECT DISTINCT
                    p.full_name,
                    p.headline,
                    p.location,
                    p.ai_summary,
                    p.ai_tags,
                    ya.school,
                    ya.major,
                    ya.class_year
                FROM people p
                JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
                WHERE p.headline IS NOT NULL 
                AND LENGTH(p.headline) > 10
                ORDER BY 
                    CASE WHEN p.ai_processed = TRUE THEN 1 ELSE 2 END,
                    RANDOM()
                LIMIT {limit}
            """)).fetchall()
            
            for i, profile in enumerate(profiles, 1):
                print(f"\n{i}. {profile.full_name}")
                print(f"   📋 {profile.headline}")
                if profile.location:
                    print(f"   📍 {profile.location}")
                print(f"   🎓 {profile.school}")
                if profile.major:
                    print(f"   📚 Major: {profile.major}")
                if profile.class_year:
                    print(f"   📅 Class: {profile.class_year}")
                
                # AI enhancements if available
                if profile.ai_summary:
                    print(f"   🤖 AI: {profile.ai_summary}")
                if profile.ai_tags:
                    print(f"   🏷️  Tags: {profile.ai_tags}")
    
    def data_quality_analysis(self):
        """Analyze data quality and completeness"""
        print("\n📈 DATA QUALITY ANALYSIS:")
        print("-" * 50)
        
        with self.engine.connect() as conn:
            total = conn.execute(text("SELECT COUNT(*) FROM people")).scalar()
            
            fields = {
                'Full Name': "full_name IS NOT NULL AND LENGTH(full_name) > 0",
                'Email': "email IS NOT NULL AND LENGTH(email) > 0", 
                'Location': "location IS NOT NULL AND LENGTH(location) > 0",
                'Headline': "headline IS NOT NULL AND LENGTH(headline) > 0",
                'Summary': "summary IS NOT NULL AND LENGTH(summary) > 0",
                'LinkedIn URL': "linkedin_url IS NOT NULL AND LENGTH(linkedin_url) > 0",
                'Profile URL': "profile_url IS NOT NULL AND LENGTH(profile_url) > 0"
            }
            
            print("Field Completeness:")
            for field_name, condition in fields.items():
                count = conn.execute(text(f"SELECT COUNT(*) FROM people WHERE {condition}")).scalar()
                percentage = (count / total) * 100
                print(f"{percentage:>6.1f}% | {field_name} ({count:,} records)")
    
    def search_suggestions(self):
        """Generate search suggestions based on data"""
        print("\n🔍 SUGGESTED SEARCHES:")
        print("-" * 50)
        
        suggestions = [
            "Try these natural language queries:",
            "",
            "By Role:",
            "  • 'students at Yale'",
            "  • 'research fellows'", 
            "  • 'medical students'",
            "  • 'computer science students'",
            "",
            "By Field:",
            "  • 'data science'",
            "  • 'medicine'",
            "  • 'economics'",
            "  • 'psychology'",
            "",
            "By School:",
            "  • 'Yale School of Medicine'",
            "  • 'Yale School of Management'",
            "  • 'Yale Law School'",
            "",
            "Combined:",
            "  • 'data science students at Yale'",
            "  • 'medical research at Yale School of Medicine'",
            "  • 'business students and management'"
        ]
        
        for suggestion in suggestions:
            print(suggestion)

def main():
    """Run comprehensive data analysis"""
    explorer = YaleDataExplorer()
    
    explorer.overview()
    explorer.analyze_schools()
    explorer.analyze_locations()
    explorer.analyze_headlines()
    explorer.analyze_majors()
    explorer.analyze_class_years()
    explorer.analyze_ai_tags()
    explorer.data_quality_analysis()
    explorer.sample_profiles(limit=5)
    explorer.search_suggestions()

if __name__ == "__main__":
    main()