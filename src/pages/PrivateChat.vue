<template>
  <div class="min-h-screen bg-gray-900 pt-20 pb-8">
    <div class="max-w-4xl mx-auto px-4">
      <!-- Header del chat -->
      <div class="bg-gray-800 rounded-t-lg p-4 border-b border-gray-700">
        <div v-if="loadingOtherUser" class="flex items-center gap-3">
          <div class="animate-pulse flex items-center gap-3">
            <div class="h-10 w-10 bg-gray-700 rounded-full"></div>
            <div class="h-4 w-32 bg-gray-700 rounded"></div>
          </div>
        </div>
        <div v-else-if="otherUser" class="flex items-center gap-3">
          <div class="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center">
            <span class="text-sm font-medium text-white">
              {{ getUserInitials(otherUser.display_name) }}
            </span>
          </div>
          <div>
            <h1 class="text-lg font-semibold text-white">
              {{ otherUser.display_name || 'Usuario' }}
            </h1>
            <p class="text-xs text-gray-400">{{ otherUser.rango || 'Novato' }}</p>
          </div>
        </div>
        <div v-else class="text-gray-400">
          Usuario no encontrado
        </div>
      </div>

      <!-- Contenedor de mensajes -->
      <div 
        ref="chatContainer"
        class="bg-gray-800 h-[500px] overflow-y-auto p-4 space-y-4"
      >
        <!-- Loading state -->
        <div v-if="loadingMessages" class="flex justify-center items-center h-full">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
        </div>

        <!-- Lista de mensajes -->
        <div v-else-if="messages.length > 0" class="space-y-4">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="[
              'flex gap-3 group',
              message.sender_id === currentUserId ? 'flex-row-reverse' : 'flex-row'
            ]"
          >
            <!-- Avatar -->
            <div class="flex-shrink-0">
              <div class="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center">
                <span class="text-xs font-medium text-white">
                  {{ message.sender_id === currentUserId 
                      ? getUserInitials(userDisplayName) 
                      : getUserInitials(otherUser?.display_name) 
                  }}
                </span>
              </div>
            </div>

            <!-- Contenido del mensaje -->
            <div 
              :class="[
                'flex flex-col max-w-[70%]',
                message.sender_id === currentUserId ? 'items-end' : 'items-start'
              ]"
            >
              <!-- Nombre del usuario -->
              <div class="flex items-center gap-2 mb-1">
                <span 
                  :class="[
                    'text-sm font-medium',
                    message.sender_id === currentUserId ? 'text-indigo-400' : 'text-gray-300'
                  ]"
                >
                  {{ message.sender_id === currentUserId 
                      ? (userDisplayName || 'Tú') 
                      : (otherUser?.display_name || 'Usuario')
                  }}
                </span>
                <span class="text-xs text-gray-500">
                  {{ formatDate(message.created_at) }}
                </span>
              </div>

              <!-- Burbuja del mensaje -->
              <div class="flex items-start gap-2" :class="message.sender_id === currentUserId ? 'flex-row-reverse' : ''">
                <div
                  :class="[
                    'px-4 py-2 rounded-2xl break-words',
                    message.sender_id === currentUserId
                      ? 'bg-indigo-600 text-white rounded-tr-none'
                      : 'bg-gray-700 text-gray-100 rounded-tl-none'
                  ]"
                >
                  <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
                </div>

                <!-- Botón eliminar (solo Admin) -->
                <button
                  v-if="isAdmin"
                  @click="handleDeleteMessage(message.id)"
                  class="p-1 text-gray-500 hover:text-red-400 hover:bg-gray-700 rounded transition-colors opacity-0 group-hover:opacity-100"
                  title="Eliminar mensaje (Admin)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Estado vacío -->
        <div v-else class="flex justify-center items-center h-full">
          <div class="text-center">
            <p class="text-gray-400 mb-2">No hay mensajes todavía</p>
            <p class="text-gray-500 text-sm">¡Inicia la conversación!</p>
          </div>
        </div>
      </div>

      <!-- Input para enviar mensajes -->
      <div class="bg-gray-800 rounded-b-lg p-4 border-t border-gray-700">
        <form @submit.prevent="handleSendMessage" class="flex gap-2 items-end">
          <div class="flex-1">
            <textarea
              v-model="newMessage"
              @keydown.enter.exact.prevent="handleSendMessage"
              placeholder="Escribe un mensaje..."
              rows="1"
              class="w-full bg-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none max-h-32"
            ></textarea>
          </div>
          <button
            type="submit"
            :disabled="!newMessage.trim() || sending"
            class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 flex items-center gap-2"
          >
            <svg v-if="!sending" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
            <div v-else class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            <span class="hidden sm:inline">{{ sending ? 'Enviando' : 'Enviar' }}</span>
          </button>
        </form>
        <p class="text-xs text-gray-500 mt-2">Presiona Enter para enviar, Shift+Enter para nueva línea</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAuth } from '../composables/useAuth.js';
import { useProfile } from '../composables/useProfile.js';
import { useToast } from '../composables/useToast.js';
import { getProfileByIdentifier } from '../services/profiles.js';
import { getPrivateMessages, sendPrivateMessage, subscribeToPrivateMessages, deletePrivateMessage } from '../services/private-chat.js';

const route = useRoute();
const { userId: currentUserId, userDisplayName } = useAuth();
const { isPro: isAdmin } = useProfile();
const { success: toastSuccess, error: toastError } = useToast();

// Estados
const otherUser = ref(null);
const loadingOtherUser = ref(true);
const messages = ref([]);
const loadingMessages = ref(true);
const newMessage = ref('');
const sending = ref(false);
const chatContainer = ref(null);

// Subscription para mensajes en tiempo real
let unsubscribe = null;

//Obtiene las iniciales de un usuario
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
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);

  if (diffMins < 1) return 'Ahora';
  if (diffMins < 60) return `Hace ${diffMins}m`;
  
  const diffHours = Math.floor(diffMins / 60);
  if (diffHours < 24) return `Hace ${diffHours}h`;

  return new Intl.DateTimeFormat('es-AR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

//Scrollea al final del chat
async function scrollToBottom() {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
}

//Carga el perfil del otro usuario
async function loadOtherUserProfile() {
  const identifier = route.params.displayName;
  
  loadingOtherUser.value = true;
  try {
    const { profile, error } = await getProfileByIdentifier(identifier);
    
    if (error || !profile) {
      console.error('Error loading user profile:', error);
      otherUser.value = null;
      return;
    }
    
    otherUser.value = profile;
  } catch (error) {
    console.error('Unexpected error loading profile:', error);
    otherUser.value = null;
  } finally {
    loadingOtherUser.value = false;
  }
}

//Carga los mensajes del chat
async function loadMessages() {
  if (!otherUser.value) return;
  
  loadingMessages.value = true;
  try {
    const { messages: chatMessages, error } = await getPrivateMessages(
      currentUserId.value,
      otherUser.value.id
    );
    
    if (error) {
      console.error('Error loading messages:', error);
      messages.value = [];
      return;
    }
    
    messages.value = chatMessages || [];
    
    await scrollToBottom();
  } catch (error) {
    console.error('Unexpected error loading messages:', error);
    messages.value = [];
  } finally {
    loadingMessages.value = false;
  }
}

//Suscribe a mensajes en tiempo real
async function subscribeToMessages() {
  if (!otherUser.value) return;
  
  try {
    unsubscribe = subscribeToPrivateMessages(
      currentUserId.value,
      otherUser.value.id,
      (newMessage) => {
        // Evitar duplicados: solo agregar si no existe
        const exists = messages.value.some(msg => msg.id === newMessage.id);
        if (!exists) {
          messages.value.push(newMessage);
          scrollToBottom();
        }
      }
    );
  } catch (error) {
    console.error('Error subscribing to messages:', error);
  }
}

//Envía un mensaje
async function handleSendMessage() {
  if (!newMessage.value.trim() || sending.value || !otherUser.value) return;
  
  sending.value = true;
  const messageContent = newMessage.value.trim();
  newMessage.value = '';
  
  try {
    const { message, error } = await sendPrivateMessage(
      currentUserId.value,
      otherUser.value.id,
      messageContent
    );
    
    if (error) {
      console.error('Error sending message:', error);
      toastError('Error al enviar el mensaje');
      newMessage.value = messageContent; // Restaurar mensaje
      return;
    }

    if (message) {
      messages.value.push({
        id: message.id,
        sender_id: currentUserId.value,
        receiver_id: otherUser.value.id,
        content: messageContent,
        created_at: new Date().toISOString(),
        read: false
      });

      toastSuccess('¡Mensaje enviado exitosamente!');
      await scrollToBottom();
    }
  } catch (error) {
    console.error('Unexpected error sending message:', error);
    toastError('Error inesperado al enviar el mensaje');
    newMessage.value = messageContent;
  } finally {
    sending.value = false;
  }
}

//Inicializa el chat
async function initializeChat() {
  await loadOtherUserProfile();

  if (otherUser.value) {
    await loadMessages();
    await subscribeToMessages();
  }
}

//Elimina un mensaje (solo Admin)
async function handleDeleteMessage(messageId) {
  if (!isAdmin.value) return;

  if (!confirm('¿Estás seguro de que quieres eliminar este mensaje?')) return;

  try {
    const { error } = await deletePrivateMessage(messageId);

    if (error) {
      console.error('Error deleting message:', error);
      toastError('Error al eliminar el mensaje');
      return;
    }

    // Eliminar del array local
    messages.value = messages.value.filter(msg => msg.id !== messageId);
    toastSuccess('Mensaje eliminado');
  } catch (error) {
    console.error('Unexpected error deleting message:', error);
    toastError('Error inesperado al eliminar el mensaje');
  }
}

onMounted(() => {
  initializeChat();
});

onUnmounted(() => {
  if (unsubscribe) {
    unsubscribe();
  }
});
</script>