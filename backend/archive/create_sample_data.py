#!/usr/bin/env python3
"""Create sample Yale people data for testing"""

import json
from datetime import datetime, date
import random

# Sample Yale people data
sample_people = [
    {
        "name": "Jennifer Fleiss",
        "firstName": "Jennifer",
        "lastName": "Fleiss",
        "email": "jennifer@renttherunway.com",
        "headline": "Co-Founder & Board Member at Rent The Runway, Board Member at Yale Ventures",
        "summary": "Jennifer Fleiss is a seasoned entrepreneur and investor focused on transforming the retail industry. As Co-Founder of Rent The Runway, she helped pioneer the sharing economy for fashion. Now serving as Board Member at Yale Ventures, helping develop innovations that impact the world's greatest challenges.",
        "location": {"name": "New York, New York, United States"},
        "publicProfileUrl": "https://linkedin.com/in/jenniferfleiss",
        "education": [
            {
                "schoolName": "Yale University",
                "degree": "BA",
                "fieldOfStudy": "Political Science",
                "startDate": {"year": 2001},
                "endDate": {"year": 2005}
            }
        ],
        "experience": [
            {
                "companyName": "Rent The Runway",
                "title": "Co-Founder & Board Member",
                "description": "Co-founded and built Rent The Runway from concept to billion-dollar valuation",
                "location": "New York, NY",
                "startDate": {"year": 2008, "month": 8},
                "endDate": None
            },
            {
                "companyName": "Yale Ventures",
                "title": "Board Member",
                "description": "Helping develop innovations that impact the world's greatest challenges",
                "location": "New Haven, CT",
                "startDate": {"year": 2024, "month": 3},
                "endDate": None
            },
            {
                "companyName": "Volition Capital",
                "title": "Venture Partner",
                "description": "Early-stage venture investing",
                "location": "Boston, MA",
                "startDate": {"year": 2021, "month": 2},
                "endDate": {"year": 2023, "month": 12}
            }
        ],
        "skills": ["Entrepreneurship", "Venture Capital", "Retail", "Fashion", "Strategy"]
    },
    {
        "name": "Daniel Tenreiro",
        "firstName": "Daniel",
        "lastName": "Tenreiro",
        "email": "daniel@autoencoder.holdings",
        "headline": "Managing Partner at Autoencoder Holdings - AI research and investment",
        "summary": "Managing Partner at Autoencoder Holdings, providing AI research and custom software to investment firms. Previously worked in consulting for buy-side firms on AI strategy and opportunistic investing in private markets.",
        "location": {"name": "New York, New York, United States"},
        "publicProfileUrl": "https://linkedin.com/in/danieltenreiro",
        "education": [
            {
                "schoolName": "Yale University",
                "degree": "Bachelor of Arts - BA",
                "fieldOfStudy": "Economics",
                "startDate": {"year": 2015},
                "endDate": {"year": 2019}
            }
        ],
        "experience": [
            {
                "companyName": "Autoencoder Holdings",
                "title": "Managing Partner",
                "description": "Providing AI research and custom software to investment firms, consulting buy-side firms on AI and opportunistically investing in private markets",
                "location": "New York, NY",
                "startDate": {"year": 2023, "month": 2},
                "endDate": None
            }
        ],
        "skills": ["Artificial Intelligence", "Investment Management", "Economics", "Data Science", "Machine Learning"]
    },
    {
        "name": "Alexandra Cavoulacos",
        "firstName": "Alexandra", 
        "lastName": "Cavoulacos",
        "email": "alex@themuse.com",
        "headline": "Co Producer and Investor at Nothing Ventured Productions, Former Founder of TheMuse",
        "summary": "Investor and 3-time Tony nominated producer in commercial theater. Former Founder & President at TheMuse.com. Focused on opening up access and opportunity for accredited investors new to Broadway using frameworks from angel investing.",
        "location": {"name": "New York, New York, United States"},
        "publicProfileUrl": "https://linkedin.com/in/alexandracavoulacos",
        "education": [
            {
                "schoolName": "Yale University",
                "degree": "B.A.",
                "fieldOfStudy": "Political Science",
                "startDate": {"year": 2004},
                "endDate": {"year": 2008}
            }
        ],
        "experience": [
            {
                "companyName": "Nothing Ventured Productions",
                "title": "Co Producer and Investor",
                "description": "Investor and producer in commercial theater, borrowing frameworks from angel investing to open up access for new Broadway investors",
                "location": "New York, NY",
                "startDate": {"year": 2023, "month": 1},
                "endDate": None
            },
            {
                "companyName": "TheMuse.com",
                "title": "Founder & President",
                "description": "Founded and scaled TheMuse to 70+ million annual users, pioneered values-based job search",
                "location": "New York, NY",
                "startDate": {"year": 2010, "month": 3},
                "endDate": {"year": 2021, "month": 7}
            }
        ],
        "skills": ["Entrepreneurship", "Media", "Career Development", "Angel Investing", "Theater Production"]
    },
    {
        "name": "Jack Weinberger",
        "firstName": "Jack",
        "lastName": "Weinberger", 
        "email": "jack@ajax.com",
        "headline": "Co-Founder at Ajax, Former Associate at Brightstar Capital Partners",
        "summary": "Co-Founder at Ajax. Previously Associate at Brightstar Capital Partners focusing on early-stage venture investments. Yale Economics graduate with experience in venture capital and entrepreneurship.",
        "location": {"name": "New York, New York, United States"},
        "publicProfileUrl": "https://linkedin.com/in/jackweinberger",
        "education": [
            {
                "schoolName": "Yale University",
                "degree": "Bachelor of Arts (B.A.)",
                "fieldOfStudy": "Economics",
                "startDate": {"year": 2013},
                "endDate": {"year": 2017}
            }
        ],
        "experience": [
            {
                "companyName": "Ajax",
                "title": "Co-Founder",
                "description": "Co-founding a new venture",
                "location": "New York, NY",
                "startDate": {"year": 2022, "month": 10},
                "endDate": None
            },
            {
                "companyName": "Brightstar Capital Partners",
                "title": "Associate",
                "description": "Early-stage venture capital investments",
                "location": "New York, NY",
                "startDate": {"year": 2019, "month": 7},
                "endDate": {"year": 2021, "month": 7}
            }
        ],
        "skills": ["Venture Capital", "Economics", "Entrepreneurship", "Investment Analysis", "Strategy"]
    },
    {
        "name": "Kathryn Minshew",
        "firstName": "Kathryn",
        "lastName": "Minshew",
        "email": "kathryn@themuse.com", 
        "headline": "Advisor at XFactor Ventures, Co-Founder of The Muse",
        "summary": "Operating Partner with XFactor Ventures, designed to be the 'first check' in female founded startups. Co-founded The Muse and pioneered the concept of values-based job search. Active advisor and angel investor with 88% investments in female founded companies.",
        "location": {"name": "New York, New York, United States"},
        "publicProfileUrl": "https://linkedin.com/in/kathrynminshew",
        "education": [
            {
                "schoolName": "Duke University",
                "degree": "Bachelor's degree",
                "fieldOfStudy": "Political Science",
                "startDate": {"year": 2003},
                "endDate": {"year": 2007}
            }
        ],
        "experience": [
            {
                "companyName": "XFactor Ventures",
                "title": "Advisor",
                "description": "Operating Partner focused on being the 'first check' in female founded startups",
                "location": "New York, NY",
                "startDate": {"year": 2020, "month": 1},
                "endDate": None
            },
            {
                "companyName": "The Muse",
                "title": "Co-Founder & CEO",
                "description": "Co-founded The Muse, grew to 70+ million annual users, pioneered values-based job search",
                "location": "New York, NY",
                "startDate": {"year": 2011, "month": 1},
                "endDate": {"year": 2020, "month": 12}
            }
        ],
        "skills": ["Entrepreneurship", "Angel Investing", "Media", "Career Development", "Female Founders"]
    }
]

def save_sample_data():
    """Save sample data to JSON file"""
    with open('sample_yale_data.json', 'w') as f:
        json.dump(sample_people, f, indent=2)
    print(f"Created sample_yale_data.json with {len(sample_people)} people")

if __name__ == "__main__":
    save_sample_data()