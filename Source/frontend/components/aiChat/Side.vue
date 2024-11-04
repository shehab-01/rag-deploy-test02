<template>
  <v-row>
    <v-col cols="12" md="12">
      <v-card variant="outlined" elevation="10" class="withbg">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <!-- <v-card-title class="text-h6" style="line-height: 1.57">{{ props.title }}</v-card-title> -->
            <h5 class="text-h5 mb-6 pl-7 pt-7">채팅 리스트</h5>
            <v-btn class="mr-4" icon size="x-small" flat><SettingsIcon stroke-width="1.5" /></v-btn>

            <!-- <template v-slot:append> -->
            <slot name="action"></slot>
            <!-- </template> -->
          </div>
        </v-card-item>
        <v-divider />
        <v-card-text>
          <v-row style="height: 70vh"> data... </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { computed } from 'vue';
import { useTheme } from 'vuetify';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import { test } from 'process';

const theme = useTheme();
const primary = theme.current.value.colors.primary;
const secondary = theme.current.value.colors.secondary;
const colorShadow = ref(['primary', 'secondary', 'info', 'success', 'warning', 'error']);

const page = {
  test() {
    console.log('tes');
  }
};
</script>
