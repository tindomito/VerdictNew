<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <!-- Header -->
            <div>
                <div class="mx-auto h-12 w-auto flex justify-center">
                    <img 
                        src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500" 
                        alt="Logo" 
                        class="h-12 w-12"
                    />
                </div>
                <h1 class="mt-6 text-center text-3xl font-bold text-gray-900">
                    Crear Cuenta
                </h1>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Únete a la comunidad de MMA más activa
                </p>
            </div>

            <!-- Formulario -->
            <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
                <!-- Mensaje de error -->
                <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
                    <div class="flex">
                        <div class="ml-3">
                            <h3 class="text-sm font-medium text-red-800">
                                Error en el registro
                            </h3>
                            <div class="mt-2 text-sm text-red-700">
                                {{ error }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Mensaje de éxito -->
                <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-md p-4">
                    <div class="flex">
                        <div class="ml-3">
                            <div class="text-sm text-green-700">
                                {{ successMessage }}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="space-y-4">
                    <!-- Display Name -->
                    <div>
                        <label for="displayName" class="block text-sm font-medium text-gray-700">
                            Nombre de usuario
                        </label>
                        <input
                            id="displayName"
                            name="displayName"
                            type="text"
                            required
                            v-model="form.displayName"
                            :disabled="loading"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            placeholder="Tu nombre de usuario"
                        />
                        <p class="mt-1 text-xs text-gray-500">
                            Este será tu nombre visible en la comunidad
                        </p>
                    </div>

                    <!-- Email -->
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">
                            Email
                        </label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            autocomplete="email"
                            required
                            v-model="form.email"
                            :disabled="loading"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            placeholder="tu@email.com"
                        />
                    </div>

                    <!-- Password -->
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">
                            Contraseña
                        </label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autocomplete="new-password"
                            required
                            v-model="form.password"
                            :disabled="loading"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            placeholder="••••••••"
                        />
                        <p class="mt-1 text-xs text-gray-500">
                            Mínimo 6 caracteres
                        </p>
                    </div>

                    <!-- Confirm Password -->
                    <div>
                        <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
                            Confirmar contraseña
                        </label>
                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type="password"
                            autocomplete="new-password"
                            required
                            v-model="form.confirmPassword"
                            :disabled="loading"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            placeholder="••••••••"
                        />
                    </div>
                </div>

                <!-- Botón submit -->
                <div>
                    <button
                        type="submit"
                        :disabled="loading || !isFormValid"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
                    >
                        <span v-if="!loading">Crear Cuenta</span>
                        <span v-else class="flex items-center">
                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Creando cuenta...
                        </span>
                    </button>
                </div>

                <!-- Links -->
                <div class="flex items-center justify-center">
                    <div class="text-sm">
                        <span class="text-gray-600">¿Ya tienes cuenta? </span>
                        <RouterLink
                            to="/login"
                            class="font-medium text-indigo-600 hover:text-indigo-500 transition duration-200"
                        >
                            Inicia sesión aquí
                        </RouterLink>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { register } from '../services/auth.js';

export default {
    name: 'Register',
    data() {
        return {
            form: {
                displayName: '',
                email: '',
                password: '',
                confirmPassword: ''
            },
            loading: false,
            error: null,
            successMessage: null
        };
    },
    computed: {
        /**
         * Valida que el formulario esté completo y correcto
         */
        isFormValid() {
            return (
                this.form.displayName.trim().length > 0 &&
                this.form.email.trim().length > 0 &&
                this.form.password.length >= 6 &&
                this.form.password === this.form.confirmPassword
            );
        }
    },
    methods: {
        /**
         * Maneja el envío del formulario de registro
         */
        async handleRegister() {
            // Validaciones adicionales
            if (this.form.password !== this.form.confirmPassword) {
                this.error = 'Las contraseñas no coinciden';
                return;
            }

            if (this.form.password.length < 6) {
                this.error = 'La contraseña debe tener al menos 6 caracteres';
                return;
            }

            if (this.form.displayName.trim().length === 0) {
                this.error = 'El nombre de usuario es requerido';
                return;
            }

            this.loading = true;
            this.error = null;
            this.successMessage = null;

            try {
                const { user, error } = await register(
                    this.form.email.trim(),
                    this.form.password,
                    this.form.displayName.trim()
                );

                if (error) {
                    // Manejo de errores específicos
                    if (error.message.includes('User already registered')) {
                        this.error = 'Ya existe una cuenta con este email';
                    } else if (error.message.includes('Password should be at least 6 characters')) {
                        this.error = 'La contraseña debe tener al menos 6 caracteres';
                    } else if (error.message.includes('Invalid email')) {
                        this.error = 'El email no es válido';
                    } else {
                        this.error = error.message || 'Error al crear la cuenta';
                    }
                    return;
                }

                if (user) {
                    this.successMessage = 'Cuenta creada exitosamente. Revisa tu email para confirmar tu cuenta.';
                    
                    // Limpiar formulario
                    this.form = {
                        displayName: '',
                        email: '',
                        password: '',
                        confirmPassword: ''
                    };

                    // Redireccionar al login después de un momento
                    setTimeout(() => {
                        this.$router.push('/login');
                    }, 3000);
                }
            } catch (error) {
                this.error = 'Error inesperado. Intenta nuevamente.';
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>