<template>
  <div class="">
    <div class="d-flex my-2">
      <v-btn @click="grid1.search()" variant="outlined">Search</v-btn>
    </div>
    <div>
      <grid :options="grid1" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Handsontable from 'handsontable';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  search: {}
});

const page = {
  init() {}
};

const grid1 = reactive({
  data: [],
  editor: true,
  pagination: true,
  columns: [
      { title: 'albumId', data: 'albumId' },
      { title: 'id', data: 'id' },
      { title: 'title', data: 'title' },
      { title: 'url', data: 'url' },
      { title: 'thumbnailUrl', data: 'thumbnailUrl' },
    ], // prettier-ignore
  hiddenColumns: {
    columns: []
  },
  afterInit() {
    grid1.search();
  },
  afterSelection(row: number, col: number) {},
  search() {
    useApi()
      .request({
        method: 'get',
        url: 'https://jsonplaceholder.typicode.com/photos',
        data: data.search
      })
      .then((result: any) => {
        grid1.data = result;
      });
  }
});
</script>
