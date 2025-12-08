<template>
    <div class="max-w-4xl mx-auto space-y-4 sm:space-y-6 px-4 sm:px-0">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <h1 class="text-2xl sm:text-3xl font-bold text-white">Feed de Publicaciones</h1>

            <!-- Filtro de categorías -->
            <div class="relative w-full sm:w-auto">
                <select
                    v-model="selectedCategory"
                    @change="handleCategoryChange"
                    class="w-full sm:w-auto pl-3 sm:pl-4 pr-8 sm:pr-10 py-2 text-sm sm:text-base border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-gray-700 text-white cursor-pointer"
                >
                    <option value="all">📂 Todas</option>
                    <option
                        v-for="category in categories"
                        :key="category.id"
                        :value="category.id"
                    >
                        {{ category.icon }} {{ category.name }}
                    </option>
                </select>
            </div>
        </div>

        <!-- Formulario para crear post -->
        <CreatePost v-if="!editingPost" @created="handlePostCreated" />

        <!-- Formulario para editar post -->
        <EditPost
            v-if="editingPost"
            :post="editingPost"
            @updated="handlePostUpdated"
            @cancel="handleCancelEdit"
        />

        <!-- Loading state inicial -->
        <div v-if="initialLoading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Lista de posts -->
        <div v-else-if="posts.length > 0" class="space-y-4 sm:space-y-6">
            <PostCard
                v-for="post in posts"
                :key="post.id"
                :post="post"
                @edit="handleEditPost"
                @delete="handleDeletePost"
                @like="handleLikePost"
                @comment="handleCommentPost"
                @share="handleSharePost"
                @comment-added="handleCommentAdded"
                @comment-deleted="handleCommentDeleted"
            />

            <!-- Botón cargar más -->
            <div v-if="hasMore" class="flex justify-center">
                <button
                    @click="loadMore"
                    :disabled="loadingMore"
                    class="w-full sm:w-auto px-6 py-3 bg-gray-800 border border-gray-600 text-white rounded-lg hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 text-sm sm:text-base"
                >
                    <span v-if="!loadingMore">Cargar más publicaciones</span>
                    <span v-else class="flex items-center justify-center">
                        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Cargando...
                    </span>
                </button>
            </div>
        </div>

        <!-- Estado vacío -->
        <div v-else class="bg-gray-800 rounded-lg shadow-md p-8 sm:p-12 text-center">
            <div class="w-20 h-20 sm:w-24 sm:h-24 mx-auto mb-4 sm:mb-6 bg-gray-700 rounded-full flex items-center justify-center">
                <svg class="w-10 h-10 sm:w-12 sm:h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
            </div>
            <h3 class="text-lg sm:text-xl font-semibold text-white mb-2">
                No hay publicaciones aún
            </h3>
            <p class="text-sm sm:text-base text-gray-300 mb-6">
                {{ selectedCategory === 'all'
                    ? 'Sé el primero en compartir algo con la comunidad'
                    : 'No hay publicaciones en esta categoría' }}
            </p>
        </div>

        <!-- Error state -->
        <div v-if="error" class="bg-red-900/20 border border-red-700 rounded-lg p-4">
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-300">Error al cargar publicaciones</h3>
                    <div class="mt-2 text-sm text-red-400">{{ error }}</div>
                    <button
                        @click="loadPosts"
                        class="mt-3 text-sm font-medium text-red-300 hover:text-red-200"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CreatePost from '../components/CreatePost.vue';
import EditPost from '../components/EditPost.vue';
import PostCard from '../components/PostCard.vue';
import { getPosts, getPost, deletePost, subscribeToPostsChanges, POST_CATEGORIES } from '../services/posts.js';
import { getSignedUrlForImage } from '../services/storage.js';

export default {
    name: 'Feed',
    components: {
        CreatePost,
        EditPost,
        PostCard
    },
    data() {
        return {
            posts: [],
            selectedCategory: 'all',
            currentPage: 0,
            pageSize: 20,
            hasMore: true,
            initialLoading: true,
            loadingMore: false,
            error: null,
            categories: POST_CATEGORIES,
            realtimeChannel: null,
            editingPost: null
        };
    },
    methods: {
        //Convierte URLs de imágenes a signed URLs
        async convertImageUrlsToSigned(posts) {
            const postsWithSignedUrls = await Promise.all(
                posts.map(async (post) => {
                    if (post.image_url && !post.image_url.includes('token=')) {
                        const { url, error } = await getSignedUrlForImage(post.image_url);
                        if (!error && url) {
                            return { ...post, image_url: url };
                        }
                    }
                    return post;
                })
            );
            return postsWithSignedUrls;
        },

        //Carga las publicaciones
        async loadPosts(reset = false) {
            if (reset) {
                this.currentPage = 0;
                this.posts = [];
                this.hasMore = true;
                this.initialLoading = true;
            } else {
                this.loadingMore = true;
            }

            this.error = null;

            try {
                const category = this.selectedCategory === 'all' ? null : this.selectedCategory;
                const { posts, error } = await getPosts(this.currentPage, this.pageSize, category);

                if (error) {
                    this.error = error.message || 'Error al cargar publicaciones';
                    return;
                }

                // Convertir URLs de imágenes a signed URLs
                const postsWithSignedUrls = await this.convertImageUrlsToSigned(posts);

                if (reset) {
                    this.posts = postsWithSignedUrls;
                } else {
                    this.posts = [...this.posts, ...postsWithSignedUrls];
                }

                // Si recibimos menos posts que el pageSize, no hay más
                this.hasMore = posts.length === this.pageSize;
            } catch (error) {
                console.error('Error loading posts:', error);
                this.error = 'Error inesperado al cargar publicaciones';
            } finally {
                this.initialLoading = false;
                this.loadingMore = false;
            }
        },

        //Carga más publicaciones (paginación)
        async loadMore() {
            this.currentPage++;
            await this.loadPosts();
        },

        //Maneja el cambio de categoría
        async handleCategoryChange() {
            await this.loadPosts(true);
        },

        //Maneja la creación de un nuevo post
        async handlePostCreated(createdPost) {
            console.log('Post created:', createdPost);

            // Obtener el post completo con datos del usuario desde la vista posts_with_users
            const { post, error } = await getPost(createdPost.id);

            if (error || !post) {
                console.error('Error al obtener post completo:', error);
                return;
            }

            // Convertir URL de imagen si existe
            let postWithSignedUrl = post;
            if (post.image_url && !post.image_url.includes('token=')) {
                const { url, error: urlError } = await getSignedUrlForImage(post.image_url);
                if (!urlError && url) {
                    postWithSignedUrl = { ...post, image_url: url };
                }
            }

            // Solo agregar si estamos en "todas las categorías" o coincide la categoría
            if (this.selectedCategory === 'all' || postWithSignedUrl.category === this.selectedCategory) {
                // Verificar si el post ya existe en el array (por la suscripción en tiempo real)
                const existingIndex = this.posts.findIndex(p => p.id === postWithSignedUrl.id);
                if (existingIndex === -1) {
                    // Agregar al principio del array
                    this.posts.unshift(postWithSignedUrl);
                }
            }
        },

        //Maneja la edición de un post
        handleEditPost(post) {
            this.editingPost = post;
            // Scroll to top para mostrar el formulario de edición
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        //Maneja la actualización de un post
        handlePostUpdated(updatedPost) {
            const index = this.posts.findIndex(p => p.id === this.editingPost.id);
            if (index !== -1) {
                this.posts[index] = { ...this.posts[index], ...updatedPost };
            }
            this.editingPost = null;
        },

        //Maneja la cancelación de la edición
        handleCancelEdit() {
            this.editingPost = null;
        },

        //Maneja la eliminación de un post
        async handleDeletePost(postId) {
            try {
                const { success, error } = await deletePost(postId);

                if (error) {
                    alert('Error al eliminar la publicación');
                    return;
                }

                if (success) {
                    // Remover del array local
                    this.posts = this.posts.filter(p => p.id !== postId);
                }
            } catch (error) {
                console.error('Error deleting post:', error);
                alert('Error inesperado al eliminar la publicación');
            }
        },

        //Maneja el like de un post (placeholder)
        handleLikePost(postId) {
            console.log('Like post:', postId);
            // FALTA IMPLEMENTAR SISTEMA DE LIKES 
        },

        //Maneja comentar un post (placeholder)
        handleCommentPost(postId) {
            console.log('Comment post:', postId);
            // Los comentarios se manejan en PostCard
        },

        //Maneja cuando se agrega un comentario
        handleCommentAdded(data) {
            console.log('Comment added to post:', data);
        },

        //Maneja cuando se elimina un comentario
        handleCommentDeleted(data) {
            console.log('Comment deleted from post:', data);
        },

        //Maneja compartir un post (placeholder)
        handleSharePost(post) {
            console.log('Share post:', post);
            // agregar compartir?
        },

        //Configura la suscripción en tiempo real
        setupRealtime() {
            this.realtimeChannel = subscribeToPostsChanges(
                // onInsert
                async (newPost) => {
                    // Convertir URL de imagen si existe
                    let postWithSignedUrl = newPost;
                    if (newPost.image_url && !newPost.image_url.includes('token=')) {
                        const { url, error: urlError } = await getSignedUrlForImage(newPost.image_url);
                        if (!urlError && url) {
                            postWithSignedUrl = { ...newPost, image_url: url };
                        }
                    }

                    // Solo agregar si estamos en "todas las categorías" o coincide la categoría
                    if (this.selectedCategory === 'all' || postWithSignedUrl.category === this.selectedCategory) {
                        // Agregar al principio del array
                        this.posts.unshift(postWithSignedUrl);
                    }
                },
                // onUpdate
                async (updatedPost) => {
                    // Convertir URL de imagen si existe
                    let postWithSignedUrl = updatedPost;
                    if (updatedPost.image_url && !updatedPost.image_url.includes('token=')) {
                        const { url, error: urlError } = await getSignedUrlForImage(updatedPost.image_url);
                        if (!urlError && url) {
                            postWithSignedUrl = { ...updatedPost, image_url: url };
                        }
                    }

                    const index = this.posts.findIndex(p => p.id === postWithSignedUrl.id);
                    if (index !== -1) {
                        this.posts[index] = postWithSignedUrl;
                    }
                },
                // onDelete
                (deletedPostId) => {
                    this.posts = this.posts.filter(p => p.id !== deletedPostId);
                }
            );
        }
    },
    async mounted() {
        await this.loadPosts(true);
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