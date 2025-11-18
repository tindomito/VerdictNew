/**
 * Servicios para manejar el almacenamiento de archivos en Supabase Storage
 */
import { supabase } from './supabase.js';

const BUCKET_NAME = 'post-images';

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

        // Obtener URL pública
        const { data: { publicUrl } } = supabase.storage
            .from(BUCKET_NAME)
            .getPublicUrl(data.path);

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
