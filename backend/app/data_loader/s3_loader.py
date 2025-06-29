import json
import boto3
from typing import Dict, List, Iterator, Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from botocore.exceptions import ClientError

from ..models import Person, Education, Experience, YaleAffiliation, Skill

logger = logging.getLogger(__name__)


class S3DataLoader:
    """Load Yale people data from S3 and import into database"""
    
    def __init__(self, aws_access_key_id: str = None, 
                 aws_secret_access_key: str = None,
                 region_name: str = 'us-east-2'):
        
        # Always use default credentials first (from ~/.aws/credentials or IAM role)
        # This is more secure and reliable than environment variables
        try:
            self.s3 = boto3.client('s3', region_name=region_name)
            # Test connection
            self.s3.head_bucket(Bucket='people-data-yale-2025')
            logger.info("Using default AWS credentials")
        except Exception as e:
            # Fall back to provided credentials
            if aws_access_key_id and aws_secret_access_key:
                self.s3 = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                )
                logger.info("Using provided AWS credentials")
            else:
                raise Exception(f"AWS credentials not available: {e}")
            
        self.bucket_name = 'people-data-yale-2025'
        
    def stream_json_from_s3(self, key: str, chunk_size: int = 64 * 1024) -> Iterator[Dict]:
        """Stream JSON data from S3 in chunks to handle large files"""
        try:
            # Get object
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            
            # First, let's check if this is a single JSON array or newline-delimited JSON
            # Read a small sample to determine format
            sample = response['Body'].read(1024).decode('utf-8')
            response['Body'].close()
            
            # Re-open the stream
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            
            if sample.strip().startswith('['):
                # This is a JSON array, we need to parse it differently
                logger.info("Detected JSON array format")
                
                # For a large JSON array, we'll read the entire file
                # This is not ideal for very large files, but necessary for parsing
                content = response['Body'].read().decode('utf-8')
                data = json.loads(content)
                
                if isinstance(data, list):
                    for item in data:
                        yield item
                else:
                    yield data
                    
            else:
                # Assume newline-delimited JSON (JSONL format)
                logger.info("Detected JSONL format")
                buffer = ""
                
                for chunk in response['Body'].iter_chunks(chunk_size=chunk_size):
                    try:
                        buffer += chunk.decode('utf-8')
                    except UnicodeDecodeError:
                        # Handle partial UTF-8 characters at chunk boundaries
                        buffer += chunk.decode('utf-8', errors='ignore')
                    
                    # Process complete lines
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if line.strip():
                            try:
                                yield json.loads(line)
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse JSON line: {e}")
                                continue
                                
                # Process any remaining data
                if buffer.strip():
                    try:
                        yield json.loads(buffer)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse final JSON: {e}")
                    
        except ClientError as e:
            logger.error(f"Failed to read from S3: {e}")
            raise
            
    def parse_person_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Parse raw person data into structured format"""
        
        # Extract basic info
        person_data = {
            'full_name': raw_data.get('name', ''),
            'first_name': raw_data.get('firstName', ''),
            'last_name': raw_data.get('lastName', ''),
            'email': raw_data.get('email'),
            'location': raw_data.get('location', {}).get('name', ''),
            'headline': raw_data.get('headline', ''),
            'summary': raw_data.get('summary', ''),
            'profile_url': raw_data.get('publicProfileUrl', ''),
            'linkedin_url': raw_data.get('linkedinUrl', raw_data.get('publicProfileUrl', '')),
        }
        
        # Extract experiences
        experiences = []
        for exp in raw_data.get('experience', []):
            experience = {
                'company': exp.get('companyName', ''),
                'title': exp.get('title', ''),
                'description': exp.get('description', ''),
                'location': exp.get('location', ''),
                'date_from': self._parse_date(exp.get('startDate')),
                'date_to': self._parse_date(exp.get('endDate')),
                'is_current': exp.get('endDate') is None
            }
            experiences.append(experience)
            
        # Extract education
        educations = []
        yale_affiliations = []
        
        for edu in raw_data.get('education', []):
            school_name = edu.get('schoolName', '')
            
            education = {
                'institution': school_name,
                'degree': edu.get('degree', ''),
                'field_of_study': edu.get('fieldOfStudy', ''),
                'title': f"{edu.get('degree', '')} in {edu.get('fieldOfStudy', '')} from {school_name}".strip(),
                'date_from': self._parse_date(edu.get('startDate')),
                'date_to': self._parse_date(edu.get('endDate')),
                'activities': edu.get('activities', '')
            }
            educations.append(education)
            
            # Check if this is Yale education
            if 'yale' in school_name.lower():
                yale_affiliation = self._extract_yale_affiliation(edu)
                if yale_affiliation:
                    yale_affiliations.append(yale_affiliation)
                    
        # Extract skills
        skills = []
        for skill in raw_data.get('skills', []):
            skills.append({
                'skill_name': skill.get('name', skill) if isinstance(skill, dict) else str(skill),
                'endorsement_count': skill.get('endorsementCount', 0) if isinstance(skill, dict) else 0
            })
            
        return {
            'person': person_data,
            'experiences': experiences,
            'educations': educations,
            'yale_affiliations': yale_affiliations,
            'skills': skills
        }
        
    def _parse_date(self, date_info: Any) -> datetime:
        """Parse various date formats"""
        if not date_info:
            return None
            
        if isinstance(date_info, dict):
            year = date_info.get('year')
            month = date_info.get('month', 1)
            day = date_info.get('day', 1)
            if year:
                return datetime(year, month, day)
        elif isinstance(date_info, str):
            try:
                return datetime.strptime(date_info, '%Y-%m-%d')
            except:
                try:
                    return datetime.strptime(date_info, '%Y')
                except:
                    pass
                    
        return None
        
    def _extract_yale_affiliation(self, education_data: Dict) -> Dict:
        """Extract Yale-specific affiliation information"""
        school_name = education_data.get('schoolName', '')
        degree = education_data.get('degree', '')
        
        affiliation = {
            'school': school_name,
            'affiliation_type': 'alumni'  # Default
        }
        
        # Determine affiliation type based on degree
        if 'BA' in degree or 'BS' in degree or 'Bachelor' in degree:
            affiliation['affiliation_type'] = 'undergraduate'
        elif 'MA' in degree or 'MS' in degree or 'MBA' in degree or 'PhD' in degree:
            affiliation['affiliation_type'] = 'graduate'
            
        # Extract class year
        end_date = education_data.get('endDate')
        if end_date:
            if isinstance(end_date, dict):
                affiliation['class_year'] = end_date.get('year')
            elif isinstance(end_date, str):
                try:
                    affiliation['class_year'] = int(end_date[:4])
                except:
                    pass
                    
        # Extract activities/organizations
        activities = education_data.get('activities', '')
        if activities:
            affiliation['clubs_organizations'] = activities
            
        return affiliation
        
    def import_to_database(self, db_session: Session, batch_size: int = 100):
        """Import data from S3 into database"""
        key = 'brightdata/education_yale/milo_20250529_110131.json'
        
        logger.info(f"Starting import from s3://{self.bucket_name}/{key}")
        
        count = 0
        batch = []
        
        try:
            for raw_person in self.stream_json_from_s3(key):
                parsed_data = self.parse_person_data(raw_person)
                
                # Create person object
                person = Person(**parsed_data['person'])
                
                # Add related data
                for exp_data in parsed_data['experiences']:
                    exp = Experience(**exp_data)
                    person.experiences.append(exp)
                    
                for edu_data in parsed_data['educations']:
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
                    count += len(batch)
                    logger.info(f"Imported {count} people")
                    batch = []
                    
            # Commit remaining
            if batch:
                db_session.add_all(batch)
                db_session.commit()
                count += len(batch)
                
            logger.info(f"Import completed. Total people imported: {count}")
            
        except Exception as e:
            logger.error(f"Import failed: {e}")
            db_session.rollback()
            raise
            
            
def download_sample_data(output_file: str = 'sample_yale_data.json', 
                        sample_size: int = 10):
    """Download a sample of the data for local testing"""
    loader = S3DataLoader()
    key = 'brightdata/education_yale/milo_20250529_110131.json'
    
    samples = []
    for i, person in enumerate(loader.stream_json_from_s3(key)):
        samples.append(person)
        if i >= sample_size - 1:
            break
            
    with open(output_file, 'w') as f:
        json.dump(samples, f, indent=2)
        
    print(f"Downloaded {len(samples)} samples to {output_file}")