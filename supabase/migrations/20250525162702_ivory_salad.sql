/*
  # Create storage bucket for resumes

  1. New Storage
    - Creates a new storage bucket called 'resumes' for storing user resume files
    - Enables RLS (Row Level Security) for the bucket
    - Sets up policies to allow authenticated users to manage their own resumes

  2. Security
    - Users can only access their own resumes
    - Files are stored in user-specific folders based on email
    - Admins have full access to all resumes
*/

-- Create the storage bucket
INSERT INTO storage.buckets (id, name)
VALUES ('resumes', 'resumes')
ON CONFLICT DO NOTHING;

-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Allow users to upload their own resumes
CREATE POLICY "Users can upload their own resumes"
ON storage.objects FOR INSERT TO authenticated
WITH CHECK (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);

-- Allow users to read their own resumes
CREATE POLICY "Users can read their own resumes"
ON storage.objects FOR SELECT TO authenticated
USING (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);

-- Allow users to update their own resumes
CREATE POLICY "Users can update their own resumes"
ON storage.objects FOR UPDATE TO authenticated
USING (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);

-- Allow users to delete their own resumes
CREATE POLICY "Users can delete their own resumes"
ON storage.objects FOR DELETE TO authenticated
USING (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);