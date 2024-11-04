<template>
  <div class="">
    <div class="d-flex my-2">
      <v-btn @click="grid1.search()" variant="outlined">Search</v-btn>
    </div>
    <div>
      <grid :options="grid1" />
    </div>
  </div>
  <div class="">
    <div class="d-flex my-2">
      <v-btn @click="grid2.search()" variant="outlined">Search</v-btn>
    </div>
    <div>
      <grid :options="grid2" />
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
  height: 231,
  search() {
    grid1.data = Handsontable.helper.createSpreadsheetData(10, 26);
  }
});

const grid2 = reactive({
  data: [],
  height: 231,
  search() {
    grid2.data = Handsontable.helper.createSpreadsheetData(50, 26);
  }
});
</script>
