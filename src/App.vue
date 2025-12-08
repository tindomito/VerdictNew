<template>
    <DarkNavbar />

    <main class="container mx-auto p-4 sm:p-6 lg:p-8">

        <RouterView />
    </main>

    <MyFooter/>

    <!-- Sistema de notificaciones toast -->
    <ToastNotification />
</template>

<script>
import DarkNavbar from './components/darkNavbar.vue';
import MyFooter from './components/myFooter.vue';
import ToastNotification from './components/ToastNotification.vue';
import { useAuth } from './composables/useAuth.js';

export default {
    name: 'App',
    components: {
        DarkNavbar,
        MyFooter,
        ToastNotification,
    },
    setup() {
        // Inicializar el sistema de autenticación
        const { initialize } = useAuth();
        return { initialize };
    },
    async mounted() {
        // Inicializar el sistema de autenticación
        await this.initialize();
        
        // Debug del estado de autenticación
        const { isAuthenticated, user, loading } = useAuth();

        
        // Cargar perfil si está autenticado
        await this.loadProfileIfAuthenticated();
    },
    methods: {
        // Carga el perfil del usuario si está autenticado
        async loadProfileIfAuthenticated() {
            const { isAuthenticated } = useAuth();
            
            if (isAuthenticated.value) {
                // Importar dinámicamente para evitar dependencias circulares
                const { useProfile } = await import('./composables/useProfile.js');
                const { loadCurrentProfile } = useProfile();
                try {
                    await loadCurrentProfile();
                } catch (error) {
                    console.error('Error loading user profile:', error);
                }
            }
        }
    }
}
</script>