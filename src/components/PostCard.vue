<template>
    <article class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
        <!-- Header del post -->
        <div class="p-6">
            <div class="flex items-start justify-between mb-4">
                <!-- Info del autor -->
                <div class="flex items-center space-x-3">
                    <RouterLink :to="`/profile/${createSlugFromDisplayName(post.display_name)}`">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
                            <img 
                                v-if="post.avatar_url" 
                                :src="post.avatar_url" 
                                :alt="post.display_name"
                                class="w-full h-full rounded-full object-cover"
                                @error="handleImageError"
                            />
                            <span v-else>{{ authorInitials }}</span>
                        </div>
                    </RouterLink>
                    <div>
                        <RouterLink 
                            :to="`/profile/${createSlugFromDisplayName(post.display_name)}`"
                            class="font-semibold text-gray-900 hover:text-indigo-600 transition-colors"
                        >
                            {{ post.display_name || 'Usuario' }}
                        </RouterLink>
                        <div class="flex items-center space-x-2 text-sm text-gray-500">
                            <span>{{ formattedDate }}</span>
                            <span>•</span>
                            <span class="flex items-center">
                                {{ getCategoryIcon(post.category) }} {{ getCategoryName(post.category) }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Botón de opciones (solo si es el autor) -->
                <div v-if="isOwnPost" class="relative">
                    <button
                        @click="showOptions = !showOptions"
                        class="p-2 hover:bg-gray-100 rounded-full transition-colors"
                    >
                        <svg class="w-5 h-5 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                        </svg>
                    </button>
                    
                    <div v-if="showOptions" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200">
                        <button
                            @click="handleEdit"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            Editar
                        </button>
                        <button
                            @click="handleDelete"
                            class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Contenido del post -->
            <div class="mb-4">
                <h2 class="text-xl font-bold text-gray-900 mb-2">
                    {{ post.title }}
                </h2>
                <p class="text-gray-700 whitespace-pre-wrap">
                    {{ post.content }}
                </p>
            </div>

            <!-- Acciones del post -->
            <div class="flex items-center space-x-6 pt-4 border-t border-gray-200">
                <!-- Likes (placeholder) -->
                <button
                    @click="handleLike"
                    class="flex items-center space-x-2 text-gray-500 hover:text-indigo-600 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"></path>
                    </svg>
                    <span class="text-sm font-medium">{{ post.likes_count || 0 }}</span>
                </button>

                <!-- Comentarios (placeholder) -->
                <button
                    @click="handleComment"
                    class="flex items-center space-x-2 text-gray-500 hover:text-indigo-600 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                    </svg>
                    <span class="text-sm font-medium">{{ post.comments_count || 0 }}</span>
                </button>

                <!-- Compartir (placeholder) -->
                <button
                    @click="handleShare"
                    class="flex items-center space-x-2 text-gray-500 hover:text-indigo-600 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
                    </svg>
                    <span class="text-sm font-medium">Compartir</span>
                </button>
            </div>
        </div>
    </article>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';
import { getCategoryName, getCategoryIcon } from '../services/posts.js';
import { createSlugFromDisplayName } from '../services/profiles.js';

export default {
    name: 'PostCard',
    props: {
        post: {
            type: Object,
            required: true
        }
    },
    emits: ['edit', 'delete', 'like', 'comment', 'share'],
    setup() {
        const { userId } = useAuth();
        return { currentUserId: userId, getCategoryName, getCategoryIcon, createSlugFromDisplayName };
    },
    data() {
        return {
            showOptions: false
        };
    },
    computed: {
        /**
         * Si el post pertenece al usuario actual
         */
        isOwnPost() {
            return this.post.user_id === this.currentUserId;
        },
        
        /**
         * Iniciales del autor
         */
        authorInitials() {
            if (this.post.display_name) {
                return this.post.display_name
                    .split(' ')
                    .map(name => name.charAt(0))
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
            }
            return 'U';
        },
        
        /**
         * Fecha formateada
         */
        formattedDate() {
            if (!this.post.created_at) return '';
            
            const date = new Date(this.post.created_at);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays === 0) return 'Hoy';
            if (diffDays === 1) return 'Ayer';
            if (diffDays < 7) return `Hace ${diffDays} días`;
            
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short',
                day: 'numeric'
            });
        }
    },
    methods: {
        handleEdit() {
            this.showOptions = false;
            this.$emit('edit', this.post);
        },
        
        handleDelete() {
            this.showOptions = false;
            if (confirm('¿Estás seguro de que quieres eliminar este post?')) {
                this.$emit('delete', this.post.id);
            }
        },
        
        handleLike() {
            this.$emit('like', this.post.id);
        },
        
        handleComment() {
            this.$emit('comment', this.post.id);
        },
        
        handleShare() {
            this.$emit('share', this.post);
        },
        
        handleImageError(event) {
            event.target.style.display = 'none';
        }
    }
};
</script>