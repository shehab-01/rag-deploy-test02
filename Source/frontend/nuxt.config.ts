// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  routeRules: {},

  typescript: {
    shim: false,
    strict: true,
    typeCheck: false
  },
  build: {
    transpile: ['vuetify', 'vuelidate']
  },
  vite: {
    define: {
      'process.env.DEBUG': false
    },
    server: {
      hmr: {
        clientPort: Number(process.env.PORT),
        host: '0.0.0.0', // Add this to allow external connections
        port: 9000, // Add this to match your port
        protocol: 'ws' // Add this for WebSocket
      },
      watch: {
        usePolling: true // Add this for better file watching
      }
    }
  },
  nitro: {
    serveStatic: true,
    // Add devProxy configuration for API
    devProxy: {
      '/api': {
        target: 'http://localhost:9090', // Your FastAPI backend
        changeOrigin: true,
        ws: true
      }
    }
  },
  modules: ['@pinia/nuxt', '@pinia-plugin-persistedstate/nuxt', 'nuxt-lodash', 'dayjs-nuxt'],
  imports: {
    autoImport: true,
    dirs: ['store', 'utils', 'types/api']
  },
  components: {
    dirs: [
      {
        path: 'components/widget',
        pathPrefix: false
      },
      {
        path: 'components',
        pathPrefix: true
      }
    ]
  },
  piniaPersistedstate: {
    storage: 'localStorage'
  },
  dayjs: {
    locales: ['ko'],
    defaultLocale: 'ko',
    defaultTimezone: 'Asia/Seoul',
    plugins: ['timezone', 'relativeTime']
  },
  hooks: {},
  devtools: {
    enabled: false
  },
  runtimeConfig: {
    public: {
      basePath: process.env.NUXT_BASE_PATH,
      apiServiceKey: process.env.NUXT_API_SERVICE_KEY,
      // Add API base URL configuration
      apiBase: process.env.NODE_ENV === 'production' ? 'http://your-production-domain:9090' : 'http://localhost:9090'
    }
  }
});
