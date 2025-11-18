# Migraciones de Base de Datos

Este directorio contiene las migraciones SQL para configurar la base de datos en Supabase.

## Configuración del Sistema de Comentarios

Para habilitar el sistema de comentarios en las publicaciones, debes ejecutar el archivo de migración en Supabase:

### Pasos para ejecutar la migración:

1. Accede a tu proyecto en [Supabase](https://supabase.com)
2. Ve a la sección **SQL Editor** en el panel izquierdo
3. Copia todo el contenido del archivo `migrations/comments.sql`
4. Pégalo en el editor SQL
5. Haz clic en **Run** para ejecutar la migración

### ¿Qué hace esta migración?

La migración `comments.sql` crea:

- **Tabla `comments`**: Almacena todos los comentarios de las publicaciones
  - `id`: UUID único del comentario
  - `post_id`: Referencia a la publicación
  - `user_id`: Referencia al usuario que creó el comentario
  - `content`: Contenido del comentario
  - `created_at`: Fecha de creación
  - `updated_at`: Fecha de última actualización

- **Vista `comments_with_users`**: Vista que combina comentarios con información del perfil del usuario
  - Incluye `display_name` y `avatar_url` del autor

- **Políticas RLS (Row Level Security)**:
  - Todos pueden ver comentarios
  - Solo usuarios autenticados pueden crear comentarios
  - Los usuarios solo pueden editar/eliminar sus propios comentarios

- **Triggers automáticos**:
  - Actualiza `updated_at` automáticamente al modificar un comentario
  - Actualiza el contador `comments_count` en la tabla `posts`

- **Índices**: Para mejorar el rendimiento de las consultas

### Verificación

Después de ejecutar la migración, verifica que:

1. La tabla `comments` existe
2. La vista `comments_with_users` está creada
3. Las políticas RLS están habilitadas
4. La columna `comments_count` existe en la tabla `posts`

### Realtime

Para habilitar actualizaciones en tiempo real de comentarios:

1. Ve a **Database** > **Replication** en Supabase
2. Activa la replicación para la tabla `comments`

Esto permitirá que los comentarios aparezcan automáticamente sin necesidad de recargar la página.
