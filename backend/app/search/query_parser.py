from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json


class FilterType(Enum):
    LOCATION = "location"
    EDUCATION = "education"
    COMPANY = "company"
    TITLE = "title"
    SKILLS = "skills"
    YALE_AFFILIATION = "yale_affiliation"
    TIME_RANGE = "time_range"
    INDUSTRY = "industry"
    INVESTMENT_FOCUS = "investment_focus"


@dataclass
class SearchFilter:
    filter_type: FilterType
    values: List[str]
    operator: str = "OR"  # OR, AND
    negated: bool = False


@dataclass
class ParsedQuery:
    original_query: str
    filters: List[SearchFilter]
    keywords: List[str]
    intent: str  # 'find_people', 'find_investors', 'find_alumni', etc.
    

class QueryParser:
    """Parse natural language queries into structured filters like happenstance.ai"""
    
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4-turbo-preview",
            openai_api_key=openai_api_key
        )
        
        # Common patterns for different filter types
        self.location_patterns = [
            "in", "from", "based in", "located in", "lives in", "works in",
            "NYC", "New York", "NY", "Manhattan", "Brooklyn"
        ]
        
        self.education_patterns = [
            "went to", "graduated from", "attended", "studied at", "alumni",
            "Yale", "Harvard", "Stanford", "MIT", "Columbia"
        ]
        
        self.investor_patterns = [
            "VC", "venture capital", "investor", "partner", "principal",
            "investment", "fund", "angel", "seed", "series"
        ]
        
        self.industry_patterns = [
            "edtech", "education", "networking", "fintech", "healthcare",
            "AI", "ML", "blockchain", "crypto", "sustainability"
        ]
        
    def parse(self, query: str) -> ParsedQuery:
        """Parse a natural language query into structured filters"""
        
        # Use LLM to extract structured information
        system_prompt = """You are a query parser for a professional networking search tool similar to happenstance.ai.
        Extract structured filters from the user's natural language query.
        
        Return a JSON object with the following structure:
        {
            "intent": "find_people|find_investors|find_alumni|find_connections",
            "filters": {
                "location": ["New York", "NYC"],
                "education": ["Yale University"],
                "company": ["Goldman Sachs"],
                "title": ["Partner", "VC", "Investor"],
                "skills": ["Machine Learning", "Python"],
                "yale_affiliation": {
                    "type": ["alumni", "undergraduate"],
                    "school": ["Yale College", "Yale SOM"],
                    "class_year_range": [2010, 2020]
                },
                "time_range": {
                    "current_only": true,
                    "min_year": 2020
                },
                "industry": ["education", "edtech", "networking"],
                "investment_focus": ["seed", "series A", "education startups"]
            },
            "keywords": ["additional", "search", "terms"]
        }
        """
        
        user_prompt = f"Parse this query: {query}"
        
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        try:
            parsed_data = json.loads(response.content)
        except:
            # Fallback to regex-based parsing
            parsed_data = self._fallback_parse(query)
            
        return self._create_parsed_query(query, parsed_data)
    
    def _fallback_parse(self, query: str) -> Dict[str, Any]:
        """Fallback regex-based parsing if LLM fails"""
        filters = {
            "intent": "find_people",
            "filters": {},
            "keywords": []
        }
        
        # Detect intent
        if any(term in query.lower() for term in ["investor", "vc", "venture", "fund"]):
            filters["intent"] = "find_investors"
        elif "alumni" in query.lower() or "alum" in query.lower():
            filters["intent"] = "find_alumni"
            
        # Extract locations
        locations = []
        for pattern in self.location_patterns:
            if pattern.lower() in query.lower():
                # Extract the location after the pattern
                match = re.search(f"{pattern}\\s+([A-Za-z\\s,]+)", query, re.IGNORECASE)
                if match:
                    locations.append(match.group(1).strip())
        
        if locations:
            filters["filters"]["location"] = locations
            
        # Extract education
        educations = []
        for pattern in self.education_patterns:
            if pattern in query:
                educations.append(pattern)
        
        if educations:
            filters["filters"]["education"] = educations
            
        # Extract titles/roles
        if any(term in query.lower() for term in self.investor_patterns):
            filters["filters"]["title"] = [
                term for term in self.investor_patterns 
                if term in query.lower()
            ]
            
        return filters
    
    def _create_parsed_query(self, query: str, parsed_data: Dict) -> ParsedQuery:
        """Convert parsed data into ParsedQuery object"""
        filters = []
        
        filter_data = parsed_data.get("filters", {})
        
        # Location filters
        if "location" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.LOCATION,
                values=filter_data["location"]
            ))
            
        # Education filters
        if "education" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.EDUCATION,
                values=filter_data["education"]
            ))
            
        # Title filters
        if "title" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.TITLE,
                values=filter_data["title"]
            ))
            
        # Company filters
        if "company" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.COMPANY,
                values=filter_data["company"]
            ))
            
        # Yale affiliation filters
        if "yale_affiliation" in filter_data:
            yale_data = filter_data["yale_affiliation"]
            values = []
            if "type" in yale_data:
                values.extend(yale_data["type"])
            if "school" in yale_data:
                values.extend(yale_data["school"])
            if values:
                filters.append(SearchFilter(
                    filter_type=FilterType.YALE_AFFILIATION,
                    values=values
                ))
                
        # Industry/Investment focus
        if "industry" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.INDUSTRY,
                values=filter_data["industry"]
            ))
            
        if "investment_focus" in filter_data:
            filters.append(SearchFilter(
                filter_type=FilterType.INVESTMENT_FOCUS,
                values=filter_data["investment_focus"]
            ))
        
        return ParsedQuery(
            original_query=query,
            filters=filters,
            keywords=parsed_data.get("keywords", []),
            intent=parsed_data.get("intent", "find_people")
        )
    
    def generate_explanation(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Generate a user-friendly explanation of the search filters"""
        explanation = {
            "filters": {},
            "key_phrases": []
        }
        
        for filter in parsed_query.filters:
            if filter.filter_type == FilterType.LOCATION:
                explanation["filters"]["Location"] = filter.values
                explanation["key_phrases"].extend([
                    f"Based in {loc}" for loc in filter.values
                ])
                
            elif filter.filter_type == FilterType.EDUCATION:
                explanation["filters"]["Education"] = filter.values
                explanation["key_phrases"].extend([
                    f"Attended {edu}" for edu in filter.values
                ])
                
            elif filter.filter_type == FilterType.TITLE:
                explanation["filters"]["Title/Role"] = filter.values
                explanation["key_phrases"].extend([
                    f"Works as {title}" for title in filter.values
                ])
                
            elif filter.filter_type == FilterType.YALE_AFFILIATION:
                explanation["filters"]["Yale Affiliation"] = filter.values
                explanation["key_phrases"].extend([
                    f"Yale {aff}" for aff in filter.values
                ])
                
            elif filter.filter_type == FilterType.INDUSTRY:
                explanation["filters"]["Industry Focus"] = filter.values
                explanation["key_phrases"].extend([
                    f"In {ind} industry" for ind in filter.values
                ])
                
            elif filter.filter_type == FilterType.INVESTMENT_FOCUS:
                explanation["filters"]["Investment Focus"] = filter.values
                explanation["key_phrases"].extend([
                    f"Invests in {focus}" for focus in filter.values
                ])
                
        return explanation