// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  // routeRules: {
  //   '/': {},
  //   '/api/**': { ssr: true, cors: true },
  //   '/demo/**': { ssr: true, prerender: true },
  //   '/spa/**': { ssr: false },
  //   '/ssr/**': { ssr: true, prerender: false },
  //   '/ssg/**': { ssr: true, prerender: true },
  //   '/old-path/**': { redirect: '/new-page ' }
  // },
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
        clientPort: Number(process.env.PORT)
      }
    }
  },
  nitro: {
    serveStatic: true
  },
  modules: [
    //
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    'nuxt-lodash',
    'dayjs-nuxt'
  ],
  imports: {
    autoImport: true,
    dirs: [
      'store',
      'utils',
      'types/api'
    ] // prettier-ignore
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
  // devServer: {
  //   port: 3000
  // },
  devServerHandlers: [],
  runtimeConfig: {
    public: {
      basePath: process.env.NUXT_BASE_PATH,
      apiServiceKey: process.env.NUXT_API_SERVICE_KEY
    }
  }
});
