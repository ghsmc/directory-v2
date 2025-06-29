from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import openai
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

from .query_parser import QueryParser, ParsedQuery
from .sql_generator import SQLGenerator
from ..models import Person, ProfileEmbedding

logger = logging.getLogger(__name__)


class SearchResult:
    def __init__(self, person: Person, score: float, 
                 matched_filters: Dict[str, List[str]] = None,
                 explanation: str = ""):
        self.person = person
        self.score = score
        self.matched_filters = matched_filters or {}
        self.explanation = explanation
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response"""
        current_position = None
        if self.person.experiences:
            current_exp = next((e for e in self.person.experiences if e.is_current), None)
            if current_exp:
                current_position = {
                    'company': current_exp.company,
                    'title': current_exp.title
                }
                
        yale_info = None
        if self.person.yale_affiliations:
            yale_aff = self.person.yale_affiliations[0]  # Take first
            yale_info = {
                'school': yale_aff.school,
                'class_year': yale_aff.class_year,
                'affiliation_type': yale_aff.affiliation_type
            }
            
        return {
            'uuid': str(self.person.uuid_id),
            'name': self.person.full_name,
            'email': self.person.email,
            'location': self.person.location,
            'headline': self.person.headline,
            'current_position': current_position,
            'yale_info': yale_info,
            'linkedin_url': self.person.linkedin_url,
            'score': self.score,
            'matched_filters': self.matched_filters,
            'explanation': self.explanation
        }


class YaleSearchEngine:
    """Main search engine combining all components"""
    
    def __init__(self, db_session: Session, openai_api_key: str):
        self.db = db_session
        self.query_parser = QueryParser(openai_api_key)
        self.sql_generator = SQLGenerator()
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        openai.api_key = openai_api_key
        
    def search(self, query: str, 
              user_id: Optional[str] = None,
              use_semantic_search: bool = True,
              limit: int = 50) -> Dict[str, Any]:
        """Execute a search query and return results"""
        
        # Parse the query
        parsed_query = self.query_parser.parse(query)
        
        # Log the search for learning
        self._log_search(query, parsed_query, user_id)
        
        # Generate and execute SQL query
        sql, params = self.sql_generator.generate_sql(
            parsed_query,
            user_id=user_id,
            limit=limit
        )
        
        # Execute search
        results = []
        result_rows = self.db.execute(text(sql), params).fetchall()
        
        for row in result_rows:
            person = self.db.query(Person).filter_by(uuid_id=row[0]).first()
            if person:
                result = SearchResult(
                    person=person,
                    score=float(row[-1]) if row[-1] else 0.0,
                    matched_filters=self._extract_matched_filters(person, parsed_query)
                )
                results.append(result)
                
        # Optionally enhance with semantic search
        if use_semantic_search and len(results) < limit:
            semantic_results = self._semantic_search(query, limit - len(results))
            results.extend(semantic_results)
            
        # Generate search explanation
        explanation = self.query_parser.generate_explanation(parsed_query)
        
        return {
            'query': query,
            'parsed_query': {
                'intent': parsed_query.intent,
                'filters': [
                    {
                        'type': f.filter_type.value,
                        'values': f.values
                    } for f in parsed_query.filters
                ],
                'keywords': parsed_query.keywords
            },
            'explanation': explanation,
            'results': [r.to_dict() for r in results],
            'total_results': len(results),
            'sql_query': sql if user_id else None  # Only show SQL to authenticated users
        }
        
    def _semantic_search(self, query: str, limit: int) -> List[SearchResult]:
        """Perform semantic search using embeddings"""
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        # Search similar profiles
        sql = """
        SELECT 
            p.uuid_id,
            1 - (pe.embedding <=> :query_embedding) as similarity_score
        FROM people p
        JOIN profile_embeddings pe ON pe.person_uuid = p.uuid_id
        WHERE 1 - (pe.embedding <=> :query_embedding) > 0.5
        ORDER BY similarity_score DESC
        LIMIT :limit
        """
        
        params = {
            'query_embedding': query_embedding,
            'limit': limit
        }
        
        results = []
        for row in self.db.execute(text(sql), params):
            person = self.db.query(Person).filter_by(uuid_id=row[0]).first()
            if person:
                result = SearchResult(
                    person=person,
                    score=float(row[1]),
                    explanation="Semantic similarity match"
                )
                results.append(result)
                
        return results
        
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text"""
        # Use sentence transformers for now (can switch to OpenAI)
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
        
    def _extract_matched_filters(self, person: Person, 
                                parsed_query: ParsedQuery) -> Dict[str, List[str]]:
        """Extract which filters matched for this person"""
        matched = {}
        
        for filter in parsed_query.filters:
            filter_type = filter.filter_type.value
            matches = []
            
            if filter_type == 'location' and person.location:
                for value in filter.values:
                    if value.lower() in person.location.lower():
                        matches.append(person.location)
                        
            elif filter_type == 'education':
                for edu in person.educations:
                    for value in filter.values:
                        if value.lower() in edu.institution.lower():
                            matches.append(f"{edu.institution} ({edu.degree})")
                            
            elif filter_type == 'title':
                for exp in person.experiences:
                    for value in filter.values:
                        if value.lower() in exp.title.lower():
                            matches.append(f"{exp.title} at {exp.company}")
                            
            if matches:
                matched[filter_type] = matches
                
        return matched
        
    def _log_search(self, query: str, parsed_query: ParsedQuery, 
                   user_id: Optional[str]):
        """Log search query for analytics and learning"""
        from ..models import SearchQuery
        
        search_log = SearchQuery(
            user_id=user_id,
            query_text=query,
            parsed_filters={
                'intent': parsed_query.intent,
                'filters': [
                    {
                        'type': f.filter_type.value,
                        'values': f.values
                    } for f in parsed_query.filters
                ]
            }
        )
        
        self.db.add(search_log)
        self.db.commit()
        
    def update_profile_embeddings(self, batch_size: int = 100):
        """Update embeddings for all profiles"""
        logger.info("Starting profile embedding update")
        
        # Get profiles without embeddings
        profiles = self.db.query(Person).outerjoin(ProfileEmbedding)\
            .filter(ProfileEmbedding.person_uuid == None).limit(batch_size).all()
            
        for person in profiles:
            # Create embedding text
            embedding_text = self._create_embedding_text(person)
            
            # Generate embedding
            embedding = self._generate_embedding(embedding_text)
            
            # Store embedding
            profile_embedding = ProfileEmbedding(
                person_uuid=person.uuid_id,
                embedding_text=embedding_text,
                embedding=embedding
            )
            
            self.db.add(profile_embedding)
            
        self.db.commit()
        logger.info(f"Updated embeddings for {len(profiles)} profiles")
        
    def _create_embedding_text(self, person: Person) -> str:
        """Create text representation of person for embedding"""
        parts = [
            person.full_name,
            person.headline or '',
            person.summary or '',
            person.location or ''
        ]
        
        # Add current position
        current_exp = next((e for e in person.experiences if e.is_current), None)
        if current_exp:
            parts.append(f"{current_exp.title} at {current_exp.company}")
            
        # Add education
        for edu in person.educations[:2]:  # Top 2 educations
            parts.append(f"{edu.degree} from {edu.institution}")
            
        # Add skills
        skills = [s.skill_name for s in person.skills[:10]]  # Top 10 skills
        if skills:
            parts.append("Skills: " + ", ".join(skills))
            
        return " ".join(filter(None, parts))