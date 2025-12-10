/**
 * Servicios para manejar el chat público/global
 * Interactúa con las tablas global_chat_messages y chat_messages_with_users de Supabase
 */
import { supabase } from './supabase.js';

/**
 * Obtiene todos los mensajes del chat global
 * @param {number} limit - Límite de mensajes a obtener (opcional)
 * @returns {Promise<{messages: Array, error: Object|null}>}
 */
export async function getGlobalMessages(limit = null) {
    try {
        let query = supabase
            .from('chat_messages_with_users')
            .select('*')
            .order('created_at', { ascending: true });

        if (limit) {
            query = query.limit(limit);
        }

        const { data, error } = await query;

        if (error) {
            console.error('Error fetching global messages:', error);
            return { messages: [], error };
        }

        return { messages: data || [], error: null };
    } catch (error) {
        console.error('Unexpected error fetching global messages:', error);
        return { messages: [], error: { message: 'Error al obtener mensajes del chat' } };
    }
}

/**
 * Obtiene un mensaje específico por su ID (con datos del usuario)
 * @param {string} messageId - ID del mensaje
 * @returns {Promise<{message: Object|null, error: Object|null}>}
 */
export async function getGlobalMessageById(messageId) {
    try {
        const { data, error } = await supabase
            .from('chat_messages_with_users')
            .select('*')
            .eq('id', messageId)
            .single();

        if (error) {
            console.error('Error fetching message by ID:', error);
            return { message: null, error };
        }

        return { message: data, error: null };
    } catch (error) {
        console.error('Unexpected error fetching message by ID:', error);
        return { message: null, error: { message: 'Error al obtener el mensaje' } };
    }
}

/**
 * Envía un mensaje al chat global
 * @param {string} userId - ID del usuario que envía
 * @param {string} content - Contenido del mensaje
 * @returns {Promise<{message: Object|null, error: Object|null}>}
 */
export async function sendGlobalMessage(userId, content) {
    try {
        // Validación básica
        if (!content || !content.trim()) {
            return {
                message: null,
                error: { message: 'El mensaje no puede estar vacío' }
            };
        }

        if (!userId) {
            return {
                message: null,
                error: { message: 'Usuario no autenticado' }
            };
        }

        const { data, error } = await supabase
            .from('global_chat_messages')
            .insert({
                user_id: userId,
                content: content.trim()
            })
            .select()
            .single();

        if (error) {
            console.error('Error sending global message:', error);
            return { message: null, error };
        }

        return { message: data, error: null };
    } catch (error) {
        console.error('Unexpected error sending global message:', error);
        return { message: null, error: { message: 'Error al enviar mensaje' } };
    }
}

/**
 * Suscribe a nuevos mensajes del chat global en tiempo real
 * @param {Function} onNewMessage - Callback cuando llega un mensaje nuevo
 * @returns {Object} Objeto del canal para desuscribirse
 */
export function subscribeToGlobalChat(onNewMessage) {
    const channel = supabase.channel('global_chat_realtime');

    channel
        .on('postgres_changes', {
            event: 'INSERT',
            schema: 'public',
            table: 'global_chat_messages'
        }, async (payload) => {
            // Obtener el mensaje completo con datos del usuario
            const { message } = await getGlobalMessageById(payload.new.id);

            if (message && onNewMessage) {
                onNewMessage(message);
            }
        })
        .subscribe();

    return channel;
}

/**
 * Desuscribe del canal de chat global
 * @param {Object} channel - Canal de Supabase a desuscribir
 */
export function unsubscribeFromGlobalChat(channel) {
    if (channel) {
        channel.unsubscribe();
    }
}
