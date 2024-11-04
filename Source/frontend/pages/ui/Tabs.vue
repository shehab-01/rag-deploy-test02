<template>
  <v-row>
    <v-col cols="12" md="12">
      <v-card>
        <v-tabs v-model="tab" bg-color="primary">
          <v-tab value="one">Tab1</v-tab>
          <v-tab value="two">Tab2</v-tab>
          <v-tab value="three">Tab3</v-tab>
        </v-tabs>
        <v-card-text>
          <v-tabs-window v-model="tab">
            <v-tabs-window-item value="one">Tab1 Contents..</v-tabs-window-item>
            <v-tabs-window-item value="two">Tab2 Contents..</v-tabs-window-item>
            <v-tabs-window-item value="three">Tab3 Contents..</v-tabs-window-item>
          </v-tabs-window>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
const tab = ref('');
</script>
