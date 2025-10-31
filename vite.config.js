// Este es el archivo de configuración de Vite.
// Como todo archivo de configuración (los que terminan en ".config.js") debe
// exportar un objeto de configuración.

// Importamos el plugin de Vue para Vite, y lo agregamos al objeto de configuración.
import vue from '@vitejs/plugin-vue';

import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  plugins: [
    tailwindcss(), vue()
  ],
})

