# Configuración de Storage en Supabase

Para que las imágenes funcionen correctamente, debes configurar el bucket `post-images` en Supabase para que sea público.

## Pasos a seguir:

### 1. Ir al SQL Editor de Supabase

1. Accede a tu proyecto en [Supabase Dashboard](https://app.supabase.com/)
2. Ve a la sección **SQL Editor** en el menú lateral izquierdo
3. Crea una nueva query

### 2. Ejecutar el script SQL

Copia y pega el contenido del archivo `supabase-storage-policy.sql` y ejecútalo.

El script hace lo siguiente:

- ✅ Hace el bucket `post-images` público
- ✅ Permite que cualquiera pueda **leer** las imágenes (necesario para mostrarlas)
- ✅ Permite que usuarios autenticados puedan **subir** nuevas imágenes
- ✅ Permite que usuarios puedan **actualizar** solo sus propias imágenes
- ✅ Permite que usuarios puedan **eliminar** solo sus propias imágenes

### 3. Verificar que funciona

1. Intenta subir una imagen en un post
2. La imagen debería cargarse correctamente
3. Al recargar la página, la imagen debería seguir visible

## Alternativa: Configuración manual

Si prefieres configurar manualmente:

### a) Hacer el bucket público

1. Ve a **Storage** en el menú lateral
2. Selecciona el bucket `post-images`
3. Haz clic en el icono de configuración (⚙️)
4. Activa la opción **Public bucket**

### b) Agregar políticas de acceso

1. Ve a **Storage** > **Policies**
2. Agrega las siguientes políticas:

**Para lectura (SELECT):**
- Target: `public` role
- Policy: `bucket_id = 'post-images'`

**Para inserción (INSERT):**
- Target: `authenticated` role
- Policy: `bucket_id = 'post-images'`

**Para actualización (UPDATE):**
- Target: `authenticated` role
- Policy: `bucket_id = 'post-images' AND auth.uid()::text = (storage.foldername(name))[1]`

**Para eliminación (DELETE):**
- Target: `authenticated` role
- Policy: `bucket_id = 'post-images' AND auth.uid()::text = (storage.foldername(name))[1]`

## Problemas comunes

**Error: "Object not found"**
- Asegúrate de que el bucket sea público
- Verifica que las políticas estén configuradas correctamente

**Las imágenes no cargan después de recargar**
- Ejecuta el script SQL completo
- Limpia el caché del navegador
