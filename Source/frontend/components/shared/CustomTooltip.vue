<template>
  <div class="custom-tooltip-container">
    <div @click="isOpen = true">
      <slot></slot>
    </div>

    <Transition name="fade">
      <div v-if="isOpen" class="tooltip-popup">
        <div class="tooltip-header">
          <h3>{{ title }}</h3>
          <button @click="isOpen = false" class="close-button">
            <v-icon icon="mdi-close"></v-icon>
          </button>
        </div>
        <div class="tooltip-content">
          <slot name="content">{{ content }}</slot>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue';

const props = defineProps<{
  title: string;
  content?: string;
}>();

const isOpen = ref(false);
</script>

<style scoped>
.custom-tooltip-container {
  position: relative;
  display: inline-block;
}

.tooltip-popup {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 450px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  z-index: 1000;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
}

.tooltip-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: #6b7280;
}

.close-button:hover {
  color: #374151;
}

.tooltip-content {
  padding: 16px;
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
