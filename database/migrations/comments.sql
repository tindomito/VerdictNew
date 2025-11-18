-- Migración para sistema de comentarios
-- Este archivo debe ejecutarse en Supabase SQL Editor

-- Crear tabla de comentarios
CREATE TABLE IF NOT EXISTS comments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_created_at ON comments(created_at);

-- Crear vista para comentarios con información del usuario
CREATE OR REPLACE VIEW comments_with_users AS
SELECT
    c.id,
    c.post_id,
    c.user_id,
    c.content,
    c.created_at,
    c.updated_at,
    p.display_name,
    p.avatar_url
FROM comments c
LEFT JOIN profiles p ON c.user_id = p.user_id;

-- Habilitar Row Level Security (RLS)
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- Policy: Todos pueden ver comentarios
CREATE POLICY "Comentarios son públicos"
    ON comments FOR SELECT
    USING (true);

-- Policy: Usuarios autenticados pueden crear comentarios
CREATE POLICY "Usuarios autenticados pueden crear comentarios"
    ON comments FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Los usuarios pueden actualizar sus propios comentarios
CREATE POLICY "Usuarios pueden actualizar sus propios comentarios"
    ON comments FOR UPDATE
    USING (auth.uid() = user_id);

-- Policy: Los usuarios pueden eliminar sus propios comentarios
CREATE POLICY "Usuarios pueden eliminar sus propios comentarios"
    ON comments FOR DELETE
    USING (auth.uid() = user_id);

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar updated_at en comentarios
DROP TRIGGER IF EXISTS update_comments_updated_at ON comments;
CREATE TRIGGER update_comments_updated_at
    BEFORE UPDATE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- OPCIONAL: Añadir columna de contador de comentarios a posts
-- Si la tabla posts no tiene esta columna, agrégala:
ALTER TABLE posts ADD COLUMN IF NOT EXISTS comments_count INTEGER DEFAULT 0;

-- Función para actualizar el contador de comentarios
CREATE OR REPLACE FUNCTION update_post_comments_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE posts
        SET comments_count = comments_count + 1
        WHERE id = NEW.post_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE posts
        SET comments_count = GREATEST(0, comments_count - 1)
        WHERE id = OLD.post_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar contador de comentarios
DROP TRIGGER IF EXISTS trigger_update_post_comments_count ON comments;
CREATE TRIGGER trigger_update_post_comments_count
    AFTER INSERT OR DELETE ON comments
    FOR EACH ROW
    EXECUTE FUNCTION update_post_comments_count();

-- Inicializar contador de comentarios para posts existentes
UPDATE posts
SET comments_count = (
    SELECT COUNT(*)
    FROM comments
    WHERE comments.post_id = posts.id
);
