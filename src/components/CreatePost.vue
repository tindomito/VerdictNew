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

export default {
    name: 'CreatePost',
    props: {
        showCancel: {
            type: Boolean,
            default: false
        }
    },
    emits: ['created', 'cancel'],
    data() {
        return {
            form: {
                title: '',
                content: '',
                category: 'general'
            },
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
         * Maneja el envío del formulario
         */
        async handleSubmit() {
            if (!this.isFormValid) return;

            this.loading = true;
            this.error = null;

            try {
                const { post, error } = await createPost({
                    title: this.form.title.trim(),
                    content: this.form.content.trim(),
                    category: this.form.category
                });

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