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
                    Iniciar Sesión
                </h1>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Accede a la comunidad de Verdict
                </p>
            </div>

            <!-- Formulario -->
            <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
                <!-- Mensaje de error -->
                <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
                    <div class="flex">
                        <div class="ml-3">
                            <h3 class="text-sm font-medium text-red-800">
                                Error de autenticación
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
                            autocomplete="current-password"
                            required
                            v-model="form.password"
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
                        :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
                    >
                        <span v-if="!loading">Iniciar Sesión</span>
                        <span v-else class="flex items-center">
                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Iniciando sesión...
                        </span>
                    </button>
                </div>

                <!-- Links -->
                <div class="flex items-center justify-center">
                    <div class="text-sm">
                        <span class="text-gray-600">¿No tienes cuenta? </span>
                        <RouterLink
                            to="/register"
                            class="font-medium text-indigo-600 hover:text-indigo-500 transition duration-200"
                        >
                            Regístrate aquí
                        </RouterLink>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { login } from '../services/auth.js';
import { useAuth } from '../composables/useAuth.js';

export default {
    name: 'Login',
    setup() {
        const { refreshUser } = useAuth();
        return { refreshUser };
    },
    data() {
        return {
            form: {
                email: '',
                password: ''
            },
            loading: false,
            error: null,
            successMessage: null
        };
    },
    methods: {
        /**
         * Maneja el envío del formulario de login
         */
        async handleLogin() {
            this.loading = true;
            this.error = null;
            this.successMessage = null;

            try {
                const { user, error } = await login(this.form.email, this.form.password);

                if (error) {
                    // Manejo de errores específicos
                    if (error.message.includes('Invalid login credentials')) {
                        this.error = 'Email o contraseña incorrectos';
                    } else if (error.message.includes('Email not confirmed')) {
                        this.error = 'Debes confirmar tu email antes de iniciar sesión';
                    } else {
                        this.error = error.message || 'Error al iniciar sesión';
                    }
                    return;
                }

                if (user) {
                    this.successMessage = 'Inicio de sesión exitoso';
                    await this.refreshUser();
                    
                    // Redireccionar después de login exitoso
                    setTimeout(() => {
                        this.$router.push('/');
                    }, 1000);
                }
            } catch (error) {
                this.error = 'Error inesperado. Intenta nuevamente.';
            } finally {
                this.loading = false;
            }
        }
    },
    mounted() {
        // Si ya está autenticado, redireccionar
        const { isAuthenticated } = useAuth();
        if (isAuthenticated.value) {
            this.$router.push('/');
        }
    }
};
</script>