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
            <div class="bg-gray-700 rounded-lg px-3 py-2">
                <div class="flex items-center justify-between mb-1">
                    <RouterLink
                        :to="`/profile/${createSlugFromDisplayName(comment.display_name)}`"
                        class="font-semibold text-sm text-white hover:text-indigo-400 transition-colors"
                    >
                        {{ comment.display_name || 'Usuario' }}
                    </RouterLink>

                    <!-- Botón de opciones (solo si es el autor o Admin) -->
                    <div v-if="isOwnComment && !isEditing" class="relative">
                        <button
                            @click="showOptions = !showOptions"
                            class="p-1 hover:bg-gray-600 rounded-full transition-colors"
                        >
                            <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                            </svg>
                        </button>

                        <div v-if="showOptions" class="absolute right-0 mt-2 w-32 bg-gray-800 rounded-md shadow-lg z-10 border border-gray-600">
                            <button
                                @click="startEditing"
                                class="block w-full text-left px-3 py-2 text-xs text-gray-300 hover:bg-gray-700"
                            >
                                Editar
                            </button>
                            <button
                                @click="handleDelete"
                                class="block w-full text-left px-3 py-2 text-xs text-red-400 hover:bg-red-900/20"
                            >
                                Eliminar
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Modo edición -->
                <div v-if="isEditing">
                    <textarea
                        v-model="editContent"
                        @keydown.escape="cancelEditing"
                        @keydown.ctrl.enter="saveEdit"
                        @keydown.meta.enter="saveEdit"
                        rows="2"
                        class="w-full px-2 py-1 bg-gray-600 text-white border border-gray-500 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                        ref="editTextarea"
                    ></textarea>
                    <div class="flex justify-end mt-2 space-x-2">
                        <button
                            @click="cancelEditing"
                            class="px-2 py-1 text-xs font-medium text-gray-300 bg-gray-600 rounded hover:bg-gray-500 transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            @click="saveEdit"
                            :disabled="!editContent.trim() || isSaving"
                            class="px-2 py-1 text-xs font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                        >
                            {{ isSaving ? 'Guardando...' : 'Guardar' }}
                        </button>
                    </div>
                </div>

                <!-- Modo visualización -->
                <p v-else class="text-sm text-gray-300 whitespace-pre-wrap break-words">
                    {{ comment.content }}
                </p>
            </div>

            <!-- Fecha -->
            <div class="mt-1 px-3">
                <span class="text-xs text-gray-400">{{ formattedDate }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';
import { useProfile } from '../composables/useProfile.js';
import { createSlugFromDisplayName } from '../services/profiles.js';

export default {
    name: 'CommentCard',
    props: {
        comment: {
            type: Object,
            required: true
        }
    },
    emits: ['edit', 'delete', 'save'],
    setup() {
        const { userId } = useAuth();
        const { isPro } = useProfile();
        return { currentUserId: userId, isAdmin: isPro, createSlugFromDisplayName };
    },
    data() {
        return {
            showOptions: false,
            isEditing: false,
            editContent: '',
            isSaving: false
        };
    },
    computed: {
        /**
         * Si el comentario pertenece al usuario actual O si es Admin
         */
        isOwnComment() {
            return this.comment.user_id === this.currentUserId || this.isAdmin;
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
        startEditing() {
            this.showOptions = false;
            this.editContent = this.comment.content;
            this.isEditing = true;
            this.$nextTick(() => {
                if (this.$refs.editTextarea) {
                    this.$refs.editTextarea.focus();
                }
            });
        },

        cancelEditing() {
            this.isEditing = false;
            this.editContent = '';
        },

        async saveEdit() {
            if (!this.editContent.trim() || this.isSaving) return;

            this.isSaving = true;
            this.$emit('save', {
                commentId: this.comment.id,
                content: this.editContent.trim()
            });
        },

        // Método para resetear el estado después de guardar (llamado desde el padre)
        resetEditState(success = true) {
            this.isSaving = false;
            if (success) {
                this.isEditing = false;
                this.editContent = '';
            }
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
