"""
Hybrid query model implementing the full query shape:
- Embedding vector (dense)
- Structured filters (hard constraints) 
- Graph traversal constraints (social hops)
- Ranking weights (multi-factor scoring)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import numpy as np
from pydantic import BaseModel


class FilterOperator(Enum):
    """Filter operators for combining conditions"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IN = "IN"
    RANGE = "RANGE"


class RankingDimension(Enum):
    """Dimensions for multi-factor ranking"""
    EMBEDDING_SIMILARITY = "embedding_similarity"
    FILTER_MATCH = "filter_match" 
    GRAPH_PROXIMITY = "graph_proximity"
    YALE_AFFINITY = "yale_affinity"
    RECENCY = "recency"
    COMPLETENESS = "completeness"


@dataclass
class StructuredFilter:
    """Hard constraint filter with operator and values"""
    field: str
    operator: FilterOperator
    values: Union[List[str], str, int, tuple]
    negated: bool = False
    
    def to_sql_condition(self) -> str:
        """Convert to SQL WHERE condition"""
        if self.operator == FilterOperator.IN:
            values_str = "', '".join(str(v) for v in self.values)
            condition = f"{self.field} IN ('{values_str}')"
        elif self.operator == FilterOperator.RANGE:
            min_val, max_val = self.values
            condition = f"{self.field} BETWEEN {min_val} AND {max_val}"
        else:
            condition = f"{self.field} = '{self.values}'"
            
        return f"NOT ({condition})" if self.negated else condition


@dataclass 
class GraphConstraint:
    """Graph traversal constraints for social hops"""
    max_hops: int = 2
    min_connection_strength: float = 0.1
    include_mutual_connections: bool = True
    connection_types: List[str] = field(default_factory=lambda: ["direct", "linkedin", "yale"])
    boost_yale_connections: bool = True


@dataclass
class RankingWeights:
    """Configurable weights for multi-factor ranking"""
    embedding_similarity: float = 0.4
    filter_match: float = 0.3
    graph_proximity: float = 0.15
    yale_affinity: float = 0.1
    recency: float = 0.03
    completeness: float = 0.02
    
    def normalize(self):
        """Ensure weights sum to 1.0"""
        total = sum([
            self.embedding_similarity, self.filter_match, self.graph_proximity,
            self.yale_affinity, self.recency, self.completeness
        ])
        if total > 0:
            self.embedding_similarity /= total
            self.filter_match /= total
            self.graph_proximity /= total
            self.yale_affinity /= total
            self.recency /= total
            self.completeness /= total


class HybridQuery(BaseModel):
    """Complete hybrid query model matching happenstance.ai architecture"""
    
    # Original user input
    raw_query: str
    
    # Dense vector for semantic similarity
    embedding: Optional[List[float]] = None
    
    # Hard constraints (structured filters)
    filters: List[StructuredFilter] = []
    
    # Graph traversal rules
    graph_constraints: Optional[GraphConstraint] = None
    
    # Multi-factor ranking configuration
    ranking_weights: RankingWeights = field(default_factory=RankingWeights)
    
    # Query metadata
    intent: str = "find_people"  # find_people, find_investors, find_alumni
    confidence: float = 0.0
    parsed_entities: Dict[str, List[str]] = {}
    
    # Search configuration
    max_results: int = 50
    include_explanation: bool = True
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_location_filter(self, locations: List[str]):
        """Add location constraint"""
        self.filters.append(StructuredFilter(
            field="location",
            operator=FilterOperator.IN,
            values=locations
        ))
    
    def add_title_filter(self, titles: List[str]):
        """Add title/role constraint"""
        self.filters.append(StructuredFilter(
            field="title", 
            operator=FilterOperator.IN,
            values=titles
        ))
    
    def add_education_filter(self, institutions: List[str]):
        """Add education constraint"""
        self.filters.append(StructuredFilter(
            field="institution",
            operator=FilterOperator.IN, 
            values=institutions
        ))
    
    def add_yale_filter(self, schools: List[str] = None, 
                       affiliation_types: List[str] = None,
                       class_year_range: tuple = None):
        """Add Yale-specific constraints"""
        if schools:
            self.filters.append(StructuredFilter(
                field="ya.school",
                operator=FilterOperator.IN,
                values=schools
            ))
        
        if affiliation_types:
            self.filters.append(StructuredFilter(
                field="ya.affiliation_type", 
                operator=FilterOperator.IN,
                values=affiliation_types
            ))
            
        if class_year_range:
            self.filters.append(StructuredFilter(
                field="ya.class_year",
                operator=FilterOperator.RANGE,
                values=class_year_range
            ))
    
    def add_industry_filter(self, industries: List[str]):
        """Add industry constraint via experience/company matching"""
        self.filters.append(StructuredFilter(
            field="company_industry", 
            operator=FilterOperator.IN,
            values=industries
        ))
    
    def set_graph_constraints(self, max_hops: int = 2, 
                            user_id: str = None,
                            boost_yale: bool = True):
        """Configure graph traversal constraints"""
        self.graph_constraints = GraphConstraint(
            max_hops=max_hops,
            boost_yale_connections=boost_yale
        )
        if user_id:
            self.graph_constraints.source_user_id = user_id
    
    def adjust_ranking_weights(self, **weights):
        """Adjust ranking weights for query optimization"""
        for dimension, weight in weights.items():
            if hasattr(self.ranking_weights, dimension):
                setattr(self.ranking_weights, dimension, weight)
        self.ranking_weights.normalize()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging/debugging"""
        return {
            "raw_query": self.raw_query,
            "embedding_dimensions": len(self.embedding) if self.embedding else 0,
            "filter_count": len(self.filters),
            "filters": [
                {
                    "field": f.field,
                    "operator": f.operator.value,
                    "values": f.values,
                    "negated": f.negated
                } for f in self.filters
            ],
            "graph_constraints": {
                "max_hops": self.graph_constraints.max_hops if self.graph_constraints else None,
                "boost_yale": self.graph_constraints.boost_yale_connections if self.graph_constraints else None
            },
            "ranking_weights": {
                "embedding_similarity": self.ranking_weights.embedding_similarity,
                "filter_match": self.ranking_weights.filter_match,
                "graph_proximity": self.ranking_weights.graph_proximity,
                "yale_affinity": self.ranking_weights.yale_affinity
            },
            "intent": self.intent,
            "confidence": self.confidence
        }


@dataclass
class SearchCandidate:
    """Individual search result with multi-factor scoring"""
    person_id: str
    person_data: Dict[str, Any]
    
    # Individual scores by dimension
    embedding_score: float = 0.0
    filter_match_score: float = 0.0  
    graph_proximity_score: float = 0.0
    yale_affinity_score: float = 0.0
    recency_score: float = 0.0
    completeness_score: float = 0.0
    
    # Combined final score
    final_score: float = 0.0
    
    # Explainability
    match_reasons: List[str] = field(default_factory=list)
    matched_filters: Dict[str, List[str]] = field(default_factory=dict)
    score_breakdown: Dict[str, float] = field(default_factory=dict)
    
    def calculate_final_score(self, weights: RankingWeights) -> float:
        """Calculate weighted final score"""
        self.final_score = (
            weights.embedding_similarity * self.embedding_score +
            weights.filter_match * self.filter_match_score +
            weights.graph_proximity * self.graph_proximity_score +
            weights.yale_affinity * self.yale_affinity_score +
            weights.recency * self.recency_score +
            weights.completeness * self.completeness_score
        )
        
        # Store breakdown for explainability
        self.score_breakdown = {
            "embedding_similarity": weights.embedding_similarity * self.embedding_score,
            "filter_match": weights.filter_match * self.filter_match_score,
            "graph_proximity": weights.graph_proximity * self.graph_proximity_score,
            "yale_affinity": weights.yale_affinity * self.yale_affinity_score,
            "recency": weights.recency * self.recency_score,
            "completeness": weights.completeness * self.completeness_score,
            "total": self.final_score
        }
        
        return self.final_score
    
    def add_match_reason(self, reason: str):
        """Add explanation for why this person matched"""
        self.match_reasons.append(reason)
    
    def add_matched_filter(self, filter_type: str, values: List[str]):
        """Track which filter values matched"""
        if filter_type not in self.matched_filters:
            self.matched_filters[filter_type] = []
        self.matched_filters[filter_type].extend(values)


class QueryResult:
    """Complete search result with candidates and metadata"""
    
    def __init__(self, query: HybridQuery, candidates: List[SearchCandidate]):
        self.query = query
        self.candidates = candidates
        self.total_results = len(candidates)
        self.execution_time_ms: Optional[float] = None
        self.debug_info: Dict[str, Any] = {}
    
    def sort_by_score(self):
        """Sort candidates by final score descending"""
        self.candidates.sort(key=lambda c: c.final_score, reverse=True)
    
    def get_top_results(self, limit: int = 20) -> List[SearchCandidate]:
        """Get top N results"""
        return self.candidates[:limit]
    
    def to_response_dict(self) -> Dict[str, Any]:
        """Convert to API response format"""
        return {
            "query": self.query.raw_query,
            "total_results": self.total_results,
            "execution_time_ms": self.execution_time_ms,
            "query_analysis": {
                "intent": self.query.intent,
                "confidence": self.query.confidence,
                "parsed_entities": self.query.parsed_entities,
                "filter_count": len(self.query.filters),
                "has_embedding": self.query.embedding is not None,
                "has_graph_constraints": self.query.graph_constraints is not None
            },
            "ranking_weights": {
                "embedding_similarity": self.query.ranking_weights.embedding_similarity,
                "filter_match": self.query.ranking_weights.filter_match,
                "graph_proximity": self.query.ranking_weights.graph_proximity,
                "yale_affinity": self.query.ranking_weights.yale_affinity
            },
            "results": [
                {
                    "person_id": c.person_id,
                    "person": c.person_data,
                    "score": c.final_score,
                    "match_reasons": c.match_reasons,
                    "matched_filters": c.matched_filters,
                    "score_breakdown": c.score_breakdown if self.query.include_explanation else None
                }
                for c in self.get_top_results(self.query.max_results)
            ]
        }