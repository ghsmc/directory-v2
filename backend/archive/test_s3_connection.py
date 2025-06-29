#!/usr/bin/env python3
"""Test S3 connection and download sample data"""

import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_s3_connection():
    """Test connection to S3 and list objects"""
    
    # Get credentials
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key or not aws_secret_key:
        print("Error: AWS credentials not found in environment variables")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return
        
    # Create S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name='us-east-2'
    )
    
    bucket_name = 'people-data-yale-2025'
    key = 'brightdata/education_yale/milo_20250529_110131.json'
    
    try:
        # Test connection by getting object metadata
        response = s3.head_object(Bucket=bucket_name, Key=key)
        print(f"✓ Successfully connected to S3")
        print(f"✓ Found file: {key}")
        print(f"  Size: {response['ContentLength'] / (1024**3):.2f} GB")
        print(f"  Last modified: {response['LastModified']}")
        
        # Download first 1MB as sample
        print("\nDownloading sample data...")
        response = s3.get_object(
            Bucket=bucket_name, 
            Key=key,
            Range='bytes=0-1048576'  # First 1MB
        )
        
        # Parse sample data
        content = response['Body'].read().decode('utf-8')
        lines = content.strip().split('\n')
        
        print(f"\nFound {len(lines)} records in sample")
        
        # Parse first record
        if lines:
            first_record = json.loads(lines[0])
            print("\nFirst record structure:")
            print(f"  Name: {first_record.get('name', 'N/A')}")
            print(f"  Location: {first_record.get('location', {}).get('name', 'N/A')}")
            print(f"  Headline: {first_record.get('headline', 'N/A')[:100]}...")
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
                    
        # Save sample to file
        with open('sample_yale_data.json', 'w') as f:
            sample_records = []
            for line in lines[:10]:  # First 10 records
                if line.strip():
                    try:
                        sample_records.append(json.loads(line))
                    except:
                        pass
            json.dump(sample_records, f, indent=2)
            
        print(f"\n✓ Saved {len(sample_records)} sample records to sample_yale_data.json")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check that your AWS credentials are correct")
        print("2. Ensure the 'codeside' user has S3 read permissions")
        print("3. Verify the bucket and key names are correct")


if __name__ == "__main__":
    test_s3_connection()