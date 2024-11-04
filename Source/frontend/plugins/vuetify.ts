// import Vue from 'vue';
import { createVuetify } from 'vuetify';
import '@mdi/font/css/materialdesignicons.css';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import VueApexCharts from 'vue3-apexcharts';
import VueTablerIcons from 'vue-tabler-icons';
import PerfectScrollbar from 'vue3-perfect-scrollbar';

import '@/assets/scss/style.scss';
import { PurpleTheme, BlueTheme } from './theme/LightTheme';

export default defineNuxtPlugin(nuxtApp => {
  const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: 'PurpleTheme',
      themes: {
        PurpleTheme
      }
    },
    defaults: {
      VBtn: {
        size: 'small',
        variant: 'flat'
      },
      VCol: {},
      VGrid: {
        padding: '100px'
      },
      VSelect: {
        hideDetails: 'auto'
      },
      VRadioGroup: {
        hideDetails: 'auto'
      },
      VCheckbox: {
        hideDetails: 'auto'
      },
      VTextField: {
        clearable: true,
        hideDetails: 'auto',
        variant: 'outlined'
      },
      VCardActions: {
        VBtn: {
          color: 'dark',
          variant: 'flat'
        }
      }
    }
  });
  nuxtApp.vueApp.use(vuetify);
  nuxtApp.vueApp.use(PerfectScrollbar);
  nuxtApp.vueApp.use(VueApexCharts);
  nuxtApp.vueApp.use(VueTablerIcons);
});
