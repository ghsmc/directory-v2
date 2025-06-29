"""
Hybrid search engine implementing the complete query pipeline:
1. Vector similarity search (semantic)
2. Structured filter application (hard constraints)  
3. Graph traversal (social hops)
4. Multi-factor ranking with explainability
"""

import time
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_, func
import openai

from .hybrid_query import (
    HybridQuery, SearchCandidate, QueryResult,
    FilterOperator, RankingWeights
)
from .enhanced_query_parser import EnhancedQueryParser
from ..models import (
    Person, Experience, Education, YaleAffiliation
)

logger = logging.getLogger(__name__)


class HybridSearchEngine:
    """
    Complete hybrid search engine matching happenstance.ai architecture
    
    Search Pipeline:
    1. Parse natural language → HybridQuery
    2. Vector search for semantic candidates  
    3. Apply structured filters (hard constraints)
    4. Graph traversal for connection filtering
    5. Multi-factor ranking with explainability
    """
    
    def __init__(self, db_session: Session, openai_api_key: str):
        self.db = db_session
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.query_parser = EnhancedQueryParser(openai_api_key)
        
        # Search configuration
        self.max_vector_candidates = 1000
        self.max_sql_candidates = 500
        self.vector_similarity_threshold = 0.1
        
    def search(self, raw_query: str, user_context: Dict[str, Any] = None, limit: int = 20) -> QueryResult:
        """
        Main search entry point
        
        Example: "Fintech PMs in NYC who went to Stanford, within 2 hops of me"
        
        Returns: QueryResult with ranked candidates and explainability
        """
        start_time = time.time()
        
        # Step 1: Parse query into hybrid components
        query = self.query_parser.parse_query(raw_query, user_context)
        query.max_results = limit
        
        logger.info(f"Parsed query: {query.intent} with {len(query.filters)} filters")
        
        # Step 2: Get candidate pool using hybrid approach
        candidates = self._get_hybrid_candidates(query)
        
        logger.info(f"Found {len(candidates)} candidates from hybrid search")
        
        # Step 3: Apply graph constraints if specified
        if query.graph_constraints and user_context and user_context.get('user_id'):
            candidates = self._apply_graph_constraints(candidates, query, user_context['user_id'])
            logger.info(f"After graph filtering: {len(candidates)} candidates")
        
        # Step 4: Multi-factor ranking
        ranked_candidates = self._rank_candidates(candidates, query)
        
        # Step 5: Build result
        execution_time = (time.time() - start_time) * 1000
        result = QueryResult(query, ranked_candidates)
        result.execution_time_ms = execution_time
        result.debug_info = {
            "vector_candidates": len(candidates),
            "final_candidates": len(ranked_candidates),
            "ranking_strategy": self._get_ranking_strategy(query)
        }
        
        logger.info(f"Search completed in {execution_time:.1f}ms, returning {len(ranked_candidates)} results")
        
        return result
    
    def _get_hybrid_candidates(self, query: HybridQuery) -> List[SearchCandidate]:
        """
        Get candidate pool using hybrid vector + structured search
        
        Two approaches combined:
        1. Vector similarity search (if embedding available)
        2. Structured SQL search (always)
        
        Results are deduplicated by person_id
        """
        all_candidates = {}  # person_id -> SearchCandidate
        
        # Approach 1: Vector similarity search
        if query.embedding:
            vector_candidates = self._vector_similarity_search(query)
            for candidate in vector_candidates:
                all_candidates[candidate.person_id] = candidate
            logger.info(f"Vector search found {len(vector_candidates)} candidates")
        
        # Approach 2: Structured SQL search  
        sql_candidates = self._structured_sql_search(query)
        for candidate in sql_candidates:
            if candidate.person_id in all_candidates:
                # Merge scores - take max of vector vs SQL
                existing = all_candidates[candidate.person_id]
                existing.filter_match_score = max(existing.filter_match_score, candidate.filter_match_score)
            else:
                all_candidates[candidate.person_id] = candidate
        
        logger.info(f"SQL search found {len(sql_candidates)} candidates")
        logger.info(f"Combined unique candidates: {len(all_candidates)}")
        
        return list(all_candidates.values())
    
    def _vector_similarity_search(self, query: HybridQuery) -> List[SearchCandidate]:
        """
        Semantic similarity search using embeddings
        
        Uses pgvector cosine similarity to find semantically similar profiles
        """
        if not query.embedding:
            return []
            
        try:
            # Convert embedding to postgres array format
            embedding_str = '[' + ','.join(map(str, query.embedding)) + ']'
            
            # Vector similarity query
            vector_query = text("""
                SELECT 
                    p.uuid_id,
                    p.full_name,
                    p.location,
                    p.headline,
                    p.summary,
                    p.linkedin_url,
                    pe.embedding <=> :embedding::vector as distance,
                    1 - (pe.embedding <=> :embedding::vector) as similarity
                FROM people p
                JOIN profile_embeddings pe ON pe.person_uuid = p.uuid_id
                WHERE pe.embedding IS NOT NULL
                ORDER BY pe.embedding <=> :embedding::vector
                LIMIT :limit
            """)
            
            results = self.db.execute(vector_query, {
                'embedding': embedding_str,
                'limit': self.max_vector_candidates
            }).fetchall()
            
            candidates = []
            for row in results:
                if row.similarity >= self.vector_similarity_threshold:
                    candidate = SearchCandidate(
                        person_id=str(row.uuid_id),
                        person_data={
                            'uuid_id': str(row.uuid_id),
                            'name': row.full_name,
                            'location': row.location,
                            'headline': row.headline,
                            'summary': row.summary,
                            'linkedin_url': row.linkedin_url
                        },
                        embedding_score=row.similarity
                    )
                    candidate.add_match_reason(f"Semantic similarity: {row.similarity:.2f}")
                    candidates.append(candidate)
            
            return candidates
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    def _structured_sql_search(self, query: HybridQuery) -> List[SearchCandidate]:
        """
        Structured search using hard constraint filters
        
        Builds dynamic SQL with JOINs based on filters in the query
        """
        if not query.filters:
            # If no filters, return top people (fallback)
            return self._get_fallback_candidates(query)
        
        # Build dynamic SQL query
        base_query = """
            SELECT DISTINCT
                p.uuid_id,
                p.full_name,
                p.location, 
                p.headline,
                p.summary,
                p.linkedin_url
        """
        
        from_clause = "FROM people p"
        join_clauses = []
        where_conditions = []
        params = {}
        
        # Analyze filters to determine needed JOINs
        needs_experience = any('e.' in f.field for f in query.filters)
        needs_education = any('ed.' in f.field for f in query.filters)
        needs_yale = any('ya.' in f.field for f in query.filters)
        
        # Add JOINs based on filter requirements
        if needs_experience:
            join_clauses.append("LEFT JOIN experience e ON e.person_uuid = p.uuid_id")
        
        if needs_education:
            join_clauses.append("LEFT JOIN education ed ON ed.person_uuid = p.uuid_id")
            
        if needs_yale:
            join_clauses.append("LEFT JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id")
        
        # Build WHERE conditions from filters
        param_counter = 0
        for filter in query.filters:
            condition, filter_params = self._build_filter_condition(filter, param_counter)
            if condition:
                where_conditions.append(condition)
                params.update(filter_params)
                param_counter += len(filter_params)
        
        # Construct full query
        full_query = base_query
        if join_clauses:
            full_query += "\n" + "\n".join(join_clauses)
        if where_conditions:
            full_query += "\nWHERE " + " AND ".join(where_conditions)
        
        full_query += f"\nLIMIT {self.max_sql_candidates}"
        
        logger.debug(f"SQL Query: {full_query}")
        logger.debug(f"Params: {params}")
        
        try:
            results = self.db.execute(text(full_query), params).fetchall()
            
            candidates = []
            for row in results:
                candidate = SearchCandidate(
                    person_id=str(row.uuid_id),
                    person_data={
                        'uuid_id': str(row.uuid_id),
                        'name': row.full_name,
                        'location': row.location,
                        'headline': row.headline,
                        'summary': row.summary,
                        'linkedin_url': row.linkedin_url
                    },
                    filter_match_score=1.0  # Perfect filter match
                )
                
                # Add match reasons based on filters
                self._add_filter_match_reasons(candidate, query.filters)
                candidates.append(candidate)
            
            return candidates
            
        except Exception as e:
            logger.error(f"SQL search failed: {e}")
            return []
    
    def _build_filter_condition(self, filter, param_offset: int) -> Tuple[str, Dict[str, Any]]:
        """Build SQL WHERE condition from StructuredFilter"""
        params = {}
        
        if filter.operator == FilterOperator.IN:
            if not filter.values:
                return "", {}
            
            # Handle case-insensitive matching for text fields
            if filter.field in ['p.location', 'e.title', 'e.company', 'ed.institution']:
                placeholders = []
                for i, value in enumerate(filter.values):
                    param_name = f"param_{param_offset + i}"
                    params[param_name] = f"%{value}%"
                    placeholders.append(f"LOWER({filter.field}) LIKE LOWER(:{param_name})")
                condition = f"({' OR '.join(placeholders)})"
            else:
                # Exact matching for other fields
                placeholders = []
                for i, value in enumerate(filter.values):
                    param_name = f"param_{param_offset + i}"
                    params[param_name] = value
                    placeholders.append(f":{param_name}")
                condition = f"{filter.field} IN ({','.join(placeholders)})"
                
        elif filter.operator == FilterOperator.RANGE:
            min_val, max_val = filter.values
            min_param = f"param_{param_offset}"
            max_param = f"param_{param_offset + 1}"
            params[min_param] = min_val
            params[max_param] = max_val
            condition = f"{filter.field} BETWEEN :{min_param} AND :{max_param}"
            
        else:
            # Default equality
            param_name = f"param_{param_offset}"
            params[param_name] = filter.values
            condition = f"{filter.field} = :{param_name}"
        
        if filter.negated:
            condition = f"NOT ({condition})"
            
        return condition, params
    
    def _add_filter_match_reasons(self, candidate: SearchCandidate, filters: List):
        """Add match reasons based on which filters were satisfied"""
        for filter in filters:
            if "location" in filter.field:
                candidate.add_match_reason(f"Location matches: {', '.join(filter.values[:2])}")
                candidate.add_matched_filter("location", filter.values)
            elif "title" in filter.field:
                candidate.add_match_reason(f"Title matches: {', '.join(filter.values[:2])}")
                candidate.add_matched_filter("title", filter.values)
            elif "company" in filter.field:
                candidate.add_match_reason(f"Company matches: {', '.join(filter.values[:2])}")
                candidate.add_matched_filter("company", filter.values)
            elif "ya.school" in filter.field:
                candidate.add_match_reason(f"Yale school: {', '.join(filter.values[:2])}")
                candidate.add_matched_filter("yale_school", filter.values)
            elif "ya.affiliation_type" in filter.field:
                candidate.add_match_reason(f"Yale affiliation: {', '.join(filter.values[:2])}")
                candidate.add_matched_filter("yale_affiliation", filter.values)
    
    def _get_fallback_candidates(self, query: HybridQuery) -> List[SearchCandidate]:
        """Fallback when no filters - return recent Yale people"""
        fallback_query = text("""
            SELECT DISTINCT
                p.uuid_id,
                p.full_name,
                p.location,
                p.headline,
                p.summary,
                p.linkedin_url
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            ORDER BY p.created_at DESC
            LIMIT :limit
        """)
        
        results = self.db.execute(fallback_query, {'limit': self.max_sql_candidates}).fetchall()
        
        candidates = []
        for row in results:
            candidate = SearchCandidate(
                person_id=str(row.uuid_id),
                person_data={
                    'uuid_id': str(row.uuid_id),
                    'name': row.full_name,
                    'location': row.location,
                    'headline': row.headline,
                    'summary': row.summary,
                    'linkedin_url': row.linkedin_url
                },
                filter_match_score=0.5
            )
            candidate.add_match_reason("Recent Yale person")
            candidates.append(candidate)
        
        return candidates
    
    def _apply_graph_constraints(self, candidates: List[SearchCandidate], 
                               query: HybridQuery, user_id: str) -> List[SearchCandidate]:
        """
        Apply graph traversal constraints (social hops)
        
        Filters candidates to only those within specified connection distance
        """
        if not query.graph_constraints:
            return candidates
        
        max_hops = query.graph_constraints.max_hops
        
        # Get user's connection network within max_hops
        connected_person_ids = self._get_connected_people(user_id, max_hops)
        
        # Filter candidates to only connected people
        filtered_candidates = []
        for candidate in candidates:
            if candidate.person_id in connected_person_ids:
                # Add graph proximity score
                hops = connected_person_ids[candidate.person_id]
                candidate.graph_proximity_score = 1.0 / hops  # Closer = higher score
                candidate.add_match_reason(f"Connected via {hops} hop{'s' if hops > 1 else ''}")
                filtered_candidates.append(candidate)
        
        return filtered_candidates
    
    def _get_connected_people(self, user_id: str, max_hops: int) -> Dict[str, int]:
        """
        Get all people connected within max_hops distance
        
        Returns: {person_id: hop_distance}
        """
        # This would typically use a graph database or precomputed connection table
        # For now, implement simple 1-2 hop logic with SQL
        
        connections = {}
        
        try:
            # Direct connections (1 hop)
            direct_query = text("""
                SELECT connected_person_uuid, 1 as hops
                FROM connections 
                WHERE person_uuid = :user_id
                UNION
                SELECT person_uuid, 1 as hops  
                FROM connections
                WHERE connected_person_uuid = :user_id
            """)
            
            direct_results = self.db.execute(direct_query, {'user_id': user_id}).fetchall()
            for row in direct_results:
                connections[str(row.connected_person_uuid)] = row.hops
            
            # Second-degree connections (2 hops) if needed
            if max_hops >= 2 and direct_results:
                direct_ids = [str(r.connected_person_uuid) for r in direct_results]
                if direct_ids:
                    second_degree_query = text("""
                        SELECT DISTINCT c2.connected_person_uuid, 2 as hops
                        FROM connections c2
                        WHERE c2.person_uuid = ANY(:direct_ids)
                        AND c2.connected_person_uuid != :user_id
                        AND c2.connected_person_uuid NOT IN :existing_connections
                    """)
                    
                    second_results = self.db.execute(second_degree_query, {
                        'direct_ids': direct_ids,
                        'user_id': user_id,
                        'existing_connections': tuple(connections.keys()) if connections else ('',)
                    }).fetchall()
                    
                    for row in second_results:
                        if str(row.connected_person_uuid) not in connections:
                            connections[str(row.connected_person_uuid)] = row.hops
            
        except Exception as e:
            logger.error(f"Graph traversal failed: {e}")
        
        return connections
    
    def _rank_candidates(self, candidates: List[SearchCandidate], query: HybridQuery) -> List[SearchCandidate]:
        """
        Multi-factor ranking with explainability
        
        Combines scores from all dimensions using configurable weights
        """
        for candidate in candidates:
            # Calculate individual dimension scores
            self._calculate_dimension_scores(candidate, query)
            
            # Calculate final weighted score
            candidate.calculate_final_score(query.ranking_weights)
        
        # Sort by final score
        candidates.sort(key=lambda c: c.final_score, reverse=True)
        
        return candidates
    
    def _calculate_dimension_scores(self, candidate: SearchCandidate, query: HybridQuery):
        """Calculate scores for each ranking dimension"""
        
        # Yale affinity score
        candidate.yale_affinity_score = self._calculate_yale_affinity(candidate, query)
        
        # Recency score (based on profile freshness)
        candidate.recency_score = 0.8  # Default - could calculate from last update
        
        # Completeness score (based on profile completeness)  
        candidate.completeness_score = self._calculate_completeness_score(candidate)
    
    def _calculate_yale_affinity(self, candidate: SearchCandidate, query: HybridQuery) -> float:
        """Calculate Yale affinity score"""
        # Check if person has Yale affiliation
        yale_query = text("""
            SELECT COUNT(*) as yale_count
            FROM yale_affiliations ya
            WHERE ya.person_uuid = :person_id
        """)
        
        result = self.db.execute(yale_query, {'person_id': candidate.person_id}).fetchone()
        
        if result and result.yale_count > 0:
            return 1.0
        else:
            return 0.0
    
    def _calculate_completeness_score(self, candidate: SearchCandidate) -> float:
        """Calculate profile completeness score"""
        person_data = candidate.person_data
        score = 0.0
        
        # Basic info
        if person_data.get('name'):
            score += 0.2
        if person_data.get('location'):
            score += 0.2
        if person_data.get('headline'):
            score += 0.3
        if person_data.get('summary'):
            score += 0.2
        if person_data.get('linkedin_url'):
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_ranking_strategy(self, query: HybridQuery) -> str:
        """Get human-readable ranking strategy"""
        weights = query.ranking_weights
        
        if weights.filter_match > 0.4:
            return "structured_priority"
        elif weights.embedding_similarity > 0.4:
            return "semantic_priority"  
        elif weights.yale_affinity > 0.3:
            return "yale_priority"
        elif weights.graph_proximity > 0.2:
            return "network_priority"
        else:
            return "balanced"