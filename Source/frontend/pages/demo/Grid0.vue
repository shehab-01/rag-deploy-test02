<template>
  <hot-table :settings="settings" :data="hotData" :rowHeaders="true"></hot-table>
</template>

<script setup>
import { HotTable, HotColumn } from '@handsontable/vue3';
import { registerAllModules } from 'handsontable/registry';
import 'handsontable/dist/handsontable.full.css';

const settings = reactive({
  licenseKey: 'non-commercial-and-evaluation',
  width: '100%',
  height: 'auto',
  colWidths: [200, 100, 100], //처음 3개의 열 길이만 이렇게 설정
  colHeaders: true,
  rowHeaders: true,
  contextMenu: true,
  dropdownMenu: true, //드롭다운 메뉴
  filters: true, //필터 메뉴
  // hiddenColumns: {
  //   columns: [2, 4, 6],
  //   indicators: true
  // },
  // hiddenRows: {
  //   rows: [1, 2, 3]
  // },
  autoWrapRow: true,
  autoWrapCol: true,
  fixedColumnsStart: 1,
  columnSorting: true, // 열 정렬
  manualColumnMove: true, //열이동
  manualRowMove: true, //행이동
  manualColumnResize: true
});

const hotData = reactive([
  ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1'],
  ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2'],
  ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3'],
  ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4', 'K4', 'L4'],
  ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5']
]);
</script>
