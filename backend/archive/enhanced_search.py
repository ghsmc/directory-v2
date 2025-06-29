#!/usr/bin/env python3
"""Enhanced search system focused on result quality"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from app.models import Person, Education, Experience, YaleAffiliation
import re
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@dataclass
class SearchResult:
    person: Person
    score: float
    match_reasons: List[str]
    matched_terms: Dict[str, List[str]]

class EnhancedYaleSearch:
    """Enhanced search engine focused on result quality"""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # Common search patterns
        self.location_keywords = {
            'nyc': ['new york', 'manhattan', 'brooklyn', 'queens', 'bronx'],
            'new york': ['new york', 'ny', 'nyc', 'manhattan'],
            'san francisco': ['san francisco', 'sf', 'bay area'],
            'boston': ['boston', 'cambridge', 'somerville'],
            'dc': ['washington', 'dc', 'd.c.'],
            'la': ['los angeles', 'hollywood', 'santa monica'],
            'chicago': ['chicago', 'illinois'],
            'seattle': ['seattle', 'washington'],
            'connecticut': ['connecticut', 'ct', 'new haven', 'hartford'],
        }
        
        self.title_keywords = {
            'vc': ['venture capital', 'venture partner', 'general partner', 'managing partner', 'principal', 'associate'],
            'investor': ['investor', 'investment', 'venture capital', 'private equity'],
            'founder': ['founder', 'co-founder', 'ceo', 'chief executive'],
            'engineer': ['engineer', 'software engineer', 'engineering', 'developer'],
            'consultant': ['consultant', 'consulting', 'advisor'],
            'professor': ['professor', 'academic', 'faculty', 'lecturer'],
            'lawyer': ['lawyer', 'attorney', 'legal', 'counsel'],
            'doctor': ['doctor', 'physician', 'md', 'medical'],
            'analyst': ['analyst', 'research', 'data analyst'],
            'manager': ['manager', 'director', 'vice president', 'vp'],
        }
        
        self.industry_keywords = {
            'tech': ['technology', 'software', 'ai', 'machine learning', 'startup'],
            'finance': ['finance', 'banking', 'investment', 'financial services'],
            'healthcare': ['healthcare', 'medical', 'pharma', 'biotech'],
            'education': ['education', 'teaching', 'academic', 'university'],
            'consulting': ['consulting', 'strategy', 'advisory'],
            'law': ['law', 'legal', 'attorney', 'lawyer'],
            'nonprofit': ['nonprofit', 'ngo', 'foundation', 'charity'],
        }
        
    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse query into structured components"""
        query_lower = query.lower()
        
        parsed = {
            'original': query,
            'locations': [],
            'titles': [],
            'industries': [],
            'yale_specific': [],
            'keywords': [],
            'intent': self._detect_intent(query_lower)
        }
        
        # Extract locations
        for loc, variants in self.location_keywords.items():
            if any(variant in query_lower for variant in variants):
                parsed['locations'].append(loc)
        
        # Extract titles/roles
        for title, variants in self.title_keywords.items():
            if any(variant in query_lower for variant in variants):
                parsed['titles'].append(title)
        
        # Extract industries
        for industry, variants in self.industry_keywords.items():
            if any(variant in query_lower for variant in variants):
                parsed['industries'].append(industry)
        
        # Extract Yale-specific terms
        yale_terms = ['yale', 'sOM', 'school of management', 'law school', 'medical school', 'college']
        for term in yale_terms:
            if term.lower() in query_lower:
                parsed['yale_specific'].append(term)
        
        # Extract other keywords
        words = re.findall(r'\b\w+\b', query_lower)
        stop_words = {'the', 'and', 'or', 'in', 'at', 'for', 'with', 'who', 'are', 'working', 'from'}
        parsed['keywords'] = [w for w in words if w not in stop_words and len(w) > 2]
        
        return parsed
    
    def _detect_intent(self, query: str) -> str:
        """Detect search intent"""
        if any(word in query for word in ['investor', 'vc', 'venture', 'fund']):
            return 'find_investors'
        elif any(word in query for word in ['founder', 'entrepreneur', 'startup']):
            return 'find_entrepreneurs'
        elif any(word in query for word in ['professor', 'academic', 'faculty']):
            return 'find_academics'
        elif any(word in query for word in ['alumni', 'graduate', 'class']):
            return 'find_alumni'
        else:
            return 'find_people'
    
    def build_search_query(self, parsed: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Build optimized SQL query"""
        
        base_query = """
        SELECT DISTINCT
            p.uuid_id,
            p.full_name,
            p.location,
            p.headline,
            p.summary,
            p.linkedin_url,
            -- Current position
            COALESCE(current_exp.company, '') as current_company,
            COALESCE(current_exp.title, '') as current_title,
            -- Yale info
            COALESCE(ya.school, '') as yale_school,
            COALESCE(ya.affiliation_type, '') as yale_type,
            COALESCE(ya.major, '') as yale_major,
            -- Scoring components
            {scoring_sql} as relevance_score
        FROM people p
        LEFT JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        LEFT JOIN LATERAL (
            SELECT e.* FROM experience e 
            WHERE e.person_uuid = p.uuid_id 
            AND e.is_current = TRUE 
            ORDER BY e.id DESC
            LIMIT 1
        ) current_exp ON TRUE
        WHERE ya.person_uuid IS NOT NULL  -- Only Yale people
        {where_clauses}
        ORDER BY relevance_score DESC
        LIMIT :limit
        """
        
        where_clauses = []
        params = {'limit': 50}
        scoring_parts = ['1.0']  # Base score
        
        # Location filtering
        if parsed['locations']:
            location_conditions = []
            for i, loc in enumerate(parsed['locations']):
                param_name = f"location_{i}"
                variants = self.location_keywords.get(loc, [loc])
                location_or = []
                for j, variant in enumerate(variants):
                    var_param = f"{param_name}_{j}"
                    location_or.append(f"p.location ILIKE :{var_param}")
                    params[var_param] = f"%{variant}%"
                location_conditions.append(f"({' OR '.join(location_or)})")
            
            if location_conditions:
                where_clauses.append(f"({' OR '.join(location_conditions)})")
                scoring_parts.append("2.0")  # Boost for location match
        
        # Title/role filtering
        if parsed['titles']:
            title_conditions = []
            for i, title in enumerate(parsed['titles']):
                param_name = f"title_{i}"
                variants = self.title_keywords.get(title, [title])
                title_or = []
                for j, variant in enumerate(variants):
                    var_param = f"{param_name}_{j}"
                    title_or.append(f"""
                        (p.headline ILIKE :{var_param} OR 
                         current_exp.title ILIKE :{var_param} OR
                         EXISTS (
                             SELECT 1 FROM experience e2 
                             WHERE e2.person_uuid = p.uuid_id 
                             AND e2.title ILIKE :{var_param}
                         ))
                    """)
                    params[var_param] = f"%{variant}%"
                title_conditions.append(f"({' OR '.join(title_or)})")
            
            if title_conditions:
                where_clauses.append(f"({' OR '.join(title_conditions)})")
                scoring_parts.append("3.0")  # High boost for title match
        
        # Industry filtering
        if parsed['industries']:
            industry_conditions = []
            for i, industry in enumerate(parsed['industries']):
                param_name = f"industry_{i}"
                variants = self.industry_keywords.get(industry, [industry])
                industry_or = []
                for j, variant in enumerate(variants):
                    var_param = f"{param_name}_{j}"
                    industry_or.append(f"""
                        (p.headline ILIKE :{var_param} OR 
                         p.summary ILIKE :{var_param} OR
                         current_exp.company ILIKE :{var_param} OR
                         EXISTS (
                             SELECT 1 FROM experience e3 
                             WHERE e3.person_uuid = p.uuid_id 
                             AND (e3.company ILIKE :{var_param} OR e3.description ILIKE :{var_param})
                         ))
                    """)
                    params[var_param] = f"%{variant}%"
                industry_conditions.append(f"({' OR '.join(industry_or)})")
            
            if industry_conditions:
                where_clauses.append(f"({' OR '.join(industry_conditions)})")
                scoring_parts.append("1.5")  # Moderate boost for industry match
        
        # Yale-specific filtering
        if parsed['yale_specific']:
            yale_conditions = []
            for i, yale_term in enumerate(parsed['yale_specific']):
                param_name = f"yale_{i}"
                if 'som' in yale_term.lower() or 'management' in yale_term.lower():
                    yale_conditions.append(f"ya.school ILIKE :{param_name}")
                    params[param_name] = "%school of management%"
                elif 'law' in yale_term.lower():
                    yale_conditions.append(f"ya.school ILIKE :{param_name}")
                    params[param_name] = "%law school%"
                elif 'medical' in yale_term.lower():
                    yale_conditions.append(f"ya.school ILIKE :{param_name}")
                    params[param_name] = "%medical%"
                elif 'college' in yale_term.lower():
                    yale_conditions.append(f"ya.school ILIKE :{param_name}")
                    params[param_name] = "%yale college%"
            
            if yale_conditions:
                where_clauses.append(f"({' OR '.join(yale_conditions)})")
                scoring_parts.append("1.0")  # Boost for Yale school match
        
        # Keyword search
        if parsed['keywords']:
            keyword_conditions = []
            for i, keyword in enumerate(parsed['keywords'][:5]):  # Limit to 5 keywords
                param_name = f"keyword_{i}"
                keyword_conditions.append(f"""
                    (p.full_name ILIKE :{param_name} OR 
                     p.headline ILIKE :{param_name} OR
                     p.summary ILIKE :{param_name} OR
                     ya.major ILIKE :{param_name})
                """)
                params[param_name] = f"%{keyword}%"
            
            if keyword_conditions:
                where_clauses.append(f"({' OR '.join(keyword_conditions)})")
                scoring_parts.append("0.5")  # Small boost for keyword match
        
        # Build final query
        scoring_sql = " + ".join(scoring_parts)
        where_sql = "\nAND " + "\nAND ".join(where_clauses) if where_clauses else ""
        
        final_query = base_query.format(
            scoring_sql=scoring_sql,
            where_clauses=where_sql
        )
        
        return final_query, params
    
    def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        """Execute enhanced search"""
        
        logger.info(f"Searching for: {query}")
        
        # Parse query
        parsed = self.parse_query(query)
        logger.info(f"Parsed query: {parsed}")
        
        # Build and execute SQL
        sql, params = self.build_search_query(parsed)
        params['limit'] = limit
        
        logger.info(f"Executing SQL with {len([k for k, v in params.items() if k != 'limit'])} parameters")
        
        results = []
        try:
            rows = self.db.execute(text(sql), params).fetchall()
            logger.info(f"Found {len(rows)} results")
            
            for row in rows:
                person = self.db.query(Person).filter_by(uuid_id=row[0]).first()
                if person:
                    # Analyze match reasons
                    match_reasons = self._analyze_match_reasons(person, parsed)
                    matched_terms = self._extract_matched_terms(person, parsed)
                    
                    result = SearchResult(
                        person=person,
                        score=float(row[11]) if row[11] else 0.0,
                        match_reasons=match_reasons,
                        matched_terms=matched_terms
                    )
                    results.append(result)
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            
        return results
    
    def _analyze_match_reasons(self, person: Person, parsed: Dict) -> List[str]:
        """Analyze why this person matched the search"""
        reasons = []
        
        # Location match
        if parsed['locations']:
            for loc in parsed['locations']:
                variants = self.location_keywords.get(loc, [loc])
                if any(var in person.location.lower() for var in variants if person.location):
                    reasons.append(f"Located in {person.location}")
        
        # Title match
        if parsed['titles']:
            current_exp = next((e for e in person.experiences if e.is_current), None)
            if current_exp:
                for title in parsed['titles']:
                    variants = self.title_keywords.get(title, [title])
                    if any(var in current_exp.title.lower() for var in variants if current_exp.title):
                        reasons.append(f"Current role: {current_exp.title}")
        
        # Yale affiliation
        if person.yale_affiliations:
            yale_aff = person.yale_affiliations[0]
            reasons.append(f"Yale {yale_aff.affiliation_type}: {yale_aff.school}")
            if yale_aff.major:
                reasons.append(f"Major: {yale_aff.major}")
        
        return reasons
    
    def _extract_matched_terms(self, person: Person, parsed: Dict) -> Dict[str, List[str]]:
        """Extract which specific terms matched"""
        matched = defaultdict(list)
        
        # Check location matches
        if person.location:
            for loc in parsed['locations']:
                variants = self.location_keywords.get(loc, [loc])
                for variant in variants:
                    if variant in person.location.lower():
                        matched['location'].append(person.location)
        
        # Check title matches
        current_exp = next((e for e in person.experiences if e.is_current), None)
        if current_exp and current_exp.title:
            for title in parsed['titles']:
                variants = self.title_keywords.get(title, [title])
                for variant in variants:
                    if variant in current_exp.title.lower():
                        matched['title'].append(current_exp.title)
        
        return dict(matched)

def test_enhanced_search():
    """Test the enhanced search system"""
    
    search_engine = EnhancedYaleSearch()
    
    # Test queries focused on result quality
    test_queries = [
        "Yale VC investors in NYC",
        "Yale entrepreneurs and founders",
        "Yale SOM graduates working in finance", 
        "Yale people in Connecticut",
        "Yale computer science graduates",
        "Yale professors and academics",
        "Yale alumni working at tech companies",
        "Yale law school graduates"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        results = search_engine.search(query, limit=5)
        
        if not results:
            print("No results found")
            continue
            
        for i, result in enumerate(results, 1):
            person = result.person
            print(f"\n{i}. {person.full_name} (Score: {result.score:.1f})")
            print(f"   Location: {person.location}")
            print(f"   Headline: {person.headline}")
            
            # Current position
            current_exp = next((e for e in person.experiences if e.is_current), None)
            if current_exp:
                print(f"   Current: {current_exp.title} at {current_exp.company}")
            
            # Yale info
            if person.yale_affiliations:
                yale_aff = person.yale_affiliations[0]
                yale_info = f"{yale_aff.school} ({yale_aff.affiliation_type})"
                if yale_aff.major:
                    yale_info += f" - {yale_aff.major}"
                print(f"   Yale: {yale_info}")
            
            # Match reasons
            if result.match_reasons:
                print(f"   Why matched: {', '.join(result.match_reasons)}")
    
    search_engine.db.close()

if __name__ == "__main__":
    test_enhanced_search()