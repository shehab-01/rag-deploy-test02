<template>
  <v-row>
    <v-col cols="12">
      <v-row>
        <!-- Basic -->
        <v-col cols="12">
          <UiChildCard title="Alert Basic">
            <div>
              <v-alert class="mb-3" color="error" variant="tonal">This is an error alert — check it out!</v-alert>
              <v-alert class="mb-3" color="warning" variant="tonal">This is a warning alert — check it out!</v-alert>
              <v-alert class="mb-3" color="info" variant="tonal">This is an info alert — check it out!</v-alert>
              <v-alert color="success" variant="tonal">This is a success alert — check it out!</v-alert>
            </div>
          </UiChildCard>
        </v-col>
        <!-- Filled -->
        <v-col cols="12">
          <UiChildCard title="Alert Filled">
            <div>
              <v-alert class="mb-3" type="error">This is an error alert — check it out!</v-alert>
              <v-alert class="mb-3" type="warning">This is a warning alert — check it out!</v-alert>
              <v-alert class="mb-3" type="info">This is an info alert — check it out!</v-alert>
              <v-alert type="success">This is a success alert — check it out!</v-alert>
            </div>
          </UiChildCard>
        </v-col>
        <!-- Closable -->
        <v-col cols="12">
          <UiChildCard title="Alert Closable">
            <div>
              <v-alert v-model="alert" border="start" variant="tonal" closable close-label="Close Alert" color="primary" title="Closable Alert">
                Aenean imperdiet. Quisque id odio. Cras dapibus. Pellentesque ut neque. Cras dapibus. Vivamus consectetuer hendrerit lacus. Sed
                mollis, eros et ultrices tempus, mauris ipsum aliquam libero, non
              </v-alert>
              <div v-if="!alert">
                <v-btn color="primary" @click="alert = true" flat> Reset </v-btn>
              </div>
            </div>
          </UiChildCard>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UiChildCard from '@/components/shared/UiChildCard.vue';

const alert = ref(true);
</script>
