#!/usr/bin/env python3
"""Download a sample of Yale data to understand the format"""

import boto3
import json

def download_sample():
    """Download first 1MB of data to understand format"""
    
    # Use default AWS credentials
    s3 = boto3.client('s3', region_name='us-east-2')
    bucket_name = 'people-data-yale-2025'
    key = 'brightdata/education_yale/milo_20250529_110131.json'
    
    try:
        # Download first 1MB
        response = s3.get_object(
            Bucket=bucket_name,
            Key=key,
            Range='bytes=0-1048576'  # First 1MB
        )
        
        content = response['Body'].read().decode('utf-8')
        
        # Save to file
        with open('yale_sample_1mb.json', 'w') as f:
            f.write(content)
            
        print(f"Downloaded {len(content)} characters to yale_sample_1mb.json")
        
        # Analyze the format
        print("\nAnalyzing format...")
        
        if content.strip().startswith('['):
            print("✓ Detected JSON array format")
            
            # Try to find the end of the first complete record
            bracket_count = 0
            in_string = False
            escape_next = False
            first_record_end = -1
            
            for i, char in enumerate(content):
                if escape_next:
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                    
                if not in_string:
                    if char == '{':
                        bracket_count += 1
                    elif char == '}':
                        bracket_count -= 1
                        if bracket_count == 0:  # Found end of first record
                            first_record_end = i + 1
                            break
                            
            if first_record_end > 0:
                # Extract first record
                start_pos = content.find('{')
                first_record_json = content[start_pos:first_record_end]
                
                try:
                    first_record = json.loads(first_record_json)
                    print(f"✓ Successfully parsed first record")
                    
                    # Show structure
                    print(f"  Name: {first_record.get('name', 'N/A')}")
                    print(f"  Education entries: {len(first_record.get('education', []))}")
                    print(f"  Experience entries: {len(first_record.get('experience', []))}")
                    
                    # Save first record
                    with open('first_record.json', 'w') as f:
                        json.dump(first_record, f, indent=2)
                    print("✓ Saved first record to first_record.json")
                    
                except json.JSONDecodeError as e:
                    print(f"✗ Failed to parse first record: {e}")
            else:
                print("✗ Could not find complete first record in sample")
                
        else:
            print("✓ Detected JSONL (newline-delimited) format")
            lines = content.split('\n')
            print(f"  Found {len(lines)} lines in sample")
            
            if lines and lines[0].strip():
                try:
                    first_record = json.loads(lines[0])
                    print(f"✓ Successfully parsed first line")
                    print(f"  Name: {first_record.get('name', 'N/A')}")
                    
                    with open('first_record.json', 'w') as f:
                        json.dump(first_record, f, indent=2)
                    print("✓ Saved first record to first_record.json")
                    
                except json.JSONDecodeError as e:
                    print(f"✗ Failed to parse first line: {e}")
                    
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    download_sample()