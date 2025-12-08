<template>
  <div class="bg-gray-800 rounded-lg shadow-md overflow-hidden">
    <!-- Cover area (placeholder) -->
    <div class="h-32 bg-gradient-to-r from-indigo-500 to-purple-600"></div>

    <!-- Profile info -->
    <div class="px-6 py-6">
      <div class="flex flex-col sm:flex-row sm:items-start sm:space-x-6">
        <!-- Avatar -->
        <div class="flex-shrink-0 -mt-16 mb-4 sm:mb-0">
          <div class="w-24 h-24 rounded-full bg-gray-800 p-1 shadow-lg">
            <div 
              class="w-full h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-2xl"
            >
              <img 
                v-if="profile.avatar_url" 
                :src="profile.avatar_url" 
                :alt="`Avatar de ${profile.display_name}`"
                class="w-full h-full rounded-full object-cover"
                @error="handleImageError"
              />
              <span v-else>{{ avatarInitials }}</span>
            </div>
          </div>
        </div>

        <!-- Información principal -->
        <div class="flex-1 min-w-0">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 class="text-2xl font-bold text-white mb-2">
                {{ profile.display_name || 'Usuario sin nombre' }}
              </h1>
              <div class="mb-3">
                <RankBadge 
                  :rango="profile.rango" 
                  :isPro="profile.pro"
                  :showProgress="true"
                />
              </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="flex space-x-2">
              <!-- Botón Editar Perfil (si es tu perfil) -->
              <button
                v-if="isOwnProfile"
                @click="$emit('edit-profile')"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
                Editar Perfil
              </button>
              
              <!-- Botones para otros perfiles -->
              <template v-else>
                <!-- Botón Seguir -->
                <button
                  @click="$emit('follow-toggle')"
                  :disabled="followLoading"
                  class="inline-flex items-center px-4 py-2 border border-gray-600 text-sm font-medium rounded-md text-gray-300 bg-gray-700 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  Seguir
                </button>

  <!-- Botón Enviar Mensaje -->
  <RouterLink
    :to="{ name: 'PrivateChat', params: { displayName: profileSlug } }"
    class="inline-flex items-center px-4 py-2 border border-gray-600 text-sm font-medium rounded-md text-gray-300 bg-gray-700 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
  >
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
    </svg>
    Mensaje
  </RouterLink>
</template>
            </div>
          </div>
          
          <!-- Bio -->
          <div v-if="profile.bio" class="mt-4">
            <p class="text-gray-300 leading-relaxed">
              {{ profile.bio }}
            </p>
          </div>

          <!-- Estadísticas -->
          <div class="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-white">{{ stats.postsCount || 0 }}</div>
              <div class="text-sm text-gray-400">Publicaciones</div>
            </div>
            <div class="bg-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-white">{{ stats.followersCount || 0 }}</div>
              <div class="text-sm text-gray-400">Seguidores</div>
            </div>
            <div class="bg-gray-700 rounded-lg p-4 text-center">
              <div class="text-2xl font-bold text-white">{{ memberSinceFormatted }}</div>
              <div class="text-sm text-gray-400">Miembro desde</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import RankBadge from './RankBadge.vue';
import { createSlugFromDisplayName } from '../services/profiles.js';

const props = defineProps({
  profile: {
    type: Object,
    required: true
  },
  isOwnProfile: {
    type: Boolean,
    required: true
  },
  stats: {
    type: Object,
    required: true
  },
  memberSinceFormatted: {
    type: String,
    required: true
  },
  followLoading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['edit-profile', 'follow-toggle']);

/**
   Computed para las iniciales del avatar
 */
const avatarInitials = computed(() => {
  if (!props.profile.display_name) return 'U';
  return props.profile.display_name
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2);
});

/**
   Computed para el slug del perfil (para chat)
 */
const profileSlug = computed(() => {
  if (!props.profile) return '';
  return props.profile.display_name 
    ? createSlugFromDisplayName(props.profile.display_name)
    : props.profile.id;
});

/**
  
Maneja errores de carga de imagen
 */
function handleImageError(event) {
  event.target.style.display = 'none';
}
</script>