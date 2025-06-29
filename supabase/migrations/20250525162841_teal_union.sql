/*
  # Storage bucket and policies for resumes

  1. New Storage
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

-- Create policy function
CREATE OR REPLACE FUNCTION create_storage_policy(
    policy_name text,
    operation text,
    bucket_name text
)
RETURNS void AS $$
BEGIN
    BEGIN
        EXECUTE format(
            'CREATE POLICY %I ON storage.objects
            FOR %s TO authenticated
            USING (bucket_id = %L AND (storage.foldername(name))[1] = auth.email())
            WITH CHECK (bucket_id = %L AND (storage.foldername(name))[1] = auth.email())',
            policy_name,
            operation,
            bucket_name,
            bucket_name
        );
    EXCEPTION WHEN duplicate_object THEN
        NULL;
    END;
END;
$$ LANGUAGE plpgsql;

-- Create policies for all operations
SELECT create_storage_policy('Users can read their own resumes', 'SELECT', 'resumes');
SELECT create_storage_policy('Users can insert their own resumes', 'INSERT', 'resumes');
SELECT create_storage_policy('Users can update their own resumes', 'UPDATE', 'resumes');
SELECT create_storage_policy('Users can delete their own resumes', 'DELETE', 'resumes');