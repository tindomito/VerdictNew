<template>
    <div class="max-w-4xl mx-auto">
        <AppH1>Configuración del Perfil</AppH1>
        
        <!-- Loading state -->
        <div v-if="loading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Main content -->
        <div v-else class="space-y-6">
            <!-- Mensajes de estado -->
            <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-md p-4">
                <div class="flex">
                    <div class="ml-3">
                        <div class="text-sm text-green-700">
                            {{ successMessage }}
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-md p-4">
                <div class="flex">
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-red-800">
                            Error al actualizar perfil
                        </h3>
                        <div class="mt-2 text-sm text-red-700">
                            {{ errorMessage }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Formulario de perfil -->
            <div class="bg-white shadow rounded-lg">
                <div class="px-6 py-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-6">Información Personal</h2>
                    
                    <form @submit.prevent="handleUpdateProfile" class="space-y-6">
                        <!-- Avatar section -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Foto de Perfil
                            </label>
                            <div class="flex items-center space-x-6">
                                <div class="w-20 h-20 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                                    <img 
                                        v-if="form.avatar_url" 
                                        :src="form.avatar_url" 
                                        :alt="'Avatar de ' + form.display_name"
                                        class="w-full h-full rounded-full object-cover"
                                        @error="handleImageError"
                                    />
                                    <span v-else>{{ avatarInitials }}</span>
                                </div>
                                <div>
                                    <input
                                        type="url"
                                        v-model="form.avatar_url"
                                        placeholder="https://ejemplo.com/tu-avatar.jpg"
                                        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                                    />
                                    <p class="mt-1 text-xs text-gray-500">
                                        URL de tu imagen de perfil (opcional)
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Nombre de usuario -->
                        <div>
                            <label for="display_name" class="block text-sm font-medium text-gray-700">
                                Nombre de Usuario
                            </label>
                            <input
                                id="display_name"
                                type="text"
                                v-model="form.display_name"
                                :disabled="saveLoading"
                                required
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
                                placeholder="Tu nombre de usuario"
                            />
                            <p class="mt-1 text-xs text-gray-500">
                                Este nombre será visible para otros usuarios
                            </p>
                        </div>

                        <!-- Bio -->
                        <div>
                            <label for="bio" class="block text-sm font-medium text-gray-700">
                                Biografía
                            </label>
                            <textarea
                                id="bio"
                                v-model="form.bio"
                                :disabled="saveLoading"
                                rows="4"
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
                                placeholder="Cuéntanos sobre ti, tu experiencia en MMA, tus luchadores favoritos..."
                            ></textarea>
                            <p class="mt-1 text-xs text-gray-500">
                                Máximo 500 caracteres. {{ bioCharCount }}/500
                            </p>
                        </div>

                        <!-- Rango (solo lectura para usuarios normales) -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Rango Actual
                            </label>
                            <div class="p-4 bg-gray-50 rounded-md">
                                <RankBadge 
                                    :rango="currentProfile?.rango || 'Novato'" 
                                    :isPro="currentProfile?.pro || false"
                                    :showProgress="true"
                                />
                                <p class="mt-2 text-xs text-gray-500">
                                    Los rangos se actualizan automáticamente según tu actividad en la comunidad
                                </p>
                            </div>
                        </div>

                        <!-- Estado PRO -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Estado PRO
                            </label>
                            <div class="p-4 bg-gray-50 rounded-md">
                                <div class="flex items-center justify-between">
                                    <div>
                                        <span class="text-sm font-medium text-gray-900">
                                            {{ currentProfile?.pro ? 'Miembro PRO' : 'Miembro Estándar' }}
                                        </span>
                                        <p class="text-xs text-gray-500 mt-1">
                                            {{ currentProfile?.pro ? 'Tienes acceso a funciones premium' : 'Actualiza para acceder a funciones premium' }}
                                        </p>
                                    </div>
                                    <div>
                                        <span 
                                            v-if="currentProfile?.pro"
                                            class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-yellow-400 to-yellow-600 text-yellow-900"
                                        >
                                            ⭐ PRO
                                        </span>
                                        <button
                                            v-else
                                            type="button"
                                            @click="handleUpgradeToPro"
                                            class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-full text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                                        >
                                            Actualizar a PRO
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Botones de acción -->
                        <div class="flex justify-between">
                            <button
                                type="button"
                                @click="resetForm"
                                :disabled="saveLoading"
                                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                            >
                                Cancelar
                            </button>
                            <button
                                type="submit"
                                :disabled="saveLoading || !isFormValid"
                                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                            >
                                <span v-if="!saveLoading">Guardar Cambios</span>
                                <span v-else class="flex items-center">
                                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Guardando...
                                </span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Sección de cuenta -->
            <div class="bg-white shadow rounded-lg">
                <div class="px-6 py-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-6">Configuración de Cuenta</h2>
                    
                    <div class="space-y-4">
                        <!-- Email (solo lectura) -->
                        <div>
                            <label class="block text-sm font-medium text-gray-700">
                                Email
                            </label>
                            <input
                                type="email"
                                :value="userEmail"
                                readonly
                                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50 text-gray-500"
                            />
                            <p class="mt-1 text-xs text-gray-500">
                                Para cambiar tu email, contáctanos
                            </p>
                        </div>

                        <!-- Cambiar contraseña -->
                        <div class="pt-4 border-t border-gray-200">
                            <h3 class="text-md font-medium text-gray-900 mb-4">Cambiar Contraseña</h3>
                            
                            <form @submit.prevent="handleChangePassword" class="space-y-4">
                                <div>
                                    <label for="new_password" class="block text-sm font-medium text-gray-700">
                                        Nueva Contraseña
                                    </label>
                                    <input
                                        id="new_password"
                                        type="password"
                                        v-model="passwordForm.newPassword"
                                        :disabled="passwordLoading"
                                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
                                        placeholder="Mínimo 6 caracteres"
                                    />
                                </div>

                                <div>
                                    <label for="confirm_password" class="block text-sm font-medium text-gray-700">
                                        Confirmar Nueva Contraseña
                                    </label>
                                    <input
                                        id="confirm_password"
                                        type="password"
                                        v-model="passwordForm.confirmPassword"
                                        :disabled="passwordLoading"
                                        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50"
                                        placeholder="Repite la contraseña"
                                    />
                                </div>

                                <!-- Mensaje de éxito de contraseña -->
                                <div v-if="passwordSuccess" class="p-3 bg-green-50 border border-green-200 rounded-md">
                                    <p class="text-sm text-green-700">{{ passwordSuccess }}</p>
                                </div>

                                <!-- Mensaje de error de contraseña -->
                                <div v-if="passwordError" class="p-3 bg-red-50 border border-red-200 rounded-md">
                                    <p class="text-sm text-red-700">{{ passwordError }}</p>
                                </div>

                                <button
                                    type="submit"
                                    :disabled="passwordLoading || !isPasswordFormValid"
                                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                                    </svg>
                                    <span v-if="!passwordLoading">Cambiar Contraseña</span>
                                    <span v-else class="flex items-center">
                                        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Cambiando...
                                    </span>
                                </button>
                            </form>
                        </div>

                        <!-- Botón de cerrar sesión -->
                        <div class="pt-4 border-t border-gray-200">
                            <button
                                @click="handleLogout"
                                type="button"
                                class="inline-flex items-center px-4 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                                </svg>
                                Cerrar Sesión
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';
import { useProfile } from '../composables/useProfile.js';
import { logout } from '../services/auth.js';
import AppH1 from '../components/AppH1.vue';
import RankBadge from '../components/RankBadge.vue';

export default {
    name: 'Settings',
    components: {
        AppH1,
        RankBadge
    },
    setup() {
        const { userEmail, clearUser } = useAuth();
        const { 
            currentProfile, 
            loadCurrentProfile, 
            updateCurrentProfile,
            profileLoading 
        } = useProfile();
        
        return {
            userEmail,
            currentProfile,
            loadCurrentProfile,
            updateCurrentProfile,
            profileLoading,
            clearUser
        };
    },
    data() {
        return {
            loading: true,
            saveLoading: false,
            successMessage: null,
            errorMessage: null,
            form: {
                display_name: '',
                bio: '',
                avatar_url: ''
            },
            passwordForm: {
                newPassword: '',
                confirmPassword: ''
            },
            passwordLoading: false,
            passwordSuccess: null,
            passwordError: null
        };
    },
    computed: {
        /**
         * Validación del formulario
         */
        isFormValid() {
            return this.form.display_name.trim().length > 0 && 
                   this.bioCharCount <= 500;
        },
        
        /**
         * Contador de caracteres de la bio
         */
        bioCharCount() {
            return this.form.bio.length;
        },
        
        /**
         * Iniciales para el avatar
         */
        avatarInitials() {
            if (this.form.display_name) {
                return this.form.display_name
                    .split(' ')
                    .map(name => name.charAt(0))
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
            }
            return 'U';
        },
        
        /**
         * Validación del formulario de contraseña
         */
        isPasswordFormValid() {
            return (
                this.passwordForm.newPassword.length >= 6 &&
                this.passwordForm.newPassword === this.passwordForm.confirmPassword
            );
        }
    },
    methods: {
        /**
         * Inicializa el formulario con los datos del perfil
         */
        initializeForm() {
            if (this.currentProfile) {
                this.form = {
                    display_name: this.currentProfile.display_name || '',
                    bio: this.currentProfile.bio || '',
                    avatar_url: this.currentProfile.avatar_url || ''
                };
            }
        },
        
        /**
         * Resetea el formulario a los valores originales
         */
        resetForm() {
            this.initializeForm();
            this.clearMessages();
        },
        
        /**
         * Limpia los mensajes de estado
         */
        clearMessages() {
            this.successMessage = null;
            this.errorMessage = null;
        },
        
        /**
         * Maneja la actualización del perfil
         */
        async handleUpdateProfile() {
            this.clearMessages();
            this.saveLoading = true;
            
            try {
                // Validaciones
                if (this.form.display_name.trim().length === 0) {
                    this.errorMessage = 'El nombre de usuario es requerido';
                    return;
                }
                
                if (this.bioCharCount > 500) {
                    this.errorMessage = 'La biografía no puede exceder 500 caracteres';
                    return;
                }
                
                // Preparar datos para actualizar
                const updates = {
                    display_name: this.form.display_name.trim(),
                    bio: this.form.bio.trim(),
                    avatar_url: this.form.avatar_url.trim() || null
                };
                
                const { success, error } = await this.updateCurrentProfile(updates);
                
                if (!success) {
                    this.errorMessage = error?.message || 'Error al actualizar el perfil';
                    return;
                }
                
                this.successMessage = 'Perfil actualizado correctamente';
                
                // Limpiar mensaje de éxito después de 3 segundos
                setTimeout(() => {
                    this.successMessage = null;
                }, 3000);
                
            } catch (error) {
                console.error('Error updating profile:', error);
                this.errorMessage = 'Error inesperado al actualizar el perfil';
            } finally {
                this.saveLoading = false;
            }
        },
        
        /**
         * Maneja la actualización a PRO (placeholder)
         */
        async handleUpgradeToPro() {
            // Por ahora solo un placeholder
            alert('Funcionalidad de actualización a PRO próximamente disponible');
        },
        
        /**
         * Maneja el cambio de contraseña
         */
        async handleChangePassword() {
            this.passwordSuccess = null;
            this.passwordError = null;
            
            // Validaciones
            if (this.passwordForm.newPassword.length < 6) {
                this.passwordError = 'La contraseña debe tener al menos 6 caracteres';
                return;
            }
            
            if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
                this.passwordError = 'Las contraseñas no coinciden';
                return;
            }
            
            this.passwordLoading = true;
            
            try {
                // Importar supabase
                const { supabase } = await import('../services/supabase.js');
                
                // Actualizar contraseña
                const { error } = await supabase.auth.updateUser({
                    password: this.passwordForm.newPassword
                });
                
                if (error) {
                    this.passwordError = error.message || 'Error al cambiar la contraseña';
                    return;
                }
                
                // Éxito
                this.passwordSuccess = 'Contraseña cambiada correctamente';
                
                // Limpiar formulario
                this.passwordForm = {
                    newPassword: '',
                    confirmPassword: ''
                };
                
                // Limpiar mensaje de éxito después de 5 segundos
                setTimeout(() => {
                    this.passwordSuccess = null;
                }, 5000);
                
            } catch (error) {
                console.error('Error changing password:', error);
                this.passwordError = 'Error inesperado al cambiar la contraseña';
            } finally {
                this.passwordLoading = false;
            }
        },
        
        /**
         * Maneja el cierre de sesión
         */
        async handleLogout() {
            if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
                try {
                    const { error } = await logout();
                    
                    if (error) {
                        console.error('Error during logout:', error);
                        this.errorMessage = 'Error al cerrar sesión';
                        return;
                    }
                    
                    this.clearUser();
                    this.$router.push('/');
                } catch (error) {
                    console.error('Unexpected error during logout:', error);
                    this.errorMessage = 'Error inesperado al cerrar sesión';
                }
            }
        },
        
        /**
         * Maneja errores de carga de imagen
         */
        handleImageError(event) {
            event.target.style.display = 'none';
        }
    },
    
    async mounted() {
        this.loading = true;
        
        try {
            // Cargar perfil actual si no está cargado
            if (!this.currentProfile) {
                await this.loadCurrentProfile();
            }
            
            // Inicializar formulario
            this.initializeForm();
        } catch (error) {
            console.error('Error loading profile in settings:', error);
            this.errorMessage = 'Error al cargar la configuración del perfil';
        } finally {
            this.loading = false;
        }
    },
    
    /**
     * Watcher para actualizar el formulario cuando cambie el perfil
     */
    watch: {
        currentProfile: {
            handler(newProfile) {
                if (newProfile) {
                    this.initializeForm();
                }
            },
            immediate: true
        }
    }
};
</script>