#!/usr/bin/env python3
"""
Fixed streaming import using line-by-line JSON parsing
This assumes the S3 file is JSONL format (one JSON record per line)
"""

import sys
import os
import json
import boto3
import logging
import re
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
    if not name or len(name.strip()) < 3:
        return True
    
    fake_patterns = ['lorem', 'ipsum', 'test user', 'example user', 'john doe', 'jane doe', 'asdf', 'qwerty']
    return any(pattern in name for pattern in fake_patterns)

def parse_brightdata_format(data):
    """Parse BrightData LinkedIn format with quality filtering"""
    
    if is_fake_or_test_data(data):
        return None
    
    if not data.get('name'):
        return None
        
    name = str(data.get('name', '')).strip()[:255]
    if len(name) < 3:
        return None
    
    person_data = {
        'full_name': name,
        'first_name': name.split()[0] if name else '',
        'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
        'email': None,
        'location': str(data.get('city', '')).strip()[:255],
        'headline': str(data.get('position', '')).strip()[:500],
        'summary': str(data.get('about', '')).strip()[:2000],
        'profile_url': str(data.get('url', '')).strip()[:500],
        'linkedin_url': str(data.get('url', '')).strip()[:500],
    }
    
    # Extract experiences
    experiences = []
    for exp in (data.get('experience', []) or [])[:10]:
        if exp and exp.get('company'):
            experiences.append({
                'company': str(exp.get('company', '')).strip()[:255],
                'title': str(exp.get('title', '')).strip()[:255],
                'description': str(exp.get('description', '')).strip()[:1000],
                'location': str(exp.get('location', '')).strip()[:255],
                'date_from': None,
                'date_to': None,
                'is_current': exp.get('end_date') == 'Present'
            })
    
    # Extract education and Yale affiliations
    educations = []
    yale_affiliations = []
    
    for edu in (data.get('education', []) or [])[:5]:
        if edu and edu.get('title'):
            school_name = str(edu.get('title', '')).strip()
            degree = str(edu.get('degree', '')).strip()
            field = str(edu.get('field', '')).strip()
            
            educations.append({
                'institution': school_name[:255],
                'degree': degree[:255],
                'field_of_study': field[:255],
                'title': f"{degree} {field}".strip()[:500],
                'date_from': None,
                'date_to': None,
                'gpa': None,
                'activities': None
            })
            
            # Check for Yale affiliation
            school_lower = school_name.lower()
            if any(yale_term in school_lower for yale_term in ['yale', 'yale university', 'yale college']):
                yale_school = "Yale University"
                if 'som' in school_lower or 'management' in school_lower:
                    yale_school = "Yale School of Management"
                elif 'law' in school_lower:
                    yale_school = "Yale Law School"
                elif 'medical' in school_lower or 'medicine' in school_lower:
                    yale_school = "Yale School of Medicine"
                elif 'college' in school_lower:
                    yale_school = "Yale College"
                
                yale_affiliations.append({
                    'affiliation_type': "alumni",
                    'school': yale_school,
                    'class_year': None,
                    'residential_college': None,
                    'major': field[:255] if field else None,
                    'sports_teams': None,
                    'clubs_organizations': None
                })
    
    # Check headline for Yale affiliation
    if person_data['headline'] and any(yale_term in person_data['headline'].lower() 
                                       for yale_term in ['yale', 'yale university']):
        if not yale_affiliations:
            yale_affiliations.append({
                'affiliation_type': "faculty",
                'school': "Yale University",
                'class_year': None,
                'residential_college': None,
                'major': None,
                'sports_teams': None,
                'clubs_organizations': None
            })
    
    # Only return if has Yale affiliation
    if not yale_affiliations:
        return None
    
    return {
        'person': person_data,
        'experiences': experiences,
        'educations': educations,
        'yale_affiliations': yale_affiliations
    }

def stream_s3_by_chunks(bucket, key, chunk_size=1024*1024):
    """Stream S3 file in chunks and extract JSON records"""
    
    s3_client = boto3.client('s3')
    logger.info(f"Streaming from s3://{bucket}/{key}")
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    
    buffer = ""
    brace_count = 0
    in_record = False
    current_record = ""
    records_processed = 0
    yale_records = 0
    seen_names = set()
    
    for chunk in response['Body'].iter_chunks(chunk_size=chunk_size):
        buffer += chunk.decode('utf-8', errors='ignore')
        
        # Process character by character but more efficiently
        i = 0
        while i < len(buffer):
            char = buffer[i]
            
            if char == '{':
                if not in_record:
                    in_record = True
                    current_record = char
                    brace_count = 1
                else:
                    current_record += char
                    brace_count += 1
            elif char == '}' and in_record:
                current_record += char
                brace_count -= 1
                
                if brace_count == 0:
                    # Complete record
                    try:
                        record = json.loads(current_record)
                        records_processed += 1
                        
                        parsed = parse_brightdata_format(record)
                        if parsed:
                            name = parsed['person']['full_name']
                            normalized_name = ' '.join(name.strip().split()).title()
                            
                            if normalized_name not in seen_names:
                                seen_names.add(normalized_name)
                                yale_records += 1
                                yield parsed
                        
                        # Progress logging
                        if records_processed % 10000 == 0:
                            logger.info(f"📊 Processed {records_processed:,} records, found {yale_records:,} Yale people")
                        
                        if yale_records % 1000 == 0 and yale_records > 0:
                            logger.info(f"🎓 Found {yale_records:,} Yale people")
                            
                    except json.JSONDecodeError:
                        pass  # Skip malformed JSON
                    
                    # Reset for next record
                    in_record = False
                    current_record = ""
                    brace_count = 0
            elif in_record:
                current_record += char
            
            i += 1
        
        # Keep incomplete record in buffer
        if in_record:
            # Find the start of the current incomplete record
            last_complete_end = buffer.rfind('}', 0, len(buffer) - len(current_record))
            if last_complete_end != -1:
                buffer = buffer[last_complete_end + 1:]
            else:
                buffer = current_record
        else:
            buffer = ""
    
    logger.info(f"🎉 Streaming complete! Processed {records_processed:,}, found {yale_records:,} Yale people")

def batch_import_to_db(data_stream, batch_size=100):
    """Import data to database in batches"""
    
    db_session = SessionLocal()
    batch = []
    total_imported = 0
    start_time = time.time()
    
    try:
        for parsed_data in data_stream:
            try:
                person = Person(**parsed_data['person'])
                
                for exp_data in parsed_data['experiences']:
                    if exp_data['company']:
                        person.experiences.append(Experience(**exp_data))
                        
                for edu_data in parsed_data['educations']:
                    if edu_data['institution']:
                        person.educations.append(Education(**edu_data))
                        
                for yale_data in parsed_data['yale_affiliations']:
                    person.yale_affiliations.append(YaleAffiliation(**yale_data))
                
                batch.append(person)
                
                if len(batch) >= batch_size:
                    db_session.add_all(batch)
                    db_session.commit()
                    total_imported += len(batch)
                    
                    elapsed = time.time() - start_time
                    rate = total_imported / elapsed if elapsed > 0 else 0
                    logger.info(f"✅ Imported {total_imported:,} people ({rate:.1f} people/sec)")
                    
                    batch = []
                    
            except Exception as e:
                logger.error(f"Error importing: {e}")
                continue
        
        # Import remaining batch
        if batch:
            db_session.add_all(batch)
            db_session.commit()
            total_imported += len(batch)
            
        logger.info(f"🎉 Import complete! Total: {total_imported:,} people")
        return total_imported
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        db_session.rollback()
        return 0
    finally:
        db_session.close()

def main():
    """Main import function"""
    logger.info("🚀 Starting FIXED streaming import")
    
    # Clear existing data
    db_session = SessionLocal()
    try:
        db_session.execute(text("DELETE FROM yale_affiliations"))
        db_session.execute(text("DELETE FROM experience"))
        db_session.execute(text("DELETE FROM education"))
        db_session.execute(text("DELETE FROM people"))
        db_session.commit()
        logger.info("✅ Data cleared")
    finally:
        db_session.close()
    
    bucket = "people-data-yale-2025"
    key = "brightdata/education_yale/milo_20250529_110131.json"
    
    try:
        data_stream = stream_s3_by_chunks(bucket, key)
        imported_count = batch_import_to_db(data_stream)
        logger.info(f"🎓 SUCCESS! Imported {imported_count:,} Yale people")
    except Exception as e:
        logger.error(f"Import error: {e}")

if __name__ == "__main__":
    main()