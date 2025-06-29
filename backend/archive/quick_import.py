#!/usr/bin/env python3
"""Quick import of sample Yale data"""

import sys
import os
sys.path.append('.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Person, Education, Experience, YaleAffiliation, Skill
import boto3
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        'email': None,
        'location': data.get('city', ''),
        'headline': data.get('position', ''),
        'summary': data.get('about', ''),
        'profile_url': data.get('url', ''),
        'linkedin_url': data.get('url', ''),
    }
    
    # Extract experiences
    experiences = []
    experience_data = data.get('experience', [])
    if experience_data:
        for exp in experience_data:
            if exp:  # Check if exp is not None
                experience = {
                    'company': exp.get('company', ''),
                    'title': exp.get('title', ''),
                    'description': exp.get('description', ''),
                    'location': exp.get('location', ''),
                    'date_from': None,
                    'date_to': None,
                    'is_current': exp.get('end_date') == 'Present'
                }
                experiences.append(experience)
    
    # Extract education and Yale affiliations
    educations = []
    yale_affiliations = []
    
    education_data = data.get('education', [])
    if education_data:
        for edu in education_data:
            if edu:  # Check if edu is not None
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
                    
                    if degree and ('BA' in degree or 'BS' in degree or 'Bachelor' in degree):
                        yale_affiliation['affiliation_type'] = 'undergraduate'
                    elif degree and ('MA' in degree or 'MS' in degree or 'MBA' in degree or 'PhD' in degree or 'JD' in degree):
                        yale_affiliation['affiliation_type'] = 'graduate'
                        
                    yale_affiliations.append(yale_affiliation)
    
    return {
        'person': person_data,
        'experiences': experiences,
        'educations': educations,
        'yale_affiliations': yale_affiliations,
        'skills': []
    }

def import_from_sample():
    """Import from the downloaded sample file"""
    
    db_session = SessionLocal()
    
    try:
        # Read the sample file we downloaded
        with open('yale_sample_1mb.json', 'r') as f:
            content = f.read()
            
        # Parse the JSON array - get just the first complete records
        start_idx = content.find('[')
        
        # Find first few complete records
        records = []
        bracket_count = 0
        in_string = False
        escape_next = False
        current_record = ""
        recording = False
        
        for i, char in enumerate(content[start_idx:]):
            if escape_next:
                escape_next = False
                current_record += char
                continue
                
            if char == '\\':
                escape_next = True
                current_record += char
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                current_record += char
                continue
                
            current_record += char
            
            if not in_string:
                if char == '{':
                    bracket_count += 1
                    if not recording:
                        recording = True
                        current_record = char
                elif char == '}':
                    bracket_count -= 1
                    if bracket_count == 0 and recording:
                        # Found complete record
                        try:
                            record = json.loads(current_record)
                            records.append(record)
                            logger.info(f"Parsed record: {record.get('name', 'Unknown')}")
                            
                            if len(records) >= 10:  # Get 10 records for testing
                                break
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse record: {e}")
                        
                        recording = False
                        current_record = ""
        
        logger.info(f"Found {len(records)} complete records")
        
        # Import the records
        yale_count = 0
        for data in records:
            parsed_data = parse_brightdata_format(data)
            
            # Only import people with Yale connections
            if not parsed_data['yale_affiliations']:
                continue
                
            yale_count += 1
            logger.info(f"Importing Yale person: {parsed_data['person']['full_name']}")
            
            # Create person object
            person = Person(**parsed_data['person'])
            
            # Add related data
            for exp_data in parsed_data['experiences']:
                if exp_data['company']:
                    exp = Experience(**exp_data)
                    person.experiences.append(exp)
                    
            for edu_data in parsed_data['educations']:
                if edu_data['institution']:
                    edu = Education(**edu_data)
                    person.educations.append(edu)
                    
            for yale_data in parsed_data['yale_affiliations']:
                yale_aff = YaleAffiliation(**yale_data)
                person.yale_affiliations.append(yale_aff)
            
            db_session.add(person)
            
        db_session.commit()
        logger.info(f"Successfully imported {yale_count} Yale people")
        
        # Test a simple query
        people = db_session.query(Person).join(YaleAffiliation).limit(5).all()
        logger.info(f"Verification: Found {len(people)} Yale people in database")
        
        for person in people:
            logger.info(f"  - {person.full_name} ({person.location})")
            for ya in person.yale_affiliations:
                logger.info(f"    Yale: {ya.school} ({ya.affiliation_type})")
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()

if __name__ == "__main__":
    import_from_sample()