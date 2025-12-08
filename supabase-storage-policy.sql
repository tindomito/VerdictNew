-- Script para configurar políticas de acceso público al bucket post-images
-- Ejecutar en el SQL Editor de Supabase

-- 1. Hacer el bucket público
UPDATE storage.buckets
SET public = true
WHERE id = 'post-images';

-- 2. Permitir que cualquiera pueda leer las imágenes (GET)
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'post-images' );

-- 3. Permitir que usuarios autenticados suban imágenes (INSERT)
CREATE POLICY "Authenticated users can upload images"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK ( bucket_id = 'post-images' );

-- 4. Permitir que usuarios autenticados actualicen sus propias imágenes (UPDATE)
CREATE POLICY "Users can update their own images"
ON storage.objects FOR UPDATE
TO authenticated
USING ( bucket_id = 'post-images' AND auth.uid()::text = (storage.foldername(name))[1] )
WITH CHECK ( bucket_id = 'post-images' AND auth.uid()::text = (storage.foldername(name))[1] );

-- 5. Permitir que usuarios autenticados eliminen sus propias imágenes (DELETE)
CREATE POLICY "Users can delete their own images"
ON storage.objects FOR DELETE
TO authenticated
USING ( bucket_id = 'post-images' AND auth.uid()::text = (storage.foldername(name))[1] );
