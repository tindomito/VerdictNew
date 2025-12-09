-- Migración para crear el sistema de Publicaciones
-- Este archivo debe ejecutarse en Supabase SQL Editor

-- =============================================================================
-- TABLA: publications
-- Sistema independiente del Feed para contenido de tipo artículo/tutorial
-- =============================================================================

CREATE TABLE IF NOT EXISTS publications (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL CHECK (char_length(title) <= 200),
    content TEXT NOT NULL CHECK (char_length(content) <= 10000),
    category TEXT NOT NULL DEFAULT 'articulo' CHECK (category IN ('articulo', 'tutorial', 'opinion', 'review', 'guia', 'entrevista', 'historia')),
    image_url TEXT,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_publications_user_id ON publications(user_id);
CREATE INDEX IF NOT EXISTS idx_publications_category ON publications(category);
CREATE INDEX IF NOT EXISTS idx_publications_created_at ON publications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_publications_with_images ON publications(image_url) WHERE image_url IS NOT NULL;

-- =============================================================================
-- VISTA: publications_with_users
-- Combina publicaciones con información del usuario (display_name, avatar_url)
-- =============================================================================

CREATE OR REPLACE VIEW publications_with_users AS
SELECT
    p.id,
    p.user_id,
    p.title,
    p.content,
    p.category,
    p.image_url,
    p.likes_count,
    p.created_at,
    p.updated_at,
    COALESCE(pr.display_name, 'Usuario') AS display_name,
    pr.avatar_url
FROM publications p
LEFT JOIN profiles pr ON p.user_id = pr.user_id;

-- =============================================================================
-- TRIGGER: Actualizar updated_at automáticamente
-- =============================================================================

CREATE OR REPLACE FUNCTION update_publications_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_publications_updated_at ON publications;
CREATE TRIGGER trigger_publications_updated_at
    BEFORE UPDATE ON publications
    FOR EACH ROW
    EXECUTE FUNCTION update_publications_updated_at();

-- =============================================================================
-- RLS (Row Level Security)
-- =============================================================================

-- Habilitar RLS en la tabla publications
ALTER TABLE publications ENABLE ROW LEVEL SECURITY;

-- Policy: Cualquiera puede leer publicaciones
CREATE POLICY "Anyone can read publications"
    ON publications
    FOR SELECT
    USING (true);

-- Policy: Usuarios autenticados pueden crear publicaciones
CREATE POLICY "Authenticated users can create publications"
    ON publications
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Policy: Usuarios solo pueden editar sus propias publicaciones
CREATE POLICY "Users can update their own publications"
    ON publications
    FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Policy: Usuarios solo pueden eliminar sus propias publicaciones
CREATE POLICY "Users can delete their own publications"
    ON publications
    FOR DELETE
    TO authenticated
    USING (auth.uid() = user_id);

-- =============================================================================
-- Habilitar Realtime para publications
-- =============================================================================

ALTER PUBLICATION supabase_realtime ADD TABLE publications;

-- =============================================================================
-- NOTAS DE CONFIGURACIÓN
-- =============================================================================
--
-- Las imágenes de las publicaciones usan el mismo bucket "post-images" que el Feed.
-- No es necesario crear un nuevo bucket ni configurar políticas adicionales de Storage.
--
-- Para ejecutar esta migración:
-- 1. Abre el SQL Editor en Supabase
-- 2. Copia y pega este archivo completo
-- 3. Ejecuta el script
-- 4. Verifica que la tabla y vista se crearon correctamente
