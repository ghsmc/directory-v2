#!/usr/bin/env python3
"""
Batch AI Enhancement for Yale Network Search
Processes all 14K+ profiles to add AI-generated summaries and tags
"""

import os
import sys
import json
import time
import openai
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_enhancement.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class BatchAIEnhancer:
    """Batch AI enhancement for all Yale profiles"""
    
    def __init__(self, batch_size: int = 20):
        self.engine = create_engine(DATABASE_URL)
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.batch_size = batch_size
        self.processed_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        
        # Yale-specific categories for tagging
        self.yale_categories = [
            "Undergraduate Student", "Graduate Student", "PhD Student", "Medical Student",
            "Law Student", "Business Student", "Current Student", "Recent Graduate",
            "Alumni", "Faculty", "Researcher", "Visiting Scholar", "Postdoc",
            "Data Science", "Computer Science", "Medicine", "Law", "Business",
            "Economics", "Psychology", "Biology", "Chemistry", "Physics",
            "Engineering", "Environmental Science", "Public Health", "Policy",
            "Consulting", "Finance", "Tech", "Healthcare", "Academia",
            "Entrepreneurship", "Nonprofit", "Government", "Research",
            "Yale College", "Yale Graduate School", "Yale Law School", 
            "Yale School of Medicine", "Yale School of Management",
            "Yale School of Public Health", "Yale School of Environment",
            "Yale Divinity School", "Yale School of Art", "Yale School of Music"
        ]
    
    def get_unprocessed_profiles(self, limit: int = None) -> List[Dict]:
        """Get profiles that haven't been AI processed yet"""
        
        query = """
        SELECT 
            p.uuid_id,
            p.full_name,
            p.headline,
            p.location,
            p.summary,
            ya.school as yale_school,
            ya.major,
            ya.class_year,
            ya.affiliation_type
        FROM people p
        JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
        WHERE p.ai_processed = FALSE OR p.ai_processed IS NULL
        ORDER BY p.created_at DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        with self.engine.connect() as conn:
            results = conn.execute(text(query)).fetchall()
            
            profiles = []
            for result in results:
                profile = {
                    'uuid_id': result.uuid_id,
                    'name': result.full_name,
                    'headline': result.headline or '',
                    'location': result.location or '',
                    'summary': result.summary or '',
                    'yale_school': result.yale_school or '',
                    'major': result.major or '',
                    'class_year': result.class_year,
                    'affiliation_type': result.affiliation_type or ''
                }
                profiles.append(profile)
            
            return profiles
    
    def generate_ai_enhancement(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI summary and tags for a single profile"""
        
        # Prepare context
        context = self._prepare_context(profile)
        
        prompt = f"""
        Analyze this Yale community member's profile and generate:
        
        1. "summary": A single, engaging sentence (under 150 characters) that captures their key focus/achievement
        2. "tags": An array of 3-6 relevant tags from these categories:
           {', '.join(self.yale_categories[:20])}  # First 20 categories
           
        Focus on their current role, field of study, career level, and Yale affiliation.
        
        Profile Context:
        {context}
        
        Return only valid JSON:
        {{
            "summary": "One engaging sentence about this person",
            "tags": ["tag1", "tag2", "tag3", "tag4"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert at creating concise, professional summaries for Yale community members. Focus on their academic/professional achievements and current focus."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3  # Lower temperature for more consistent results
            )
            
            # Parse response
            ai_content = response.choices[0].message.content.strip()
            
            # Clean up markdown if present
            if ai_content.startswith('```json'):
                ai_content = ai_content.replace('```json', '').replace('```', '').strip()
            elif ai_content.startswith('```'):
                ai_content = ai_content.replace('```', '').strip()
            
            # Parse JSON
            ai_result = json.loads(ai_content)
            
            return {
                'ai_summary': ai_result.get('summary', '')[:500],  # Limit length
                'ai_tags': ai_result.get('tags', [])[:8],  # Limit to 8 tags max
                'ai_enhanced': True
            }
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing error for {profile['name']}: {e}")
            return self._fallback_enhancement(profile)
        except Exception as e:
            logger.error(f"AI generation error for {profile['name']}: {e}")
            return self._fallback_enhancement(profile)
    
    def _prepare_context(self, profile: Dict[str, Any]) -> str:
        """Prepare profile context for AI processing"""
        
        context_parts = []
        
        # Basic info
        context_parts.append(f"Name: {profile['name']}")
        
        if profile['headline']:
            context_parts.append(f"Headline: {profile['headline']}")
        
        if profile['location']:
            context_parts.append(f"Location: {profile['location']}")
        
        # Yale info
        if profile['yale_school']:
            context_parts.append(f"Yale School: {profile['yale_school']}")
        
        if profile['major']:
            context_parts.append(f"Major: {profile['major']}")
        
        if profile['class_year']:
            context_parts.append(f"Class Year: {profile['class_year']}")
        
        if profile['affiliation_type']:
            context_parts.append(f"Affiliation: {profile['affiliation_type']}")
        
        if profile['summary']:
            context_parts.append(f"Summary: {profile['summary'][:200]}")  # Limit summary length
        
        return "\n".join(context_parts)
    
    def _fallback_enhancement(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback enhancement if AI fails"""
        
        # Simple rule-based enhancement
        name = profile['name']
        headline = profile['headline'].lower() if profile['headline'] else ''
        school = profile['yale_school']
        
        # Generate basic summary
        if 'student' in headline:
            summary = f"{name} is a student at {school}"
        elif 'professor' in headline or 'faculty' in headline:
            summary = f"{name} is faculty at {school}"
        elif 'research' in headline:
            summary = f"{name} is a researcher at {school}"
        else:
            summary = f"{name} is affiliated with {school}"
        
        # Generate basic tags
        tags = ["Yale University"]
        
        if 'student' in headline:
            tags.append("Current Student")
        if 'graduate' in headline or 'phd' in headline:
            tags.append("Graduate Student")
        if 'medical' in headline or 'medicine' in headline:
            tags.extend(["Medicine", "Yale School of Medicine"])
        if 'law' in headline:
            tags.extend(["Law", "Yale Law School"])
        if 'business' in headline or 'management' in headline:
            tags.extend(["Business", "Yale School of Management"])
        if 'data' in headline and 'science' in headline:
            tags.append("Data Science")
        if 'computer' in headline:
            tags.append("Computer Science")
        
        return {
            'ai_summary': summary[:500],
            'ai_tags': list(set(tags))[:6],  # Remove duplicates and limit
            'ai_enhanced': False
        }
    
    def save_enhancement(self, profile_uuid: str, enhancement: Dict[str, Any]) -> bool:
        """Save AI enhancement to database"""
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE people 
                    SET 
                        ai_summary = :summary,
                        ai_tags = :tags,
                        ai_processed = TRUE,
                        ai_processed_at = CURRENT_TIMESTAMP
                    WHERE uuid_id = :uuid_id
                """), {
                    'summary': enhancement['ai_summary'],
                    'tags': json.dumps(enhancement['ai_tags']),
                    'uuid_id': profile_uuid
                })
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Database save error for {profile_uuid}: {e}")
            return False
    
    def process_batch(self, profiles: List[Dict[str, Any]]) -> int:
        """Process a batch of profiles"""
        
        successful = 0
        
        for profile in profiles:
            try:
                # Generate AI enhancement
                enhancement = self.generate_ai_enhancement(profile)
                
                # Save to database
                if self.save_enhancement(profile['uuid_id'], enhancement):
                    successful += 1
                    self.processed_count += 1
                    
                    logger.info(f"✅ Enhanced {profile['name']} ({self.processed_count} total)")
                    
                    # Log the enhancement for review
                    if enhancement['ai_enhanced']:
                        logger.info(f"   Summary: {enhancement['ai_summary']}")
                        logger.info(f"   Tags: {enhancement['ai_tags']}")
                else:
                    self.error_count += 1
                
                # Small delay to respect rate limits
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Failed to process {profile['name']}: {e}")
                self.error_count += 1
        
        return successful
    
    def run_batch_enhancement(self, max_profiles: int = None):
        """Run batch AI enhancement on all unprocessed profiles"""
        
        logger.info("🤖 STARTING BATCH AI ENHANCEMENT")
        logger.info("=" * 60)
        
        # Get total count
        with self.engine.connect() as conn:
            total_unprocessed = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM people 
                WHERE ai_processed = FALSE OR ai_processed IS NULL
            """)).fetchone().count
        
        logger.info(f"📊 Found {total_unprocessed:,} unprocessed profiles")
        
        if max_profiles and max_profiles < total_unprocessed:
            total_unprocessed = max_profiles
            logger.info(f"🎯 Processing {max_profiles:,} profiles (limited)")
        
        # Process in batches
        processed_total = 0
        
        while processed_total < total_unprocessed:
            # Get next batch
            remaining = total_unprocessed - processed_total
            current_batch_size = min(self.batch_size, remaining)
            
            profiles = self.get_unprocessed_profiles(limit=current_batch_size)
            
            if not profiles:
                logger.info("✅ No more profiles to process")
                break
            
            logger.info(f"\n🔄 Processing batch of {len(profiles)} profiles...")
            
            # Process batch
            successful = self.process_batch(profiles)
            processed_total += len(profiles)
            
            # Progress update
            elapsed = datetime.now() - self.start_time
            rate = self.processed_count / elapsed.total_seconds() if elapsed.total_seconds() > 0 else 0
            
            logger.info(f"📈 Progress: {processed_total:,}/{total_unprocessed:,} ({processed_total/total_unprocessed*100:.1f}%)")
            logger.info(f"⚡ Rate: {rate:.1f} profiles/sec | Errors: {self.error_count}")
            
            # Longer delay between batches
            time.sleep(1)
        
        # Final summary
        elapsed = datetime.now() - self.start_time
        
        logger.info(f"\n🎉 BATCH ENHANCEMENT COMPLETE!")
        logger.info(f"✅ Successfully processed: {self.processed_count:,}")
        logger.info(f"❌ Errors: {self.error_count}")
        logger.info(f"⏱️  Total time: {elapsed}")
        logger.info(f"💰 Estimated cost: ${self.processed_count * 0.0002:.2f}")

def main():
    """Main function with command line options"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch AI Enhancement for Yale Network')
    parser.add_argument('--limit', type=int, help='Limit number of profiles to process')
    parser.add_argument('--batch-size', type=int, default=20, help='Batch size for processing')
    parser.add_argument('--test', action='store_true', help='Test mode (process only 5 profiles)')
    
    args = parser.parse_args()
    
    if args.test:
        args.limit = 5
        logger.info("🧪 Running in TEST MODE")
    
    enhancer = BatchAIEnhancer(batch_size=args.batch_size)
    enhancer.run_batch_enhancement(max_profiles=args.limit)

if __name__ == "__main__":
    main()