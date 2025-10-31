<template>
    <div class="inline-flex items-center space-x-2">
        <!-- Badge del rango -->
        <span 
            :class="[
                'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                rankColorClass
            ]"
        >
            <span :class="iconClass" class="mr-1">{{ rankIcon }}</span>
            {{ rango }}
        </span>
        
        <!-- Badge PRO (opcional) -->
        <span 
            v-if="isPro" 
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold bg-gradient-to-r from-yellow-400 to-yellow-600 text-yellow-900"
        >
            ⭐ PRO
        </span>
        
        <!-- Indicador de progreso (opcional) -->
        <div 
            v-if="showProgress" 
            class="flex items-center space-x-1 text-xs text-gray-500"
        >
            <span>{{ rankIndex + 1 }}/{{ totalRanks }}</span>
            <div class="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div 
                    class="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-300"
                    :style="{ width: `${progress}%` }"
                ></div>
            </div>
        </div>
    </div>
</template>

<script>
import { getRangoIndex, RANGOS } from '../services/profiles.js';

export default {
    name: 'RankBadge',
    props: {
        /**
         * Rango del usuario
         */
        rango: {
            type: String,
            required: true,
            validator: (value) => RANGOS.includes(value)
        },
        /**
         * Si el usuario tiene suscripción PRO
         */
        isPro: {
            type: Boolean,
            default: false
        },
        /**
         * Mostrar barra de progreso del rango
         */
        showProgress: {
            type: Boolean,
            default: false
        },
        /**
         * Tamaño del badge
         */
        size: {
            type: String,
            default: 'normal',
            validator: (value) => ['small', 'normal', 'large'].includes(value)
        }
    },
    computed: {
        /**
         * Índice numérico del rango (0-9)
         */
        rankIndex() {
            return getRangoIndex(this.rango);
        },
        
        /**
         * Número total de rangos
         */
        totalRanks() {
            return RANGOS.length;
        },
        
        /**
         * Porcentaje de progreso del rango
         */
        progress() {
            return ((this.rankIndex + 1) / this.totalRanks) * 100;
        },
        
        /**
         * Icono asociado al rango
         */
        rankIcon() {
            const icons = {
                'Novato': '🥋',
                'Aprendiz': '🎯',
                'Luchador': '👊',
                'Guerrero': '⚔️',
                'Veterano': '🛡️',
                'Experto': '🏆',
                'Maestro': '👑',
                'Leyenda': '⭐',
                'Campeón': '🥇',
                'Hall of Fame': '💎'
            };
            return icons[this.rango] || '🥋';
        },
        
        /**
         * Clases CSS para colorear el badge según el rango
         */
        rankColorClass() {
            const colorClasses = {
                'Novato': 'bg-gray-100 text-gray-800',
                'Aprendiz': 'bg-green-100 text-green-800',
                'Luchador': 'bg-blue-100 text-blue-800',
                'Guerrero': 'bg-purple-100 text-purple-800',
                'Veterano': 'bg-indigo-100 text-indigo-800',
                'Experto': 'bg-yellow-100 text-yellow-800',
                'Maestro': 'bg-orange-100 text-orange-800',
                'Leyenda': 'bg-red-100 text-red-800',
                'Campeón': 'bg-pink-100 text-pink-800',
                'Hall of Fame': 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
            };
            return colorClasses[this.rango] || 'bg-gray-100 text-gray-800';
        },
        
        /**
         * Clases para el icono
         */
        iconClass() {
            return this.rango === 'Hall of Fame' ? 'text-yellow-200' : '';
        }
    }
};
</script>