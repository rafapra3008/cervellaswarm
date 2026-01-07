import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// CervellaSwarm Dashboard - Vite Config
// PORTA 8100 = CervellaSwarm (dedicata!)
// PORTA 8000 = Contabilita' (NON usare!)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API calls to FastAPI backend - PORTA 8100!
      '/api': {
        target: 'http://localhost:8100',
        changeOrigin: true,
      },
    },
  },
})
