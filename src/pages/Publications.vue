<template>
    <div class="max-w-4xl mx-auto space-y-4 sm:space-y-6 px-4 sm:px-0">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 class="text-2xl sm:text-3xl font-bold text-white">Publicaciones</h1>
                <p class="text-gray-400 text-sm mt-1">Comparte artículos, tutoriales y más contenido</p>
            </div>

            <!-- Filtro de categorías -->
            <div class="relative w-full sm:w-auto">
                <select
                    v-model="selectedCategory"
                    @change="handleCategoryChange"
                    class="w-full sm:w-auto pl-3 sm:pl-4 pr-8 sm:pr-10 py-2 text-sm sm:text-base border border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-gray-700 text-white cursor-pointer"
                >
                    <option value="all">📂 Todas las categorías</option>
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

        <!-- Formulario para crear publicación -->
        <CreatePublication v-if="!editingPublication" @created="handlePublicationCreated" />

        <!-- Formulario para editar publicación -->
        <EditPublication
            v-if="editingPublication"
            :publication="editingPublication"
            @updated="handlePublicationUpdated"
            @cancel="handleCancelEdit"
        />

        <!-- Loading state inicial -->
        <div v-if="initialLoading" class="flex justify-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Lista de publicaciones -->
        <div v-else-if="publications.length > 0" class="space-y-4 sm:space-y-6">
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
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
            </div>
            <h3 class="text-lg sm:text-xl font-semibold text-white mb-2">
                No hay publicaciones aún
            </h3>
            <p class="text-sm sm:text-base text-gray-300 mb-6">
                {{ selectedCategory === 'all'
                    ? 'Sé el primero en compartir un artículo o tutorial'
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
                        @click="loadPublications"
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
import CreatePublication from '../components/CreatePublication.vue';
import EditPublication from '../components/EditPublication.vue';
import PublicationCard from '../components/PublicationCard.vue';
import {
    getPublications,
    deletePublication,
    subscribeToPublicationsChanges,
    PUBLICATION_CATEGORIES
} from '../services/publications.js';
import { getSignedUrlForImage } from '../services/storage.js';
import { useToast } from '../composables/useToast.js';

export default {
    name: 'Publications',
    components: {
        CreatePublication,
        EditPublication,
        PublicationCard
    },
    setup() {
        const { success, error: showError } = useToast();
        return { toastSuccess: success, toastError: showError };
    },
    data() {
        return {
            publications: [],
            selectedCategory: 'all',
            currentPage: 0,
            pageSize: 20,
            hasMore: true,
            initialLoading: true,
            loadingMore: false,
            error: null,
            categories: PUBLICATION_CATEGORIES,
            realtimeChannel: null,
            editingPublication: null
        };
    },
    methods: {
        async convertImageUrlsToSigned(publications) {
            const publicationsWithSignedUrls = await Promise.all(
                publications.map(async (publication) => {
                    if (publication.image_url && !publication.image_url.includes('token=')) {
                        const { url, error } = await getSignedUrlForImage(publication.image_url);
                        if (!error && url) {
                            return { ...publication, image_url: url };
                        }
                    }
                    return publication;
                })
            );
            return publicationsWithSignedUrls;
        },

        async loadPublications(reset = false) {
            if (reset) {
                this.currentPage = 0;
                this.publications = [];
                this.hasMore = true;
                this.initialLoading = true;
            } else {
                this.loadingMore = true;
            }

            this.error = null;

            try {
                const category = this.selectedCategory === 'all' ? null : this.selectedCategory;
                const { publications, error } = await getPublications(this.currentPage, this.pageSize, category);

                if (error) {
                    this.error = error.message || 'Error al cargar publicaciones';
                    return;
                }

                const publicationsWithSignedUrls = await this.convertImageUrlsToSigned(publications);

                if (reset) {
                    this.publications = publicationsWithSignedUrls;
                } else {
                    this.publications = [...this.publications, ...publicationsWithSignedUrls];
                }

                this.hasMore = publications.length === this.pageSize;
            } catch (error) {
                console.error('Error loading publications:', error);
                this.error = 'Error inesperado al cargar publicaciones';
            } finally {
                this.initialLoading = false;
                this.loadingMore = false;
            }
        },

        async loadMore() {
            this.currentPage++;
            await this.loadPublications();
        },

        async handleCategoryChange() {
            await this.loadPublications(true);
        },

        async handlePublicationCreated(createdPublication) {
            console.log('Publication created:', createdPublication);

            // Usar directamente los datos recibidos (ya incluyen display_name y avatar_url)
            let publicationWithSignedUrl = { ...createdPublication };

            // Convertir URL de imagen si es necesario
            if (createdPublication.image_url && !createdPublication.image_url.includes('token=')) {
                const { url, error: urlError } = await getSignedUrlForImage(createdPublication.image_url);
                if (!urlError && url) {
                    publicationWithSignedUrl.image_url = url;
                }
            }

            // Agregar al feed si coincide con el filtro de categoría
            if (this.selectedCategory === 'all' || publicationWithSignedUrl.category === this.selectedCategory) {
                const existingIndex = this.publications.findIndex(p => p.id === publicationWithSignedUrl.id);
                if (existingIndex === -1) {
                    this.publications.unshift(publicationWithSignedUrl);
                }
            }
        },

        handleEditPublication(publication) {
            this.editingPublication = publication;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        handlePublicationUpdated(updatedPublication) {
            const index = this.publications.findIndex(p => p.id === this.editingPublication.id);
            if (index !== -1) {
                this.publications[index] = { ...this.publications[index], ...updatedPublication };
            }
            this.editingPublication = null;
        },

        handleCancelEdit() {
            this.editingPublication = null;
        },

        async handleDeletePublication(publicationId) {
            try {
                const { success, error } = await deletePublication(publicationId);

                if (error) {
                    this.toastError('Error al eliminar la publicación');
                    return;
                }

                if (success) {
                    this.publications = this.publications.filter(p => p.id !== publicationId);
                    this.toastSuccess('Publicación eliminada');
                }
            } catch (error) {
                console.error('Error deleting publication:', error);
                this.toastError('Error inesperado al eliminar la publicación');
            }
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

        setupRealtime() {
            this.realtimeChannel = subscribeToPublicationsChanges(
                async (newPublication) => {
                    let publicationWithSignedUrl = newPublication;
                    if (newPublication.image_url && !newPublication.image_url.includes('token=')) {
                        const { url, error: urlError } = await getSignedUrlForImage(newPublication.image_url);
                        if (!urlError && url) {
                            publicationWithSignedUrl = { ...newPublication, image_url: url };
                        }
                    }

                    if (this.selectedCategory === 'all' || publicationWithSignedUrl.category === this.selectedCategory) {
                        const existingIndex = this.publications.findIndex(p => p.id === publicationWithSignedUrl.id);
                        if (existingIndex === -1) {
                            this.publications.unshift(publicationWithSignedUrl);
                        }
                    }
                },
                async (updatedPublication) => {
                    let publicationWithSignedUrl = updatedPublication;
                    if (updatedPublication.image_url && !updatedPublication.image_url.includes('token=')) {
                        const { url, error: urlError } = await getSignedUrlForImage(updatedPublication.image_url);
                        if (!urlError && url) {
                            publicationWithSignedUrl = { ...updatedPublication, image_url: url };
                        }
                    }

                    const index = this.publications.findIndex(p => p.id === publicationWithSignedUrl.id);
                    if (index !== -1) {
                        this.publications[index] = publicationWithSignedUrl;
                    }
                },
                (deletedPublicationId) => {
                    this.publications = this.publications.filter(p => p.id !== deletedPublicationId);
                }
            );
        }
    },
    async mounted() {
        await this.loadPublications(true);
        this.setupRealtime();
    },
    beforeUnmount() {
        if (this.realtimeChannel) {
            this.realtimeChannel.unsubscribe();
        }
    }
};
</script>
