// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  srcDir: 'src',
  buildDir: 'build',
  app: {
    head: {
      charset: 'utf-8',
    },
    layoutTransition: { name: 'layout', mode: 'out-in' },
  },
  nitro: {
    devProxy: {
      '/api': {
        target: 'https://blogapi.shinestar.fun/api',
        changeOrigin: true,
        prependPath: true,
      },
    },
    routeRules: {
      '/api/**': {
        cors: true,
        proxy: 'https://blogapi.shinestar.fun/api/**',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        },
      },
    },
  },
})
