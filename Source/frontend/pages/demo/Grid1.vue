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

<script setup>
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
  // width: 800,
  // height: 275,
  colHeaders: true,
  rowHeaders: true,
  afterInit() {
    console.log('grdi1.afterInit..');
    grid1.search();
  },
  search() {
    console.log('search.this:', this);
    grid1.data = Handsontable.helper.createSpreadsheetData(10, 26);
  }
});
</script>
