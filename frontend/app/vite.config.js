import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // ensures relative paths, important for Nginx
  base: './',
  build: {
    // explicitly state the output directory
    outDir: 'dist',
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5001',
    }
  }
})
