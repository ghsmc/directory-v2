from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, date

from .query_parser import ParsedQuery, SearchFilter, FilterType


class SQLGenerator:
    """Generate SQL queries from parsed search queries like happenstance.ai"""
    
    def __init__(self):
        self.base_query = """
        SELECT DISTINCT
            p.uuid_id,
            p.full_name,
            p.email,
            p.location,
            p.headline,
            p.summary,
            p.linkedin_url,
            p.twitter_handle,
            -- Current position
            current_exp.company,
            current_exp.title as current_title,
            -- Education
            yale_edu.institution as yale_institution,
            yale_edu.degree as yale_degree,
            yale_edu.field_of_study,
            yale_edu.date_from as yale_start,
            yale_edu.date_to as yale_end,
            -- Yale affiliations
            ya.affiliation_type,
            ya.school as yale_school,
            ya.class_year,
            -- Scoring
            {score_calculation} as relevance_score
        FROM people p
        {joins}
        WHERE 1=1
        {where_clauses}
        {group_by}
        {order_by}
        LIMIT :limit OFFSET :offset
        """
        
    def generate_sql(self, parsed_query: ParsedQuery, 
                    user_id: Optional[str] = None,
                    include_connections: bool = True,
                    limit: int = 50,
                    offset: int = 0) -> Tuple[str, Dict[str, Any]]:
        """Generate SQL query from parsed query"""
        
        joins = []
        where_clauses = []
        score_parts = []
        params = {
            "limit": limit,
            "offset": offset
        }
        
        # Always join current experience
        joins.append("""
        LEFT JOIN LATERAL (
            SELECT e.* FROM experience e 
            WHERE e.person_uuid = p.uuid_id 
            AND e.is_current = TRUE 
            ORDER BY e.date_from DESC 
            LIMIT 1
        ) current_exp ON TRUE
        """)
        
        # Join Yale education if needed
        if any(f.filter_type in [FilterType.EDUCATION, FilterType.YALE_AFFILIATION] 
               for f in parsed_query.filters):
            joins.append("""
            LEFT JOIN LATERAL (
                SELECT ed.* FROM education ed 
                WHERE ed.person_uuid = p.uuid_id 
                AND ed.institution LIKE '%Yale%'
                ORDER BY ed.date_from DESC 
                LIMIT 1
            ) yale_edu ON TRUE
            """)
            
            joins.append("""
            LEFT JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            """)
        
        # Build WHERE clauses for each filter
        for i, filter in enumerate(parsed_query.filters):
            clause, filter_params = self._build_filter_clause(filter, i)
            if clause:
                where_clauses.append(clause)
                params.update(filter_params)
                
        # Add keyword search if present
        if parsed_query.keywords:
            keyword_clause, keyword_params = self._build_keyword_clause(
                parsed_query.keywords
            )
            where_clauses.append(keyword_clause)
            params.update(keyword_params)
            
        # Build scoring calculation
        score_calculation = self._build_score_calculation(parsed_query)
        
        # Construct final query
        sql = self.base_query.format(
            score_calculation=score_calculation,
            joins="\n".join(joins),
            where_clauses="\nAND ".join(where_clauses) if where_clauses else "",
            group_by="GROUP BY p.uuid_id, current_exp.company, current_exp.title, yale_edu.institution, yale_edu.degree, yale_edu.field_of_study, yale_edu.date_from, yale_edu.date_to, ya.affiliation_type, ya.school, ya.class_year",
            order_by="ORDER BY relevance_score DESC"
        )
        
        return sql, params
    
    def _build_filter_clause(self, filter: SearchFilter, index: int) -> Tuple[str, Dict]:
        """Build WHERE clause for a single filter"""
        
        if filter.filter_type == FilterType.LOCATION:
            # Handle location search
            location_conditions = []
            params = {}
            
            for i, location in enumerate(filter.values):
                param_name = f"location_{index}_{i}"
                location_conditions.append(f"p.location ILIKE :{param_name}")
                params[param_name] = f"%{location}%"
                
            clause = f"({' OR '.join(location_conditions)})"
            return clause, params
            
        elif filter.filter_type == FilterType.EDUCATION:
            # Search in education history
            edu_conditions = []
            params = {}
            
            joins = """
            EXISTS (
                SELECT 1 FROM education ed 
                WHERE ed.person_uuid = p.uuid_id 
                AND ({conditions})
            )
            """
            
            for i, edu in enumerate(filter.values):
                param_name = f"education_{index}_{i}"
                edu_conditions.append(f"ed.institution ILIKE :{param_name}")
                params[param_name] = f"%{edu}%"
                
            clause = joins.format(conditions=' OR '.join(edu_conditions))
            return clause, params
            
        elif filter.filter_type == FilterType.TITLE:
            # Search current and past titles
            title_conditions = []
            params = {}
            
            for i, title in enumerate(filter.values):
                param_name = f"title_{index}_{i}"
                # Search in current position
                title_conditions.append(f"current_exp.title ILIKE :{param_name}")
                # Also search in all experiences
                title_conditions.append(f"""
                    EXISTS (
                        SELECT 1 FROM experience e 
                        WHERE e.person_uuid = p.uuid_id 
                        AND e.title ILIKE :{param_name}
                    )
                """)
                params[param_name] = f"%{title}%"
                
            clause = f"({' OR '.join(title_conditions)})"
            return clause, params
            
        elif filter.filter_type == FilterType.COMPANY:
            # Search in company history
            company_conditions = []
            params = {}
            
            for i, company in enumerate(filter.values):
                param_name = f"company_{index}_{i}"
                company_conditions.append(f"""
                    EXISTS (
                        SELECT 1 FROM experience e 
                        WHERE e.person_uuid = p.uuid_id 
                        AND e.company ILIKE :{param_name}
                    )
                """)
                params[param_name] = f"%{company}%"
                
            clause = f"({' OR '.join(company_conditions)})"
            return clause, params
            
        elif filter.filter_type == FilterType.YALE_AFFILIATION:
            # Search Yale-specific affiliations
            yale_conditions = []
            params = {}
            
            for i, affiliation in enumerate(filter.values):
                param_name = f"yale_aff_{index}_{i}"
                
                # Check different affiliation types
                if affiliation.lower() in ["alumni", "undergraduate", "graduate"]:
                    yale_conditions.append(f"ya.affiliation_type ILIKE :{param_name}")
                    params[param_name] = f"%{affiliation}%"
                else:
                    # Check school names
                    yale_conditions.append(f"ya.school ILIKE :{param_name}")
                    params[param_name] = f"%{affiliation}%"
                    
            clause = f"({' OR '.join(yale_conditions)})" if yale_conditions else "1=1"
            return clause, params
            
        elif filter.filter_type == FilterType.INDUSTRY:
            # Search in experience descriptions and summaries
            industry_conditions = []
            params = {}
            
            for i, industry in enumerate(filter.values):
                param_name = f"industry_{index}_{i}"
                industry_conditions.append(f"""
                    (
                        p.summary ILIKE :{param_name} OR
                        EXISTS (
                            SELECT 1 FROM experience e 
                            WHERE e.person_uuid = p.uuid_id 
                            AND e.description ILIKE :{param_name}
                        )
                    )
                """)
                params[param_name] = f"%{industry}%"
                
            clause = f"({' OR '.join(industry_conditions)})"
            return clause, params
            
        elif filter.filter_type == FilterType.INVESTMENT_FOCUS:
            # Search for investment focus in descriptions
            focus_conditions = []
            params = {}
            
            for i, focus in enumerate(filter.values):
                param_name = f"invest_focus_{index}_{i}"
                focus_conditions.append(f"""
                    (
                        p.summary ILIKE :{param_name} OR
                        p.headline ILIKE :{param_name} OR
                        EXISTS (
                            SELECT 1 FROM experience e 
                            WHERE e.person_uuid = p.uuid_id 
                            AND (e.description ILIKE :{param_name} OR e.title ILIKE :{param_name})
                        )
                    )
                """)
                params[param_name] = f"%{focus}%"
                
            clause = f"({' OR '.join(focus_conditions)})"
            return clause, params
            
        return "", {}
    
    def _build_keyword_clause(self, keywords: List[str]) -> Tuple[str, Dict]:
        """Build clause for keyword search"""
        keyword_conditions = []
        params = {}
        
        for i, keyword in enumerate(keywords):
            param_name = f"keyword_{i}"
            keyword_conditions.append(f"""
                (
                    to_tsvector('english', coalesce(p.full_name, '') || ' ' || 
                                          coalesce(p.headline, '') || ' ' || 
                                          coalesce(p.summary, '')) 
                    @@ plainto_tsquery('english', :{param_name})
                )
            """)
            params[param_name] = keyword
            
        clause = f"({' OR '.join(keyword_conditions)})" if keyword_conditions else "1=1"
        return clause, params
    
    def _build_score_calculation(self, parsed_query: ParsedQuery) -> str:
        """Build relevance score calculation"""
        score_parts = []
        
        # Base score
        score_parts.append("1.0")
        
        # Boost for Yale affiliation
        if any(f.filter_type == FilterType.YALE_AFFILIATION for f in parsed_query.filters):
            score_parts.append("""
                CASE WHEN ya.person_uuid IS NOT NULL THEN 2.0 ELSE 0 END
            """)
            
        # Boost for current position matching
        if any(f.filter_type == FilterType.TITLE for f in parsed_query.filters):
            score_parts.append("""
                CASE WHEN current_exp.title IS NOT NULL THEN 1.5 ELSE 0 END
            """)
            
        # Boost for location match
        if any(f.filter_type == FilterType.LOCATION for f in parsed_query.filters):
            score_parts.append("""
                CASE WHEN p.location IS NOT NULL THEN 1.0 ELSE 0 END
            """)
            
        return " + ".join(score_parts)
    
    def generate_vector_search_sql(self, query_embedding: List[float], 
                                  limit: int = 50) -> Tuple[str, Dict]:
        """Generate SQL for vector similarity search"""
        sql = """
        SELECT 
            p.*,
            pe.embedding <-> :query_embedding as distance,
            1 - (pe.embedding <-> :query_embedding) as similarity_score
        FROM people p
        JOIN profile_embeddings pe ON pe.person_uuid = p.uuid_id
        ORDER BY pe.embedding <-> :query_embedding
        LIMIT :limit
        """
        
        params = {
            "query_embedding": query_embedding,
            "limit": limit
        }
        
        return sql, params