import { createRouter, createWebHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import PublicChat from '../pages/PublicChat.vue';
import Login from '../pages/Login.vue';
import Register from '../pages/Register.vue';
import Profile from '../pages/Profile.vue';
import Settings from '../pages/Settings.vue';
import Feed from '../pages/Feed.vue';
import PrivateChat from '../pages/PrivateChat.vue';
import Messages from '../pages/MessagesView.vue';

// Definimos la lista de rutas de nuestra aplicación
const routes = [
    {
        path: '/',
        component: Home,
        name: 'Home'
    },
    {
        path: '/chat',
        component: PublicChat,
        name: 'PublicChat'
    },
    {
        path: '/login',
        component: Login,
        name: 'Login'
    },
    {
        path: '/register',
        component: Register,
        name: 'Register'
    },
    {
        path: '/profile/:id?',
        component: Profile,
        name: 'Profile',
        props: true
    },
    {
        path: '/settings',
        component: Settings,
        name: 'Settings',
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/feed',
        component: Feed,
        name: 'Feed',
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/chat/:displayName',
        component: PrivateChat,
        name: 'PrivateChat',
        props: true,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/messages',
        component: Messages,
        name: 'Messages',
        meta: {
            requiresAuth: true
        }
    }
];

const router = createRouter({
    routes,
    history: createWebHistory(),
});

// Guard global para rutas que requieren autenticación
router.beforeEach(async (to, from, next) => {
    console.log('Router guard:', { to: to.path, requiresAuth: to.meta.requiresAuth });

    // Importar composable de auth
    const { useAuth } = await import('../composables/useAuth.js');
    const { isAuthenticated, user, loading, initialize } = useAuth();

    // Asegurar que la autenticación esté inicializada
    await initialize();

    // Verificar si la ruta requiere autenticación
    if (to.meta.requiresAuth) {
        console.log('Auth check for protected route:', {
            isAuthenticated: isAuthenticated.value,
            user: user.value,
            loading: loading.value
        });

        if (!isAuthenticated.value) {
            console.log('User not authenticated, redirecting to login');
            // Redireccionar al login si no está autenticado
            next({
                name: 'Login',
                query: { redirect: to.fullPath }
            });
            return;
        }
    }

    // Si va a /profile sin ID y está autenticado, redirigir a su propio perfil
    if (to.name === 'Profile' && !to.params.id) {
        const { userId } = useAuth();

        console.log('Profile redirect check:', {
            isAuthenticated: isAuthenticated.value,
            userId: userId.value
        });

        if (isAuthenticated.value && userId.value) {
            console.log('Redirecting to own profile:', userId.value);
            next({
                name: 'Profile',
                params: { id: userId.value }
            });
            return;
        }
    }

    next();
});

export default router;