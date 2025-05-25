/*
  # Initial Database Schema Setup

  1. Tables
    - Creates users profile table
    - Creates storage schema and tables
    - Sets up resume storage system
  
  2. Security
    - Enables RLS on all tables
    - Creates policies for user data access
    - Sets up storage access policies
    
  3. Indexes
    - Adds performance optimized indexes
*/

-- Create users profile table
CREATE TABLE IF NOT EXISTS public.profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id),
  email text UNIQUE NOT NULL,
  full_name text,
  university text,
  linkedin_url text,
  clarity boolean,
  interests text[],
  target_companies text[],
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create profile policies
CREATE POLICY "Users can view own profile"
  ON public.profiles
  FOR SELECT
  TO authenticated
  USING (id = auth.uid());

CREATE POLICY "Users can update own profile"
  ON public.profiles
  FOR UPDATE
  TO authenticated
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

CREATE POLICY "Users can insert own profile"
  ON public.profiles
  FOR INSERT
  TO authenticated
  WITH CHECK (id = auth.uid());

-- Create storage schema
CREATE SCHEMA IF NOT EXISTS storage;

-- Create buckets table
CREATE TABLE IF NOT EXISTS storage.buckets (
  id text PRIMARY KEY,
  name text NOT NULL,
  owner uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  public boolean DEFAULT false,
  avif_autodetection boolean DEFAULT false,
  file_size_limit bigint DEFAULT 5242880, -- 5MB limit
  allowed_mime_types text[] DEFAULT ARRAY['application/pdf']::text[]
);

-- Create objects table
CREATE TABLE IF NOT EXISTS storage.objects (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bucket_id text NOT NULL REFERENCES storage.buckets(id),
  name text NOT NULL,
  owner uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  last_accessed_at timestamptz DEFAULT now(),
  metadata jsonb DEFAULT '{}'::jsonb,
  path_tokens text[] GENERATED ALWAYS AS (string_to_array(name, '/')) STORED
);

-- Create resumes bucket
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'resumes',
  'resumes',
  false,
  5242880, -- 5MB limit
  ARRAY['application/pdf']::text[]
)
ON CONFLICT (id) DO UPDATE
SET 
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

-- Enable RLS on storage objects
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Create storage policies
CREATE POLICY "Users can read own resumes"
  ON storage.objects
  FOR SELECT
  TO authenticated
  USING (bucket_id = 'resumes' AND owner = auth.uid());

CREATE POLICY "Users can upload own resumes"
  ON storage.objects
  FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'resumes' AND owner = auth.uid());

CREATE POLICY "Users can update own resumes"
  ON storage.objects
  FOR UPDATE
  TO authenticated
  USING (bucket_id = 'resumes' AND owner = auth.uid())
  WITH CHECK (bucket_id = 'resumes' AND owner = auth.uid());

CREATE POLICY "Users can delete own resumes"
  ON storage.objects
  FOR DELETE
  TO authenticated
  USING (bucket_id = 'resumes' AND owner = auth.uid());

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS objects_bucket_id_idx ON storage.objects (bucket_id);
CREATE INDEX IF NOT EXISTS objects_owner_idx ON storage.objects (owner);
CREATE INDEX IF NOT EXISTS profiles_email_idx ON public.profiles (email);