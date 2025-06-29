#!/usr/bin/env python3
"""Test AWS access and list available buckets"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_aws_access():
    """Test AWS access"""
    
    # Get credentials
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if not aws_access_key or not aws_secret_key:
        print("Error: AWS credentials not found")
        return
        
    print(f"Using AWS Access Key: {aws_access_key}")
    
    # Create S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name='us-east-2'
    )
    
    try:
        # List all buckets
        print("\nListing available buckets:")
        response = s3.list_buckets()
        
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
            
        # Try to list objects in the target bucket
        bucket_name = 'people-data-yale-2025'
        print(f"\nTrying to list objects in {bucket_name}:")
        
        try:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix='brightdata/',
                MaxKeys=5
            )
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size'] / (1024**2):.2f} MB)")
            else:
                print("  No objects found")
                
        except Exception as e:
            print(f"  Error accessing bucket: {e}")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure the AWS Secret Access Key is correct in your .env file")


if __name__ == "__main__":
    test_aws_access()