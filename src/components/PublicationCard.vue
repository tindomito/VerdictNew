<template>
    <article class="bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
        <!-- Header de la publicación -->
        <div class="p-6">
            <div class="flex items-start justify-between mb-4">
                <!-- Info del autor -->
                <div class="flex items-center space-x-3">
                    <RouterLink :to="`/profile/${createSlugFromDisplayName(publication.display_name)}`">
                        <div class="w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-pink-600 flex items-center justify-center text-white font-bold">
                            <img
                                v-if="avatarUrl"
                                :src="avatarUrl"
                                :alt="publication.display_name"
                                class="w-full h-full rounded-full object-cover"
                                @error="handleAvatarError"
                            />
                            <span v-else>{{ authorInitials }}</span>
                        </div>
                    </RouterLink>
                    <div>
                        <RouterLink
                            :to="`/profile/${createSlugFromDisplayName(publication.display_name)}`"
                            class="font-semibold text-white hover:text-indigo-400 transition-colors"
                        >
                            {{ publication.display_name || 'Usuario' }}
                        </RouterLink>
                        <div class="flex items-center space-x-2 text-sm text-gray-400">
                            <span>{{ formattedDate }}</span>
                            <span>•</span>
                            <span class="flex items-center">
                                {{ getCategoryIcon(publication.category) }} {{ getCategoryName(publication.category) }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Botón de opciones (solo si es el autor) -->
                <div v-if="isOwnPublication" class="relative">
                    <button
                        @click="showOptions = !showOptions"
                        class="p-2 hover:bg-gray-700 rounded-full transition-colors"
                    >
                        <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path>
                        </svg>
                    </button>

                    <div v-if="showOptions" class="absolute right-0 mt-2 w-48 bg-gray-700 rounded-md shadow-lg z-10 border border-gray-600">
                        <button
                            @click="handleEdit"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-600"
                        >
                            Editar
                        </button>
                        <button
                            @click="handleDelete"
                            class="block w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-900/20"
                        >
                            Eliminar
                        </button>
                    </div>
                </div>
            </div>

            <!-- Contenido de la publicación -->
            <div class="mb-4">
                <h2 class="text-xl font-bold text-white mb-3">
                    {{ publication.title }}
                </h2>
                <p class="text-gray-300 whitespace-pre-wrap leading-relaxed">
                    {{ publication.content }}
                </p>

                <!-- Imagen de la publicación -->
                <div v-if="publication.image_url" class="mt-4">
                    <img
                        :src="publication.image_url"
                        :alt="publication.title"
                        class="w-full rounded-lg object-cover max-h-[500px] cursor-pointer hover:opacity-95 transition-opacity"
                        @click="openImageModal"
                        @error="handleImageError"
                    />
                </div>
            </div>

            <!-- Acciones de la publicación -->
            <div class="flex items-center space-x-6 pt-4 border-t border-gray-700">
                <button
                    @click="handleLike"
                    class="flex items-center space-x-2 text-gray-400 hover:text-pink-400 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                    </svg>
                    <span class="text-sm font-medium">{{ publication.likes_count || 0 }}</span>
                </button>

                <button
                    @click="handleBookmark"
                    class="flex items-center space-x-2 text-gray-400 hover:text-yellow-400 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
                    </svg>
                    <span class="text-sm font-medium">Guardar</span>
                </button>

                <button
                    @click="handleShare"
                    class="flex items-center space-x-2 text-gray-400 hover:text-indigo-400 transition-colors"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
                    </svg>
                    <span class="text-sm font-medium">Compartir</span>
                </button>
            </div>
        </div>

        <!-- Modal para imagen en tamaño completo -->
        <Teleport to="body">
            <transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="opacity-0"
                enter-to-class="opacity-100"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
            >
                <div
                    v-if="showImageModal"
                    @click="closeImageModal"
                    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90 p-4"
                >
                    <div class="relative max-w-7xl max-h-screen">
                        <button
                            @click="closeImageModal"
                            class="absolute top-4 right-4 p-2 bg-gray-800 text-white rounded-full hover:bg-gray-700 transition-colors z-10"
                        >
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                        <img
                            :src="publication.image_url"
                            :alt="publication.title"
                            class="max-w-full max-h-screen object-contain"
                            @click.stop
                        />
                    </div>
                </div>
            </transition>
        </Teleport>

        <!-- Modal de confirmación de eliminación -->
        <Teleport to="body">
            <transition
                enter-active-class="transition ease-out duration-300"
                enter-from-class="opacity-0"
                enter-to-class="opacity-100"
                leave-active-class="transition ease-in duration-200"
                leave-from-class="opacity-100"
                leave-to-class="opacity-0"
            >
                <div
                    v-if="showDeleteConfirmation"
                    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
                    @click="cancelDelete"
                >
                    <transition
                        enter-active-class="transition ease-out duration-300"
                        enter-from-class="opacity-0 scale-95"
                        enter-to-class="opacity-100 scale-100"
                        leave-active-class="transition ease-in duration-200"
                        leave-from-class="opacity-100 scale-100"
                        leave-to-class="opacity-0 scale-95"
                    >
                        <div
                            @click.stop
                            class="bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6"
                        >
                            <div class="flex items-center justify-center mb-4">
                                <div class="w-12 h-12 rounded-full bg-red-900/30 flex items-center justify-center">
                                    <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                                    </svg>
                                </div>
                            </div>

                            <h3 class="text-lg font-semibold text-white text-center mb-2">
                                ¿Eliminar publicación?
                            </h3>

                            <div class="mb-6">
                                <p class="text-sm text-gray-300 text-center mb-3">
                                    Estás por eliminar la siguiente publicación:
                                </p>
                                <div class="bg-gray-700 rounded-lg p-3 border border-gray-600">
                                    <p class="text-sm font-medium text-white line-clamp-2">
                                        {{ publication.title }}
                                    </p>
                                    <p class="text-xs text-gray-400 mt-1">
                                        {{ getCategoryIcon(publication.category) }} {{ getCategoryName(publication.category) }}
                                    </p>
                                </div>
                                <p class="text-sm text-gray-300 text-center mt-3">
                                    Esta acción no se puede deshacer.
                                </p>
                            </div>

                            <div class="flex gap-3">
                                <button
                                    @click="cancelDelete"
                                    class="flex-1 px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors font-medium"
                                >
                                    Cancelar
                                </button>
                                <button
                                    @click="confirmDelete"
                                    class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                                >
                                    Eliminar
                                </button>
                            </div>
                        </div>
                    </transition>
                </div>
            </transition>
        </Teleport>
    </article>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';
import { getPublicationCategoryName, getPublicationCategoryIcon } from '../services/publications.js';
import { createSlugFromDisplayName } from '../services/profiles.js';
import { getSignedUrlForImage } from '../services/storage.js';

export default {
    name: 'PublicationCard',
    props: {
        publication: {
            type: Object,
            required: true
        }
    },
    emits: ['edit', 'delete', 'like', 'bookmark', 'share'],
    setup() {
        const { userId } = useAuth();
        return {
            currentUserId: userId,
            getCategoryName: getPublicationCategoryName,
            getCategoryIcon: getPublicationCategoryIcon,
            createSlugFromDisplayName
        };
    },
    data() {
        return {
            showOptions: false,
            showImageModal: false,
            showDeleteConfirmation: false,
            avatarUrl: this.publication.avatar_url
        };
    },
    async mounted() {
        if (this.publication.avatar_url && !this.publication.avatar_url.includes('token=')) {
            const { url, error } = await getSignedUrlForImage(this.publication.avatar_url);
            if (!error && url) {
                this.avatarUrl = url;
            }
        }
    },
    computed: {
        isOwnPublication() {
            return this.publication.user_id === this.currentUserId;
        },

        authorInitials() {
            if (this.publication.display_name) {
                return this.publication.display_name
                    .split(' ')
                    .map(name => name.charAt(0))
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
            }
            return 'U';
        },

        formattedDate() {
            if (!this.publication.created_at) return '';

            const date = new Date(this.publication.created_at);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffMinutes = Math.floor(diffTime / (1000 * 60));
            const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

            if (diffMinutes < 1) return 'Ahora';
            if (diffMinutes < 60) return `Hace ${diffMinutes} min`;
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
            this.$emit('edit', this.publication);
        },

        handleDelete() {
            this.showOptions = false;
            this.showDeleteConfirmation = true;
        },

        confirmDelete() {
            this.showDeleteConfirmation = false;
            this.$emit('delete', this.publication.id);
        },

        cancelDelete() {
            this.showDeleteConfirmation = false;
        },

        handleLike() {
            this.$emit('like', this.publication.id);
        },

        handleBookmark() {
            this.$emit('bookmark', this.publication.id);
        },

        handleShare() {
            this.$emit('share', this.publication);
        },

        handleAvatarError(event) {
            event.target.style.display = 'none';
        },

        handleImageError(event) {
            console.error('Error loading publication image:', this.publication.image_url);
            setTimeout(() => {
                event.target.src = this.publication.image_url + '?retry=' + Date.now();
            }, 1000);
        },

        openImageModal() {
            this.showImageModal = true;
        },

        closeImageModal() {
            this.showImageModal = false;
        }
    }
};
</script>
