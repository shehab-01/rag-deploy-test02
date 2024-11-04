<template>
  <v-row>
    <v-col cols="6">
      <UiChildCard title="File Upload">
        <v-btn color="primary" prepend-icon="mdi-file-upload" @click="(data.file = null), fileInput.click()">
          <span>파일업로드</span>
        </v-btn>
        <v-file-input
          v-show="false"
          label="File.."
          ref="fileInput"
          accept=".xls, .xlsx"
          prepend-icon="mdi-file"
          v-model="data.file"
          @change="page.uploadFile($event)"
        ></v-file-input>
      </UiChildCard>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UiChildCard from '@/components/shared/UiChildCard.vue';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const fileInput = ref<HTMLInputElement>();
const data = reactive({
  file: null
});

const page = {
  init() {},
  uploadFile(e: Event) {
    if (data.file) {
      console.log('file:', data.file);
    }
  }
};
</script>
