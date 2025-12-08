<template>
    <div class="border-t border-gray-700 pt-4 mt-2">
        <!-- Formulario para nuevo comentario -->
        <div class="mb-4">
            <div class="flex space-x-3">
                <!-- Avatar del usuario actual -->
                <div class="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold flex-shrink-0">
                    <span class="text-xs">{{ currentUserInitials }}</span>
                </div>

                <!-- Input de comentario -->
                <div class="flex-1">
                    <textarea
                        v-model="newCommentContent"
                        @keydown.ctrl.enter="submitComment"
                        @keydown.meta.enter="submitComment"
                        placeholder="Escribe un comentario..."
                        rows="2"
                        class="w-full px-3 py-2 bg-gray-700 text-white border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none text-sm placeholder-gray-400"
                    ></textarea>

                    <!-- Botones de acción -->
                    <div class="flex justify-end mt-2 space-x-2">
                        <button
                            v-if="newCommentContent.trim()"
                            @click="newCommentContent = ''"
                            class="px-3 py-1.5 text-xs font-medium text-gray-300 bg-gray-700 border border-gray-600 rounded-lg hover:bg-gray-600 transition-colors"
                        >
                            Cancelar
                        </button>
                        <button
                            @click="submitComment"
                            :disabled="!newCommentContent.trim() || isSubmitting"
                            class="px-3 py-1.5 text-xs font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <span v-if="!isSubmitting">Comentar</span>
                            <span v-else>Enviando...</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center py-4">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Lista de comentarios -->
        <div v-else-if="comments.length > 0" class="space-y-1">
            <CommentCard
                v-for="comment in comments"
                :key="comment.id"
                :comment="comment"
                @edit="handleEditComment"
                @delete="handleDeleteComment"
            />

            <!-- Botón cargar más comentarios -->
            <div v-if="hasMore" class="pt-2">
                <button
                    @click="loadMoreComments"
                    :disabled="loadingMore"
                    class="text-xs font-medium text-indigo-400 hover:text-indigo-300 disabled:opacity-50"
                >
                    <span v-if="!loadingMore">Cargar más comentarios</span>
                    <span v-else>Cargando...</span>
                </button>
            </div>
        </div>

        <!-- Estado vacío -->
        <div v-else class="text-center py-4">
            <p class="text-sm text-gray-400">No hay comentarios aún. ¡Sé el primero en comentar!</p>
        </div>

        <!-- Error state -->
        <div v-if="error" class="bg-red-900/20 border border-red-700 rounded-lg p-3 mt-3">
            <p class="text-xs text-red-400">{{ error }}</p>
        </div>
    </div>
</template>

<script>
import CommentCard from './CommentCard.vue';
import {
    createComment,
    getCommentsByPost,
    deleteComment,
    subscribeToCommentsChanges
} from '../services/comments.js';
import { useAuth } from '../composables/useAuth.js';
import { useToast } from '../composables/useToast.js';

export default {
    name: 'CommentsList',
    components: {
        CommentCard
    },
    props: {
        postId: {
            type: String,
            required: true
        }
    },
    emits: ['comment-added', 'comment-deleted'],
    setup() {
        const { userId } = useAuth();
        const { success, error: showError } = useToast();
        return { currentUserId: userId, toastSuccess: success, toastError: showError };
    },
    data() {
        return {
            comments: [],
            newCommentContent: '',
            loading: true,
            loadingMore: false,
            isSubmitting: false,
            error: null,
            currentPage: 0,
            pageSize: 50,
            hasMore: false,
            realtimeChannel: null
        };
    },
    computed: {
        currentUserInitials() {
            // TODO: Obtener del perfil del usuario
            return 'TU';
        }
    },
    methods: {
        /**
         * Carga los comentarios de la publicación
         */
        async loadComments(reset = false) {
            if (reset) {
                this.currentPage = 0;
                this.comments = [];
                this.hasMore = false;
                this.loading = true;
            } else {
                this.loadingMore = true;
            }

            this.error = null;

            try {
                const { comments, error } = await getCommentsByPost(
                    this.postId,
                    this.currentPage,
                    this.pageSize
                );

                if (error) {
                    this.error = error.message || 'Error al cargar comentarios';
                    return;
                }

                if (reset) {
                    this.comments = comments;
                } else {
                    this.comments = [...this.comments, ...comments];
                }

                this.hasMore = comments.length === this.pageSize;
            } catch (error) {
                console.error('Error loading comments:', error);
                this.error = 'Error inesperado al cargar comentarios';
            } finally {
                this.loading = false;
                this.loadingMore = false;
            }
        },

        /**
         * Carga más comentarios (paginación)
         */
        async loadMoreComments() {
            this.currentPage++;
            await this.loadComments();
        },

        /**
         * Envía un nuevo comentario
         */
        async submitComment() {
            if (!this.newCommentContent.trim() || this.isSubmitting) return;

            this.isSubmitting = true;
            this.error = null;

            try {
                const { comment, error } = await createComment({
                    post_id: this.postId,
                    content: this.newCommentContent.trim()
                });

                if (error) {
                    this.error = error.message || 'Error al crear comentario';
                    this.toastError(error.message || 'Error al crear comentario');
                    return;
                }

                if (comment) {
                    this.newCommentContent = '';
                    this.$emit('comment-added', comment);
                    // Notificación de éxito
                    this.toastSuccess('¡Comentario publicado exitosamente!');
                    // El comentario se agregará automáticamente por Realtime
                }
            } catch (error) {
                console.error('Error creating comment:', error);
                this.error = 'Error inesperado al crear comentario';
                this.toastError('Error inesperado al crear comentario');
            } finally {
                this.isSubmitting = false;
            }
        },

        /**
         * Maneja la edición de un comentario
         */
        handleEditComment(comment) {
            // TODO: Implementar edición de comentarios
            console.log('Edit comment:', comment);
        },

        /**
         * Maneja la eliminación de un comentario
         */
        async handleDeleteComment(commentId) {
            try {
                const { success, error } = await deleteComment(commentId);

                if (error) {
                    this.error = 'Error al eliminar comentario';
                    this.toastError('Error al eliminar comentario');
                    return;
                }

                if (success) {
                    this.comments = this.comments.filter(c => c.id !== commentId);
                    this.$emit('comment-deleted', commentId);
                    this.toastSuccess('Comentario eliminado exitosamente');
                }
            } catch (error) {
                console.error('Error deleting comment:', error);
                this.error = 'Error inesperado al eliminar comentario';
                this.toastError('Error inesperado al eliminar comentario');
            }
        },

        /**
         * Configura la suscripción en tiempo real
         */
        setupRealtime() {
            this.realtimeChannel = subscribeToCommentsChanges(
                this.postId,
                // onInsert
                (newComment) => {
                    // Agregar al final del array
                    this.comments.push(newComment);
                },
                // onUpdate
                (updatedComment) => {
                    const index = this.comments.findIndex(c => c.id === updatedComment.id);
                    if (index !== -1) {
                        this.comments[index] = updatedComment;
                    }
                },
                // onDelete
                (deletedCommentId) => {
                    this.comments = this.comments.filter(c => c.id !== deletedCommentId);
                }
            );
        }
    },
    async mounted() {
        await this.loadComments(true);
        this.setupRealtime();
    },
    beforeUnmount() {
        // Limpiar suscripción de Realtime
        if (this.realtimeChannel) {
            this.realtimeChannel.unsubscribe();
        }
    }
};
</script>
