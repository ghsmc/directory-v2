#!/usr/bin/env python3
"""Import real Yale data into the database"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Person, Education, Experience, YaleAffiliation, Skill
from app.data_loader.s3_loader import S3DataLoader
import logging
from datetime import datetime
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_brightdata_format(data):
    """Parse BrightData LinkedIn format into our format"""
    
    # Basic person info
    person_data = {
        'full_name': data.get('name', ''),
        'first_name': data.get('name', '').split()[0] if data.get('name') else '',
        'last_name': ' '.join(data.get('name', '').split()[1:]) if data.get('name') else '',
        'email': None,  # Not provided in this dataset
        'location': data.get('city', ''),
        'headline': data.get('position', ''),
        'summary': data.get('about', ''),
        'profile_url': data.get('url', ''),
        'linkedin_url': data.get('url', ''),
    }
    
    # Extract experiences
    experiences = []
    for exp in data.get('experience', []):
        experience = {
            'company': exp.get('company', ''),
            'title': exp.get('title', ''),
            'description': exp.get('description', ''),
            'location': exp.get('location', ''),
            'date_from': parse_date_string(exp.get('start_date')),
            'date_to': parse_date_string(exp.get('end_date')),
            'is_current': exp.get('end_date') == 'Present'
        }
        experiences.append(experience)
        
    # Handle nested positions within companies
    for exp in data.get('experience', []):
        if 'positions' in exp:
            for pos in exp['positions']:
                experience = {
                    'company': exp.get('company', pos.get('subtitle', '')),
                    'title': pos.get('title', ''),
                    'description': pos.get('description', ''),
                    'location': exp.get('location', ''),
                    'date_from': parse_date_string(pos.get('start_date')),
                    'date_to': parse_date_string(pos.get('end_date')),
                    'is_current': pos.get('end_date') == 'Present'
                }
                experiences.append(experience)
    
    # Extract education
    educations = []
    yale_affiliations = []
    
    for edu in data.get('education', []):
        school_name = edu.get('title', '')
        degree = edu.get('degree', '')
        field = edu.get('field', '')
        
        education = {
            'institution': school_name,
            'degree': degree,
            'field_of_study': field,
            'title': f"{degree} in {field} from {school_name}".strip(),
            'date_from': None,
            'date_to': None,
            'activities': ''
        }
        educations.append(education)
        
        # Check if this is Yale education
        if 'yale' in school_name.lower():
            yale_affiliation = {
                'school': school_name,
                'affiliation_type': 'alumni',
                'class_year': None,
                'residential_college': None,
                'major': field,
                'sports_teams': None,
                'clubs_organizations': None
            }
            
            # Determine affiliation type based on degree
            if degree and ('BA' in degree or 'BS' in degree or 'Bachelor' in degree):
                yale_affiliation['affiliation_type'] = 'undergraduate'
            elif degree and ('MA' in degree or 'MS' in degree or 'MBA' in degree or 'PhD' in degree or 'JD' in degree):
                yale_affiliation['affiliation_type'] = 'graduate'
                
            yale_affiliations.append(yale_affiliation)
    
    # Extract skills (not present in this format)
    skills = []
    
    return {
        'person': person_data,
        'experiences': experiences,
        'educations': educations,
        'yale_affiliations': yale_affiliations,
        'skills': skills
    }

def parse_date_string(date_str):
    """Parse various date string formats"""
    if not date_str or date_str == 'Present':
        return None
        
    # Try different formats
    formats = ['%b %Y', '%Y', '%m/%Y']
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue
            
    return None

def import_batch(db_session, people_data, batch_size=50):
    """Import a batch of people"""
    
    batch = []
    yale_count = 0
    
    for data in people_data:
        try:
            parsed_data = parse_brightdata_format(data)
            
            # Only import people with Yale connections
            if not parsed_data['yale_affiliations']:
                continue
                
            yale_count += 1
            
            # Create person object
            person = Person(**parsed_data['person'])
            
            # Add related data
            for exp_data in parsed_data['experiences']:
                if exp_data['company']:  # Only add if company exists
                    exp = Experience(**exp_data)
                    person.experiences.append(exp)
                    
            for edu_data in parsed_data['educations']:
                if edu_data['institution']:  # Only add if institution exists
                    edu = Education(**edu_data)
                    person.educations.append(edu)
                    
            for yale_data in parsed_data['yale_affiliations']:
                yale_aff = YaleAffiliation(**yale_data)
                person.yale_affiliations.append(yale_aff)
                
            for skill_data in parsed_data['skills']:
                skill = Skill(**skill_data)
                person.skills.append(skill)
                
            batch.append(person)
            
            # Commit in batches
            if len(batch) >= batch_size:
                db_session.add_all(batch)
                db_session.commit()
                logger.info(f"Imported batch of {len(batch)} people (Yale people so far: {yale_count})")
                batch = []
                
        except Exception as e:
            logger.error(f"Error processing person: {e}")
            continue
            
    # Commit remaining
    if batch:
        db_session.add_all(batch)
        db_session.commit()
        logger.info(f"Imported final batch of {len(batch)} people")
        
    return yale_count

def import_data_efficiently():
    """Import data efficiently in chunks"""
    
    loader = S3DataLoader()
    db_session = SessionLocal()
    
    try:
        key = 'brightdata/education_yale/milo_20250529_110131.json'
        logger.info(f"Starting import from s3://people-data-yale-2025/{key}")
        
        total_processed = 0
        yale_imported = 0
        
        # Process data in chunks
        current_batch = []
        batch_size = 100
        
        for person_data in loader.stream_json_from_s3(key):
            current_batch.append(person_data)
            total_processed += 1
            
            if len(current_batch) >= batch_size:
                yale_count = import_batch(db_session, current_batch, batch_size=50)
                yale_imported += yale_count
                logger.info(f"Processed {total_processed} people, imported {yale_imported} Yale people")
                current_batch = []
                
            # Limit for testing - remove this for full import
            if total_processed >= 1000:  # Test with first 1000 records
                logger.info("Stopping at 1000 records for testing")
                break
                
        # Process remaining
        if current_batch:
            yale_count = import_batch(db_session, current_batch, batch_size=50)
            yale_imported += yale_count
            
        logger.info(f"Import completed! Processed {total_processed} people, imported {yale_imported} Yale people")
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()

if __name__ == "__main__":
    import_data_efficiently()