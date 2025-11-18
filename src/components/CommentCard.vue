<template>
    <div class="flex space-x-3 py-3">
        <!-- Avatar del usuario -->
        <RouterLink :to="`/profile/${createSlugFromDisplayName(comment.display_name)}`">
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold flex-shrink-0">
                <img
                    v-if="comment.avatar_url"
                    :src="comment.avatar_url"
                    :alt="comment.display_name"
                    class="w-full h-full rounded-full object-cover"
                    @error="handleImageError"
                />
                <span v-else class="text-xs">{{ authorInitials }}</span>
            </div>
        </RouterLink>

        <!-- Contenido del comentario -->
        <div class="flex-1 min-w-0">
            <div class="bg-gray-50 rounded-lg px-3 py-2">
                <div class="flex items-center justify-between mb-1">
                    <RouterLink
                        :to="`/profile/${createSlugFromDisplayName(comment.display_name)}`"
                        class="font-semibold text-sm text-gray-900 hover:text-indigo-600 transition-colors"
                    >
                        {{ comment.display_name || 'Usuario' }}
                    </RouterLink>

                    <!-- Botón de opciones (solo si es el autor) -->
                    <div v-if="isOwnComment" class="relative">
                        <button
                            @click="showOptions = !showOptions"
                            class="p-1 hover:bg-gray-200 rounded-full transition-colors"
                        >
                            <svg class="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                            </svg>
                        </button>

                        <div v-if="showOptions" class="absolute right-0 mt-2 w-32 bg-white rounded-md shadow-lg z-10 border border-gray-200">
                            <button
                                @click="handleEdit"
                                class="block w-full text-left px-3 py-2 text-xs text-gray-700 hover:bg-gray-100"
                            >
                                Editar
                            </button>
                            <button
                                @click="handleDelete"
                                class="block w-full text-left px-3 py-2 text-xs text-red-600 hover:bg-red-50"
                            >
                                Eliminar
                            </button>
                        </div>
                    </div>
                </div>

                <p class="text-sm text-gray-700 whitespace-pre-wrap break-words">
                    {{ comment.content }}
                </p>
            </div>

            <!-- Fecha -->
            <div class="mt-1 px-3">
                <span class="text-xs text-gray-500">{{ formattedDate }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';
import { createSlugFromDisplayName } from '../services/profiles.js';

export default {
    name: 'CommentCard',
    props: {
        comment: {
            type: Object,
            required: true
        }
    },
    emits: ['edit', 'delete'],
    setup() {
        const { userId } = useAuth();
        return { currentUserId: userId, createSlugFromDisplayName };
    },
    data() {
        return {
            showOptions: false
        };
    },
    computed: {
        /**
         * Si el comentario pertenece al usuario actual
         */
        isOwnComment() {
            return this.comment.user_id === this.currentUserId;
        },

        /**
         * Iniciales del autor
         */
        authorInitials() {
            if (this.comment.display_name) {
                return this.comment.display_name
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
            if (!this.comment.created_at) return '';

            const date = new Date(this.comment.created_at);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffMinutes = Math.floor(diffTime / (1000 * 60));
            const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            if (diffMinutes < 1) return 'Ahora';
            if (diffMinutes < 60) return `Hace ${diffMinutes}m`;
            if (diffHours < 24) return `Hace ${diffHours}h`;
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
            this.$emit('edit', this.comment);
        },

        handleDelete() {
            this.showOptions = false;
            if (confirm('¿Estás seguro de que quieres eliminar este comentario?')) {
                this.$emit('delete', this.comment.id);
            }
        },

        handleImageError(event) {
            event.target.style.display = 'none';
        }
    }
};
</script>
