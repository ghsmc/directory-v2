#!/usr/bin/env python3
"""
Comprehensive Search API for Yale Network Search
Handles natural language queries with SQL optimization and ranking
"""

import os
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")

@dataclass
class SearchFilters:
    """Structured search filters extracted from natural language queries"""
    locations: List[str] = None
    roles: List[str] = None  
    industries: List[str] = None
    yale_schools: List[str] = None
    majors: List[str] = None
    class_years: List[int] = None
    companies: List[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        # Initialize empty lists if None
        for field in ['locations', 'roles', 'industries', 'yale_schools', 'majors', 'companies', 'keywords']:
            if getattr(self, field) is None:
                setattr(self, field, [])

class YaleNetworkSearch:
    """Advanced search engine for Yale Network"""
    
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Pre-defined mappings for better query parsing
        self.location_mappings = {
            'nyc': 'New York',
            'new york city': 'New York', 
            'sf': 'San Francisco',
            'bay area': 'San Francisco',
            'silicon valley': 'San Francisco',
            'dc': 'Washington',
            'washington dc': 'Washington',
            'la': 'Los Angeles',
            'boston': 'Boston',
            'chicago': 'Chicago',
            'london': 'London',
            'connecticut': 'Connecticut',
            'ct': 'Connecticut'
        }
        
        self.role_keywords = {
            'vc': ['venture capital', 'vc', 'investor', 'partner'],
            'founder': ['founder', 'ceo', 'entrepreneur', 'startup'],
            'doctor': ['doctor', 'physician', 'md', 'medical'],
            'lawyer': ['lawyer', 'attorney', 'legal', 'law'],
            'professor': ['professor', 'academic', 'faculty', 'researcher'],
            'consultant': ['consultant', 'consulting', 'mckinsey', 'bcg', 'bain'],
            'banker': ['banker', 'investment banking', 'goldman', 'morgan stanley', 'jp morgan'],
            'engineer': ['engineer', 'software', 'tech', 'developer', 'programming']
        }
        
        self.yale_school_mappings = {
            'som': 'Yale School of Management',
            'school of management': 'Yale School of Management',
            'business school': 'Yale School of Management',
            'law school': 'Yale Law School',
            'medical school': 'Yale School of Medicine',
            'school of medicine': 'Yale School of Medicine',
            'divinity school': 'Yale Divinity School',
            'school of art': 'Yale School of Art',
            'school of music': 'Yale School of Music',
            'graduate school': 'Yale Graduate School',
            'college': 'Yale College',
            'undergrad': 'Yale College'
        }
    
    def parse_query(self, query: str) -> SearchFilters:
        """Parse natural language query into structured search filters"""
        
        query_lower = query.lower()
        filters = SearchFilters()
        
        # Extract locations
        for location_key, location_value in self.location_mappings.items():
            if location_key in query_lower:
                filters.locations.append(location_value)
        
        # Extract major cities only
        major_cities = [
            'new york', 'san francisco', 'los angeles', 'chicago', 'boston', 
            'washington', 'london', 'paris', 'tokyo', 'seattle', 'denver', 
            'austin', 'miami', 'atlanta', 'philadelphia', 'detroit', 'phoenix',
            'dallas', 'houston', 'portland', 'nashville', 'charlotte'
        ]
        
        for city in major_cities:
            if city in query_lower:
                city_title = city.title()
                if city_title not in filters.locations:
                    filters.locations.append(city_title)
        
        # Extract roles using keyword mapping
        for role_category, keywords in self.role_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if role_category not in filters.roles:
                        filters.roles.append(role_category)
        
        # Extract Yale schools
        for school_key, school_value in self.yale_school_mappings.items():
            if school_key in query_lower:
                if school_value not in filters.yale_schools:
                    filters.yale_schools.append(school_value)
        
        # Extract class years
        year_matches = re.findall(r'\b(19|20)\d{2}\b', query)
        for year in year_matches:
            try:
                year_int = int(year)
                if 1900 <= year_int <= 2030:
                    filters.class_years.append(year_int)
            except ValueError:
                pass
        
        # Extract known companies only
        known_companies = [
            'goldman sachs', 'goldman', 'morgan stanley', 'jp morgan', 'jpmorgan',
            'mckinsey', 'bcg', 'bain', 'google', 'apple', 'microsoft', 'amazon', 
            'facebook', 'meta', 'tesla', 'netflix', 'uber', 'airbnb', 'salesforce',
            'oracle', 'ibm', 'intel', 'nvidia', 'spotify', 'twitter', 'linkedin',
            'blackstone', 'kkr', 'carlyle', 'apollo', 'blackrock', 'vanguard'
        ]
        
        for company in known_companies:
            if company in query_lower:
                company_title = company.title()
                if company_title not in filters.companies:
                    filters.companies.append(company_title)
        
        # Extract remaining keywords (after removing parsed terms)
        remaining_query = query_lower
        for location in filters.locations:
            remaining_query = remaining_query.replace(location.lower(), '')
        for role in filters.roles:
            remaining_query = remaining_query.replace(role, '')
        
        # Clean up and extract keywords
        keywords = [word.strip() for word in remaining_query.split() 
                   if len(word.strip()) > 2 and word.strip() not in ['from', 'who', 'went', 'yale', 'and', 'the', 'are', 'in']]
        filters.keywords = keywords[:5]  # Limit to 5 keywords
        
        return filters
    
    def build_search_query(self, filters: SearchFilters, limit: int = 50) -> Tuple[str, Dict]:
        """Build optimized SQL query from search filters"""
        
        base_query = """
        SELECT DISTINCT
            p.uuid_id,
            p.full_name,
            p.headline,
            p.location,
            p.summary,
            p.profile_url,
            p.ai_summary,
            p.ai_tags,
            p.ai_processed,
            ya.school as yale_school,
            ya.major,
            ya.class_year,
            ya.affiliation_type,
            -- Enhanced relevance scoring with AI content
            COALESCE(ts_rank(to_tsvector('english', p.full_name), plainto_tsquery('english', :search_text)), 0) * 4 +
            COALESCE(ts_rank(to_tsvector('english', p.headline), plainto_tsquery('english', :search_text)), 0) * 3 +
            COALESCE(ts_rank(to_tsvector('english', COALESCE(p.ai_summary, '')), plainto_tsquery('english', :search_text)), 0) * 3 +
            COALESCE(ts_rank(to_tsvector('english', p.location), plainto_tsquery('english', :search_text)), 0) * 2 +
            COALESCE(ts_rank(to_tsvector('english', COALESCE(ya.school, '')), plainto_tsquery('english', :search_text)), 0) * 2 +
            COALESCE(ts_rank(to_tsvector('english', COALESCE(ya.major, '')), plainto_tsquery('english', :search_text)), 0) * 1.5 +
            COALESCE(ts_rank(to_tsvector('english', COALESCE(p.summary, '')), plainto_tsquery('english', :search_text)), 0) * 1
            as relevance_score
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        WHERE 1=1
        """
        
        conditions = []
        params = {
            'search_text': ' '.join(filters.keywords) if filters.keywords else 'yale',
            'limit': limit
        }
        
        # Location filters
        if filters.locations:
            location_conditions = []
            for i, location in enumerate(filters.locations):
                param_name = f'location_{i}'
                location_conditions.append(f"p.location ILIKE :{param_name}")
                params[param_name] = f'%{location}%'
            conditions.append(f"({' OR '.join(location_conditions)})")
        
        # Role filters (search in headline)
        if filters.roles:
            role_conditions = []
            for i, role in enumerate(filters.roles):
                param_name = f'role_{i}'
                # Create role-specific search terms
                role_terms = self.role_keywords.get(role, [role])
                role_query = ' | '.join(role_terms)  # OR operator for tsquery
                role_conditions.append(f"to_tsvector('english', p.headline) @@ plainto_tsquery('english', :{param_name})")
                params[param_name] = role_query
            conditions.append(f"({' OR '.join(role_conditions)})")
        
        # Yale school filters
        if filters.yale_schools:
            school_conditions = []
            for i, school in enumerate(filters.yale_schools):
                param_name = f'school_{i}'
                school_conditions.append(f"ya.school ILIKE :{param_name}")
                params[param_name] = f'%{school}%'
            conditions.append(f"({' OR '.join(school_conditions)})")
        
        # Major filters
        if filters.majors:
            major_conditions = []
            for i, major in enumerate(filters.majors):
                param_name = f'major_{i}'
                major_conditions.append(f"ya.major ILIKE :{param_name}")
                params[param_name] = f'%{major}%'
            conditions.append(f"({' OR '.join(major_conditions)})")
        
        # Class year filters
        if filters.class_years:
            year_conditions = []
            for i, year in enumerate(filters.class_years):
                param_name = f'year_{i}'
                # Allow range around the year (±2 years)
                year_conditions.append(f"ya.class_year BETWEEN :{param_name}_min AND :{param_name}_max")
                params[f'{param_name}_min'] = year - 2
                params[f'{param_name}_max'] = year + 2
            conditions.append(f"({' OR '.join(year_conditions)})")
        
        # Company filters (search in headline)
        if filters.companies:
            company_conditions = []
            for i, company in enumerate(filters.companies):
                param_name = f'company_{i}'
                company_conditions.append(f"p.headline ILIKE :{param_name}")
                params[param_name] = f'%{company}%'
            conditions.append(f"({' OR '.join(company_conditions)})")
        
        # Add all conditions to query
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        # Add ordering and limit
        base_query += """
        ORDER BY relevance_score DESC, p.full_name ASC
        LIMIT :limit
        """
        
        return base_query, params
    
    def search(self, query: str, limit: int = 50) -> Dict[str, Any]:
        """Perform comprehensive search with natural language query"""
        
        # Parse the query
        filters = self.parse_query(query)
        
        # Build and execute SQL query
        sql_query, params = self.build_search_query(filters, limit)
        
        with self.engine.connect() as conn:
            try:
                results = conn.execute(text(sql_query), params).fetchall()
                
                # Format results with AI enhancements
                people = []
                for result in results:
                    person = {
                        'uuid_id': result.uuid_id,
                        'name': result.full_name,
                        'headline': result.headline,
                        'location': result.location,
                        'summary': result.summary,
                        'profile_url': result.profile_url,
                        'ai_summary': result.ai_summary,
                        'ai_tags': result.ai_tags,
                        'ai_processed': result.ai_processed,
                        'yale_school': result.yale_school,
                        'major': result.major,
                        'class_year': result.class_year,
                        'affiliation_type': result.affiliation_type,
                        'relevance_score': float(result.relevance_score) if result.relevance_score else 0.0
                    }
                    people.append(person)
                
                return {
                    'query': query,
                    'filters_detected': {
                        'locations': filters.locations,
                        'roles': filters.roles,
                        'industries': filters.industries,
                        'yale_schools': filters.yale_schools,
                        'majors': filters.majors,
                        'class_years': filters.class_years,
                        'companies': filters.companies,
                        'keywords': filters.keywords
                    },
                    'results': people,
                    'total_found': len(people),
                    'search_time_ms': 0  # Could add timing if needed
                }
                
            except Exception as e:
                return {
                    'query': query,
                    'error': str(e),
                    'results': [],
                    'total_found': 0
                }

def test_search_api():
    """Test the search API with various queries"""
    
    print("🔍 TESTING YALE NETWORK SEARCH API")
    print("=" * 60)
    
    search_engine = YaleNetworkSearch()
    
    test_queries = [
        "VC investors from NYC who went to Yale",
        "founders in San Francisco",
        "doctors in Boston",
        "SOM graduates working at Goldman Sachs",
        "Yale Law School alumni in DC",
        "software engineers in Silicon Valley",
        "consultants from class of 2010"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: '{query}'")
        print("-" * 40)
        
        result = search_engine.search(query, limit=5)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        print(f"Filters detected: {result['filters_detected']}")
        print(f"Found {result['total_found']} people")
        
        for j, person in enumerate(result['results'][:3], 1):
            print(f"\n  {j}. {person['name']}")
            print(f"     {person['headline']}")
            print(f"     {person['yale_school']} • {person['location']}")
            print(f"     Relevance: {person['relevance_score']:.2f}")

if __name__ == "__main__":
    test_search_api()