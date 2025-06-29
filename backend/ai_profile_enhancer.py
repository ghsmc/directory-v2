#!/usr/bin/env python3
"""
AI-powered profile enhancement using ChatGPT
Generates one-sentence summaries + structured bullet points for Yale alumni
"""

import sys
import os
import openai
import json
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import time

sys.path.append('.')

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://georgemccain@localhost:5432/yale_network")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class AIProfileEnhancer:
    """Enhance Yale alumni profiles with AI-generated summaries"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.db = SessionLocal()
    
    def enhance_profile(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-enhanced profile with summary and bullet points"""
        
        # Prepare profile context for AI
        context = self._prepare_profile_context(person_data)
        
        # Generate AI summary
        ai_summary = self._generate_ai_summary(context)
        
        # Add AI enhancements to person data
        enhanced_profile = person_data.copy()
        enhanced_profile.update(ai_summary)
        
        return enhanced_profile
    
    def _prepare_profile_context(self, person_data: Dict[str, Any]) -> str:
        """Prepare profile context for AI processing"""
        
        context_parts = []
        
        # Basic info
        name = person_data.get('name', 'Unknown')
        headline = person_data.get('headline', '')
        location = person_data.get('location', '')
        
        context_parts.append(f"Name: {name}")
        if headline:
            context_parts.append(f"Current Role: {headline}")
        if location:
            context_parts.append(f"Location: {location}")
        
        # Yale affiliation and major
        yale_school = person_data.get('yale_school', 'Yale University')
        major = person_data.get('major', '')
        if major:
            context_parts.append(f"Yale Affiliation: {yale_school}, Major: {major}")
        else:
            context_parts.append(f"Yale Affiliation: {yale_school}")
        
        # Work experience
        current_title = person_data.get('current_title', '')
        current_company = person_data.get('current_company', '')
        if current_title and current_company:
            context_parts.append(f"Current Position: {current_title} at {current_company}")
        
        # Additional context from experience if available
        experience = person_data.get('experience_summary', '')
        if experience:
            context_parts.append(f"Experience: {experience}")
        
        return "\\n".join(context_parts)
    
    def _generate_ai_summary(self, context: str) -> Dict[str, Any]:
        """Generate AI summary using ChatGPT"""
        
        prompt = f"""
        Create a professional profile summary for this Yale alumni. Format as JSON with:
        1. "summary": One engaging sentence highlighting their key professional focus/achievement
        2. "education_focus": Yale school/degree/major + other notable education (if any)
        3. "work_focus": Career trajectory, current role, key companies/industries
        4. "notable_highlights": Unique achievements, expertise areas, or interesting background
        
        Keep each bullet point concise (under 100 characters). Focus on professional accomplishments.
        Include their major/field of study if available.
        
        Profile Context:
        {context}
        
        Return only valid JSON:
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {"role": "system", "content": "You are a professional profile writer specializing in Yale alumni bios. Create concise, engaging professional summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Parse AI response
            ai_content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if ai_content.startswith('```json'):
                ai_content = ai_content.replace('```json', '').replace('```', '').strip()
            elif ai_content.startswith('```'):
                ai_content = ai_content.replace('```', '').strip()
            
            # Parse JSON response
            ai_summary = json.loads(ai_content)
            
            return {
                'ai_summary': ai_summary.get('summary', ''),
                'ai_education_focus': ai_summary.get('education_focus', ''),
                'ai_work_focus': ai_summary.get('work_focus', ''),
                'ai_notable_highlights': ai_summary.get('notable_highlights', ''),
                'ai_enhanced': True
            }
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error for profile: {e}")
            return self._fallback_summary(context)
        except Exception as e:
            print(f"⚠️  AI generation error: {e}")
            return self._fallback_summary(context)
    
    def _fallback_summary(self, context: str) -> Dict[str, Any]:
        """Generate fallback summary if AI fails"""
        
        lines = context.split('\\n')
        name = "Yale alumni"
        role = "Professional"
        
        for line in lines:
            if line.startswith('Name:'):
                name = line.replace('Name:', '').strip()
            elif line.startswith('Current Role:'):
                role = line.replace('Current Role:', '').strip()
        
        return {
            'ai_summary': f"{name} is a {role} and Yale alumni.",
            'ai_education_focus': "Yale University graduate",
            'ai_work_focus': role if role != "Professional" else "Various professional roles",
            'ai_notable_highlights': "Yale University education",
            'ai_enhanced': False
        }
    
    def enhance_batch(self, profiles: List[Dict[str, Any]], batch_size: int = 10) -> List[Dict[str, Any]]:
        """Enhance multiple profiles in batches"""
        
        enhanced_profiles = []
        total_profiles = len(profiles)
        
        print(f"🤖 Enhancing {total_profiles} profiles with AI...")
        
        for i in range(0, total_profiles, batch_size):
            batch = profiles[i:i + batch_size]
            
            print(f"   Processing batch {i//batch_size + 1}/{(total_profiles-1)//batch_size + 1}...")
            
            for profile in batch:
                enhanced_profile = self.enhance_profile(profile)
                enhanced_profiles.append(enhanced_profile)
                
                # Small delay to respect rate limits
                time.sleep(0.1)
            
            # Longer delay between batches
            if i + batch_size < total_profiles:
                time.sleep(1)
        
        print(f"✅ Enhanced {len(enhanced_profiles)} profiles")
        return enhanced_profiles
    
    def get_sample_profiles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get sample profiles from database for testing"""
        
        query = text("""
            SELECT DISTINCT 
                p.full_name as name,
                p.headline,
                p.location,
                ya.school as yale_school,
                ya.major,
                e.title as current_title,
                e.company as current_company
            FROM people p
            JOIN yale_affiliations ya ON ya.person_uuid = p.uuid_id
            LEFT JOIN experience e ON e.person_uuid = p.uuid_id AND e.is_current = true
            WHERE p.headline IS NOT NULL AND p.headline != ''
            LIMIT :limit
        """)
        
        results = self.db.execute(query, {'limit': limit}).fetchall()
        
        profiles = []
        for result in results:
            profile = {
                'name': result.name,
                'headline': result.headline,
                'location': result.location,
                'yale_school': result.yale_school,
                'major': getattr(result, 'major', '') or '',
                'current_title': result.current_title or '',
                'current_company': result.current_company or ''
            }
            profiles.append(profile)
        
        return profiles
    
    def display_enhanced_profile(self, profile: Dict[str, Any]):
        """Display enhanced profile in a clean format"""
        
        print(f"\\n{profile['name']}")
        print(f"{profile.get('ai_summary', 'No summary available')}")
        print(f"")
        
        # Clean bullet points without labels
        education = profile.get('ai_education_focus', '')
        work = profile.get('ai_work_focus', '')
        highlights = profile.get('ai_notable_highlights', '')
        
        if education and education != 'N/A':
            print(f"• {education}")
        if work and work != 'N/A':
            print(f"• {work}")
        if highlights and highlights != 'N/A':
            print(f"• {highlights}")
        
        print(f"")
        print("-" * 60)
    
    def close(self):
        """Close database connection"""
        self.db.close()

def test_ai_enhancement():
    """Test AI profile enhancement on sample data"""
    
    print("🤖 TESTING AI PROFILE ENHANCEMENT")
    print("=" * 60)
    
    enhancer = AIProfileEnhancer()
    
    try:
        # Get sample profiles
        print("📋 Getting sample profiles...")
        sample_profiles = enhancer.get_sample_profiles(limit=5)
        
        if not sample_profiles:
            print("❌ No profiles found in database")
            return
        
        print(f"✅ Found {len(sample_profiles)} sample profiles")
        
        # Enhance profiles with AI
        enhanced_profiles = enhancer.enhance_batch(sample_profiles)
        
        # Display results
        print(f"\\n🎯 AI-ENHANCED YALE ALUMNI PROFILES:")
        print("=" * 60)
        
        for profile in enhanced_profiles:
            enhancer.display_enhanced_profile(profile)
        
        # Cost estimation
        total_tokens_used = len(enhanced_profiles) * 200  # Rough estimate
        estimated_cost = total_tokens_used * 0.00015 / 1000  # GPT-4o-mini pricing
        
        print(f"\\n💰 COST ESTIMATION:")
        print(f"   Profiles enhanced: {len(enhanced_profiles)}")
        print(f"   Estimated tokens: {total_tokens_used:,}")
        print(f"   Estimated cost: ${estimated_cost:.4f}")
        print(f"   For 50K profiles: ~${estimated_cost * 10000:.2f}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        enhancer.close()

if __name__ == "__main__":
    test_ai_enhancement()