<template>
    <div class="max-w-4xl mx-auto">
        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="bg-red-900/20 border border-red-700 rounded-md p-6">
            <div class="flex">
                <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-300">
                        Error al cargar perfil
                    </h3>
                    <div class="mt-2 text-sm text-red-400">
                        {{ error }}
                    </div>
                    <div class="mt-4">
                        <button
                            @click="loadProfile"
                            class="bg-red-800 hover:bg-red-700 text-red-200 px-4 py-2 rounded-md text-sm font-medium transition duration-200"
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
        <ProfileHeader
        :profile="profile"
        :isOwnProfile="isOwnProfile"
        :stats="stats"
        :memberSinceFormatted="memberSinceFormatted"
        :followLoading="followLoading"
        @edit-profile="$router.push('/settings')"
        @follow-toggle="handleFollowToggle"
        />

            <!-- Pestañas de contenido -->
            <div class="bg-gray-800 rounded-lg shadow-md overflow-hidden">
                <div class="border-b border-gray-700">
                    <nav class="-mb-px flex">
                        <button
                            v-for="tab in tabs"
                            :key="tab.id"
                            @click="activeTab = tab.id"
                            :class="[
                                'py-4 px-6 font-medium text-sm border-b-2 transition duration-200',
                                activeTab === tab.id
                                    ? 'border-indigo-500 text-indigo-400'
                                    : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-600'
                            ]"
                        >
                            {{ tab.name }}
                        </button>
                    </nav>
                </div>

                <!-- Contenido de las pestañas -->
                <div class="p-6">
                    <!-- Pestaña de Publicaciones -->
                    <div v-if="activeTab === 'publications'">
                        <!-- Loading de publicaciones -->
                        <div v-if="publicationsLoading" class="flex justify-center py-12">
                            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
                        </div>

                        <!-- Error cargando publicaciones -->
                        <div v-else-if="publicationsError" class="text-center py-12">
                            <svg class="w-16 h-16 mx-auto mb-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <h3 class="text-lg font-medium text-white mb-2">Error al cargar publicaciones</h3>
                            <p class="text-gray-400 mb-4">{{ publicationsError }}</p>
                            <button
                                @click="loadUserPublications"
                                class="text-indigo-400 hover:text-indigo-300 font-medium"
                            >
                                Reintentar
                            </button>
                        </div>

                        <!-- Lista de publicaciones -->
                        <div v-else-if="publications.length > 0" class="space-y-4">
                            <PublicationCard
                                v-for="publication in publications"
                                :key="publication.id"
                                :publication="publication"
                                @edit="handleEditPublication"
                                @delete="handleDeletePublication"
                                @like="handleLikePublication"
                                @bookmark="handleBookmarkPublication"
                                @share="handleSharePublication"
                            />
                        </div>

                        <!-- Sin publicaciones -->
                        <div v-else class="text-center py-12 text-gray-400">
                            <svg class="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                            <h3 class="text-lg font-medium text-white mb-2">Sin publicaciones</h3>
                            <p class="text-gray-400">
                                {{ isOwnProfile ? 'Aún no has creado ninguna publicación.' : 'Este usuario no ha creado publicaciones.' }}
                            </p>
                            <RouterLink
                                v-if="isOwnProfile"
                                to="/publicaciones"
                                class="inline-block mt-4 text-indigo-400 hover:text-indigo-300 font-medium"
                            >
                                Crear mi primera publicación →
                            </RouterLink>
                        </div>
                    </div>

                    <!-- Pestaña de Información -->
                    <div v-else-if="activeTab === 'info'" class="space-y-6">
                        <div>
                            <h3 class="text-lg font-medium text-white mb-4">Información del Usuario</h3>
                            <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <dt class="text-sm font-medium text-gray-400">Rango Actual</dt>
                                    <dd class="mt-1">
                                        <RankBadge :rango="profile.rango" :isPro="profile.pro" />
                                    </dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-400">Miembro desde</dt>
                                    <dd class="mt-1 text-sm text-white">{{ memberSinceDetailed }}</dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-400">Última actividad</dt>
                                    <dd class="mt-1 text-sm text-white">{{ lastActivityFormatted }}</dd>
                                </div>
                                <div>
                                    <dt class="text-sm font-medium text-gray-400">Estado</dt>
                                    <dd class="mt-1">
                                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-300">
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
import { getPublicationsByUser, deletePublication } from '../services/publications.js';
import { getSignedUrlForImage } from '../services/storage.js';
import RankBadge from '../components/RankBadge.vue';
import PublicationCard from '../components/PublicationCard.vue';
import ProfileHeader from '../components/ProfileHeader.vue';
import { ref, computed, onMounted, watch } from 'vue';

export default {
    name: 'Profile',
    components: {
        RankBadge,
        PublicationCard,
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
            activeTab: 'publications',
            followLoading: false,
            publications: [],
            publicationsLoading: false,
            publicationsError: null,
            stats: {
                publicationsCount: 0,
                followersCount: 0,
                followingCount: 0
            },
            tabs: [
                { id: 'publications', name: 'Publicaciones' },
                { id: 'info', name: 'Información' }
            ]
        };
    },
    computed: {
        //ID del usuario del perfil a mostrar
        profileIdentifier() {
            // Si hay ID en la ruta, usarlo; si no, usar el del usuario actual
            return this.route.params.id || this.currentUserId;
        },
        
        //Si es el perfil del usuario actual
        isOwnProfile() {
            // Comparar tanto por ID como por slug del display_name actual
            if (this.profile && this.currentUserId) {
                const currentUserSlug = createSlugFromDisplayName(this.currentUserDisplayName);
                return this.profile.id === this.currentUserId || 
                       this.profileIdentifier === currentUserSlug;
            }
            return this.profileIdentifier === this.currentUserId;
        },
        
        //Display name del usuario actual
        currentUserDisplayName() {
            const { userDisplayName } = useAuth();
            return userDisplayName.value;
        },
        
        //Iniciales para el avatar
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
        
        //Fecha formateada de cuando se unió (formato corto)
        memberSinceFormatted() {
            if (!this.profile?.created_at) return 'N/A';
            
            const date = new Date(this.profile.created_at);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short' 
            });
        },
        
        //Fecha detallada de cuando se unió
        memberSinceDetailed() {
            if (!this.profile?.created_at) return 'Fecha desconocida';
            
            const date = new Date(this.profile.created_at);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'long',
                day: 'numeric'
            });
        },
        
        //Última actividad formateada
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
    watch: {
        //Watch para detectar cambios en el parámetro de la ruta
        'route.params.id'(newId, oldId) {
            if (newId && newId !== oldId) {
                console.log('Route param changed:', { oldId, newId });
                // Resetear estados
                this.publications = [];
                this.publicationsError = null;
                this.error = null;

                // Recargar perfil
                this.loadProfile();
            }
        }
    },
    methods: {
        //Carga el perfil del usuario
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

                // Convertir URL de avatar si existe
                if (profile.avatar_url && !profile.avatar_url.includes('token=')) {
                    const { url, error: urlError } = await getSignedUrlForImage(profile.avatar_url);
                    if (!urlError && url) {
                        profile.avatar_url = url;
                    }
                }

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
        
        //Carga las estadísticas del perfil
        async loadStats() {
            // Cargar publicaciones del usuario para contar
            await this.loadUserPublications();

            this.stats = {
                publicationsCount: this.publications.length,
                followersCount: 0,
                followingCount: 0
            };
        },

        //Carga las publicaciones del usuario
        async loadUserPublications() {
            if (!this.profile?.id) return;

            this.publicationsLoading = true;
            this.publicationsError = null;

            try {
                const { publications, error } = await getPublicationsByUser(this.profile.id);

                if (error) {
                    this.publicationsError = error.message || 'Error al cargar publicaciones';
                    return;
                }

                // Convertir URLs de imágenes a signed URLs
                const publicationsWithSignedUrls = await Promise.all(
                    (publications || []).map(async (publication) => {
                        if (publication.image_url && !publication.image_url.includes('token=')) {
                            const { url, error: urlError } = await getSignedUrlForImage(publication.image_url);
                            if (!urlError && url) {
                                return { ...publication, image_url: url };
                            }
                        }
                        return publication;
                    })
                );

                this.publications = publicationsWithSignedUrls;
            } catch (error) {
                console.error('Error loading user publications:', error);
                this.publicationsError = 'Error inesperado al cargar publicaciones';
            } finally {
                this.publicationsLoading = false;
            }
        },

        //Maneja la eliminación de una publicación
        async handleDeletePublication(publicationId) {
            try {
                const { success, error } = await deletePublication(publicationId);

                if (error) {
                    alert('Error al eliminar la publicación');
                    return;
                }

                if (success) {
                    // Remover del array local
                    this.publications = this.publications.filter(p => p.id !== publicationId);
                    // Actualizar stats
                    this.stats.publicationsCount = this.publications.length;
                }
            } catch (error) {
                console.error('Error deleting publication:', error);
                alert('Error inesperado al eliminar la publicación');
            }
        },

        //Placeholders para acciones de publicaciones
        handleEditPublication(publication) {
            console.log('Edit publication:', publication);
        },

        handleLikePublication(publicationId) {
            console.log('Like publication:', publicationId);
        },

        handleBookmarkPublication(publicationId) {
            console.log('Bookmark publication:', publicationId);
        },

        handleSharePublication(publication) {
            console.log('Share publication:', publication);
        },
        
        //Maneja el toggle de seguir/no seguir
        async handleFollowToggle() {
            
            this.followLoading = true;
            
            setTimeout(() => {
                this.followLoading = false;
                // AGREGAR lógica de seguir/no seguir?
            }, 1000);
        },
        
        // Maneja errores de carga de imagen
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
    }
};
</script>