<template>
  <v-row>
    <v-col cols="12" md="12">
      <UiParentCard title="Basic Shadow">
        <v-row justify="center" class="mb-5 mt-1 px-8 px-3">
          <v-col v-for="(m, n) in 25" :key="n" cols="6" sm="auto">
            <v-card height="100" width="100" class="mb-5" :class="['d-flex justify-center align-center bg-primary flex-column', `elevation-${n}`]">
              <h6 class="text-h6">elevation</h6>
              <div>{{ n }}</div>
            </v-card>
          </v-col>
        </v-row>
      </UiParentCard>
    </v-col>

    <v-col cols="12" md="12">
      <UiParentCard title="Color Shadow">
        <v-row>
          <v-col cols="6" lg="2" md="3" sm="4" v-for="color in colorShadow" :key="color">
            <v-card :class="`${color}-shadow bg-${color} px-4 py-6 text-center`">
              {{ color }}
            </v-card>
          </v-col>
        </v-row>
      </UiParentCard>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import UiParentCard from '@/components/shared/UiParentCard.vue';
const colorShadow = ref(['primary', 'secondary', 'info', 'success', 'warning', 'error', 'primary']);
</script>
