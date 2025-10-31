<template>
    <div class="max-w-4xl mx-auto">
        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-6">
            <div class="flex">
                <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-800">
                        Error al cargar perfil
                    </h3>
                    <div class="mt-2 text-sm text-red-700">
                        {{ error }}
                    </div>
                    <div class="mt-4">
                        <button
                            @click="loadProfile"
                            class="bg-red-100 hover:bg-red-200 text-red-800 px-4 py-2 rounded-md text-sm font-medium transition duration-200"
                        >
                            Reintentar
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Profile content -->
        <div v-else-if="profile" class="space-y-6">
            <!-- Header del perfil -->
                        <div class="bg-white rounded-lg shadow-md overflow-hidden">
                <!-- Cover area (placeholder) -->
                <div class="h-32 bg-gradient-to-r from-indigo-500 to-purple-600"></div>
                
                <!-- Profile info -->
                <div class="px-6 py-6">
                    <div class="flex flex-col sm:flex-row sm:items-start sm:space-x-6">
                        <!-- Avatar -->
                        <div class="flex-shrink-0 -mt-16 mb-4 sm:mb-0">
                            <div class="w-24 h-24 rounded-full bg-white p-1 shadow-lg">
                                <div 
                                    class="w-full h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl"
                                >
                                    <img 
                                        v-if="profile.avatar_url" 
                                        :src="profile.avatar_url" 
                                        :alt="`Avatar de ${profile.display_name}`"
                                        class="w-full h-full rounded-full object-cover"
                                        @error="handleImageError"
                                    />
                                    <span v-else>{{ avatarInitials }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Información principal -->
                        <div class="flex-1 min-w-0">
                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                                <div>
                                    <h1 class="text-2xl font-bold text-gray-900 mb-2">
                                        {{ profile.display_name || 'Usuario sin nombre' }}
                                    </h1>
                                    <div class="mb-3">
                                        <RankBadge 
                                            :rango="profile.rango" 
                                            :isPro="profile.pro"
                                            :showProgress="true"
                                        />
                                    </div>
                                </div>
                                
                                <!-- Botón de acción -->
                                <div class="flex space-x-2">
                                    <button
                                        v-if="isOwnProfile"
                                        @click="$router.push('/settings')"
                                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                    >
                                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                        </svg>
                                        Editar Perfil
                                    </button>
                                    <button
                                        v-else
                                        @click="handleFollowToggle"
                                        :disabled="followLoading"
                                        class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                                    >
                                        <!-- Placeholder para futura funcionalidad de seguir -->
                                        Seguir
                                    </button>
                                    
                                </div>
                            </div>
                            
                            <!-- Bio -->
                            <div v-if="profile.bio" class="mt-4">
                                <p class="text-gray-700 leading-relaxed">
                                    {{ profile.bio }}
                                </p>
                            </div>
                            
                            <!-- Estadísticas -->
                            <div class="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
                                <div class="bg-gray-50 rounded-lg p-4 text-center">
                                    <div class="text-2xl font-bold text-gray-900">{{ stats.postsCount || 0 }}</div>
                                    <div class="text-sm text-gray-600">Publicaciones</div>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4 text-center">
                                    <div class="text-2xl font-bold text-gray-900">{{ stats.followersCount || 0 }}</div>
                                    <div class="text-sm text-gray-600">Seguidores</div>
                                </div>
                                <div class="bg-gray-50 rounded-lg p-4 text-center">
                                    <div class="text-2xl font-bold text-gray-900">{{ memberSinceFormatted }}</div>
                                    <div class="text-sm text-gray-600">Miembro desde</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pestañas de contenido -->
            <div class="bg-white rounded-lg shadow-md overflow-hidden">
                <div class="border-b border-gray-200">
                    <nav class="-mb-px flex">
                        <button
                            v-for="tab in tabs"
                            :key="tab.id"
                            @click="activeTab = tab.id"
                            :class="[
                                'py-4 px-6 font-medium text-sm border-b-2 transition duration-200',
                                activeTab === tab.id
                                    ? 'border-indigo-500 text-indigo-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            ]"
                        >
                            {{ tab.name }}
                        </button>
                    </nav>
                </div>

                <!-- Contenido de las pestañas -->
                <div class="p-6">
                    <!-- Pestaña de Publicaciones -->
                    <div v-if="activeTab === 'posts'">
                        <!-- Loading de posts -->
                        <div v-if="postsLoading" class="flex justify-center py-12">
                            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
                        </div>
                        
                        <!-- Error cargando posts -->
                        <div v-else-if="postsError" class="text-center py-12">
                            <svg class="w-16 h-16 mx-auto mb-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <h3 class="text-lg font-medium text-gray-900 mb-2">Error al cargar publicaciones</h3>
                            <p class="text-gray-500 mb-4">{{ postsError }}</p>
                            <button
                                @click="loadUserPosts"
                                class="text-indigo-600 hover:text-indigo-700 font-medium"
                            >
                                Reintentar
                            </button>
                        </div>
                        
                        <!-- Lista de posts -->
                        <div v-else-if="posts.length > 0" class="space-y-4">
                            <PostCard
                                v-for="post in posts"
                                :key="post.id"
                                :post="post"
                                @edit="handleEditPost"
                                @delete="handleDeletePost"
                                @like="handleLikePost"
                                @comment="handleCommentPost"
                                @share="handleSharePost"
                            />
                        </div>
                        
                        <!-- Sin publicaciones -->
                        <div v-else class="text-center py-12 text-gray-500">
                            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <h3 class="text-lg font-medium text-gray-900 mb-2">Sin publicaciones</h3>
                            <p class="text-gray-500">
                                {{ isOwnProfile ? 'Aún no has creado ninguna publicación.' : 'Este usuario no ha creado publicaciones.' }}
                            </p>
                            <RouterLink
                                v-if="isOwnProfile"
                                to="/feed"
                                class="inline-block mt-4 text-indigo-600 hover:text-indigo-700 font-medium"
                            >
                                Crear mi primera publicación →
                            </RouterLink>
                        </div>
                    </div>

                    <!-- Pestaña de Información -->
                    <div v-else-if="activeTab === 'info'" class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium text-gray-900 mb-4">Información del Usuario</h3>
                            <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <dt class="text-sm font-medium text-gray-500">Rango Actual</dt>
                                    <dd class="mt-1">
                                        <RankBadge :rango="profile.rango" :isPro="profile.pro" />
                                    </dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-500">Miembro desde</dt>
                                    <dd class="mt-1 text-sm text-gray-900">{{ memberSinceDetailed }}</dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-500">Última actividad</dt>
                                    <dd class="mt-1 text-sm text-gray-900">{{ lastActivityFormatted }}</dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-500">Estado</dt>
                                    <dd class="mt-1">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                            Activo
                                        </span>
                                    </dd>
                                </div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useRoute } from 'vue-router';
import { useAuth } from '../composables/useAuth.js';
import { useExternalProfile } from '../composables/useProfile.js';
import { getProfileByIdentifier, createSlugFromDisplayName } from '../services/profiles.js';
import { getPostsByUser } from '../services/posts.js';
import RankBadge from '../components/RankBadge.vue';
import PostCard from '../components/PostCard.vue';
import ProfileHeader from '../components/ProfileHeader.vue';

export default {
    name: 'Profile',
    components: {
        RankBadge,
        PostCard,
        ProfileHeader
    },
    setup() {
        const route = useRoute();
        const { userId, initialize: initializeAuth } = useAuth();
        const { getCachedProfile } = useExternalProfile();
        
        return {
            route,
            currentUserId: userId,
            getCachedProfile,
            initializeAuth
        };
    },
    data() {
        return {
            profile: null,
            loading: true,
            error: null,
            activeTab: 'posts',
            followLoading: false,
            posts: [],
            postsLoading: false,
            postsError: null,
            stats: {
                postsCount: 0,
                followersCount: 0,
                followingCount: 0
            },
            tabs: [
                { id: 'posts', name: 'Publicaciones' },
                { id: 'info', name: 'Información' }
            ]
        };
    },
    computed: {
        /**
         * ID del usuario del perfil a mostrar
         */
        profileIdentifier() {
            // Si hay ID en la ruta, usarlo; si no, usar el del usuario actual
            return this.route.params.id || this.currentUserId;
        },
        
        /**
         * Si es el perfil del usuario actual
         */
        isOwnProfile() {
            // Comparar tanto por ID como por slug del display_name actual
            if (this.profile && this.currentUserId) {
                const currentUserSlug = createSlugFromDisplayName(this.currentUserDisplayName);
                return this.profile.id === this.currentUserId || 
                       this.profileIdentifier === currentUserSlug;
            }
            return this.profileIdentifier === this.currentUserId;
        },
        
        /**
         * Display name del usuario actual
         */
        currentUserDisplayName() {
            const { userDisplayName } = useAuth();
            return userDisplayName.value;
        },
        
        /**
         * Iniciales para el avatar
         */
        avatarInitials() {
            if (this.profile?.display_name) {
                return this.profile.display_name
                    .split(' ')
                    .map(name => name.charAt(0))
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
            }
            return 'U';
        },
        
        /**
         * Fecha formateada de cuando se unió (formato corto)
         */
        memberSinceFormatted() {
            if (!this.profile?.created_at) return 'N/A';
            
            const date = new Date(this.profile.created_at);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short' 
            });
        },
        
        /**
         * Fecha detallada de cuando se unió
         */
        memberSinceDetailed() {
            if (!this.profile?.created_at) return 'Fecha desconocida';
            
            const date = new Date(this.profile.created_at);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'long',
                day: 'numeric'
            });
        },
        
        /**
         * Última actividad formateada
         */
        lastActivityFormatted() {
            if (!this.profile?.updated_at) return 'Nunca';
            
            const date = new Date(this.profile.updated_at);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays === 1) return 'Hace 1 día';
            if (diffDays < 7) return `Hace ${diffDays} días`;
            if (diffDays < 30) return `Hace ${Math.ceil(diffDays / 7)} semanas`;
            return `Hace ${Math.ceil(diffDays / 30)} meses`;
        }
    },
    methods: {
        /**
         * Carga el perfil del usuario
         */
        async loadProfile() {
            console.log('=== ENTERING loadProfile ===');
            console.log('Loading profile for identifier:', this.profileIdentifier);
            
            // Verificar que tengamos un identificador
            if (!this.profileIdentifier) {
                console.log('=== NO IDENTIFIER ===');
                this.error = 'Usuario no identificado';
                this.loading = false;
                return;
            }

            console.log('=== SETTING LOADING TRUE ===');
            this.loading = true;
            this.error = null;
            
            try {
                console.log('=== CALLING getProfileByIdentifier ===');
                console.log('Fetching profile from Supabase...');
                
                // Usar la nueva función que maneja tanto ID como slug
                const { profile, error } = await getProfileByIdentifier(this.profileIdentifier);
                
                console.log('=== PROFILE RESULT ===', { profile, error });
                
                if (error) {
                    console.log('=== PROFILE ERROR ===', error);
                    this.error = error.message || 'Error al cargar el perfil';
                    return;
                }
                
                if (!profile) {
                    console.log('=== PROFILE NOT FOUND ===');
                    this.error = 'Perfil no encontrado';
                    return;
                }
                
                console.log('=== SETTING PROFILE ===', profile);
                this.profile = profile;
                
                // Actualizar URL si se accedió por slug pero queremos mostrar el slug correcto
                if (this.route.params.id !== profile.id) {
                    const correctSlug = createSlugFromDisplayName(profile.display_name);
                    if (this.route.params.id !== correctSlug) {
                        // Actualizar la URL sin recargar la página
                        const newPath = `/profile/${correctSlug}`;
                        this.$router.replace(newPath);
                    }
                }
                
                console.log('=== PROFILE SET, LOADING STATS ===');
                await this.loadStats();
                console.log('=== STATS LOADED ===');
            } catch (error) {
                console.error('=== CATCH ERROR ===', error);
                this.error = 'Error inesperado al cargar el perfil';
            } finally {
                console.log('=== SETTING LOADING FALSE ===');
                this.loading = false;
                console.log('=== EXITING loadProfile ===');
            }
        },
        
        /**
         * Carga las estadísticas del perfil
         */
        async loadStats() {
            // Cargar posts del usuario para contar
            await this.loadUserPosts();
            
            this.stats = {
                postsCount: this.posts.length,
                followersCount: 0,
                followingCount: 0
            };
        },
        
        /**
         * Carga los posts del usuario
         */
        async loadUserPosts() {
            if (!this.profile?.id) return;
            
            this.postsLoading = true;
            this.postsError = null;
            
            try {
                const { posts, error } = await getPostsByUser(this.profile.id);
                
                if (error) {
                    this.postsError = error.message || 'Error al cargar publicaciones';
                    return;
                }
                
                this.posts = posts || [];
            } catch (error) {
                console.error('Error loading user posts:', error);
                this.postsError = 'Error inesperado al cargar publicaciones';
            } finally {
                this.postsLoading = false;
            }
        },
        
        /**
         * Maneja la eliminación de un post
         */
        async handleDeletePost(postId) {
            // Importar dinámicamente para no cargar siempre
            const { deletePost } = await import('../services/posts.js');
            
            try {
                const { success, error } = await deletePost(postId);
                
                if (error) {
                    alert('Error al eliminar la publicación');
                    return;
                }
                
                if (success) {
                    // Remover del array local
                    this.posts = this.posts.filter(p => p.id !== postId);
                    // Actualizar stats
                    this.stats.postsCount = this.posts.length;
                }
            } catch (error) {
                console.error('Error deleting post:', error);
                alert('Error inesperado al eliminar la publicación');
            }
        },
        
        /**
         * Placeholders para acciones de posts
         */
        handleEditPost(post) {
            console.log('Edit post:', post);
        },
        
        handleLikePost(postId) {
            console.log('Like post:', postId);
        },
        
        handleCommentPost(postId) {
            console.log('Comment post:', postId);
        },
        
        handleSharePost(post) {
            console.log('Share post:', post);
        },
        
        /**
         * Maneja el toggle de seguir/no seguir
         */
        async handleFollowToggle() {
            // Placeholder para futura funcionalidad
            this.followLoading = true;
            
            setTimeout(() => {
                this.followLoading = false;
                // aca va la lógica de seguir/no seguir
            }, 1000);
        },
        
        /**
         * Maneja errores de carga de imagen
         */
        handleImageError(event) {
            event.target.style.display = 'none';
        }
    },
    
    async mounted() {
        try {
            console.log('Profile mounted');
            
            // Asegurar que la auth esté inicializada
            await this.initializeAuth();
            
            console.log('Route params:', this.route.params);
            console.log('Current user ID:', this.currentUserId);
            console.log('Profile identifier:', this.profileIdentifier);
            console.log('Initial loading state:', this.loading);
            console.log('Initial profile state:', this.profile);
            
            console.log('About to call loadProfile...');
            await this.loadProfile();
            console.log('LoadProfile completed');
            console.log('Final loading state:', this.loading);
            console.log('Final profile state:', this.profile);
            console.log('Final error state:', this.error);
        } catch (error) {
            console.error('Error in mounted:', error);
            this.error = 'Error al cargar la página';
            this.loading = false;
        }
    },
    
    /**
     * Recargar cuando cambie el ID en la ruta
     */
    async beforeRouteUpdate(to, from, next) {
        if (to.params.id !== from.params.id) {
            await this.loadProfile();
        }
        next();
    }
};
</script>