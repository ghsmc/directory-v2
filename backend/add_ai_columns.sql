-- Add AI-generated columns to the people table
-- This will store AI-enhanced summaries and tags for better search

BEGIN;

-- Add AI-generated summary column
ALTER TABLE people 
ADD COLUMN IF NOT EXISTS ai_summary TEXT;

-- Add AI-generated tags column (JSON array for flexibility)
ALTER TABLE people 
ADD COLUMN IF NOT EXISTS ai_tags JSONB;

-- Add AI processing status column
ALTER TABLE people 
ADD COLUMN IF NOT EXISTS ai_processed BOOLEAN DEFAULT FALSE;

-- Add AI processing timestamp
ALTER TABLE people 
ADD COLUMN IF NOT EXISTS ai_processed_at TIMESTAMP;

-- Create index on AI tags for fast searching
CREATE INDEX IF NOT EXISTS idx_people_ai_tags 
ON people USING gin(ai_tags);

-- Create index on AI summary for full-text search
CREATE INDEX IF NOT EXISTS idx_people_ai_summary_gin 
ON people USING gin(to_tsvector('english', COALESCE(ai_summary, '')));

-- Create index on AI processing status
CREATE INDEX IF NOT EXISTS idx_people_ai_processed 
ON people (ai_processed);

COMMIT;

-- Check the updated schema
\d people;