"""
Data Enrichment System
Extracts and structures rich information from headlines and creates virtual experience/education records
"""

import psycopg2
import re
import json
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class DataEnricher:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        
    def extract_experience_from_headline(self, headline: str) -> List[Dict]:
        """Extract work experience information from rich headlines"""
        experiences = []
        
        # Pattern for current roles
        current_patterns = [
            r'(?:Currently\s+)?(?:Current\s+)?(\w+(?:\s+\w+)*)\s+at\s+([^|•▪️,]+)',
            r'(\w+(?:\s+\w+)*)\s+@\s+([^|•▪️,]+)',
            r'(\w+(?:\s+\w+)*)\s+\|\s+([^|•▪️,]+)',
            r'(\w+(?:\s+\w+)*),\s+([^|•▪️,]+)',
        ]
        
        # Pattern for former roles
        former_patterns = [
            r'(?:Former|Ex-|Previously)\s+(\w+(?:\s+\w+)*)\s+(?:at\s+)?([^|•▪️,]+)',
            r'(?:Former|Ex-|Previously)\s+([^|•▪️,]+)',
        ]
        
        # Pattern for founder/co-founder
        founder_patterns = [
            r'(?:Co-)?Founder(?:\s+(?:&|and)\s+\w+)?\s+(?:at\s+|@\s+)?([^|•▪️,]+)',
            r'(?:Co-)?Founder(?:\s+(?:&|and)\s+\w+)?\s+([^|•▪️,]+)',
        ]
        
        # Extract current roles
        for pattern in current_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    title = match.group(1).strip()
                    company = match.group(2).strip()
                    experiences.append({
                        'title': title,
                        'company': company,
                        'is_current': True,
                        'type': 'current'
                    })
        
        # Extract founder roles
        for pattern in founder_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                company = match.group(1).strip()
                experiences.append({
                    'title': 'Founder' if 'Co-' not in match.group(0) else 'Co-Founder',
                    'company': company,
                    'is_current': True,
                    'type': 'founder'
                })
        
        # Extract former roles
        for pattern in former_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 2:
                    title = match.group(1).strip()
                    company = match.group(2).strip()
                else:
                    title = match.group(1).strip()
                    company = ''
                    
                experiences.append({
                    'title': title,
                    'company': company,
                    'is_current': False,
                    'type': 'former'
                })
        
        return experiences
    
    def extract_education_from_headline(self, headline: str) -> List[Dict]:
        """Extract education information from headlines"""
        education = []
        
        # Pattern for degrees
        degree_patterns = [
            r'(PhD|Ph\.D\.?|Doctorate)\s+(?:in\s+)?([^|•▪️,]+)',
            r'(MBA|M\.B\.A\.?)\s+(?:from\s+)?([^|•▪️,]+)',
            r'(MS|M\.S\.?|Master\'?s?)\s+(?:in\s+)?([^|•▪️,]+)',
            r'(BS|B\.S\.?|Bachelor\'?s?)\s+(?:in\s+)?([^|•▪️,]+)',
            r'(JD|J\.D\.?|Law\s+Degree)\s+(?:from\s+)?([^|•▪️,]+)',
            r'(MD|M\.D\.?)\s+(?:from\s+)?([^|•▪️,]+)',
        ]
        
        # Pattern for universities
        yale_patterns = [
            r'Yale\s+([^|•▪️,]+)',
            r'([^|•▪️,]*)\s+at\s+Yale',
            r'Yale\s+University',
            r'Yale\s+College',
            r'Yale\s+Law\s+School',
            r'Yale\s+School\s+of\s+Medicine',
            r'Yale\s+MBA',
        ]
        
        # Extract degrees
        for pattern in degree_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                degree = match.group(1)
                field = match.group(2).strip() if len(match.groups()) >= 2 else ''
                education.append({
                    'degree': degree,
                    'field_of_study': field,
                    'institution': 'Unknown',
                    'type': 'degree'
                })
        
        # Extract Yale connections
        for pattern in yale_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) >= 1 and match.group(1):
                    program = match.group(1).strip()
                else:
                    program = 'General Studies'
                    
                education.append({
                    'degree': 'Unknown',
                    'field_of_study': program,
                    'institution': 'Yale University',
                    'type': 'yale'
                })
        
        return education
    
    def extract_skills_from_headline(self, headline: str) -> List[str]:
        """Extract skills and specialties from headlines"""
        skills = []
        
        # Common skill patterns
        skill_patterns = [
            r'(?:experience\s+(?:in|with)\s+)([^|•▪️,]+)',
            r'(?:skilled\s+in\s+)([^|•▪️,]+)',
            r'(?:specializing\s+in\s+)([^|•▪️,]+)',
            r'(?:expert\s+in\s+)([^|•▪️,]+)',
        ]
        
        # Technology skills
        tech_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'MATLAB', 'R', 'SQL',
            'Machine Learning', 'AI', 'Artificial Intelligence', 'Data Science',
            'Deep Learning', 'Computer Vision', 'NLP', 'Natural Language Processing',
            'React', 'Node.js', 'AWS', 'Docker', 'Kubernetes',
            'VLSI', 'Verilog', 'VHDL', 'FPGA'
        ]
        
        # Business skills
        business_skills = [
            'Project Management', 'Leadership', 'Strategy', 'Consulting',
            'Marketing', 'Sales', 'Finance', 'Operations', 'Analytics'
        ]
        
        # Extract from patterns
        for pattern in skill_patterns:
            matches = re.finditer(pattern, headline, re.IGNORECASE)
            for match in matches:
                skill = match.group(1).strip()
                skills.append(skill)
        
        # Find mentioned tech skills
        for skill in tech_skills:
            if skill.lower() in headline.lower():
                skills.append(skill)
        
        # Find mentioned business skills
        for skill in business_skills:
            if skill.lower() in headline.lower():
                skills.append(skill)
        
        return list(set(skills))  # Remove duplicates
    
    def enrich_profile_data(self, person_id: str, headline: str) -> Dict:
        """Enrich a single profile with extracted data"""
        experiences = self.extract_experience_from_headline(headline)
        education = self.extract_education_from_headline(headline)
        skills = self.extract_skills_from_headline(headline)
        
        return {
            'person_id': person_id,
            'experiences': experiences,
            'education': education,
            'skills': skills,
            'enrichment_source': 'headline_extraction'
        }
    
    def process_all_rich_profiles(self, limit: int = None):
        """Process all profiles with rich headlines"""
        cur = self.conn.cursor()
        
        # Get profiles with substantial headlines
        query = "SELECT uuid_id, full_name, headline FROM people WHERE length(headline) > 30"
        if limit:
            query += f" LIMIT {limit}"
        
        cur.execute(query)
        profiles = cur.fetchall()
        
        enriched_data = []
        
        for uuid_id, name, headline in profiles:
            enrichment = self.enrich_profile_data(str(uuid_id), headline)
            enrichment['name'] = name
            enrichment['headline'] = headline
            enriched_data.append(enrichment)
        
        return enriched_data
    
    def create_virtual_experience_table(self):
        """Create a virtual experience view from enriched headline data"""
        cur = self.conn.cursor()
        
        # Create a function to extract experience data
        create_function_sql = """
        CREATE OR REPLACE FUNCTION extract_experiences_from_headline(headline TEXT)
        RETURNS TABLE(
            title TEXT,
            company TEXT,
            is_current BOOLEAN,
            experience_type TEXT
        ) AS $$
        BEGIN
            -- This is a simplified version - in practice, we'd use the Python enricher
            RETURN QUERY
            SELECT 
                regexp_replace(split_part(headline, ' at ', 1), '^.*\\s', '') as title,
                split_part(split_part(headline, ' at ', 2), '|', 1) as company,
                NOT (headline ~* 'former|ex-|previously') as is_current,
                CASE 
                    WHEN headline ~* 'founder' THEN 'founder'
                    WHEN headline ~* 'former|ex-|previously' THEN 'former'
                    ELSE 'current'
                END as experience_type
            WHERE headline ~* '\\sat\\s|\\s@\\s|founder';
        END;
        $$ LANGUAGE plpgsql;
        """
        
        try:
            cur.execute(create_function_sql)
            self.conn.commit()
            print("✅ Created experience extraction function")
        except Exception as e:
            print(f"Error creating function: {e}")
            self.conn.rollback()
    
    def generate_sample_report(self, limit: int = 20):
        """Generate a sample report of enriched data"""
        enriched_data = self.process_all_rich_profiles(limit)
        
        print(f"=== DATA ENRICHMENT REPORT ===")
        print(f"Processed {len(enriched_data)} profiles")
        
        total_experiences = sum(len(p['experiences']) for p in enriched_data)
        total_education = sum(len(p['education']) for p in enriched_data)
        total_skills = sum(len(p['skills']) for p in enriched_data)
        
        print(f"Extracted {total_experiences} experience records")
        print(f"Extracted {total_education} education records")
        print(f"Extracted {total_skills} skills")
        
        print(f"\n=== SAMPLE ENRICHED PROFILES ===")
        for i, profile in enumerate(enriched_data[:5]):
            print(f"\n{i+1}. {profile['name']}")
            print(f"   Headline: {profile['headline']}")
            if profile['experiences']:
                print(f"   Experiences:")
                for exp in profile['experiences']:
                    current = "Current" if exp['is_current'] else "Former"
                    print(f"     • {current}: {exp['title']} at {exp['company']}")
            if profile['education']:
                print(f"   Education:")
                for edu in profile['education']:
                    print(f"     • {edu['degree']} in {edu['field_of_study']} at {edu['institution']}")
            if profile['skills']:
                print(f"   Skills: {', '.join(profile['skills'][:5])}{'...' if len(profile['skills']) > 5 else ''}")
        
        return enriched_data

def main():
    enricher = DataEnricher()
    enriched_data = enricher.generate_sample_report(50)
    
    # Save to JSON for further analysis
    with open('/Users/georgemccain/Desktop/untitled folder 4/yale-network-search/backend/enriched_data_sample.json', 'w') as f:
        json.dump(enriched_data, f, indent=2, default=str)
    
    print(f"\n✅ Saved enriched data sample to enriched_data_sample.json")

if __name__ == "__main__":
    main()