/*
  # Storage bucket and policies for resumes
  
  1. Storage
    - Creates 'resumes' bucket for storing user resumes
  
  2. Security  
    - Creates policies for authenticated users to:
      - Upload resumes to their own folder
      - Read their own resumes  
      - Update their own resumes
      - Delete their own resumes
    - Folders are based on user email
*/

-- Create bucket function if it doesn't exist
CREATE OR REPLACE FUNCTION create_bucket_if_not_exists(bucket_name text)
RETURNS void AS $$
BEGIN
    INSERT INTO storage.buckets (id, name)
    VALUES (bucket_name, bucket_name)
    ON CONFLICT (id) DO NOTHING;
END;
$$ LANGUAGE plpgsql;

-- Create the bucket
SELECT create_bucket_if_not_exists('resumes');

-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Create SELECT policy
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can read their own resumes" ON storage.objects;
    CREATE POLICY "Users can read their own resumes"
    ON storage.objects FOR SELECT TO authenticated
    USING (
        bucket_id = 'resumes' AND 
        (storage.foldername(name))[1] = auth.email()
    );
END $$;

-- Create INSERT policy
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can insert their own resumes" ON storage.objects;
    CREATE POLICY "Users can insert their own resumes"
    ON storage.objects FOR INSERT TO authenticated
    WITH CHECK (
        bucket_id = 'resumes' AND 
        (storage.foldername(name))[1] = auth.email()
    );
END $$;

-- Create UPDATE policy
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can update their own resumes" ON storage.objects;
    CREATE POLICY "Users can update their own resumes"
    ON storage.objects FOR UPDATE TO authenticated
    USING (
        bucket_id = 'resumes' AND 
        (storage.foldername(name))[1] = auth.email()
    )
    WITH CHECK (
        bucket_id = 'resumes' AND 
        (storage.foldername(name))[1] = auth.email()
    );
END $$;

-- Create DELETE policy
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can delete their own resumes" ON storage.objects;
    CREATE POLICY "Users can delete their own resumes"
    ON storage.objects FOR DELETE TO authenticated
    USING (
        bucket_id = 'resumes' AND 
        (storage.foldername(name))[1] = auth.email()
    );
END $$;