<template>
  <section class="container flex-column-center">
    <header class="main-header-section flex-row-center">
      <h2 class="main-header flex-row-center">{{ cardTitle }}</h2>
      <p class="main-describe ml-4 text-15">{{ cardDescription }}</p>
    </header>
    <div class="main-content">
      <slot name="content"></slot>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps({
  cardTitle: String,
  cardDescription: String
});
</script>
<style scoped>
.main-header-section {
  width: 90%;
  height: 4rem;
}

.main-header {
  background-color: #598958;
  color: white;
  height: 100%;
  flex: 1 1 0;
}
.main-describe {
  color: #929292;
  height: 100%;
  flex: 5 1 0;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.main-content {
  width: 90%;
  min-height: 20rem;
  height: auto;
  border: 1px solid #929292;
}
</style>
