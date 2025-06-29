#!/usr/bin/env python3
"""
Improved streaming JSON import with robust parsing
Uses ijson for proper streaming JSON parsing to handle large files efficiently
"""

import sys
import os
import json
import boto3
import logging
import ijson
from datetime import datetime
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.append('.')
from app.models import Base, Person, Education, Experience, YaleAffiliation, Skill

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://georgemccain@localhost:5432/yale_network"
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=30, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def is_fake_or_test_data(data):
    """Filter out fake, test, or low-quality data"""
    
    name = str(data.get('name', '')).lower()
    about = str(data.get('about', '')).lower()
    position = str(data.get('position', '')).lower()
    
    # Skip if no name
    if not name or len(name.strip()) < 2:
        return True
    
    # Common fake/test patterns
    fake_patterns = [
        # Lorem ipsum variations
        'lorem', 'ipsum', 'dolor', 'consectetur', 'adipiscing',
        # Test data
        'test user', 'test person', 'test account', 'example user',
        'sample user', 'demo user', 'fake user', 'dummy user',
        # Generic placeholders
        'john doe', 'jane doe', 'first last', 'user name',
        'your name', 'full name', 'enter name', 'add name',
        # Obvious fakes
        'asdf', 'qwerty', '123456', 'aaaaa', 'xxxxx',
        # Bot indicators
        'linkedin user', 'network user', 'social user',
    ]
    
    # Check name against fake patterns
    for pattern in fake_patterns:
        if pattern in name:
            return True
    
    # Check about/position for lorem ipsum or test content
    combined_text = f"{about} {position}"
    lorem_indicators = [
        'lorem ipsum', 'dolor sit amet', 'consectetur adipiscing',
        'sed do eiusmod', 'tempor incididunt', 'ut labore',
        'this is a test', 'sample text', 'placeholder text',
        'example description', 'dummy content'
    ]
    
    for indicator in lorem_indicators:
        if indicator in combined_text:
            return True
    
    # Filter very short or suspicious names
    if len(name.strip()) < 3:
        return True
    
    return False

def parse_brightdata_format(data):
    """Parse BrightData LinkedIn format with quality filtering"""
    
    # First check if this is fake/test data
    if is_fake_or_test_data(data):
        return None
    
    # Skip if no name
    if not data.get('name'):
        return None
        
    # Basic person info with safe string handling
    name = data.get('name') or ''
    city = data.get('city') or ''
    position = data.get('position') or ''
    about = data.get('about') or ''
    url = data.get('url') or ''
    
    # Additional quality checks
    if len(name.strip()) < 3:
        return None
    
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
    
    # Extract experiences
    experiences = []
    experience_data = data.get('experience', [])
    if experience_data:
        for i, exp in enumerate(experience_data[:10]):
            if exp and exp.get('company'):
                company = str(exp.get('company') or '').strip()[:255]
                title = str(exp.get('title') or '').strip()[:255]
                
                # Skip fake companies
                fake_companies = ['lorem corp', 'ipsum inc', 'test company', 'example corp', 'acme corp']
                if any(fake in company.lower() for fake in fake_companies):
                    continue
                
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
    
    # Extract education and Yale affiliations
    educations = []
    yale_affiliations = []
    
    education_data = data.get('education', [])
    if education_data:
        for edu in education_data[:5]:
            if edu and edu.get('title'):
                school_name = str(edu.get('title') or '').strip()
                degree = str(edu.get('degree') or '').strip()
                field = str(edu.get('field') or '').strip()
                
                # Skip fake schools
                fake_schools = ['lorem university', 'test college', 'example school', 'sample university']
                if any(fake in school_name.lower() for fake in fake_schools):
                    continue
                
                education = {
                    'institution': school_name[:255],
                    'degree': degree[:255],
                    'field_of_study': field[:255],
                    'title': f"{degree} {field}".strip()[:500],
                    'date_from': None,
                    'date_to': None,
                    'gpa': None,
                    'activities': None
                }
                educations.append(education)
                
                # Check for Yale affiliation
                school_lower = school_name.lower()
                if any(yale_term in school_lower for yale_term in [
                    'yale', 'yale university', 'yale college', 'yale som', 'yale law', 
                    'yale medical', 'yale school', 'yale grad', 'yale doctoral'
                ]):
                    # Determine affiliation type
                    affiliation_type = "alumni"
                    if any(term in school_lower for term in ['student', 'candidate', 'current']):
                        affiliation_type = "student"
                    elif any(term in school_lower for term in ['faculty', 'professor', 'lecturer']):
                        affiliation_type = "faculty"
                    
                    # Extract school
                    yale_school = school_name
                    if 'som' in school_lower or 'business' in school_lower or 'management' in school_lower:
                        yale_school = "Yale School of Management"
                    elif 'law' in school_lower:
                        yale_school = "Yale Law School"
                    elif 'medical' in school_lower or 'medicine' in school_lower:
                        yale_school = "Yale School of Medicine"
                    elif 'college' in school_lower:
                        yale_school = "Yale College"
                    else:
                        yale_school = "Yale University"
                    
                    yale_affiliation = {
                        'affiliation_type': affiliation_type,
                        'school': yale_school,
                        'class_year': None,
                        'residential_college': None,
                        'major': field[:255] if field else None,
                        'sports_teams': None,
                        'clubs_organizations': None
                    }
                    yale_affiliations.append(yale_affiliation)
    
    # Also check current position for Yale affiliation
    if person_data['headline']:
        headline_lower = person_data['headline'].lower()
        if any(yale_term in headline_lower for yale_term in [
            'yale', 'yale university', 'yale college', 'yale som', 'yale law'
        ]):
            affiliation_type = "faculty"
            if any(term in headline_lower for term in ['student', 'candidate', 'phd', 'graduate']):
                affiliation_type = "student"
            
            yale_affiliation = {
                'affiliation_type': affiliation_type,
                'school': "Yale University",
                'class_year': None,
                'residential_college': None,
                'major': None,
                'sports_teams': None,
                'clubs_organizations': None
            }
            # Only add if not already present
            if not yale_affiliations:
                yale_affiliations.append(yale_affiliation)
    
    # Only return if has Yale affiliation
    if not yale_affiliations:
        return None
    
    return {
        'person': person_data,
        'experiences': experiences,
        'educations': educations,
        'yale_affiliations': yale_affiliations
    }

def stream_json_with_ijson(bucket, key):
    """Stream JSON using ijson for proper incremental parsing"""
    
    s3_client = boto3.client('s3')
    logger.info(f"Starting improved streaming from s3://{bucket}/{key}")
    
    # Get object info
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    file_size = head_response['ContentLength']
    logger.info(f"File size: {file_size / (1024*1024*1024):.1f} GB")
    
    # Stream the file
    response = s3_client.get_object(Bucket=bucket, Key=key)
    
    records_processed = 0
    yale_records = 0
    filtered_fake = 0
    seen_names = set()
    
    try:
        # Use ijson to parse JSON incrementally
        parser = ijson.parse(response['Body'])
        
        current_record = {}
        in_array = False
        current_path = []
        
        for prefix, event, value in parser:
            
            # Track when we're in the main array
            if prefix == '' and event == 'start_array':
                in_array = True
                logger.info("📖 Started parsing JSON array")
                continue
                
            if prefix == '' and event == 'end_array':
                logger.info("🎉 Finished parsing JSON array")
                break
            
            # Parse individual records
            if prefix.startswith('item'):
                if event == 'start_map':
                    current_record = {}
                elif event == 'end_map':
                    # Complete record parsed
                    records_processed += 1
                    
                    try:
                        # Parse and filter for Yale people
                        parsed = parse_brightdata_format(current_record)
                        if parsed:
                            # Check for duplicates
                            name = parsed['person']['full_name']
                            normalized_name = ' '.join(name.strip().split()).title()
                            
                            if normalized_name not in seen_names:
                                seen_names.add(normalized_name)
                                yale_records += 1
                                yield parsed
                            else:
                                logger.debug(f"Filtered duplicate: {normalized_name}")
                        else:
                            filtered_fake += 1
                            
                        # Progress logging
                        if records_processed % 5000 == 0:
                            logger.info(f"📊 Processed {records_processed:,} records, found {yale_records:,} Yale people, filtered {filtered_fake:,}")
                        
                        if yale_records % 500 == 0 and yale_records > 0:
                            logger.info(f"🎓 Progress: Found {yale_records:,} clean Yale people")
                            
                    except Exception as e:
                        logger.error(f"Error processing record {records_processed}: {e}")
                        continue
                
                elif event in ('string', 'number', 'boolean', 'null'):
                    # Extract the field name from prefix
                    parts = prefix.split('.')
                    if len(parts) >= 2:
                        field_name = parts[-1]
                        current_record[field_name] = value
    
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        raise
    
    logger.info(f"🎉 Streaming complete! Total: {records_processed:,}, Clean Yale: {yale_records:,}, Filtered: {filtered_fake:,}")

def batch_import_to_db(data_stream, batch_size=50):
    """Import cleaned data in batches to database"""
    
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
                    logger.info(f"✅ Imported {total_imported:,} clean Yale people ({rate:.1f} people/sec)")
                    
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
        logger.info(f"🎉 Import completed! Total: {total_imported:,} Yale people in {elapsed:.1f} seconds")
        
        return total_imported
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        db_session.rollback()
        return 0
    finally:
        db_session.close()

def main():
    """Main improved import function"""
    logger.info("🚀 Starting IMPROVED streaming Yale data import")
    logger.info("🧩 Using ijson for robust JSON parsing")
    
    # Clear existing data
    logger.info("🗑️  Clearing existing data...")
    db_session = SessionLocal()
    try:
        db_session.execute(text("DELETE FROM yale_affiliations"))
        db_session.execute(text("DELETE FROM experience"))
        db_session.execute(text("DELETE FROM education"))
        db_session.execute(text("DELETE FROM people"))
        db_session.commit()
        logger.info("✅ Existing data cleared")
    except Exception as e:
        logger.error(f"Failed to clear data: {e}")
        return
    finally:
        db_session.close()
    
    # Stream and import data
    bucket = "people-data-yale-2025"
    key = "brightdata/education_yale/milo_20250529_110131.json"
    
    try:
        data_stream = stream_json_with_ijson(bucket, key)
        imported_count = batch_import_to_db(data_stream)
        
        if imported_count > 0:
            logger.info(f"🎓 SUCCESS! Imported {imported_count:,} clean Yale people")
        else:
            logger.error("❌ Import failed - no records imported")
            
    except Exception as e:
        logger.error(f"Import error: {e}")

if __name__ == "__main__":
    main()