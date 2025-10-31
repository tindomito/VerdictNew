<template>
    <div class="max-w-6xl mx-auto">
        <AppH1>Chat Global</AppH1>
        <p class="text-gray-600 mb-6">Conecta en tiempo real con la comunidad MMA</p>

        <div class="flex flex-col lg:flex-row gap-6">
            <!-- Lista de mensajes -->
            <section class="flex-1 bg-white rounded-lg shadow-md overflow-hidden flex flex-col" style="height: 600px;">
                <div class="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
                    <h2 class="text-white font-semibold flex items-center">
                        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z"></path>
                            <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z"></path>
                        </svg>
                        Mensajes ({{ messages.length }})
                    </h2>
                </div>

                <!-- Loading state -->
                <div v-if="loading" class="flex-1 flex items-center justify-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
                </div>

                <!-- Lista de mensajes -->
                <div v-else ref="messageContainer" class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
                    <div
                        v-for="message in messages"
                        :key="message.id"
                        :class="[
                            'flex items-start space-x-3 animate-fade-in',
                            message.user_id === currentUserId ? 'flex-row-reverse space-x-reverse' : ''
                        ]"
                    >
                        <!-- Avatar -->
                        <RouterLink 
                            :to="`/profile/${createSlugFromDisplayName(message.display_name)}`"
                            class="flex-shrink-0"
                        >
                            <div class="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
                                <img 
                                    v-if="message.avatar_url" 
                                    :src="message.avatar_url" 
                                    :alt="message.display_name"
                                    class="w-full h-full rounded-full object-cover"
                                    @error="handleImageError"
                                />
                                <span v-else>{{ getInitials(message.display_name) }}</span>
                            </div>
                        </RouterLink>

                        <!-- Mensaje -->
                        <div :class="[
                            'flex-1 max-w-md',
                            message.user_id === currentUserId ? 'text-right' : ''
                        ]">
                            <div class="flex items-baseline space-x-2 mb-1">
                                <RouterLink 
                                    :to="`/profile/${createSlugFromDisplayName(message.display_name)}`"
                                    :class="[
                                        'font-semibold text-sm hover:text-indigo-600 transition-colors',
                                        message.user_id === currentUserId ? 'order-2' : ''
                                    ]"
                                >
                                    {{ message.display_name || 'Usuario' }}
                                </RouterLink>
                                <span class="text-xs text-gray-500">
                                    {{ formatTime(message.created_at) }}
                                </span>
                            </div>
                            <div :class="[
                                'inline-block px-4 py-2 rounded-2xl shadow-sm',
                                message.user_id === currentUserId 
                                    ? 'bg-indigo-600 text-white rounded-br-none' 
                                    : 'bg-white text-gray-800 rounded-bl-none'
                            ]">
                                <p class="text-sm whitespace-pre-wrap break-words">{{ message.content }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Mensaje vacío -->
                    <div v-if="messages.length === 0" class="text-center py-12 text-gray-500">
                        <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                        </svg>
                        <p class="text-gray-600 font-medium">No hay mensajes aún</p>
                        <p class="text-sm text-gray-500 mt-1">Sé el primero en enviar un mensaje</p>
                    </div>
                </div>
            </section>

            <!-- Formulario de envío -->
            <aside class="lg:w-80">
                <div class="bg-white rounded-lg shadow-md p-6 sticky top-4">
                    <h2 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                        <svg class="w-5 h-5 mr-2 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"></path>
                        </svg>
                        Enviar Mensaje
                    </h2>

                    <!-- Info del usuario -->
                    <div v-if="isAuthenticated" class="mb-4 p-3 bg-indigo-50 rounded-lg">
                        <p class="text-xs text-gray-600 mb-1">Enviando como:</p>
                        <p class="font-medium text-gray-900">{{ userDisplayName || userEmail }}</p>
                    </div>

                    <!-- Formulario -->
                    <form v-if="isAuthenticated" @submit.prevent="handleSubmit">
                        <div class="mb-4">
                            <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                                Mensaje
                            </label>
                            <textarea 
                                id="content"
                                v-model="newMessage.content"
                                :disabled="sending"
                                required
                                rows="4"
                                maxlength="500"
                                placeholder="Escribe tu mensaje..."
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none disabled:opacity-50"
                            ></textarea>
                            <p class="mt-1 text-xs text-gray-500 text-right">
                                {{ newMessage.content.length }}/500
                            </p>
                        </div>

                        <button 
                            type="submit"
                            :disabled="sending || !newMessage.content.trim()"
                            class="w-full bg-indigo-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
                        >
                            <span v-if="!sending">Enviar</span>
                            <span v-else class="flex items-center justify-center">
                                <svg class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Enviando...
                            </span>
                        </button>
                    </form>

                    <!-- No autenticado -->
                    <div v-else class="text-center py-8">
                        <svg class="w-12 h-12 mx-auto mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                        </svg>
                        <p class="text-gray-600 mb-4">Debes iniciar sesión para enviar mensajes</p>
                        <RouterLink 
                            to="/login"
                            class="inline-block bg-indigo-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-indigo-700 transition duration-200"
                        >
                            Iniciar Sesión
                        </RouterLink>
                    </div>
                </div>
            </aside>
        </div>
    </div>
</template>

<script>
import AppH1 from '../components/AppH1.vue';
import { supabase } from '../services/supabase';
import { useAuth } from '../composables/useAuth.js';
import { createSlugFromDisplayName } from '../services/profiles.js';

export default {
    name: 'PublicChat',
    components: { AppH1 },
    setup() {
        const { isAuthenticated, userId, userEmail, userDisplayName } = useAuth();
        return { 
            isAuthenticated, 
            currentUserId: userId, 
            userEmail, 
            userDisplayName,
            createSlugFromDisplayName
        };
    },
    data() {
        return {
            messages: [],
            newMessage: {
                content: ''
            },
            loading: true,
            sending: false,
            chatChannel: null
        };
    },
    methods: {
        /**
 * Envía un nuevo mensaje
 */
        async handleSubmit() {
            if (!this.newMessage.content.trim()) return;
            
            this.sending = true;
            
            try {
                const { data, error } = await supabase
                    .from('global_chat_messages')
                    .insert({
                        user_id: this.currentUserId,
                        content: this.newMessage.content.trim()
                    })
                    .select()
                    .single();
                
                if (error) {
                    console.error('Error sending message:', error);
                    alert('Error al enviar mensaje');
                    return;
                }
                
                // OPTIMISTIC UPDATE: Agregar el mensaje inmediatamente
                if (data) {
                    this.messages.push({
                        id: data.id,
                        user_id: this.currentUserId,
                        content: data.content,
                        created_at: data.created_at,
                        display_name: this.userDisplayName || 'Usuario',
                        avatar_url: null // o el avatar si lo tenés
                    });
                }
                
                // Limpiar el campo
                this.newMessage.content = '';
                
                // Scroll al final
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            } catch (error) {
                console.error('Unexpected error:', error);
                alert('Error inesperado al enviar mensaje');
            } finally {
                this.sending = false;
            }
        },
        
        /**
         * Carga los mensajes iniciales
         */
        async loadMessages() {
            this.loading = true;
            
            try {
                const { data, error } = await supabase
                    .from('chat_messages_with_users')
                    .select('*')
                    .order('created_at', { ascending: true });
                
                if (error) {
                    console.error('Error loading messages:', error);
                    return;
                }
                
                this.messages = data || [];
                
                // Scroll al final después de cargar
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            } catch (error) {
                console.error('Unexpected error loading messages:', error);
            } finally {
                this.loading = false;
            }
        },
        
        /**
         * Configura suscripción en tiempo real
         */
/**
 * Configura suscripción en tiempo real
 */
        setupRealtime() {
            this.chatChannel = supabase.channel('global_chat_realtime');
            
            this.chatChannel.on('postgres_changes', {
                event: 'INSERT',
                schema: 'public',
                table: 'global_chat_messages'
            }, async (payload) => {
                // Evitar duplicados: solo agregar si no existe
                const exists = this.messages.some(msg => msg.id === payload.new.id);
                if (exists) return;
                
                // Obtener el mensaje completo con datos del usuario
                const { data } = await supabase
                    .from('chat_messages_with_users')
                    .select('*')
                    .eq('id', payload.new.id)
                    .single();
                
                if (data) {
                    this.messages.push(data);
                    
                    // Auto-scroll si estoy cerca del final
                    this.$nextTick(() => {
                        const container = this.$refs.messageContainer;
                        if (container) {
                            const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100;
                            if (isNearBottom) {
                                this.scrollToBottom();
                            }
                        }
                    });
                }
            });
            
            this.chatChannel.subscribe();
        },
        
        /**
         * Scroll al final del chat
         */
        scrollToBottom() {
            const container = this.$refs.messageContainer;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },
        
        /**
         * Obtiene iniciales del nombre
         */
        getInitials(name) {
            if (!name) return 'U';
            return name.split(' ')
                .map(n => n.charAt(0))
                .join('')
                .toUpperCase()
                .slice(0, 2);
        },
        
        /**
         * Formatea la hora del mensaje
         */
        formatTime(timestamp) {
            if (!timestamp) return '';
            
            const date = new Date(timestamp);
            const now = new Date();
            const diffMs = now - date;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return 'Ahora';
            if (diffMins < 60) return `Hace ${diffMins}m`;
            
            const diffHours = Math.floor(diffMins / 60);
            if (diffHours < 24) return `Hace ${diffHours}h`;
            
            return date.toLocaleDateString('es-ES', { 
                day: 'numeric', 
                month: 'short' 
            });
        },
        
        /**
         * Maneja errores de carga de imagen
         */
        handleImageError(event) {
            event.target.style.display = 'none';
        }
    },
    
    async mounted() {
        await this.loadMessages();
        this.setupRealtime();
    },
    
    beforeUnmount() {
        if (this.chatChannel) {
            this.chatChannel.unsubscribe();
        }
    }
};
</script>

<style scoped>
@keyframes fade-in {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fade-in 0.3s ease-out;
}
</style>