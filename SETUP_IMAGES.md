# Configuración de Imágenes en Posts

Este documento describe cómo configurar el soporte de imágenes en los posts usando Supabase Storage.

## Paso 1: Ejecutar la migración SQL

1. Accede al panel de Supabase: https://supabase.com/dashboard
2. Selecciona tu proyecto
3. Ve a "SQL Editor" en el menú lateral
4. Ejecuta el contenido del archivo `database/migrations/add_post_images.sql`

Esto agregará la columna `image_url` a la tabla `posts`.

## Paso 2: Crear el bucket de Storage

1. En el panel de Supabase, ve a "Storage" en el menú lateral
2. Haz clic en "Create a new bucket"
3. Nombre del bucket: `post-images`
4. Selecciona "Public bucket" (para permitir acceso público a las imágenes)
5. Haz clic en "Create bucket"

## Paso 3: Configurar las políticas de seguridad (RLS)

Después de crear el bucket, configura las siguientes políticas:

### 3.1. Lectura pública de imágenes

1. En Storage, selecciona el bucket `post-images`
2. Ve a la pestaña "Policies"
3. Haz clic en "New Policy"
4. Selecciona "Custom policy"
5. Configura:
   - **Name**: `Public read access`
   - **Allowed operation**: SELECT
   - **Target roles**: `public`
   - **Policy definition**: `true`
6. Guarda la política

### 3.2. Subida de imágenes para usuarios autenticados

1. Crea una nueva política con:
   - **Name**: `Authenticated users can upload`
   - **Allowed operation**: INSERT
   - **Target roles**: `authenticated`
   - **Policy definition**: `(auth.uid() IS NOT NULL)`
2. Guarda la política

### 3.3. Actualización de imágenes propias

1. Crea una nueva política con:
   - **Name**: `Users can update their own images`
   - **Allowed operation**: UPDATE
   - **Target roles**: `authenticated`
   - **Policy definition**: `(auth.uid() IS NOT NULL)`
2. Guarda la política

### 3.4. Eliminación de imágenes propias

1. Crea una nueva política con:
   - **Name**: `Users can delete their own images`
   - **Allowed operation**: DELETE
   - **Target roles**: `authenticated`
   - **Policy definition**: `(auth.uid() IS NOT NULL)`
2. Guarda la política

## Paso 4: Verificar la configuración

Una vez completados los pasos anteriores, la funcionalidad de imágenes estará activa:

- Los usuarios podrán subir imágenes al crear posts (máx. 5MB)
- Formatos soportados: JPG, PNG, GIF, WebP
- Las imágenes se almacenarán en: `post-images/{user_id}/{timestamp}-{random}.{ext}`
- Las imágenes se mostrarán en las tarjetas de posts
- Al hacer clic en una imagen, se abrirá en tamaño completo
- Las imágenes se eliminarán automáticamente cuando se elimine el post

## Características implementadas

### Componente CreatePost
- Selector de imagen con drag & drop
- Vista previa de la imagen antes de publicar
- Validación de formato y tamaño
- Subida automática al bucket al crear el post

### Componente EditPost
- Mantiene la imagen actual del post
- Permite cambiar la imagen
- Permite eliminar la imagen
- Elimina la imagen anterior al subir una nueva

### Componente PostCard
- Muestra la imagen del post (si existe)
- Modal para ver la imagen en tamaño completo
- Click en la imagen para ampliar

## Notas importantes

- Las imágenes se suben directamente al bucket de Supabase
- No se almacenan en el servidor de la aplicación
- Las URLs de las imágenes son públicas y accesibles desde cualquier lugar
- Las imágenes están optimizadas para carga rápida
- Se recomienda implementar compresión de imágenes en el frontend si se requiere
