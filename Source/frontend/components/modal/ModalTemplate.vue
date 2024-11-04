<template>
  <v-dialog :max-width="maxWidth" :max-height="maxHeight" v-model="isModalOpen" @update:model-value="closeModal">
    <v-card>
      <v-card-text class="wrapper-modal">
        <v-icon class="modal-icon">{{ icon }}</v-icon>
        <h2 class="modal-title">{{ title }}</h2>
        <p class="modal-description">{{ description }}</p>
        <slot name="content" clsss="justify-center"></slot>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn @click="closeModal" class="cancel-button" v-if="cancelButtonText">{{ cancelButtonText }}</v-btn>
        <v-btn @click="confirmModal" class="confirm-button" v-if="confirmButtonText">{{ confirmButtonText }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import type { ModalProps } from '@/types/modal';

const props = defineProps<ModalProps>();
const emit = defineEmits(['closeModal', 'confirmModal']);
const isModalOpen = ref(props.isModalOpen);

watch(
  () => props.isModalOpen,
  newVal => {
    isModalOpen.value = newVal;
  }
);

const closeModal = (): void => {
  emit('closeModal');
};

const confirmModal = (): void => {
  emit('confirmModal');
};
</script>

<style scoped>
.wrapper-modal {
  text-align: center;
}

.modal-icon {
  color: green;
  font-size: 4rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 1rem;
}

.modal-description {
  font-size: 1rem;
  margin-top: 0.5rem;
}

.v-btn {
  height: 2.5rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.cancel-button {
  background-color: white !important;
  color: black !important;
  border: 1px solid #598958 !important;
}

.confirm-button {
  background-color: #598958 !important;
  color: white !important;
  border: 1px solid #598958 !important;
}
</style>
