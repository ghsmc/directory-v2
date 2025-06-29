"""
AI-Powered Query Enhancement System
Generates comprehensive filters, traits, key phrases, and SQL queries for complex searches
"""

from openai import OpenAI
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class SearchEnhancement:
    """Enhanced search query with AI-generated components"""
    original_query: str
    traits: List[str]
    work_filters: List[str]
    key_phrases: List[str]
    company_patterns: List[str]
    title_patterns: List[str]
    sql_conditions: str
    explanation: str

class AIQueryEnhancer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def enhance_query(self, query: str) -> SearchEnhancement:
        """
        Use AI to generate comprehensive search enhancement for a natural language query
        """
        prompt = f"""
        Analyze this search query and generate comprehensive search enhancement components:
        
        Query: "{query}"
        
        Generate a JSON response with these components:
        
        1. "traits" - List of key professional traits this person would have
        2. "work_filters" - List of work experience requirements
        3. "key_phrases" - List of phrases likely to appear in their profile/experience
        4. "company_patterns" - List of company name patterns or types
        5. "title_patterns" - List of job title patterns to match
        6. "sql_conditions" - SQL WHERE clause conditions for searching experience table
        7. "explanation" - Brief explanation of the search strategy
        
        Database schema context:
        - people table: full_name, headline, summary, location
        - experience table: company, title, description, date_from, date_to, is_current
        - education table: institution, degree, field_of_study, title
        - yale_affiliations table: affiliation_type, school, class_year, major
        
        Example for "Software engineers who've worked on growth at a Series A-C company":
        {{
          "traits": [
            "Is a software engineer",
            "Has worked on growth initiatives",
            "Has experience at venture-backed companies",
            "Has worked at companies during Series A-C funding stages"
          ],
          "work_filters": [
            "Has software engineering experience",
            "Has worked on growth or growth engineering",
            "Has worked at startups or venture-backed companies",
            "Has experience during Series A, B, or C funding rounds"
          ],
          "key_phrases": [
            "software engineer",
            "backend developer",
            "full stack engineer",
            "growth engineer",
            "growth team",
            "user acquisition",
            "growth metrics",
            "Series A",
            "Series B", 
            "Series C",
            "venture-backed",
            "startup"
          ],
          "company_patterns": [
            "Series A startup",
            "Series B company", 
            "Series C startup",
            "venture-backed",
            "VC-funded"
          ],
          "title_patterns": [
            "software engineer",
            "backend engineer",
            "frontend engineer", 
            "full stack engineer",
            "growth engineer",
            "platform engineer",
            "staff engineer",
            "principal engineer",
            "lead engineer",
            "software developer",
            "SWE"
          ],
          "sql_conditions": "((e.title ILIKE '%software engineer%' OR e.title ILIKE '%swe%' OR e.title ILIKE '%developer%' OR e.title ILIKE '%backend engineer%' OR e.title ILIKE '%frontend engineer%' OR e.title ILIKE '%full stack%' OR e.title ILIKE '%platform engineer%' OR e.title ILIKE '%staff engineer%' OR e.title ILIKE '%principal engineer%' OR e.title ILIKE '%lead engineer%' OR e.title ILIKE '%growth engineer%') AND (e.title ILIKE '%growth%' OR e.description ILIKE '%growth%' OR e.description ILIKE '%user acquisition%' OR e.description ILIKE '%growth metrics%') AND (e.description ILIKE '%Series A%' OR e.description ILIKE '%Series B%' OR e.description ILIKE '%Series C%' OR e.description ILIKE '%venture%' OR e.description ILIKE '%startup%' OR e.company ILIKE '%startup%'))",
          "explanation": "Searching for software engineers with growth experience at venture-backed companies during Series A-C stages by matching job titles, growth-related keywords, and funding stage indicators."
        }}
        
        Generate similar comprehensive enhancement for: "{query}"
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing search queries and generating comprehensive database search strategies. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to extract JSON
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            
            enhancement_data = json.loads(content)
            
            return SearchEnhancement(
                original_query=query,
                traits=enhancement_data.get('traits', []),
                work_filters=enhancement_data.get('work_filters', []),
                key_phrases=enhancement_data.get('key_phrases', []),
                company_patterns=enhancement_data.get('company_patterns', []),
                title_patterns=enhancement_data.get('title_patterns', []),
                sql_conditions=enhancement_data.get('sql_conditions', ''),
                explanation=enhancement_data.get('explanation', '')
            )
            
        except Exception as e:
            print(f"Error enhancing query: {e}")
            # Return basic enhancement as fallback
            return SearchEnhancement(
                original_query=query,
                traits=[f"Related to {query}"],
                work_filters=[f"Has experience in {query}"],
                key_phrases=query.lower().split(),
                company_patterns=[],
                title_patterns=[],
                sql_conditions=f"(e.title ILIKE '%{query}%' OR e.description ILIKE '%{query}%')",
                explanation=f"Basic search for {query}"
            )
    
    def generate_enhanced_sql(self, enhancement: SearchEnhancement, limit: int = 20) -> str:
        """
        Generate a comprehensive SQL query using the AI enhancement
        Works with both experience table (if populated) and headline/summary for fallback
        """
        sql = f"""
        WITH enhanced_search AS (
            SELECT DISTINCT 
                p.uuid_id,
                p.full_name as name,
                p.headline,
                p.location,
                p.summary,
                p.ai_summary,
                p.ai_tags,
                p.ai_processed,
                ya.school as yale_school,
                ya.major,
                ya.class_year,
                ya.affiliation_type,
                p.profile_url,
                -- Relevance scoring
                (
                    -- Headline matches (highest weight for current data)
                    CASE WHEN {self._generate_headline_conditions(enhancement.key_phrases)} THEN 3.0 ELSE 0.0 END +
                    -- Summary matches (medium weight)  
                    CASE WHEN {self._generate_summary_conditions(enhancement.key_phrases)} THEN 2.0 ELSE 0.0 END +
                    -- Experience table matches (if available)
                    CASE WHEN {self._generate_title_conditions(enhancement.title_patterns)} THEN 2.5 ELSE 0.0 END +
                    CASE WHEN {self._generate_description_conditions(enhancement.key_phrases)} THEN 1.5 ELSE 0.0 END +
                    -- AI tags matches
                    CASE WHEN {self._generate_ai_tags_conditions(enhancement.key_phrases)} THEN 1.0 ELSE 0.0 END +
                    -- Yale affiliation bonus
                    CASE WHEN ya.person_uuid IS NOT NULL THEN 0.5 ELSE 0.0 END
                ) as relevance_score
            FROM people p
            LEFT JOIN experience e ON p.uuid_id = e.person_uuid
            LEFT JOIN yale_affiliations ya ON p.uuid_id = ya.person_uuid
            WHERE (
                -- Primary search conditions (headline, summary, experience)
                {self._generate_people_conditions(enhancement.key_phrases)}
                OR {enhancement.sql_conditions if enhancement.sql_conditions else 'FALSE'}
            )
        )
        SELECT *
        FROM enhanced_search
        WHERE relevance_score > 0
        ORDER BY relevance_score DESC, name ASC
        LIMIT {limit};
        """
        
        return sql
    
    def _generate_title_conditions(self, title_patterns: List[str]) -> str:
        """Generate SQL conditions for job title matching"""
        if not title_patterns:
            return "FALSE"
        
        conditions = []
        for pattern in title_patterns:
            conditions.append(f"e.title ILIKE '%{pattern}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_description_conditions(self, key_phrases: List[str]) -> str:
        """Generate SQL conditions for description matching"""
        if not key_phrases:
            return "FALSE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"e.description ILIKE '%{phrase}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_company_conditions(self, company_patterns: List[str]) -> str:
        """Generate SQL conditions for company matching"""
        if not company_patterns:
            return "FALSE"
            
        conditions = []
        for pattern in company_patterns:
            conditions.append(f"e.company ILIKE '%{pattern}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_fallback_conditions(self, key_phrases: List[str]) -> str:
        """Generate basic fallback conditions"""
        if not key_phrases:
            return "TRUE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"(e.title ILIKE '%{phrase}%' OR e.description ILIKE '%{phrase}%' OR p.headline ILIKE '%{phrase}%')")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_headline_conditions(self, key_phrases: List[str]) -> str:
        """Generate SQL conditions for headline matching"""
        if not key_phrases:
            return "FALSE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"p.headline ILIKE '%{phrase}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_summary_conditions(self, key_phrases: List[str]) -> str:
        """Generate SQL conditions for summary matching"""
        if not key_phrases:
            return "FALSE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"p.summary ILIKE '%{phrase}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_ai_tags_conditions(self, key_phrases: List[str]) -> str:
        """Generate SQL conditions for AI tags matching"""
        if not key_phrases:
            return "FALSE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"p.ai_tags::text ILIKE '%{phrase}%'")
        
        return f"({' OR '.join(conditions)})"
    
    def _generate_people_conditions(self, key_phrases: List[str]) -> str:
        """Generate comprehensive conditions for people table"""
        if not key_phrases:
            return "FALSE"
            
        conditions = []
        for phrase in key_phrases:
            conditions.append(f"(p.headline ILIKE '%{phrase}%' OR p.summary ILIKE '%{phrase}%' OR p.full_name ILIKE '%{phrase}%')")
        
        return f"({' OR '.join(conditions)})"

def test_enhancer():
    """Test the AI query enhancer"""
    enhancer = AIQueryEnhancer()
    
    test_queries = [
        "Software engineers who've worked on growth at a Series A-C company",
        "Product managers at tech startups",
        "Data scientists with machine learning experience",
        "Founders of healthcare companies",
        "Investment bankers at top firms"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        enhancement = enhancer.enhance_query(query)
        
        print(f"\nTraits:")
        for trait in enhancement.traits:
            print(f"  • {trait}")
        
        print(f"\nWork Filters:")
        for filter_item in enhancement.work_filters:
            print(f"  • {filter_item}")
        
        print(f"\nKey Phrases:")
        print(f"  {', '.join(enhancement.key_phrases)}")
        
        print(f"\nCompany Patterns:")
        print(f"  {', '.join(enhancement.company_patterns)}")
        
        print(f"\nTitle Patterns:")
        print(f"  {', '.join(enhancement.title_patterns)}")
        
        print(f"\nSQL Conditions:")
        print(f"  {enhancement.sql_conditions}")
        
        print(f"\nExplanation:")
        print(f"  {enhancement.explanation}")
        
        # Generate full SQL
        sql = enhancer.generate_enhanced_sql(enhancement)
        print(f"\nGenerated SQL:")
        print(sql)

if __name__ == "__main__":
    test_enhancer()