// ===============================|| Ui Buttons ||=============================== //
<template>
  <v-row>
    <v-col cols="12">
      <v-row>
        <!-- Base Buttons -->
        <v-col cols="12" sm="12">
          <UiChildCard title="Default">
            <div class="d-flex gap-3 align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height d-flex justify-space-between">
              <v-btn>elevates (default)</v-btn>
              <v-btn variant="flat" color="primary">flat</v-btn>
              <v-btn variant="tonal" color="primary">tonal</v-btn>
              <v-btn variant="outlined" color="primary">outlined</v-btn>
              <v-btn variant="text" color="primary">text</v-btn>
              <v-btn variant="plain" color="primary">plain</v-btn>
            </div>
          </UiChildCard>
        </v-col>

        <!-- Color Buttons -->
        <v-col cols="12" lg="6">
          <UiChildCard title="Colors">
            <div class="d-flex gap-3 align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height">
              <v-btn v-for="btn in btnsColor" :key="btn" :color="btn" variant="flat">
                {{ btn }}
              </v-btn>
            </div>
          </UiChildCard>
        </v-col>

        <!-- Outlined Buttons -->
        <v-col cols="12" lg="6">
          <UiChildCard title="Outlined">
            <div class="d-flex gap-3 justify-center align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height">
              <v-btn color="primary" variant="outlined">primary</v-btn>
              <v-btn color="secondary" variant="outlined">secondary</v-btn>
              <v-btn variant="flat" disabled> Disabled </v-btn>
              <v-btn color="info" variant="outlined">link</v-btn>
            </div>
          </UiChildCard>
        </v-col>

        <!-- Sizes -->
        <v-col cols="12" lg="12">
          <UiChildCard title="Size">
            <div class="d-flex gap-2 justify-space-around align-center flex-column flex-md-row fill-height">
              <v-btn size="x-small" color="primary" flat> Extra small </v-btn>
              <v-btn size="small" color="primary" flat> Small </v-btn>
              <v-btn color="primary" flat> Normal </v-btn>
              <v-btn color="primary" size="large" flat> Large </v-btn>
              <v-btn size="x-large" color="primary" flat> Extra large </v-btn>
            </div>
          </UiChildCard>
        </v-col>

        <!-- Text Buttons -->
        <v-col cols="12" lg="6">
          <UiChildCard title="Text Color">
            <div class="d-flex flex-wrap gap-3 my-2 align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height">
              <v-btn v-for="btn in btnsColor" :key="btn" :color="btn" variant="text">
                {{ btn }}
              </v-btn>
            </div>
          </UiChildCard>
        </v-col>

        <!-- Icon Color Sizes -->
        <v-col cols="12" lg="6">
          <UiChildCard title="Icon Size">
            <div class="d-flex flex-wrap justify-center gap-3 align-center flex-column flex-sm-row fill-height">
              <v-btn color="primary" icon size="x-small" flat><BellIcon stroke-width="1.5" /></v-btn>
              <v-btn color="secondary" icon size="small" flat><BellIcon stroke-width="1.5" /></v-btn>
              <v-btn color="success" icon flat><BellIcon stroke-width="1.5" /></v-btn>
              <v-btn color="error" icon size="large" flat><BellIcon stroke-width="1.5" /></v-btn>
              <v-btn color="warning" icon size="x-large" flat><BellIcon stroke-width="1.5" /></v-btn>
            </div>
          </UiChildCard>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref } from 'vue';
/*import tabler icons*/
import { TrashIcon, SendIcon, BellIcon } from 'vue-tabler-icons';
import UiChildCard from '@/components/shared/UiChildCard.vue';
// icons
import { AccessPointIcon } from 'vue-tabler-icons';
// import BaseButtons from '@/components/ui-components/button/BaseButtons.vue';
// import ColorsButtons from '@/components/ui-components/button/ColorsButtons.vue';
// import OutlinedButtons from '@/components/ui-components/button/OutlinedButtons.vue';
// import SizeButtons from '@/components/ui-components/button/SizeButtons.vue';
// import TextButtons from '@/components/ui-components/button/TextButtons.vue';
// import IconColorSizes from '@/components/ui-components/button/IconColorSizes.vue';
// buttons color data
const btnsColor = ref(['primary', 'secondary', 'success', 'error', 'warning']);
</script>
