"""
Enhanced query parser that extracts hybrid query components:
- Natural language → structured intent
- Embedding generation  
- Hard filters extraction
- Graph constraints detection
- Ranking weight optimization
"""

import re
import json
import openai
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

from .hybrid_query import (
    HybridQuery, StructuredFilter, FilterOperator, 
    GraphConstraint, RankingWeights
)

logger = logging.getLogger(__name__)


class EnhancedQueryParser:
    """Advanced query parser implementing happenstance.ai style parsing"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        # Location normalization mapping
        self.location_mappings = {
            'nyc': ['new york', 'manhattan', 'brooklyn', 'queens', 'bronx', 'new york city'],
            'new york': ['ny', 'nyc', 'manhattan', 'new york city'],
            'san francisco': ['sf', 'bay area', 'palo alto', 'silicon valley'],
            'boston': ['cambridge', 'somerville', 'greater boston'],
            'washington dc': ['dc', 'd.c.', 'dmv', 'virginia', 'maryland'],
            'los angeles': ['la', 'hollywood', 'santa monica', 'california'],
            'connecticut': ['ct', 'new haven', 'hartford', 'stamford'],
        }
        
        # Title/role synonyms
        self.title_mappings = {
            'product manager': ['pm', 'product lead', 'product owner'],
            'venture capital': ['vc', 'venture partner', 'general partner', 'managing partner'],
            'investor': ['angel investor', 'investment partner', 'principal'],
            'founder': ['co-founder', 'ceo', 'chief executive', 'entrepreneur'],
            'software engineer': ['swe', 'engineer', 'developer', 'programmer'],
            'consultant': ['consulting', 'advisor', 'strategy consultant'],
            'professor': ['faculty', 'academic', 'lecturer', 'researcher'],
            'lawyer': ['attorney', 'counsel', 'legal advisor'],
            'doctor': ['physician', 'md', 'medical doctor'],
        }
        
        # Industry keywords
        self.industry_mappings = {
            'fintech': ['financial technology', 'payments', 'banking technology'],
            'edtech': ['education technology', 'learning platforms', 'online education'],
            'healthcare': ['healthtech', 'medical', 'pharma', 'biotech'],
            'artificial intelligence': ['ai', 'machine learning', 'ml', 'deep learning'],
            'sustainability': ['clean energy', 'climate tech', 'renewable energy'],
            'real estate': ['proptech', 'property technology', 'real estate tech'],
        }
        
        # Yale-specific patterns
        self.yale_patterns = {
            'schools': {
                'yale college': ['yc', 'yale undergraduate'],
                'yale som': ['school of management', 'business school'],
                'yale law school': ['yls', 'law school'],
                'yale medical school': ['yale medicine', 'medical school'],
                'yale school of public health': ['ysph', 'public health'],
                'yale divinity school': ['yds', 'divinity'],
                'yale school of art': ['art school'],
                'yale school of music': ['music school'],
            },
            'affiliations': ['alumni', 'alum', 'graduate', 'student', 'faculty', 'professor'],
            'class_year_patterns': [
                r"class of (\d{4})",
                r"'(\d{2})",
                r"(\d{4}) graduate",
                r"graduated (\d{4})"
            ]
        }
    
    def parse_query(self, raw_query: str, user_context: Dict[str, Any] = None) -> HybridQuery:
        """
        Parse natural language query into complete HybridQuery
        
        Example: "Fintech PMs in NYC who went to Stanford, within 2 hops of me"
        Returns hybrid query with embedding, filters, graph constraints, ranking weights
        """
        
        # Create base query object
        query = HybridQuery(raw_query=raw_query)
        
        # Step 1: Generate embedding for semantic search
        query.embedding = self._generate_embedding(raw_query)
        
        # Step 2: Extract structured intent using LLM
        parsed_intent = self._extract_structured_intent(raw_query)
        query.intent = parsed_intent.get('intent', 'find_people')
        query.confidence = parsed_intent.get('confidence', 0.0)
        query.parsed_entities = parsed_intent.get('entities', {})
        
        # Step 3: Extract hard filters
        self._extract_filters(query, parsed_intent)
        
        # Step 4: Detect graph constraints
        self._extract_graph_constraints(query, parsed_intent, user_context)
        
        # Step 5: Optimize ranking weights based on query type
        self._optimize_ranking_weights(query, parsed_intent)
        
        return query
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate OpenAI embedding for semantic search"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return []
    
    def _extract_structured_intent(self, query: str) -> Dict[str, Any]:
        """Use LLM to extract structured intent from natural language"""
        
        system_prompt = """You are an expert query parser for a professional networking platform like happenstance.ai.
        
        Parse the user's natural language query and extract structured information.
        
        Return JSON with this exact structure:
        {
            "intent": "find_people|find_investors|find_alumni|find_connections",
            "confidence": 0.85,
            "entities": {
                "locations": ["New York", "NYC"],
                "titles": ["Product Manager", "PM"],
                "companies": ["Goldman Sachs", "McKinsey"],
                "schools": ["Stanford University", "Yale University"],
                "industries": ["Fintech", "Healthcare"],
                "yale_specific": {
                    "schools": ["Yale SOM", "Yale College"],
                    "affiliations": ["alumni", "undergraduate"],
                    "class_years": [2015, 2020]
                },
                "connection_constraints": {
                    "max_hops": 2,
                    "connection_types": ["direct", "mutual"]
                },
                "temporal": {
                    "current_only": true,
                    "recent_activity": false
                }
            },
            "ranking_hints": {
                "prioritize_embedding": false,
                "prioritize_filters": true,
                "prioritize_yale_connections": true
            }
        }
        
        Extract as much structured information as possible. Be precise with location and title normalization."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Parse this query: {query}"}
                ],
                temperature=0
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"LLM parsing failed: {e}")
            return self._fallback_regex_parse(query)
    
    def _fallback_regex_parse(self, query: str) -> Dict[str, Any]:
        """Regex-based fallback parsing"""
        query_lower = query.lower()
        
        result = {
            "intent": "find_people",
            "confidence": 0.6,
            "entities": {},
            "ranking_hints": {}
        }
        
        # Detect intent
        if any(term in query_lower for term in ['investor', 'vc', 'venture', 'fund']):
            result["intent"] = "find_investors"
        elif any(term in query_lower for term in ['alumni', 'alum', 'graduated']):
            result["intent"] = "find_alumni"
        
        # Extract locations
        locations = []
        for canonical, variants in self.location_mappings.items():
            if any(variant in query_lower for variant in variants + [canonical]):
                locations.append(canonical.title())
        
        # Extract titles
        titles = []
        for canonical, variants in self.title_mappings.items():
            if any(variant in query_lower for variant in variants + [canonical]):
                titles.append(canonical.title())
        
        # Extract Yale info
        yale_info = {}
        for school, variants in self.yale_patterns['schools'].items():
            if any(variant in query_lower for variant in variants + [school]):
                if 'schools' not in yale_info:
                    yale_info['schools'] = []
                yale_info['schools'].append(school.title())
        
        # Extract class years
        for pattern in self.yale_patterns['class_year_patterns']:
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                if 'class_years' not in yale_info:
                    yale_info['class_years'] = []
                for match in matches:
                    try:
                        year = int(match) if len(match) == 4 else 2000 + int(match)
                        yale_info['class_years'].append(year)
                    except ValueError:
                        pass
        
        # Build entities
        if locations:
            result["entities"]["locations"] = locations
        if titles:
            result["entities"]["titles"] = titles
        if yale_info:
            result["entities"]["yale_specific"] = yale_info
        
        # Extract graph constraints
        hops_match = re.search(r'(\d+)\s*hops?', query_lower)
        if hops_match:
            result["entities"]["connection_constraints"] = {
                "max_hops": int(hops_match.group(1))
            }
        
        return result
    
    def _extract_filters(self, query: HybridQuery, parsed_intent: Dict[str, Any]):
        """Extract hard constraint filters"""
        entities = parsed_intent.get('entities', {})
        
        # Location filters
        if 'locations' in entities:
            expanded_locations = []
            for loc in entities['locations']:
                expanded_locations.append(loc)
                # Add variants
                loc_lower = loc.lower()
                if loc_lower in self.location_mappings:
                    expanded_locations.extend(self.location_mappings[loc_lower])
            
            query.filters.append(StructuredFilter(
                field="p.location",
                operator=FilterOperator.IN,
                values=expanded_locations
            ))
        
        # Title filters
        if 'titles' in entities:
            expanded_titles = []
            for title in entities['titles']:
                expanded_titles.append(title)
                title_lower = title.lower()
                if title_lower in self.title_mappings:
                    expanded_titles.extend(self.title_mappings[title_lower])
            
            query.filters.append(StructuredFilter(
                field="e.title",
                operator=FilterOperator.IN,
                values=expanded_titles
            ))
        
        # Company filters
        if 'companies' in entities:
            query.filters.append(StructuredFilter(
                field="e.company",
                operator=FilterOperator.IN,
                values=entities['companies']
            ))
        
        # Education filters
        if 'schools' in entities:
            query.filters.append(StructuredFilter(
                field="ed.institution",
                operator=FilterOperator.IN,
                values=entities['schools']
            ))
        
        # Yale-specific filters
        yale_data = entities.get('yale_specific', {})
        if yale_data:
            if 'schools' in yale_data:
                query.filters.append(StructuredFilter(
                    field="ya.school",
                    operator=FilterOperator.IN,
                    values=yale_data['schools']
                ))
            
            if 'affiliations' in yale_data:
                query.filters.append(StructuredFilter(
                    field="ya.affiliation_type",
                    operator=FilterOperator.IN,
                    values=yale_data['affiliations']
                ))
            
            if 'class_years' in yale_data:
                years = yale_data['class_years']
                if len(years) == 1:
                    query.filters.append(StructuredFilter(
                        field="ya.class_year",
                        operator=FilterOperator.IN,
                        values=[years[0]]
                    ))
                elif len(years) >= 2:
                    query.filters.append(StructuredFilter(
                        field="ya.class_year",
                        operator=FilterOperator.RANGE,
                        values=(min(years), max(years))
                    ))
        
        # Industry filters
        if 'industries' in entities:
            query.filters.append(StructuredFilter(
                field="company_industry",
                operator=FilterOperator.IN,
                values=entities['industries']
            ))
        
        # Temporal filters
        temporal = entities.get('temporal', {})
        if temporal.get('current_only'):
            query.filters.append(StructuredFilter(
                field="e.is_current",
                operator=FilterOperator.IN,
                values=[True]
            ))
    
    def _extract_graph_constraints(self, query: HybridQuery, parsed_intent: Dict[str, Any], user_context: Dict[str, Any] = None):
        """Extract graph traversal constraints"""
        entities = parsed_intent.get('entities', {})
        constraints = entities.get('connection_constraints', {})
        
        if constraints or any(term in query.raw_query.lower() for term in ['hops', 'connections', 'network']):
            max_hops = constraints.get('max_hops', 2)
            connection_types = constraints.get('connection_types', ['direct', 'linkedin', 'yale'])
            
            query.graph_constraints = GraphConstraint(
                max_hops=max_hops,
                connection_types=connection_types,
                boost_yale_connections=True
            )
    
    def _optimize_ranking_weights(self, query: HybridQuery, parsed_intent: Dict[str, Any]):
        """Optimize ranking weights based on query characteristics"""
        hints = parsed_intent.get('ranking_hints', {})
        
        # Start with defaults
        weights = RankingWeights()
        
        # Adjust based on query type
        if query.intent == 'find_investors':
            # For investor queries, prioritize title/role matching
            weights.filter_match = 0.5
            weights.embedding_similarity = 0.3
            weights.yale_affinity = 0.2
            
        elif query.intent == 'find_alumni':
            # For alumni queries, prioritize Yale connections
            weights.yale_affinity = 0.4
            weights.filter_match = 0.3
            weights.embedding_similarity = 0.3
            
        elif len(query.filters) > 3:
            # Many filters = prioritize structured matching
            weights.filter_match = 0.5
            weights.embedding_similarity = 0.25
            weights.yale_affinity = 0.15
            weights.graph_proximity = 0.1
            
        elif query.graph_constraints:
            # Graph queries = boost network proximity
            weights.graph_proximity = 0.3
            weights.filter_match = 0.35
            weights.embedding_similarity = 0.25
            weights.yale_affinity = 0.1
            
        else:
            # Default semantic search
            weights.embedding_similarity = 0.45
            weights.filter_match = 0.3
            weights.yale_affinity = 0.15
            weights.graph_proximity = 0.1
        
        # Apply hints
        if hints.get('prioritize_embedding'):
            weights.embedding_similarity += 0.1
            weights.filter_match -= 0.1
        
        if hints.get('prioritize_filters'):
            weights.filter_match += 0.1
            weights.embedding_similarity -= 0.1
        
        if hints.get('prioritize_yale_connections'):
            weights.yale_affinity += 0.1
            weights.embedding_similarity -= 0.05
            weights.filter_match -= 0.05
        
        # Normalize and assign
        weights.normalize()
        query.ranking_weights = weights
    
    def explain_query_parsing(self, query: HybridQuery) -> Dict[str, Any]:
        """Generate explanation of how query was parsed"""
        return {
            "original_query": query.raw_query,
            "intent": query.intent,
            "confidence": query.confidence,
            "parsed_entities": query.parsed_entities,
            "filters_extracted": [
                {
                    "field": f.field,
                    "operator": f.operator.value,
                    "values": f.values,
                    "purpose": self._explain_filter_purpose(f)
                }
                for f in query.filters
            ],
            "graph_constraints": {
                "enabled": query.graph_constraints is not None,
                "max_hops": query.graph_constraints.max_hops if query.graph_constraints else None,
                "boost_yale": query.graph_constraints.boost_yale_connections if query.graph_constraints else None
            },
            "ranking_optimization": {
                "embedding_weight": query.ranking_weights.embedding_similarity,
                "filter_weight": query.ranking_weights.filter_match,
                "graph_weight": query.ranking_weights.graph_proximity,
                "yale_weight": query.ranking_weights.yale_affinity,
                "strategy": self._explain_ranking_strategy(query)
            },
            "embedding_dimensions": len(query.embedding) if query.embedding else 0
        }
    
    def _explain_filter_purpose(self, filter: StructuredFilter) -> str:
        """Explain what each filter does"""
        if "location" in filter.field:
            return "Geographic constraint"
        elif "title" in filter.field:
            return "Role/position constraint"
        elif "company" in filter.field:
            return "Company constraint"
        elif "institution" in filter.field:
            return "Education constraint"
        elif "ya." in filter.field:
            return "Yale affiliation constraint"
        elif "is_current" in filter.field:
            return "Current position constraint"
        else:
            return "Custom constraint"
    
    def _explain_ranking_strategy(self, query: HybridQuery) -> str:
        """Explain the ranking strategy chosen"""
        weights = query.ranking_weights
        
        if weights.filter_match > 0.4:
            return "Structured matching prioritized"
        elif weights.embedding_similarity > 0.4:
            return "Semantic similarity prioritized"
        elif weights.yale_affinity > 0.3:
            return "Yale connections prioritized"
        elif weights.graph_proximity > 0.2:
            return "Network proximity prioritized"
        else:
            return "Balanced multi-factor ranking"