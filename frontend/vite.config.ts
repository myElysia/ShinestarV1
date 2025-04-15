import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "./",
  server: {
    host: "0.0.0.0",
    port: 3000,
    open: true,
  },
  // 配置别名，引用 src 可以通过 import layout from '@/layout/index.vue'
  resolve: {
    alias: [
      {
        find: "@",
        replacement: resolve(__dirname, 'src')
      }
    ]
  }
})
