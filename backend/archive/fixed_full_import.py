#!/usr/bin/env python3
"""Fixed full import that handles JSON arrays properly"""

import sys
import os
import json
import boto3
import logging
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
        for i, exp in enumerate(experience_data[:10]):
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
                    for pos in exp['positions'][:3]:
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
        for edu in education_data[:5]:
            if edu and edu.get('title'):
                school_name = str(edu.get('title') or '').strip()
                degree = str(edu.get('degree') or '').strip()
                field = str(edu.get('field') or '').strip()
                
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
                
                # Check for Yale affiliation - be more liberal
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
            # Current Yale affiliation
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

def stream_json_array_from_s3(bucket, key):
    """Stream and parse large JSON array from S3"""
    
    s3_client = boto3.client('s3')
    logger.info(f"Starting to stream data from s3://{bucket}/{key}")
    
    # Get object info
    head_response = s3_client.head_object(Bucket=bucket, Key=key)
    file_size = head_response['ContentLength']
    logger.info(f"File size: {file_size / (1024*1024*1024):.1f} GB")
    
    # Stream the file in chunks
    chunk_size = 8 * 1024 * 1024  # 8MB chunks
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    
    buffer = ""
    records_found = 0
    yale_records = 0
    in_record = False
    bracket_count = 0
    current_record = ""
    
    # Read the file in chunks
    for chunk in response['Body'].iter_chunks(chunk_size=chunk_size):
        buffer += chunk.decode('utf-8', errors='ignore')
        
        # Process the buffer
        i = 0
        while i < len(buffer):
            char = buffer[i]
            
            if char == '{':
                bracket_count += 1
                if not in_record:
                    in_record = True
                    current_record = char
                else:
                    current_record += char
            elif char == '}':
                if in_record:
                    current_record += char
                    bracket_count -= 1
                    
                    if bracket_count == 0:
                        # Complete record found
                        try:
                            record = json.loads(current_record)
                            records_found += 1
                            
                            # Parse and filter for Yale people
                            parsed = parse_brightdata_format(record)
                            if parsed:
                                yale_records += 1
                                yield parsed
                                
                            # Progress logging
                            if records_found % 1000 == 0:
                                logger.info(f"Processed {records_found:,} records, found {yale_records:,} Yale people")
                            
                            if yale_records % 50 == 0 and yale_records > 0:
                                logger.info(f"🎓 Progress: Found {yale_records} Yale people (from {records_found:,} total records)")
                                
                        except json.JSONDecodeError as e:
                            logger.debug(f"Failed to parse record at position {records_found}: {e}")
                        
                        in_record = False
                        current_record = ""
                        bracket_count = 0
            else:
                if in_record:
                    current_record += char
            
            i += 1
        
        # Keep the last incomplete record in buffer
        if in_record and bracket_count > 0:
            # Find last complete boundary
            last_brace = buffer.rfind('}')
            if last_brace > -1:
                # Keep everything after the last complete record
                buffer = buffer[last_brace + 1:]
            else:
                # Keep current record
                buffer = current_record
        else:
            buffer = ""
    
    logger.info(f"🎉 Streaming complete! Total records: {records_found:,}, Yale records: {yale_records:,}")

def batch_import_to_db(data_stream, batch_size=50):
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
                    logger.info(f"✅ Imported {total_imported:,} Yale people ({rate:.1f} people/sec)")
                    
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
        logger.info(f"🎉 Import completed! Total imported: {total_imported:,} Yale people in {elapsed:.1f} seconds")
        
        # Verification
        final_count = db_session.execute(text("SELECT COUNT(*) FROM people")).scalar()
        yale_aff_count = db_session.execute(text("SELECT COUNT(*) FROM yale_affiliations")).scalar()
        logger.info(f"📊 Verification: {final_count} total people, {yale_aff_count} with Yale affiliations")
        
        return total_imported
        
    except Exception as e:
        logger.error(f"Import failed: {e}")
        db_session.rollback()
        return 0
    finally:
        db_session.close()

def main():
    """Main import function"""
    logger.info("🚀 Starting FIXED full scale Yale data import")
    
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
        data_stream = stream_json_array_from_s3(bucket, key)
        imported_count = batch_import_to_db(data_stream)
        
        if imported_count > 0:
            logger.info(f"🎓 SUCCESS! Imported {imported_count:,} Yale people")
        else:
            logger.error("❌ Import failed - no records imported")
            
    except Exception as e:
        logger.error(f"Import error: {e}")

if __name__ == "__main__":
    main()