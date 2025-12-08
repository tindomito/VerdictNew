/**
 * Servicios para manejar el almacenamiento de archivos en Supabase Storage
 */
import { supabase } from './supabase.js';

const BUCKET_NAME = 'post-images';
const AVATAR_FOLDER = 'avatars'; // Subcarpeta para avatares de perfil

/**
 * Sube una imagen al bucket de Supabase
 * @param {File} file - Archivo de imagen a subir
 * @param {string} userId - ID del usuario que sube la imagen
 * @returns {Promise<{url: string|null, error: Object|null}>}
 */
export async function uploadPostImage(file, userId) {
    try {
        // Validar que sea una imagen
        if (!file.type.startsWith('image/')) {
            return { url: null, error: { message: 'El archivo debe ser una imagen' } };
        }

        // Validar tamaño (máximo 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            return { url: null, error: { message: 'La imagen no debe superar los 5MB' } };
        }

        // Generar nombre único para el archivo
        const fileExt = file.name.split('.').pop();
        const fileName = `${userId}/${Date.now()}-${Math.random().toString(36).substring(7)}.${fileExt}`;

        // Subir archivo
        const { data, error } = await supabase.storage
            .from(BUCKET_NAME)
            .upload(fileName, file, {
                cacheControl: '3600',
                upsert: false
            });

        if (error) {
            console.error('Error uploading image:', error);
            return { url: null, error };
        }

        console.log('Image uploaded successfully:', data);

        // Obtener URL pública
        const { data: { publicUrl } } = supabase.storage
            .from(BUCKET_NAME)
            .getPublicUrl(fileName);

        console.log('Public URL generated:', publicUrl);
        return { url: publicUrl, error: null };
    } catch (error) {
        console.error('Error in uploadPostImage:', error);
        return { url: null, error: { message: 'Error al subir la imagen' } };
    }
}

/**
 * Elimina una imagen del bucket de Supabase
 * @param {string} imageUrl - URL de la imagen a eliminar
 * @returns {Promise<{success: boolean, error: Object|null}>}
 */
export async function deletePostImage(imageUrl) {
    try {
        if (!imageUrl) {
            return { success: true, error: null };
        }

        // Extraer el path del archivo de la URL
        const url = new URL(imageUrl);
        const pathParts = url.pathname.split(`/${BUCKET_NAME}/`);
        if (pathParts.length < 2) {
            return { success: false, error: { message: 'URL de imagen inválida' } };
        }

        const filePath = pathParts[1];

        // Eliminar archivo
        const { error } = await supabase.storage
            .from(BUCKET_NAME)
            .remove([filePath]);

        if (error) {
            console.error('Error deleting image:', error);
            return { success: false, error };
        }

        return { success: true, error: null };
    } catch (error) {
        console.error('Error in deletePostImage:', error);
        // No fallar si hay error al eliminar la imagen
        return { success: true, error: null };
    }
}

/**
 * Actualiza la imagen de un post (elimina la anterior y sube la nueva)
 * @param {File} newFile - Nueva imagen
 * @param {string} oldImageUrl - URL de la imagen anterior
 * @param {string} userId - ID del usuario
 * @returns {Promise<{url: string|null, error: Object|null}>}
 */
export async function updatePostImage(newFile, oldImageUrl, userId) {
    try {
        // Subir nueva imagen
        const { url, error } = await uploadPostImage(newFile, userId);

        if (error) {
            return { url: null, error };
        }

        // Eliminar imagen anterior (si existe)
        if (oldImageUrl) {
            await deletePostImage(oldImageUrl);
        }

        return { url, error: null };
    } catch (error) {
        console.error('Error in updatePostImage:', error);
        return { url: null, error: { message: 'Error al actualizar la imagen' } };
    }
}

/**
 * Valida si un archivo es una imagen válida
 * @param {File} file - Archivo a validar
 * @returns {Object} - { valid: boolean, error: string|null }
 */
export function validateImageFile(file) {
    if (!file) {
        return { valid: false, error: 'No se ha seleccionado ningún archivo' };
    }

    if (!file.type.startsWith('image/')) {
        return { valid: false, error: 'El archivo debe ser una imagen' };
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        return { valid: false, error: 'La imagen no debe superar los 5MB' };
    }

    // Validar formatos permitidos
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, error: 'Formato no permitido. Use JPG, PNG, GIF o WebP' };
    }

    return { valid: true, error: null };
}

/**
 * Sube una imagen de avatar de perfil al bucket de Supabase
 * @param {File} file - Archivo de imagen a subir
 * @param {string} userId - ID del usuario que sube la imagen
 * @returns {Promise<{url: string|null, error: Object|null}>}
 */
export async function uploadProfileAvatar(file, userId) {
    try {
        // Validar que sea una imagen
        const validation = validateImageFile(file);
        if (!validation.valid) {
            return { url: null, error: { message: validation.error } };
        }

        // Generar nombre único para el archivo
        const fileExt = file.name.split('.').pop();
        const fileName = `${AVATAR_FOLDER}/${userId}.${fileExt}`;

        // Subir archivo (upsert true para sobrescribir si existe)
        const { data, error } = await supabase.storage
            .from(BUCKET_NAME)
            .upload(fileName, file, {
                cacheControl: '3600',
                upsert: true // Sobrescribir avatar anterior del mismo usuario
            });

        if (error) {
            console.error('Error uploading avatar:', error);
            return { url: null, error };
        }

        console.log('Avatar uploaded successfully:', data);

        // Obtener URL pública
        const { data: { publicUrl } } = supabase.storage
            .from(BUCKET_NAME)
            .getPublicUrl(fileName);

        console.log('Avatar Public URL generated:', publicUrl);
        return { url: publicUrl, error: null };
    } catch (error) {
        console.error('Error in uploadProfileAvatar:', error);
        return { url: null, error: { message: 'Error al subir el avatar' } };
    }
}

/**
 * Normaliza una URL de imagen para que use el formato público correcto
 * @param {string} imageUrl - URL de la imagen
 * @returns {Promise<{url: string|null, error: Object|null}>}
 */
export async function getSignedUrlForImage(imageUrl) {
    try {
        if (!imageUrl) {
            return { url: null, error: { message: 'No se proporcionó URL' } };
        }

        // Si la URL ya es correcta (del dominio de Supabase), devolverla tal cual
        if (imageUrl.includes('supabase.co/storage/v1/object/public/')) {
            return { url: imageUrl, error: null };
        }

        // Si es una URL antigua que necesita conversión, regenerar la URL pública
        // Extraer el path del archivo
        let filePath;
        try {
            const url = new URL(imageUrl);
            const pathParts = url.pathname.split(`/${BUCKET_NAME}/`);
            if (pathParts.length >= 2) {
                filePath = pathParts[1];
            } else {
                // Si no se puede parsear, devolver la URL tal cual
                return { url: imageUrl, error: null };
            }
        } catch {
            // Si falla el parseo de URL, devolver tal cual
            return { url: imageUrl, error: null };
        }

        // Generar nueva URL pública
        const { data: { publicUrl } } = supabase.storage
            .from(BUCKET_NAME)
            .getPublicUrl(filePath);

        return { url: publicUrl, error: null };
    } catch (error) {
        console.error('Error in getSignedUrlForImage:', error);
        return { url: imageUrl, error: null }; // En caso de error, devolver la URL original
    }
}

/**
 * Elimina el avatar de perfil del bucket de Supabase
 * @param {string} avatarUrl - URL del avatar a eliminar
 * @returns {Promise<{success: boolean, error: Object|null}>}
 */
export async function deleteProfileAvatar(avatarUrl) {
    try {
        if (!avatarUrl) {
            return { success: true, error: null };
        }

        // Extraer el path del archivo de la URL
        const url = new URL(avatarUrl);
        const pathParts = url.pathname.split(`/${BUCKET_NAME}/`);
        if (pathParts.length < 2) {
            return { success: false, error: { message: 'URL de avatar inválida' } };
        }

        const filePath = pathParts[1];

        // Solo eliminar si está en la carpeta de avatares
        if (!filePath.startsWith(AVATAR_FOLDER)) {
            return { success: true, error: null }; // No eliminar URLs externas
        }

        // Eliminar archivo
        const { error } = await supabase.storage
            .from(BUCKET_NAME)
            .remove([filePath]);

        if (error) {
            console.error('Error deleting avatar:', error);
            return { success: false, error };
        }

        return { success: true, error: null };
    } catch (error) {
        console.error('Error in deleteProfileAvatar:', error);
        // No fallar si hay error al eliminar el avatar
        return { success: true, error: null };
    }
}

/**
 * Actualiza el avatar de perfil (elimina el anterior y sube el nuevo)
 * @param {File} newFile - Nueva imagen de avatar
 * @param {string} oldAvatarUrl - URL del avatar anterior
 * @param {string} userId - ID del usuario
 * @returns {Promise<{url: string|null, error: Object|null}>}
 */
export async function updateProfileAvatar(newFile, oldAvatarUrl, userId) {
    try {
        // Subir nueva imagen (con upsert true, sobrescribe automáticamente)
        const { url, error } = await uploadProfileAvatar(newFile, userId);

        if (error) {
            return { url: null, error };
        }

        return { url, error: null };
    } catch (error) {
        console.error('Error in updateProfileAvatar:', error);
        return { url: null, error: { message: 'Error al actualizar el avatar' } };
    }
}
