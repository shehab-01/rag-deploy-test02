<template>
  <div class="flex-column-center">
    <header class="header">
      <div class="header-content">
        <h1>{{ title }}</h1>
        <p>{{ subtitle }}</p>
      </div>
      <div class="description">
        <p>{{ pageDescription }}</p>
      </div>
    </header>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    required: true
  },
  pageDescription: {
    type: String,
    required: false
  }
});
</script>

<style scoped>
.header {
  width: 60%;
  height: 8rem;
  /* box-sizing: border-box; */
  /* padding: 1rem 2rem; */
  /* margin-bottom: 1rem; */
}

.header-content {
  width: 100%;
  height: 80%;
  background-color: #598958;
  color: #fff;
  padding: 0 2rem;
  display: grid;
  grid-template-columns: 2fr 7fr;
  align-items: center;
  gap: 1rem;
  /* margin-bottom: 1rem; */
}

h1 {
  font-size: 1.5rem;
  font-weight: bold;
}

p {
  font-size: 1.2rem;
}

.description p {
  width: 100%;
  height: 20%;
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
}
</style>
