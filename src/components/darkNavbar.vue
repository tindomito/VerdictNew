<template>
  <nav class="relative bg-gray-800 after:pointer-events-none after:absolute after:inset-x-0 after:bottom-0 after:h-px after:bg-white/10">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        
        <!-- Botón menú móvil -->
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden" data-mobile-menu>
          <button
            @click.stop="mobileMenuOpen = !mobileMenuOpen"
            class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-white/5 hover:text-white focus:outline-2 focus:-outline-offset-1 focus:outline-indigo-500"
          >
            <span class="sr-only">Open main menu</span>
            <svg v-if="!mobileMenuOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-6 w-6">
              <path d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-6 w-6">
              <path d="M6 18 18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <!-- Logo y enlaces -->
        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex shrink-0 items-center">
            <RouterLink to="/" class="flex items-center">
              <img src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=500" alt="Logo" class="h-8 w-auto" />
              <span class="ml-2 text-white font-bold text-lg">MMA Social</span>
            </RouterLink>
          </div>
          <div class="hidden sm:ml-6 sm:flex space-x-4">
            <RouterLink 
              to="/" 
              class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white"
              active-class="!bg-gray-900 !text-white"
            >
              Home
            </RouterLink>
            <RouterLink 
              to="/chat" 
              class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white"
              active-class="!bg-gray-900 !text-white"
            >
              Chat General
            </RouterLink>
            <!-- Enlaces adicionales cuando esté autenticado -->
            <template v-if="isAuthenticated">
              <RouterLink 
                to="/feed" 
                class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white"
                active-class="!bg-gray-900 !text-white"
              >
                Feed
              </RouterLink>
            </template>
          </div>
        </div>

        <!-- Sección derecha del navbar -->
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0 gap-3">
          <!-- Buscador de usuarios (solo cuando está autenticado) -->
          <template v-if="isAuthenticated">
            <div class="relative hidden sm:block" data-search-dropdown>
              <div class="relative">
                <input
                  v-model="searchQuery"
                  @input="handleSearch"
                  @focus="searchFocused = true"
                  type="text"
                  placeholder="Buscar usuarios..."
                  class="w-64 rounded-md bg-gray-700 px-3 py-1.5 pl-10 text-sm text-white placeholder-gray-400 focus:outline-2 focus:outline-indigo-500 focus:bg-gray-600"
                />
                <svg 
                  class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
              
              <!-- Dropdown de resultados -->
              <div 
                v-show="searchFocused && (searchResults.length > 0 || (searchQuery.length > 0 && !searchLoading))"
                class="absolute right-0 mt-2 w-80 rounded-md bg-gray-800 py-2 shadow-lg ring-1 ring-black ring-opacity-5 z-[100] max-h-96 overflow-y-auto"
              >
                <!-- Loading state -->
                <div v-if="searchLoading" class="px-4 py-3 text-sm text-gray-400 text-center">
                  <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-500 mx-auto"></div>
                </div>
                
                <!-- Resultados -->
                <template v-else-if="searchResults.length > 0">
                  <RouterLink
                    v-for="user in searchResults"
                    :key="user.id"
                    :to="`/profile/${user.slug}`"
                    @click="closeSearch"
                    class="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 transition duration-200"
                  >
                    <div class="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
                      <span class="text-sm font-medium text-white">
                        {{ getUserInitials(user.display_name || user.email) }}
                      </span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-white truncate">
                        {{ user.display_name || 'Usuario sin nombre' }}
                      </p>
                      <p class="text-xs text-gray-400 truncate">
                        {{ user.rango || 'Novato' }}
                      </p>
                    </div>
                  </RouterLink>
                </template>
                
                <!-- No results -->
                <div v-else-if="searchQuery.length > 0" class="px-4 py-3 text-sm text-gray-400 text-center">
                  No se encontraron usuarios
                </div>
              </div>
            </div>
          </template>

          <!-- Si NO está autenticado -->
          <template v-if="!isAuthenticated && !loading">
            <div class="hidden sm:flex sm:space-x-2">
              <RouterLink 
                to="/login"
                class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-white/5 hover:text-white border border-gray-600 hover:border-gray-400 transition duration-200"
              >
                Iniciar Sesión
              </RouterLink>
              <RouterLink 
                to="/register"
                class="rounded-md px-3 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition duration-200"
              >
                Registrarse
              </RouterLink>
            </div>
          </template>

          <!-- Si está autenticado -->
          <template v-if="isAuthenticated">
            <!-- Botón de notificaciones -->
            <button class="relative rounded-full p-1 text-gray-400 hover:text-white focus:outline-2 focus:outline-offset-2 focus:outline-indigo-500">
              <span class="sr-only">View notifications</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-6 w-6">
                <path d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>

            <!-- Dropdown perfil -->
            <div class="relative" data-dropdown>
              <button 
                @click.stop="profileMenuOpen = !profileMenuOpen" 
                class="relative flex items-center space-x-2 rounded-full focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 text-gray-300 hover:text-white p-2"
              >
                <span class="sr-only">Open user menu</span>
                <div class="flex items-center space-x-2">
                  <div class="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center">
                    <span class="text-sm font-medium text-white">
                      {{ userInitials }}
                    </span>
                  </div>
                  <span class="hidden sm:block text-sm font-medium">
                    {{ userDisplayName || userEmail }}
                  </span>
                  <svg 
                    class="h-4 w-4" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
              </button>
              
              <div v-show="profileMenuOpen" class="absolute right-0 mt-2 w-48 rounded-md bg-gray-800 py-1 shadow-lg ring-1 ring-black ring-opacity-5 z-[100]">
                <div class="px-4 py-2 text-xs text-gray-400 border-b border-gray-700">
                  Conectado como<br>
                  <span class="font-medium text-gray-200">{{ userEmail }}</span>
                </div>
                <RouterLink 
                  :to="`/profile/${userProfileSlug}`"
                  @click="profileMenuOpen = false"
                  class="block px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition duration-200"
                >
                  <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  Mi Perfil
                </RouterLink>
                <RouterLink 
                  to="/settings" 
                  @click="profileMenuOpen = false"
                  class="block px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition duration-200"
                >
                  <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  Configuración
                </RouterLink>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/5 hover:text-white transition duration-200"
                >
                  <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                  </svg>
                  Cerrar Sesión
                </button>
              </div>
            </div>
          </template>

          <!-- Loading state -->
          <template v-if="loading">
            <div class="flex items-center space-x-2">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Menú móvil -->
    <div 
      v-show="mobileMenuOpen" 
      class="sm:hidden px-2 space-y-1 bg-gray-800 pb-3 relative z-50" 
      data-mobile-menu-content
    >
      <RouterLink 
        to="/" 
        @click="closeMobileMenu"
        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
        active-class="!bg-gray-900 !text-white"
      >
        Home
      </RouterLink>
      <RouterLink 
        to="/chat" 
        @click="closeMobileMenu"
        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
        active-class="!bg-gray-900 !text-white"
      >
        Chat General
      </RouterLink>
      
      <!-- Enlaces adicionales cuando esté autenticado (móvil) -->
      <template v-if="isAuthenticated">
        <RouterLink 
          to="/feed" 
          @click="closeMobileMenu"
          class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
          active-class="!bg-gray-900 !text-white"
        >
          Feed
        </RouterLink>

        <!-- Buscador móvil -->
        <div class="pt-3 pb-2" data-search-dropdown>
          <div class="relative">
            <input
              v-model="searchQuery"
              @input="handleSearch"
              @focus="searchFocused = true"
              type="text"
              placeholder="Buscar usuarios..."
              class="w-full rounded-md bg-gray-700 px-3 py-2 pl-10 text-sm text-white placeholder-gray-400 focus:outline-2 focus:outline-indigo-500 focus:bg-gray-600"
            />
            <svg 
              class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          
          <!-- Resultados búsqueda móvil -->
          <div v-if="searchFocused && searchQuery.length > 0" class="mt-2 space-y-1">
            <!-- Loading -->
            <div v-if="searchLoading" class="px-3 py-2 text-sm text-gray-400 text-center">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-500 mx-auto"></div>
            </div>
            
            <!-- Resultados -->
            <template v-else-if="searchResults.length > 0">
              <RouterLink
                v-for="user in searchResults"
                :key="user.id"
                :to="`/profile/${user.slug}`"
                @click="closeSearch(); closeMobileMenu()"
                class="flex items-center gap-3 rounded-md px-3 py-2 hover:bg-white/5"
              >
                <div class="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center shrink-0">
                  <span class="text-sm font-medium text-white">
                    {{ getUserInitials(user.display_name || user.email) }}
                  </span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-white truncate">
                    {{ user.display_name || 'Usuario sin nombre' }}
                  </p>
                  <p class="text-xs text-gray-400 truncate">
                    {{ user.rango || 'Novato' }}
                  </p>
                </div>
              </RouterLink>
            </template>
            
            <!-- No results -->
            <div v-else class="px-3 py-2 text-sm text-gray-400 text-center">
              No se encontraron usuarios
            </div>
          </div>
        </div>

        <div class="border-t border-gray-700 pt-3 mt-3">
          <div class="px-3 py-2 text-xs text-gray-400 truncate">
            {{ userEmail }}
          </div>
          <RouterLink 
            :to="`/profile/${userProfileSlug}`"
            @click="closeMobileMenu"
            class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
          >
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
            Mi Perfil
          </RouterLink>
          <RouterLink 
            to="/settings" 
            @click="closeMobileMenu"
            class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
          >
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            Configuración
          </RouterLink>
          <button 
            @click="handleLogout"
            class="block w-full text-left rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
          >
            <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Cerrar Sesión
          </button>
        </div>
      </template>

      <!-- Enlaces de auth para móvil cuando NO esté autenticado -->
      <template v-if="!isAuthenticated && !loading">
        <div class="border-t border-gray-700 pt-3 mt-3 space-y-1">
          <RouterLink 
            to="/login" 
            @click="closeMobileMenu"
            class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-white/5 hover:text-white"
          >
            Iniciar Sesión
          </RouterLink>
          <RouterLink 
            to="/register" 
            @click="closeMobileMenu"
            class="block rounded-md px-3 py-2 text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Registrarse
          </RouterLink>
        </div>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth.js';
import { logout } from '../services/auth.js';
import { createSlugFromDisplayName, searchProfiles } from '../services/profiles.js';

const router = useRouter();
const { isAuthenticated, loading, userEmail, userDisplayName, clearUser, initialize, userId } = useAuth();

const mobileMenuOpen = ref(false);
const profileMenuOpen = ref(false);

// Estados del buscador
const searchQuery = ref('');
const searchResults = ref([]);
const searchLoading = ref(false);
const searchFocused = ref(false);
let searchTimeout = null;

/**
 * Computed para obtener el slug del perfil del usuario actual
 */
const userProfileSlug = computed(() => {
  if (userDisplayName.value) {
    return createSlugFromDisplayName(userDisplayName.value);
  }
  return userId.value;
});

const userInitials = computed(() => {
  if (userDisplayName.value) {
    return userDisplayName.value
      .split(' ')
      .map(name => name.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  }
  if (userEmail.value) {
    return userEmail.value.charAt(0).toUpperCase();
  }
  return 'U';
});

/**
 * Obtiene las iniciales de un usuario para el avatar
 */
function getUserInitials(name) {
  if (!name) return 'U';
  return name
    .split(' ')
    .map(n => n.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Busca usuarios en la base de datos
 */
async function searchUsers(query) {
  if (!query || query.length < 2) {
    searchResults.value = [];
    return;
  }

  searchLoading.value = true;

  try {
    const { profiles, error } = await searchProfiles(query, 10);

    if (error) throw error;

    // Los perfiles ya vienen con el slug desde searchProfiles
    searchResults.value = profiles;
  } catch (error) {
    console.error('Error buscando usuarios:', error);
    searchResults.value = [];
  } finally {
    searchLoading.value = false;
  }
}

/**
 * Maneja el input de búsqueda con debounce
 */
function handleSearch() {
  clearTimeout(searchTimeout);
  
  if (searchQuery.value.length < 2) {
    searchResults.value = [];
    return;
  }

  searchTimeout = setTimeout(() => {
    searchUsers(searchQuery.value);
  }, 300);
}

/**
 * Cierra el buscador
 */
function closeSearch() {
  searchFocused.value = false;
  searchQuery.value = '';
  searchResults.value = [];
}

/**
 * Cierra el menú móvil
 */
function closeMobileMenu() {
  mobileMenuOpen.value = false;
}

/**
 * Maneja el logout del usuario
 */
async function handleLogout() {
  try {
    profileMenuOpen.value = false;
    mobileMenuOpen.value = false;
    const { error } = await logout();
    
    if (error) {
      console.error('Error during logout:', error);
    }
    
    clearUser();
    router.push('/');
  } catch (error) {
    console.error('Unexpected error during logout:', error);
  }
}

/**
 * Cierra los menús cuando se hace click fuera
 */
function handleClickOutside(event) {
  // Verifica si el click fue dentro del menú móvil o su botón
  const mobileMenuButton = event.target.closest('[data-mobile-menu]');
  const mobileMenuContent = event.target.closest('[data-mobile-menu-content]');
  
  if (!mobileMenuButton && !mobileMenuContent) {
    mobileMenuOpen.value = false;
  }
  
  // Verifica si el click fue dentro del dropdown del perfil
  if (!event.target.closest('[data-dropdown]')) {
    profileMenuOpen.value = false;
  }

  // Verifica si el click fue dentro del buscador
  if (!event.target.closest('[data-search-dropdown]')) {
    searchFocused.value = false;
  }
}

onMounted(() => {
  initialize();
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  clearTimeout(searchTimeout);
});
</script>