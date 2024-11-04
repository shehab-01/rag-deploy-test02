<template>
  <NuxtLoadingIndicator />
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <Loading />
  <ModalMessage :option="{}" />
</template>

<script setup lang="ts">
onMounted(() => {
  max.ui.loading(false);
  console.info('App.meta.env:', import.meta.env);
  console.info('App.process.env:', process.env);
});
</script>
