-- Migración para configurar políticas de storage para avatares de perfil
-- Este script configura los permisos necesarios para que usuarios autenticados
-- puedan subir, actualizar y eliminar sus propias fotos de perfil

-- ============================================================================
-- POLÍTICAS PARA EL BUCKET 'post-images' - CARPETA 'avatars'
-- ============================================================================

-- 1. Permitir a usuarios autenticados SUBIR su propio avatar
-- Política: Los usuarios pueden subir archivos a avatars/{su_user_id}.*
CREATE POLICY "Users can upload their own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
    bucket_id = 'post-images'
    AND (storage.foldername(name))[1] = 'avatars'
    AND (storage.filename(name)) LIKE auth.uid()::text || '.%'
);

-- 2. Permitir a usuarios autenticados ACTUALIZAR su propio avatar
-- Política: Los usuarios pueden actualizar archivos en avatars/{su_user_id}.*
CREATE POLICY "Users can update their own avatar"
ON storage.objects
FOR UPDATE
TO authenticated
USING (
    bucket_id = 'post-images'
    AND (storage.foldername(name))[1] = 'avatars'
    AND (storage.filename(name)) LIKE auth.uid()::text || '.%'
)
WITH CHECK (
    bucket_id = 'post-images'
    AND (storage.foldername(name))[1] = 'avatars'
    AND (storage.filename(name)) LIKE auth.uid()::text || '.%'
);

-- 3. Permitir a usuarios autenticados ELIMINAR su propio avatar
-- Política: Los usuarios pueden eliminar archivos en avatars/{su_user_id}.*
CREATE POLICY "Users can delete their own avatar"
ON storage.objects
FOR DELETE
TO authenticated
USING (
    bucket_id = 'post-images'
    AND (storage.foldername(name))[1] = 'avatars'
    AND (storage.filename(name)) LIKE auth.uid()::text || '.%'
);

-- 4. Permitir lectura pública de avatares
-- Política: Cualquiera puede ver los avatares (público)
CREATE POLICY "Anyone can view avatars"
ON storage.objects
FOR SELECT
TO public
USING (
    bucket_id = 'post-images'
    AND (storage.foldername(name))[1] = 'avatars'
);

-- ============================================================================
-- NOTAS IMPORTANTES:
-- ============================================================================
--
-- 1. Estas políticas usan las funciones de Supabase Storage:
--    - storage.foldername(name): Extrae la carpeta del path
--    - storage.filename(name): Extrae el nombre del archivo
--    - auth.uid(): Obtiene el ID del usuario autenticado
--
-- 2. El patrón de nombres de archivo es: avatars/{user_id}.{extension}
--    Por ejemplo: avatars/abc123-def456-ghi789.jpg
--
-- 3. Cada usuario solo puede manipular archivos que empiecen con su propio ID
--
-- 4. La lectura es pública para que cualquiera pueda ver los avatares
--
-- 5. Si ya existen políticas con estos nombres, primero elimínalas:
--    DROP POLICY IF EXISTS "Users can upload their own avatar" ON storage.objects;
--    DROP POLICY IF EXISTS "Users can update their own avatar" ON storage.objects;
--    DROP POLICY IF EXISTS "Users can delete their own avatar" ON storage.objects;
--    DROP POLICY IF EXISTS "Anyone can view avatars" ON storage.objects;
--
-- ============================================================================
