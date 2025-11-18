<template>
    <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Crear Publicación</h2>
        
        <form @submit.prevent="handleSubmit">
            <!-- Selector de categoría -->
            <div class="mb-4">
                <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
                    Categoría
                </label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <button
                        v-for="category in categories"
                        :key="category.id"
                        type="button"
                        @click="form.category = category.id"
                        :class="[
                            'flex items-center justify-center space-x-2 px-3 py-2 rounded-lg border-2 transition-all duration-200',
                            form.category === category.id
                                ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                                : 'border-gray-200 hover:border-indigo-300 text-gray-700'
                        ]"
                    >
                        <span>{{ category.icon }}</span>
                        <span class="text-sm font-medium">{{ category.name }}</span>
                    </button>
                </div>
            </div>

            <!-- Título -->
            <div class="mb-4">
                <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
                    Título
                </label>
                <input
                    id="title"
                    v-model="form.title"
                    type="text"
                    required
                    maxlength="200"
                    :disabled="loading"
                    placeholder="¿De qué quieres hablar?"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <p class="mt-1 text-xs text-gray-500">
                    {{ form.title.length }}/200 caracteres
                </p>
            </div>

            <!-- Contenido -->
            <div class="mb-4">
                <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                    Contenido
                </label>
                <textarea
                    id="content"
                    v-model="form.content"
                    required
                    rows="6"
                    maxlength="5000"
                    :disabled="loading"
                    placeholder="Comparte tu análisis, opinión o predicción..."
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                ></textarea>
                <p class="mt-1 text-xs text-gray-500">
                    {{ form.content.length }}/5000 caracteres
                </p>
            </div>

            <!-- Imagen -->
            <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Imagen (opcional)
                </label>

                <!-- Vista previa de imagen -->
                <div v-if="imagePreview" class="mb-3 relative">
                    <img
                        :src="imagePreview"
                        alt="Vista previa"
                        class="max-h-64 rounded-lg object-cover"
                    />
                    <button
                        type="button"
                        @click="removeImage"
                        :disabled="loading"
                        class="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors disabled:opacity-50"
                    >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <!-- Selector de archivo -->
                <div v-else class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-400 transition-colors">
                    <input
                        ref="fileInput"
                        type="file"
                        accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                        @change="handleImageSelect"
                        :disabled="loading"
                        class="hidden"
                    />
                    <button
                        type="button"
                        @click="$refs.fileInput.click()"
                        :disabled="loading"
                        class="inline-flex items-center space-x-2 text-indigo-600 hover:text-indigo-700 disabled:opacity-50"
                    >
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        <span class="text-sm font-medium">Seleccionar imagen</span>
                    </button>
                    <p class="mt-2 text-xs text-gray-500">
                        JPG, PNG, GIF o WebP (máx. 5MB)
                    </p>
                </div>

                <!-- Error de imagen -->
                <p v-if="imageError" class="mt-2 text-sm text-red-600">
                    {{ imageError }}
                </p>
            </div>

            <!-- Mensaje de error -->
            <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p class="text-sm text-red-700">{{ error }}</p>
            </div>

            <!-- Botones -->
            <div class="flex justify-end space-x-3">
                <button
                    v-if="showCancel"
                    type="button"
                    @click="handleCancel"
                    :disabled="loading"
                    class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    Cancelar
                </button>
                <button
                    type="submit"
                    :disabled="loading || !isFormValid"
                    class="px-6 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                    <span v-if="!loading">Publicar</span>
                    <span v-else class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Publicando...
                    </span>
                </button>
            </div>
        </form>
    </div>
</template>

<script>
import { POST_CATEGORIES, createPost } from '../services/posts.js';
import { uploadPostImage, validateImageFile } from '../services/storage.js';
import { useAuth } from '../composables/useAuth.js';

export default {
    name: 'CreatePost',
    props: {
        showCancel: {
            type: Boolean,
            default: false
        }
    },
    emits: ['created', 'cancel'],
    setup() {
        const { userId } = useAuth();
        return { currentUserId: userId };
    },
    data() {
        return {
            form: {
                title: '',
                content: '',
                category: 'general'
            },
            selectedImage: null,
            imagePreview: null,
            imageError: null,
            loading: false,
            error: null,
            categories: POST_CATEGORIES
        };
    },
    computed: {
        /**
         * Valida que el formulario esté completo
         */
        isFormValid() {
            return (
                this.form.title.trim().length > 0 &&
                this.form.content.trim().length > 0 &&
                this.form.title.length <= 200 &&
                this.form.content.length <= 5000
            );
        }
    },
    methods: {
        /**
         * Maneja la selección de imagen
         */
        handleImageSelect(event) {
            const file = event.target.files[0];
            if (!file) return;

            // Validar archivo
            const { valid, error } = validateImageFile(file);
            if (!valid) {
                this.imageError = error;
                this.selectedImage = null;
                this.imagePreview = null;
                return;
            }

            // Guardar archivo y crear vista previa
            this.selectedImage = file;
            this.imageError = null;

            const reader = new FileReader();
            reader.onload = (e) => {
                this.imagePreview = e.target.result;
            };
            reader.readAsDataURL(file);
        },

        /**
         * Elimina la imagen seleccionada
         */
        removeImage() {
            this.selectedImage = null;
            this.imagePreview = null;
            this.imageError = null;
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }
        },

        /**
         * Maneja el envío del formulario
         */
        async handleSubmit() {
            if (!this.isFormValid) return;

            this.loading = true;
            this.error = null;

            try {
                let imageUrl = null;

                // Subir imagen si existe
                if (this.selectedImage) {
                    const { url, error } = await uploadPostImage(this.selectedImage, this.currentUserId);
                    if (error) {
                        this.error = error.message || 'Error al subir la imagen';
                        this.loading = false;
                        return;
                    }
                    imageUrl = url;
                }

                // Crear post
                const postData = {
                    title: this.form.title.trim(),
                    content: this.form.content.trim(),
                    category: this.form.category
                };

                if (imageUrl) {
                    postData.image_url = imageUrl;
                }

                const { post, error } = await createPost(postData);

                if (error) {
                    this.error = error.message || 'Error al crear la publicación';
                    return;
                }

                // Emitir evento de creación exitosa
                this.$emit('created', post);

                // Limpiar formulario
                this.form = {
                    title: '',
                    content: '',
                    category: 'general'
                };
                this.removeImage();

                // Mostrar mensaje de éxito
                this.showSuccessMessage();
            } catch (error) {
                console.error('Error creating post:', error);
                this.error = 'Error inesperado al crear la publicación';
            } finally {
                this.loading = false;
            }
        },

        /**
         * Maneja la cancelación
         */
        handleCancel() {
            if (this.form.title || this.form.content) {
                if (confirm('¿Descartar los cambios?')) {
                    this.form = {
                        title: '',
                        content: '',
                        category: 'general'
                    };
                    this.$emit('cancel');
                }
            } else {
                this.$emit('cancel');
            }
        },

        /**
         * Muestra mensaje de éxito temporal
         */
        showSuccessMessage() {
            // Podrías agregar un toast/notificación aquí
            console.log('Post creado exitosamente');
        }
    }
};
</script>