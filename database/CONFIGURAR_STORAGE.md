# Configuración de Supabase Storage para Avatares

## Paso 1: Verificar que el bucket existe

1. Ve a tu proyecto en Supabase: https://app.supabase.com
2. Navega a **Storage** en el menú lateral
3. Verifica que existe el bucket **`post-images`**
4. Si no existe, créalo con estos ajustes:
   - **Nombre**: `post-images`
   - **Public bucket**: ✅ Activado (para que las imágenes sean accesibles públicamente)

## Paso 2: Aplicar las políticas de seguridad

### Opción A: Usando el SQL Editor de Supabase (Recomendado)

1. En tu proyecto de Supabase, ve a **SQL Editor**
2. Haz clic en **New Query**
3. Copia y pega el contenido del archivo:
   ```
   database/migrations/configure_avatar_storage_policies.sql
   ```
4. Haz clic en **Run** para ejecutar la migración
5. Verifica que no haya errores

### Opción B: Usando la CLI de Supabase

```bash
# Si tienes instalada la CLI de Supabase
supabase db push
```

## Paso 3: Verificar las políticas

1. Ve a **Storage** > **Policies**
2. Selecciona el bucket **`post-images`**
3. Deberías ver 4 políticas creadas:
   - ✅ `Users can upload their own avatar` (INSERT)
   - ✅ `Users can update their own avatar` (UPDATE)
   - ✅ `Users can delete their own avatar` (DELETE)
   - ✅ `Anyone can view avatars` (SELECT)

## Paso 4: Probar la funcionalidad

1. Inicia sesión en tu aplicación
2. Ve a **Configuración de Perfil**
3. Intenta subir una imagen de avatar
4. Si funciona correctamente, deberías ver:
   - La imagen subida a `post-images/avatars/{tu_user_id}.{extension}`
   - La vista previa de la imagen
   - El avatar actualizado en tu perfil

## Troubleshooting

### Error: "new row violates row-level security policy"

Esto significa que las políticas no se aplicaron correctamente. Solución:

1. Ve a **SQL Editor**
2. Ejecuta este comando para ver las políticas existentes:
   ```sql
   SELECT * FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage';
   ```
3. Si hay políticas duplicadas o conflictivas, elimínalas:
   ```sql
   DROP POLICY IF EXISTS "Users can upload their own avatar" ON storage.objects;
   DROP POLICY IF EXISTS "Users can update their own avatar" ON storage.objects;
   DROP POLICY IF EXISTS "Users can delete their own avatar" ON storage.objects;
   DROP POLICY IF EXISTS "Anyone can view avatars" ON storage.objects;
   ```
4. Vuelve a ejecutar la migración

### Error: "The resource already exists"

Esto significa que las políticas ya existen. Si necesitas recrearlas:

1. Primero elimínalas (ver comando arriba)
2. Luego vuelve a ejecutar la migración

### Error: "storage.foldername does not exist"

Esto significa que tu versión de Supabase no tiene estas funciones helper. Usa esta versión alternativa:

```sql
-- Versión alternativa sin funciones helper
CREATE POLICY "Users can upload their own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
    bucket_id = 'post-images'
    AND name LIKE 'avatars/' || auth.uid()::text || '.%'
);

CREATE POLICY "Users can update their own avatar"
ON storage.objects
FOR UPDATE
TO authenticated
USING (
    bucket_id = 'post-images'
    AND name LIKE 'avatars/' || auth.uid()::text || '.%'
);

CREATE POLICY "Users can delete their own avatar"
ON storage.objects
FOR DELETE
TO authenticated
USING (
    bucket_id = 'post-images'
    AND name LIKE 'avatars/' || auth.uid()::text || '.%'
);

CREATE POLICY "Anyone can view avatars"
ON storage.objects
FOR SELECT
TO public
USING (
    bucket_id = 'post-images'
    AND name LIKE 'avatars/%'
);
```

## Estructura de Archivos

Después de configurar, los avatares se guardarán con esta estructura:

```
post-images/
├── avatars/
│   ├── {user_id_1}.jpg
│   ├── {user_id_2}.png
│   └── {user_id_3}.webp
└── {user_id_1}/
    ├── {timestamp}-{random}.jpg  (imágenes de posts)
    └── ...
```

## Seguridad

✅ Cada usuario solo puede modificar su propio avatar
✅ Las URLs siguen el patrón: `avatars/{user_id}.{extension}`
✅ No se pueden subir archivos fuera de la carpeta `avatars/`
✅ No se pueden modificar avatares de otros usuarios
✅ La lectura es pública para todos

## Referencias

- [Supabase Storage Policies](https://supabase.com/docs/guides/storage/security/access-control)
- [Supabase Auth Helpers](https://supabase.com/docs/guides/auth/auth-helpers)
