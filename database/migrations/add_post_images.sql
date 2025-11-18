-- Migración para agregar soporte de imágenes en posts
-- Este archivo debe ejecutarse en Supabase SQL Editor

-- Agregar columna image_url a la tabla posts
ALTER TABLE posts ADD COLUMN IF NOT EXISTS image_url TEXT;

-- Crear índice para búsquedas por posts con imágenes
CREATE INDEX IF NOT EXISTS idx_posts_with_images ON posts(image_url) WHERE image_url IS NOT NULL;

-- IMPORTANTE: Configuración del Storage Bucket
-- Después de ejecutar esta migración, debes crear un bucket en Supabase:
--
-- 1. Ve a Storage en el panel de Supabase
-- 2. Crea un nuevo bucket llamado "post-images"
-- 3. Configura las políticas de acceso (RLS):

-- Policy: Permitir lectura pública de imágenes
-- En la interfaz de Supabase Storage, crea esta política para el bucket "post-images":
-- Name: Public read access
-- Policy: SELECT
-- Target roles: public
-- Using expression: true

-- Policy: Permitir subida de imágenes a usuarios autenticados
-- Name: Authenticated users can upload
-- Policy: INSERT
-- Target roles: authenticated
-- Using expression: auth.uid() IS NOT NULL

-- Policy: Permitir actualización de imágenes al autor
-- Name: Users can update their own images
-- Policy: UPDATE
-- Target roles: authenticated
-- Using expression: auth.uid() IS NOT NULL

-- Policy: Permitir eliminación de imágenes al autor
-- Name: Users can delete their own images
-- Policy: DELETE
-- Target roles: authenticated
-- Using expression: auth.uid() IS NOT NULL

-- Nota: Las políticas de Storage se configuran en la UI de Supabase, no mediante SQL
-- Alternativamente, puedes usar la API de Supabase para configurarlas programáticamente
