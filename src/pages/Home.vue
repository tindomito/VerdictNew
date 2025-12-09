<template>
    <div class="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900">
        <!-- Hero Section -->
        <section class="relative overflow-hidden py-20 sm:py-32">
            <!-- Background decorativo -->
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.1),transparent_50%)]"></div>
            
            <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center">
                    <!-- Badge -->
                    <div class="inline-flex items-center px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 mb-8">
                        <span class="text-indigo-400 text-sm font-medium">🥊 La comunidad #1 de MMA</span>
                    </div>
                    
                    <!-- Título principal -->
                    <h1 class="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 tracking-tight">
                        Conecta con la
                        <span class="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                            comunidad MMA
                        </span>
                    </h1>
                    
                    <!-- Subtítulo -->
                    <p class="text-xl sm:text-2xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
                        Comparte tus conocimientos, analiza peleas y conecta con otros fanáticos de las artes marciales mixtas
                    </p>
                    
                    <!-- CTAs -->
                    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <RouterLink
                            v-if="!isAuthenticated"
                            to="/register"
                            class="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/50"
                        >
                            <span class="relative z-10">Comenzar ahora</span>
                            <svg class="ml-2 w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        </RouterLink>
                        
                        <RouterLink
                            v-if="isAuthenticated"
                            to="/publicaciones"
                            class="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-indigo-500/50"
                        >
                            <span class="relative z-10">Ver Publicaciones</span>
                            <svg class="ml-2 w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        </RouterLink>
                        
                        <RouterLink
                            to="/chat"
                            class="inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-gray-300 bg-white/5 backdrop-blur-sm border border-white/10 rounded-lg hover:bg-white/10 hover:border-white/20 transition-all duration-300"
                        >
                            Explorar Chat
                        </RouterLink>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="py-20 relative">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-16">
                    <h2 class="text-3xl sm:text-4xl font-bold text-white mb-4">
                        Todo lo que necesitas
                    </h2>
                    <p class="text-xl text-gray-400">
                        Una plataforma completa para la comunidad MMA
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <!-- Feature 1 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Comunidad Activa</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Conecta con fanáticos, analistas y practicantes de MMA de todo el mundo
                        </p>
                    </div>

                    <!-- Feature 2 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Chat en Tiempo Real</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Discute peleas en vivo, comparte análisis y debate con otros usuarios
                        </p>
                    </div>

                    <!-- Feature 3 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Sistema de Rangos</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Progresa desde Novato hasta Hall of Fame según tu actividad y conocimiento
                        </p>
                    </div>

                    <!-- Feature 4 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Perfiles Personalizados</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Crea tu perfil, comparte tu experiencia y muestra tus conocimientos
                        </p>
                    </div>

                    <!-- Feature 5 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Predicciones y Recompensas</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Comparte análisis, predicciones y contenido sobre tus peleas favoritas
                        </p>
                    </div>

                    <!-- Feature 6 -->
                    <div class="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 hover:border-indigo-500/50 transition-all duration-300">
                        <div class="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                            <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                            </svg>
                        </div>
                        <h3 class="text-xl font-bold text-white mb-3">Tiempo Real</h3>
                        <p class="text-gray-400 leading-relaxed">
                            Todas las actualizaciones y mensajes se sincronizan instantáneamente
                        </p>
                    </div>
                </div>
            </div>
        </section>



        <!-- CTA Final -->
        <section class="py-20 relative" v-if="!isAuthenticated">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <h2 class="text-4xl sm:text-5xl font-bold text-white mb-6">
                    ¿Listo para unirte?
                </h2>
                <p class="text-xl text-gray-400 mb-10">
                    Crea tu cuenta gratis y comienza a conectar con la comunidad MMA
                </p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <RouterLink
                        to="/register"
                        class="inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-white bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg hover:scale-105 transition-all duration-300 hover:shadow-2xl hover:shadow-indigo-500/50"
                    >
                        Crear cuenta gratis
                        <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                        </svg>
                    </RouterLink>
                    <RouterLink
                        to="/login"
                        class="inline-flex items-center justify-center px-8 py-4 text-lg font-medium text-gray-300 bg-white/5 backdrop-blur-sm border border-white/10 rounded-lg hover:bg-white/10 hover:border-white/20 transition-all duration-300"
                    >
                        Ya tengo cuenta
                    </RouterLink>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import { useAuth } from '../composables/useAuth.js';

export default {
    name: 'Home',
    setup() {
        const { isAuthenticated } = useAuth();
        
        return {
            isAuthenticated
        };
    }
}
</script>