<template>
  <v-row>
    <!-- Side -->
    <v-col cols="3">
      <v-card elevation="10" class="withbg" height="75vh">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <h5 class="text-h5 mb-6 pl-7 pt-7">문서 현황</h5>
            <v-btn class="mr-4" icon size="x-small" flat @click="data.dialog4 = true"><UploadIcon stroke-width="1.5" /></v-btn>
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <v-divider />
        <v-card-text style="padding-left: 0; padding-right: 0">
          <draggable-tree-view v-model:active="active" :items="items" @update:items="handleTreeUpdate" @click="fileClick.getFileName" />
        </v-card-text>
      </v-card>
    </v-col>

    <!-- Main Chat -->
    <v-col cols="9" md="9">
      <v-card elevation="10" class="withbg d-flex flex-column" height="75vh">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <h5 class="text-h5 mb-6 pl-7 pt-7">File View</h5>
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <v-divider />

        <v-card-text ref="chatContainer" class="flex-grow-1" style="padding: 0">
          <v-row>
            <v-col>
              <div :style="{ width: '100%', height: '62%' }">
                <PDF :page="1" pdfWidth="85%" :src="pdfFile" />
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-dialog v-model="data.dialog4" max-width="500">
    <template v-slot:default="{ isActive }">
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">File Upload</div>
          <v-btn icon="mdi-close" variant="text" @click="isActive.value = false"></v-btn>
        </v-card-title>
        <v-divider class="mb-4"></v-divider>
        <v-card-text>
          <div class="text-medium-emphasis mb-4">Upload a PDF file to your document repository.</div>
          <v-file-input
            v-model="fileInput"
            label="Choose PDF file"
            accept="application/pdf,.pdf"
            prepend-icon="mdi-file-pdf-box"
            @update:model-value="onFileChange"
            :error-messages="fileError"
          ></v-file-input>
          <v-text-field v-model="directoryPath" label="Directory Path" placeholder="e.g., documents/manuals"></v-text-field>
          <v-select v-model="docLanguage" :items="['en', 'ko', 'ja']" label="Document Language"></v-select>
        </v-card-text>
        <v-divider class="mt-2"></v-divider>
        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn class="text-none" rounded="xl" text="Cancel" @click="isActive.value = false"></v-btn>
          <v-btn class="text-none" rounded="xl" text="Upload" color="primary" @click="uploadFile" :loading="uploading"></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue';
import { useTheme } from 'vuetify';
import { UploadIcon } from 'vue-tabler-icons';
import { VTreeview } from 'vuetify/labs/VTreeview';
import PDF from 'pdf-vue3';
import pdfFile from '@/assets/pdfs/사용자매뉴얼.pdf';
import { title } from 'process';
import { idText } from 'typescript';
import DraggableTreeView from '../shared/DraggableTreeView.vue';

import axios from 'axios';

const theme = useTheme();
const chatContainer = ref(null);
const active = ref([]);

const fileInput = ref(null);
const directoryPath = ref('');
const docLanguage = ref('en');
const uploading = ref(false);
const fileError = ref('');
const data = reactive({
  dialog4: false
});

// treeView items
const items = ref([
  {
    id: 1,
    title: 'root',
    children: [
      {
        id: 2,
        title: '사용매뉴얼',
        children: [
          {
            id: 21,
            title: '9241837_CHPI_CPI_7400N_사용설명서_내수용_003_23_05_04.pdf'
          }
        ]
      },
      {
        id: 3,
        title: '고객상담',
        children: [
          {
            id: 31,
            title: '대외문서',
            children: [
              {
                id: 311,
                title: 'number02.pdf'
              }
            ]
          },
          {
            id: 32,
            title: '고객센터 교육자료',
            children: []
          },
          {
            id: 33,
            title: '상담스크립트',
            children: []
          }
        ]
      },
      {
        id: 4,
        title: 'FAQ',
        children: []
      }
    ]
  }
]);

const handleTreeUpdate = (newItems: any) => {
  items.value = newItems;
  // Here you can also make an API call to update the backend if needed
};

// treeView item click 했을때
const fileClick = {
  getFileName(event: any) {
    // console.log(event.target.innerText);
    console.log(event.target);
    // fileClick.getFileContent(event.target.innerText);
  },

  // Db에서 pdf 가지고오는 api
  getFileContent(filename: string) {
    useApi()
      .request({
        method: 'post',
        url: '/api/demo/get-file-content',
        data: { filename: filename },
        responseType: 'arraybuffer'
      })
      .then((result: any) => {
        console.log(result);
        // pdfUrl.value = createPdfDataUrl(result);
      });
  }
};

const handleError = (error: any) => {
  console.error('Error loading PDF:', error);
};

const selected = computed(() => {
  if (!active.value.length) return undefined;

  const id = active.value[0];
  return findItemById(items.value[0], id);
});

function findItemById(item: any, id: number | string): any {
  if (item.id === id) return item;
  if (item.children) {
    for (let child of item.children) {
      const found = findItemById(child, id);
      if (found) return found;
    }
  }
  return undefined;
}

const test = {
  search(event: any) {
    console.log(event);
  }
};

// file upload
const onFileChange = (file: any) => {
  fileError.value = '';
  if (file) {
    if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
      console.log('Valid PDF file selected:', file.name);
    } else {
      fileError.value = 'Please select a PDF file';
      fileInput.value = null;
    }
  }
};

const uploadFile = async () => {
  if (!fileInput.value) {
    fileError.value = 'Please select a file';
    return;
  }

  uploading.value = true;
  const formData = new FormData();
  formData.append('file', fileInput.value);
  formData.append('directory_path', directoryPath.value);
  formData.append('docLanguage', docLanguage.value);

  try {
    const result = await useApi().request({
      method: 'post',
      url: '/api/demo/upload-embed',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log('Upload result:', result);
    alert(`File '${fileInput.value.name}' uploaded successfully.`);
    data.dialog4 = false;
  } catch (error) {
    console.error('Error uploading file:', error);
    alert('Error uploading file');
  } finally {
    uploading.value = false;
  }
};
</script>

<style scoped></style>
