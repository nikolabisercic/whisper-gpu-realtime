import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 6542,
    host: true,
    proxy: {
      '/ws': {
        target: 'ws://localhost:6541',
        ws: true,
      }
    }
  }
})