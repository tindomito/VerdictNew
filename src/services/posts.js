/**
 * Servicios para manejar publicaciones (posts)
 * Interactúa con la tabla posts de Supabase
 */
import { supabase } from './supabase.js';
import { deletePostImage } from './storage.js';

/**
 * Categorías disponibles para posts
 */
export const POST_CATEGORIES = [
    { id: 'general', name: 'General', icon: '💬' },
    { id: 'resultados', name: 'Resultados', icon: '🏆' },
    { id: 'predicciones', name: 'Predicciones', icon: '🔮' },
    { id: 'analisis', name: 'Análisis', icon: '📊' },
    { id: 'tecnica', name: 'Técnica', icon: '🥋' },
    { id: 'noticias', name: 'Noticias', icon: '📰' },
    { id: 'discusion', name: 'Discusión', icon: '🗣️' }
];

/**
 * Crea un nuevo post
 * @param {Object} postData - Datos del post
 * @returns {Promise<{post: Object|null, error: Object|null}>}
 */
export async function createPost(postData) {
    try {
        const { data: { user } } = await supabase.auth.getUser();

        if (!user) {
            return { post: null, error: { message: 'Usuario no autenticado' } };
        }

        const insertData = {
            user_id: user.id,
            title: postData.title,
            content: postData.content,
            category: postData.category || 'general'
        };

        // Agregar image_url si existe
        if (postData.image_url) {
            insertData.image_url = postData.image_url;
        }

        const { data, error } = await supabase
            .from('posts')
            .insert(insertData)
            .select()
            .single();

        if (error) {
            return { post: null, error };
        }

        return { post: data, error: null };
    } catch (error) {
        return { post: null, error: { message: 'Error al crear post' } };
    }
}

/**
 * Obtiene todos los posts con paginación
 * @param {number} page - Página actual (empezando en 0)
 * @param {number} pageSize - Tamaño de página
 * @param {string} category - Filtrar por categoría (opcional)
 * @returns {Promise<{posts: Array, error: Object|null}>}
 */
export async function getPosts(page = 0, pageSize = 20, category = null) {
    try {
        const from = page * pageSize;
        const to = from + pageSize - 1;

        let query = supabase
            .from('posts_with_users')
            .select('*')
            .order('created_at', { ascending: false })
            .range(from, to);

        // Filtrar por categoría si se especifica
        if (category && category !== 'all') {
            query = query.eq('category', category);
        }

        const { data, error } = await query;

        if (error) {
            return { posts: [], error };
        }

        return { posts: data || [], error: null };
    } catch (error) {
        return { posts: [], error: { message: 'Error al obtener posts' } };
    }
}

/**
 * Obtiene un post específico por ID
 * @param {string} postId - ID del post
 * @returns {Promise<{post: Object|null, error: Object|null}>}
 */
export async function getPost(postId) {
    try {
        const { data, error } = await supabase
            .from('posts_with_users')
            .select('*')
            .eq('id', postId)
            .single();

        if (error) {
            return { post: null, error };
        }

        return { post: data, error: null };
    } catch (error) {
        return { post: null, error: { message: 'Error al obtener post' } };
    }
}

/**
 * Obtiene posts de un usuario específico
 * @param {string} userId - ID del usuario
 * @param {number} page - Página actual
 * @param {number} pageSize - Tamaño de página
 * @returns {Promise<{posts: Array, error: Object|null}>}
 */
export async function getPostsByUser(userId, page = 0, pageSize = 20) {
    try {
        const from = page * pageSize;
        const to = from + pageSize - 1;

        const { data, error } = await supabase
            .from('posts_with_users')
            .select('*')
            .eq('user_id', userId)
            .order('created_at', { ascending: false })
            .range(from, to);

        if (error) {
            return { posts: [], error };
        }

        return { posts: data || [], error: null };
    } catch (error) {
        return { posts: [], error: { message: 'Error al obtener posts del usuario' } };
    }
}

/**
 * Actualiza un post existente
 * @param {string} postId - ID del post
 * @param {Object} updates - Datos a actualizar
 * @returns {Promise<{post: Object|null, error: Object|null}>}
 */
export async function updatePost(postId, updates) {
    try {
        const { data, error } = await supabase
            .from('posts')
            .update(updates)
            .eq('id', postId)
            .select()
            .single();

        if (error) {
            return { post: null, error };
        }

        return { post: data, error: null };
    } catch (error) {
        return { post: null, error: { message: 'Error al actualizar post' } };
    }
}

/**
 * Elimina un post
 * @param {string} postId - ID del post
 * @returns {Promise<{success: boolean, error: Object|null}>}
 */
export async function deletePost(postId) {
    try {
        // Primero obtener el post para saber si tiene imagen
        const { data: post } = await supabase
            .from('posts')
            .select('image_url')
            .eq('id', postId)
            .single();

        // Eliminar el post
        const { error } = await supabase
            .from('posts')
            .delete()
            .eq('id', postId);

        if (error) {
            return { success: false, error };
        }

        // Eliminar la imagen si existe
        if (post?.image_url) {
            await deletePostImage(post.image_url);
        }

        return { success: true, error: null };
    } catch (error) {
        return { success: false, error: { message: 'Error al eliminar post' } };
    }
}

/**
 * Suscribe a cambios en tiempo real de posts
 * @param {Function} onInsert - Callback cuando se inserta un post
 * @param {Function} onUpdate - Callback cuando se actualiza un post
 * @param {Function} onDelete - Callback cuando se elimina un post
 * @returns {Object} Subscription object
 */
export function subscribeToPostsChanges(onInsert, onUpdate, onDelete) {
    const channel = supabase.channel('posts_changes');

    if (onInsert) {
        channel.on('postgres_changes', {
            event: 'INSERT',
            schema: 'public',
            table: 'posts'
        }, async (payload) => {
            // Obtener el post completo con datos del usuario
            const { post } = await getPost(payload.new.id);
            if (post) {
                onInsert(post);
            }
        });
    }

    if (onUpdate) {
        channel.on('postgres_changes', {
            event: 'UPDATE',
            schema: 'public',
            table: 'posts'
        }, async (payload) => {
            const { post } = await getPost(payload.new.id);
            if (post) {
                onUpdate(post);
            }
        });
    }

    if (onDelete) {
        channel.on('postgres_changes', {
            event: 'DELETE',
            schema: 'public',
            table: 'posts'
        }, (payload) => {
            onDelete(payload.old.id);
        });
    }

    channel.subscribe();
    return channel;
}

/**
 * Obtiene el nombre de una categoría
 * @param {string} categoryId - ID de la categoría
 * @returns {string} Nombre de la categoría
 */
export function getCategoryName(categoryId) {
    const category = POST_CATEGORIES.find(cat => cat.id === categoryId);
    return category ? category.name : 'General';
}

/**
 * Obtiene el icono de una categoría
 * @param {string} categoryId - ID de la categoría
 * @returns {string} Icono de la categoría
 */
export function getCategoryIcon(categoryId) {
    const category = POST_CATEGORIES.find(cat => cat.id === categoryId);
    return category ? category.icon : '💬';
}