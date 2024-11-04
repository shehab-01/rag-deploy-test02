<template>
  <v-row>
    <v-col cols="12" md="12">
      <UiParentCard title="Sample Page">
        <div class="pa-1"><p class="text-body-1">This is a sample page</p></div>
      </UiParentCard>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import UiParentCard from '@/components/shared/UiParentCard.vue';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  search: {}
});

const page = {
  header: { title: '샘플페이지' },
  init() {},
  search() {}
};
</script>

<style scoped></style>
