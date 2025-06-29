#!/usr/bin/env python3
"""Test loading real Yale data from S3"""

import sys
import os
sys.path.append('.')

from app.data_loader.s3_loader import S3DataLoader
import json

def test_data_loading():
    """Test data loading from S3"""
    
    try:
        # Initialize loader (will use default AWS credentials)
        loader = S3DataLoader()
        print("✓ S3 connection established")
        
        # Test streaming a small sample
        key = 'brightdata/education_yale/milo_20250529_110131.json'
        print(f"Streaming data from {key}...")
        
        count = 0
        sample_records = []
        
        for record in loader.stream_json_from_s3(key):
            sample_records.append(record)
            count += 1
            
            if count >= 5:  # Just get first 5 records for testing
                break
                
        print(f"✓ Successfully streamed {count} records")
        
        # Show sample record structure
        if sample_records:
            first_record = sample_records[0]
            print(f"\nSample record structure:")
            print(f"  Name: {first_record.get('name', 'N/A')}")
            print(f"  Location: {first_record.get('location', {}).get('name', 'N/A')}")
            print(f"  Education entries: {len(first_record.get('education', []))}")
            print(f"  Experience entries: {len(first_record.get('experience', []))}")
            
            # Check for Yale education
            yale_education = [
                edu for edu in first_record.get('education', [])
                if 'yale' in edu.get('schoolName', '').lower()
            ]
            
            if yale_education:
                print(f"\n  Yale Education Found:")
                for edu in yale_education:
                    print(f"    - {edu.get('schoolName')} ({edu.get('degree', 'N/A')})")
                    
            # Test parsing
            print(f"\nTesting data parsing...")
            parsed = loader.parse_person_data(first_record)
            print(f"  Parsed person: {parsed['person']['full_name']}")
            print(f"  Experiences: {len(parsed['experiences'])}")
            print(f"  Educations: {len(parsed['educations'])}")
            print(f"  Yale affiliations: {len(parsed['yale_affiliations'])}")
            
        # Save sample for inspection
        with open('real_yale_sample.json', 'w') as f:
            json.dump(sample_records, f, indent=2)
            
        print(f"\n✓ Saved {len(sample_records)} sample records to real_yale_sample.json")
        print("✓ Data loading test successful!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_loading()