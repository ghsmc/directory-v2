/*
  # Resume Storage Setup

  1. Storage Configuration
    - Creates 'resumes' bucket for storing user resumes
    - Sets 5MB file size limit
    - Restricts to PDF files only
    - Makes bucket private

  2. Security
    - Enables RLS
    - Creates policies for authenticated users to:
      - Upload resumes to their own folder
      - Read their own resumes
      - Update their own resumes
      - Delete their own resumes
    - Folders are based on user email
*/

-- Create storage schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS storage;

-- Create the storage bucket with proper configuration
CREATE TABLE IF NOT EXISTS storage.buckets (
  id text PRIMARY KEY,
  name text NOT NULL,
  public boolean DEFAULT false,
  file_size_limit bigint DEFAULT 5242880, -- 5MB limit
  allowed_mime_types text[] DEFAULT ARRAY['application/pdf']::text[]
);

-- Create objects table if it doesn't exist
CREATE TABLE IF NOT EXISTS storage.objects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bucket_id text REFERENCES storage.buckets(id),
  name text NOT NULL,
  owner uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  last_accessed_at timestamptz DEFAULT now(),
  metadata jsonb DEFAULT '{}'::jsonb,
  path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/')) STORED
);

-- Insert the resumes bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'resumes',
  'resumes',
  false,
  5242880,
  ARRAY['application/pdf']::text[]
)
ON CONFLICT (id) DO UPDATE
SET 
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can read their own resumes" ON storage.objects;
DROP POLICY IF EXISTS "Users can upload their own resumes" ON storage.objects;
DROP POLICY IF EXISTS "Users can update their own resumes" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete their own resumes" ON storage.objects;

-- Allow users to read their own resumes
CREATE POLICY "Users can read their own resumes"
ON storage.objects FOR SELECT TO authenticated
USING (
  bucket_id = 'resumes' AND 
  owner = auth.uid()
);

-- Allow users to upload their own resumes
CREATE POLICY "Users can upload their own resumes"
ON storage.objects FOR INSERT TO authenticated
WITH CHECK (
  bucket_id = 'resumes' AND 
  owner = auth.uid()
);

-- Allow users to update their own resumes
CREATE POLICY "Users can update their own resumes"
ON storage.objects FOR UPDATE TO authenticated
USING (
  bucket_id = 'resumes' AND 
  owner = auth.uid()
)
WITH CHECK (
  bucket_id = 'resumes' AND 
  owner = auth.uid()
);

-- Allow users to delete their own resumes
CREATE POLICY "Users can delete their own resumes"
ON storage.objects FOR DELETE TO authenticated
USING (
  bucket_id = 'resumes' AND 
  owner = auth.uid()
);