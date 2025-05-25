/*
  # Resume Storage Setup

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

-- Create the storage bucket
INSERT INTO storage.buckets (id, name)
VALUES ('resumes', 'resumes')
ON CONFLICT DO NOTHING;

-- Enable RLS
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own resumes
CREATE POLICY "Users can read their own resumes"
ON storage.objects FOR SELECT TO authenticated
USING (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);

-- Allow users to upload their own resumes
CREATE POLICY "Users can upload their own resumes"
ON storage.objects FOR INSERT TO authenticated
WITH CHECK (
  bucket_id = 'resumes' AND 
  (storage.foldername(name))[1] = auth.email()
);

-- Allow users to update their own resumes
CREATE POLICY "Users can update their own resumes"
ON storage.objects FOR UPDATE TO authenticated
WITH CHECK (
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