<template>
  <div class="min-h-screen bg-gray-900 pt-20 pb-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-white mb-2">Mensajes</h1>
        <p class="text-gray-400">Tus conversaciones privadas</p>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-red-900/20 border border-red-500 rounded-lg p-6 text-center">
        <p class="text-red-400 text-lg mb-4">{{ error }}</p>
        <button
          @click="loadConversations"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-200"
        >
          Reintentar
        </button>
      </div>

      <!-- Lista de conversaciones -->
      <div v-else-if="conversations.length > 0" class="bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div
          v-for="conversation in conversations"
          :key="conversation.otherUserId"
          @click="openChat(conversation)"
          class="flex items-center gap-4 p-4 hover:bg-gray-700 border-b border-gray-700 last:border-b-0 cursor-pointer transition duration-200"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <div class="h-14 w-14 rounded-full bg-indigo-600 flex items-center justify-center">
              <span class="text-lg font-medium text-white">
                {{ getUserInitials(conversation.otherUserDisplayName) }}
              </span>
            </div>
          </div>

          <!-- Info de la conversación -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-1">
              <h3 class="text-white font-semibold truncate">
                {{ conversation.otherUserDisplayName || 'Usuario' }}
              </h3>
              <span class="text-xs text-gray-400 flex-shrink-0 ml-2">
                {{ formatDate(conversation.lastMessageDate) }}
              </span>
            </div>
            
            <div class="flex items-center gap-2">
              <p class="text-sm text-gray-400 truncate">
                <span v-if="conversation.isLastMessageFromMe" class="text-gray-500">Tú: </span>
                {{ conversation.lastMessage }}
              </p>
            </div>

            <div class="flex items-center gap-2 mt-1">
              <span class="text-xs px-2 py-0.5 bg-gray-700 text-gray-300 rounded-full">
                {{ conversation.otherUserRango || 'Novato' }}
              </span>
            </div>
          </div>

          <!-- Indicador de chat -->
          <div class="flex-shrink-0">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-else class="bg-gray-800 rounded-lg shadow-lg p-12 text-center">
        <svg class="w-20 h-20 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
        </svg>
        <h3 class="text-xl font-semibold text-white mb-2">No tienes conversaciones</h3>
        <p class="text-gray-400 mb-6">Comienza a chatear con otros usuarios desde sus perfiles</p>
        <RouterLink
          to="/feed"
          class="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-200"
        >
          Ir al Feed
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth.js';
import { getConversations } from '../services/private-chat.js';
import { createSlugFromDisplayName } from '../services/profiles.js';

const router = useRouter();
const { userId: currentUserId } = useAuth();

// Estados
const conversations = ref([]);
const loading = ref(true);
const error = ref(null);

/**
 * Obtiene las iniciales de un usuario
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

//Formatea la fecha de un mensaje
function formatDate(dateString) {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);

  if (diffMins < 1) return 'Ahora';
  if (diffMins < 60) return `Hace ${diffMins}m`;
  
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `Hace ${diffHours}h`;

  const diffDays = Math.floor(diffHours / 24);
  if (diffDays === 1) return 'Ayer';
  if (diffDays < 7) return `Hace ${diffDays}d`;

  return new Intl.DateTimeFormat('es-AR', {
    day: '2-digit',
    month: '2-digit'
  }).format(date);
}

//Carga las conversaciones del usuario
async function loadConversations() {
  loading.value = true;
  error.value = null;

  try {
    const { conversations: userConversations, error: convError } = await getConversations(currentUserId.value);

    if (convError) {
      console.error('Error loading conversations:', convError);
      error.value = 'Error al cargar las conversaciones';
      return;
    }

    conversations.value = userConversations || [];
  } catch (err) {
    console.error('Unexpected error loading conversations:', err);
    error.value = 'Error inesperado al cargar las conversaciones';
  } finally {
    loading.value = false;
  }
}

//Abre el chat con un usuario
function openChat(conversation) {
  const slug = conversation.otherUserDisplayName 
    ? createSlugFromDisplayName(conversation.otherUserDisplayName)
    : conversation.otherUserId;
  
  router.push({ name: 'PrivateChat', params: { displayName: slug } });
}

onMounted(() => {
  loadConversations();
});
</script>