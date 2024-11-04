<template>
  <!-- Loading -->
  <div class="loading" v-if="isLoading">
    <div class="loader"></div>
  </div>
</template>

<script setup lang="ts">
const isLoading = computed(() => {
  return store.page().isLoading;
});
</script>

<style scoped></style>
