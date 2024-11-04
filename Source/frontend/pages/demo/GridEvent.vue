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

const grid1 = reactive({
  data: [],
  width: '100%',
  height: 'auto',
  colHeaders: true,
  rowHeaders: false,
  afterInit() {
    grid1.search();
  },
  afterSelection(row, column) {
    // console.log('afterSelection:', row, column);
    console.log('afterSelection:');

    let selectedCell = this.getDataAtCell(row, column);
    let selectedCol = this.getDataAtCol(column);
    let selectedRow = this.getDataAtRow(row);
    // let selectedRow = this.getSourceDataAtRow(row);
    console.log(`selected cell [${row}][${column}] with value [${selectedCell}]`);
    console.log(`column values: ${JSON.stringify(selectedCol)}`);
    console.log(`row values: ${JSON.stringify(selectedRow)}`);
  },
  search() {
    grid1.data = Handsontable.helper.createSpreadsheetData(20, 26);
  }
});
</script>
