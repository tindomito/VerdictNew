<template>
    <div 
        :class="[
            'bg-white rounded-lg shadow-md overflow-hidden transition-all duration-200',
            clickable ? 'hover:shadow-lg cursor-pointer' : '',
            compact ? 'p-4' : 'p-6'
        ]"
        @click="handleClick"
    >
        <!-- Header del perfil -->
        <div class="flex items-start space-x-4">
            <!-- Avatar -->
            <div class="flex-shrink-0">
                <div 
                    :class="[
                        'rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold',
                        compact ? 'w-12 h-12 text-lg' : 'w-16 h-16 text-xl'
                    ]"
                >
                    <img 
                        v-if="profile.avatar_url" 
                        :src="profile.avatar_url" 
                        :alt="`Avatar de ${displayName}`"
                        class="w-full h-full rounded-full object-cover"
                        @error="handleImageError"
                    />
                    <span v-else>{{ avatarInitials }}</span>
                </div>
            </div>

            <!-- Información del usuario -->
            <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-1">
                    <h3 
                        :class="[
                            'font-semibold text-gray-900 truncate',
                            compact ? 'text-base' : 'text-lg'
                        ]"
                    >
                        {{ displayName }}
                    </h3>
                </div>
                
                <!-- Rango y PRO -->
                <div class="mb-2">
                    <RankBadge 
                        :rango="profile.rango" 
                        :isPro="profile.pro"
                        :showProgress="showRankProgress && !compact"
                    />
                </div>

                <!-- Bio (si no es compact) -->
                <p 
                    v-if="!compact && profile.bio" 
                    class="text-sm text-gray-600 line-clamp-2"
                >
                    {{ profile.bio }}
                </p>
                
                <!-- Estadísticas básicas -->
                <div 
                    v-if="showStats" 
                    class="flex items-center space-x-4 mt-3 text-xs text-gray-500"
                >
                    <span class="flex items-center">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                        </svg>
                        Miembro desde {{ memberSince }}
                    </span>
                </div>
            </div>

            <!-- Botón de acción (opcional) -->
            <div v-if="showAction && !compact" class="flex-shrink-0">
                <button
                    @click.stop="$emit('action', profile)"
                    class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                    {{ actionText }}
                </button>
            </div>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
        </div>
    </div>
</template>

<script>
import RankBadge from './RankBadge.vue';

export default {
    name: 'ProfileCard',
    components: {
        RankBadge
    },
    props: {
        /**
         * Objeto del perfil a mostrar
         */
        profile: {
            type: Object,
            required: true
        },
        /**
         * Si la tarjeta es clickeable
         */
        clickable: {
            type: Boolean,
            default: false
        },
        /**
         * Versión compacta de la tarjeta
         */
        compact: {
            type: Boolean,
            default: false
        },
        /**
         * Mostrar progreso del rango
         */
        showRankProgress: {
            type: Boolean,
            default: false
        },
        /**
         * Mostrar estadísticas básicas
         */
        showStats: {
            type: Boolean,
            default: true
        },
        /**
         * Mostrar botón de acción
         */
        showAction: {
            type: Boolean,
            default: false
        },
        /**
         * Texto del botón de acción
         */
        actionText: {
            type: String,
            default: 'Ver Perfil'
        },
        /**
         * Estado de carga
         */
        loading: {
            type: Boolean,
            default: false
        }
    },
    emits: ['click', 'action'],
    computed: {
        /**
         * Nombre para mostrar
         */
        displayName() {
            return this.profile?.display_name || 'Usuario sin nombre';
        },
        
        /**
         * Iniciales para el avatar
         */
        avatarInitials() {
            if (this.profile?.display_name) {
                return this.profile.display_name
                    .split(' ')
                    .map(name => name.charAt(0))
                    .join('')
                    .toUpperCase()
                    .slice(0, 2);
            }
            return 'U';
        },
        
        /**
         * Fecha formateada de cuando se unió
         */
        memberSince() {
            if (!this.profile?.created_at) return 'Desconocido';
            
            const date = new Date(this.profile.created_at);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short' 
            });
        }
    },
    methods: {
        /**
         * Maneja el click en la tarjeta
         */
        handleClick() {
            if (this.clickable) {
                this.$emit('click', this.profile);
            }
        },
        
        /**
         * Maneja errores de carga de imagen
         */
        handleImageError(event) {
            event.target.style.display = 'none';
        }
    }
};
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>