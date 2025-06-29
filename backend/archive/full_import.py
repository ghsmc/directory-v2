#!/usr/bin/env python3
"""Full scale import of Yale data using streaming approach"""

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
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL, 
                      pool_size=20, 
                      max_overflow=30,
                      pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_brightdata_format(data):
    """Parse BrightData LinkedIn format - optimized version"""
    
    # Skip if no name
    if not data.get('name'):
        return None
        
    # Basic person info with safe string handling
    name = data.get('name') or ''
    city = data.get('city') or ''
    position = data.get('position') or ''
    about = data.get('about') or ''
    url = data.get('url') or ''
    
    person_data = {
        'full_name': str(name).strip()[:255],
        'first_name': str(name).split()[0] if name else '',
        'last_name': ' '.join(str(name).split()[1:]) if name else '',
        'email': None,
        'location': str(city).strip()[:255],
        'headline': str(position).strip()[:500],
        'summary': str(about).strip()[:2000],
        'profile_url': str(url).strip()[:500],
        'linkedin_url': str(url).strip()[:500],
    }
    
    # Extract experiences - limit to top 10
    experiences = []
    experience_data = data.get('experience', [])
    if experience_data:
        for i, exp in enumerate(experience_data[:10]):  # Limit to 10 experiences
            if exp and exp.get('company'):
                company = str(exp.get('company') or '').strip()[:255]
                title = str(exp.get('title') or '').strip()[:255]
                description = str(exp.get('description') or '').strip()[:1000]
                location = str(exp.get('location') or '').strip()[:255]
                
                experience = {
                    'company': company,
                    'title': title,
                    'description': description,
                    'location': location,
                    'date_from': None,
                    'date_to': None,
                    'is_current': exp.get('end_date') == 'Present'
                }
                experiences.append(experience)
                
                # Handle nested positions
                if exp.get('positions'):
                    for pos in exp['positions'][:3]:  # Limit nested positions
                        if pos and pos.get('title'):
                            nested_exp = {
                                'company': exp.get('company', '').strip()[:255],
                                'title': pos.get('title', '').strip()[:255],
                                'description': pos.get('description', '').strip()[:1000],
                                'location': exp.get('location', '').strip()[:255],
                                'date_from': None,
                                'date_to': None,
                                'is_current': pos.get('end_date') == 'Present'
                            }
                            experiences.append(nested_exp)
    
    # Extract education and Yale affiliations
    educations = []
    yale_affiliations = []
    
    education_data = data.get('education', [])
    if education_data:
        for edu in education_data[:5]:  # Limit to 5 education entries
            if edu and edu.get('title'):
                school_name = str(edu.get('title') or '').strip()
                degree = str(edu.get('degree') or '').strip()
                field = str(edu.get('field') or '').strip()
                
                education = {
                    'institution': school_name[:255],
                    'degree': degree[:255],
                    'field_of_study': field[:255],
                    'title': f"{degree} in {field} from {school_name}".strip()[:500],
                    'date_from': None,
                    'date_to': None,
                    'activities': ''
                }
                educations.append(education)
                
                # Check if this is Yale education
                if 'yale' in school_name.lower():
                    yale_affiliation = {
                        'school': school_name[:255],
                        'affiliation_type': 'alumni',
                        'class_year': None,
                        'residential_college': None,
                        'major': field[:255] if field else None,
                        'sports_teams': None,
                        'clubs_organizations': None
                    }
                    
                    if degree:
                        degree_lower = degree.lower()
                        if any(x in degree_lower for x in ['ba', 'bs', 'bachelor']):
                            yale_affiliation['affiliation_type'] = 'undergraduate'
                        elif any(x in degree_lower for x in ['ma', 'ms', 'mba', 'phd', 'jd', 'md']):
                            yale_affiliation['affiliation_type'] = 'graduate'
                            
                    yale_affiliations.append(yale_affiliation)
    
    # Only return if has Yale affiliation
    if not yale_affiliations:
        return None
    
    return {
        'person': person_data,
        'experiences': experiences,
        'educations': educations,
        'yale_affiliations': yale_affiliations,
        'skills': []
    }

def stream_and_parse_s3_data():
    """Stream data from S3 and parse JSON efficiently"""
    
    s3 = boto3.client('s3', region_name='us-east-2')
    bucket_name = 'people-data-yale-2025'
    key = 'brightdata/education_yale/milo_20250529_110131.json'
    
    logger.info(f"Starting to stream data from s3://{bucket_name}/{key}")
    
    # Get the object
    response = s3.get_object(Bucket=bucket_name, Key=key)
    
    # Read the file in chunks and parse JSON records
    buffer = ""
    bracket_count = 0
    in_string = False
    escape_next = False
    current_record = ""
    recording = False
    records_found = 0
    yale_records = 0
    
    chunk_size = 1024 * 1024  # 1MB chunks
    
    for chunk in response['Body'].iter_chunks(chunk_size=chunk_size):
        buffer += chunk.decode('utf-8', errors='ignore')
        
        # Process character by character to find complete JSON objects
        i = 0
        while i < len(buffer):
            char = buffer[i]
            
            if escape_next:
                escape_next = False
                current_record += char
                i += 1
                continue
                
            if char == '\\':
                escape_next = True
                current_record += char
                i += 1
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                current_record += char
                i += 1
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
                            records_found += 1
                            
                            # Parse and filter for Yale people
                            parsed = parse_brightdata_format(record)
                            if parsed:
                                yale_records += 1
                                yield parsed
                                
                            if records_found % 1000 == 0:
                                logger.info(f"Processed {records_found} records, found {yale_records} Yale people")
                            
                            # Also log every 25 Yale people found for better progress visibility
                            if yale_records % 25 == 0 and yale_records > 0:
                                logger.info(f"Progress: Found {yale_records} Yale people (from {records_found} total records)")
                                
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse record at position {records_found}: {e}")
                        
                        recording = False
                        current_record = ""
                        bracket_count = 0
            
            i += 1
        
        # Keep unprocessed part of buffer
        if recording and current_record:
            # Find the last complete character boundary
            last_brace = buffer.rfind('}')
            if last_brace > -1:
                buffer = buffer[last_brace + 1:]
            else:
                buffer = current_record
        else:
            buffer = ""
    
    logger.info(f"Streaming complete. Total records: {records_found}, Yale records: {yale_records}")

def batch_import_to_db(data_stream, batch_size=100):
    """Import data in batches to database"""
    
    db_session = SessionLocal()
    batch = []
    total_imported = 0
    start_time = time.time()
    
    try:
        for parsed_data in data_stream:
            try:
                # Create person object
                person = Person(**parsed_data['person'])
                
                # Add experiences
                for exp_data in parsed_data['experiences']:
                    if exp_data['company']:
                        exp = Experience(**exp_data)
                        person.experiences.append(exp)
                        
                # Add education
                for edu_data in parsed_data['educations']:
                    if edu_data['institution']:
                        edu = Education(**edu_data)
                        person.educations.append(edu)
                        
                # Add Yale affiliations
                for yale_data in parsed_data['yale_affiliations']:
                    yale_aff = YaleAffiliation(**yale_data)
                    person.yale_affiliations.append(yale_aff)
                
                batch.append(person)
                
                # Commit in batches
                if len(batch) >= batch_size:
                    db_session.add_all(batch)
                    db_session.commit()
                    total_imported += len(batch)
                    
                    elapsed = time.time() - start_time
                    rate = total_imported / elapsed if elapsed > 0 else 0
                    logger.info(f"✅ Imported {total_imported} Yale people ({rate:.1f} people/sec)")
                    
                    batch = []
                    
            except Exception as e:
                logger.error(f"Error importing person {parsed_data['person'].get('full_name', 'Unknown')}: {e}")
                continue
        
        # Import remaining batch
        if batch:
            db_session.add_all(batch)
            db_session.commit()
            total_imported += len(batch)
            
        elapsed = time.time() - start_time
        logger.info(f"Import completed! Total imported: {total_imported} Yale people in {elapsed:.1f} seconds")
        
    except Exception as e:
        logger.error(f"Batch import failed: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()
    
    return total_imported

def full_import():
    """Run the full import process"""
    
    logger.info("Starting full scale Yale data import")
    
    # Clear existing data
    db_session = SessionLocal()
    try:
        logger.info("Clearing existing data...")
        db_session.query(YaleAffiliation).delete()
        db_session.query(Experience).delete()
        db_session.query(Education).delete()
        db_session.query(Person).delete()
        db_session.commit()
        logger.info("Existing data cleared")
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        db_session.rollback()
    finally:
        db_session.close()
    
    # Start streaming and importing
    data_stream = stream_and_parse_s3_data()
    total_imported = batch_import_to_db(data_stream, batch_size=50)
    
    # Verify import
    db_session = SessionLocal()
    try:
        final_count = db_session.query(Person).count()
        yale_count = db_session.query(Person).join(YaleAffiliation).count()
        logger.info(f"Verification: {final_count} total people, {yale_count} with Yale affiliations")
    finally:
        db_session.close()
    
    return total_imported

if __name__ == "__main__":
    full_import()