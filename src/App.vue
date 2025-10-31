<template>
    <DarkNavbar />

    <main class="container mx-auto p-4 sm:p-6 lg:p-8">
        <!-- 
        RouterView es un componete que registra globalmente el use(router) (en main.js).
        Esto define dónde queremos que se monte los componentes de las vistas que 
        correspondan a la URL.
        -->
        <RouterView />
    </main>

    <MyFooter/>
</template>

<script>
import DarkNavbar from './components/darkNavbar.vue';
import MyFooter from './components/myFooter.vue';
import { useAuth } from './composables/useAuth.js';

export default {
    name: 'App',
    components: { 
        DarkNavbar,
        MyFooter,
    },
    setup() {
        // Inicializar el sistema de autenticación
        const { initialize } = useAuth();
        return { initialize };
    },
    async mounted() {
        // console.log('App mounted - initializing auth...');
        
        // Inicializar el sistema de autenticación
        await this.initialize();
        
        // Debug del estado de autenticación
        const { isAuthenticated, user, loading } = useAuth();
        // console.log('Auth state after init:', {
        //     isAuthenticated: isAuthenticated.value,
        //     user: user.value,
        //     loading: loading.value
        // });
        
        // Cargar perfil si está autenticado
        await this.loadProfileIfAuthenticated();
    },
    methods: {
        /**
         * Carga el perfil del usuario si está autenticado
         */
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