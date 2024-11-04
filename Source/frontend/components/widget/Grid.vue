<template>
  <div>
    <hot-table ref="grid" :settings="settings" :rowHeaders="true"></hot-table>
    <div class="no-data flex-column-center" :id="options.guid" v-if="options.data.length == 0">
      <h2>검색 결과가 없습니다.</h2>
      <ul>
        <li v-for="(message, index) in options.noDataMessages" :key="index">{{ message }}</li>
      </ul>
    </div>
    <div class="" v-if="options.pagination && totalPages > 0">
      <v-pagination v-model="pagination.page" :length="totalPages" :total-visible="5" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Handsontable from 'handsontable';
// import Handsontable from 'handsontable/base';
import { HotTable, HotColumn } from '@handsontable/vue3';
// import type { GridSettings } from 'handsontable/settings';
import type { GridDefSettings } from '@/types/comm/grid';
import { registerAllModules } from 'handsontable/registry';
import { registerPlugin, UndoRedo } from 'handsontable/plugins';
import { registerCellType, NumericCellType } from 'handsontable/cellTypes';
import { registerLanguageDictionary, koKR } from 'handsontable/i18n';
import 'handsontable/dist/handsontable.full.css';

// @Handsontable Register
// registerPlugin(UndoRedo);
// registerCellType(NumericCellType);
registerLanguageDictionary(koKR);

const props = defineProps({
  data: {
    Type: Array,
    required: false,
    default: []
  },
  options: {
    Type: Object,
    required: true,
    default: null
  }
});

const pagination = reactive({
  data: [],
  page: 1,
  pageSize: 10
});

let grid = ref();
let options: { inst: object; guid: string; data: []; pagination?: false; noDataMessages?: [] } = props.options;
// let settings: GridSettings = Handsontable.DefaultSettings;
let settings: GridDefSettings = Handsontable.DefaultSettings;

// 데이터 업데이트
const bakHeight = 0;
const updateData = () => {
  const hotInstance = grid.value.hotInstance;
  const hotSettings = hotInstance.getSettings();

  if (options.pagination) {
    hotInstance.updateData(paginatedItems.value);
  } else {
    hotInstance.updateData(options.data);
  }

  if (options.data.length == 0) {
    noData();
  } else {
    hotInstance.updateSettings({
      height: hotSettings.backHeight
    });
  }
};

// 데이터 없는경우
const noData = () => {
  const hotInstance = grid.value.hotInstance;
  const hotSettings = hotInstance.getSettings();
  hotInstance.updateSettings({
    height: 25 + 2
  });

  setTimeout(() => {
    let noDataMessage = document.getElementById(hotInstance.guid);
    noDataMessage.style.height = hotSettings.backHeight - 25 + 'px';
  }, 0);
};

// 변경값 감시: 데이터
watch(
  () => props.options.data,
  (newVal, oldVal) => {
    // console.log('watch.data:', toRaw(newVal), oldVal);

    // 데이터 로드
    // const hotInstance = grid.value.hotInstance;
    // grid.value.hotInstance.loadData(newVal);
    // grid.value.hotInstance.render();

    // 데이터 업데이트
    // grid.value.hotInstance.updateData(newVal);

    // 데이터 업데이트
    if (options.pagination) {
      pagination.page = 1;
      pagination.data = options.data;
    }
    updateData();
  }
);

// 변경값 감시: 페이징
watch(
  () => pagination.page,
  () => {
    // console.log('watch.page:', pagination.page);
    updateData();
  }
);

// 페이징 계산
const totalPages = computed(() => {
  return Math.ceil(pagination.data.length / pagination.pageSize);
});
const paginatedItems = computed(() => {
  const start = (pagination.page - 1) * pagination.pageSize;
  const end = start + pagination.pageSize;
  return pagination.data.slice(start, end);
});

onBeforeMount(() => {
  // console.log('onBeforeMount..');

  // 기본설정
  settings = useMerge(
    {
      licenseKey: 'non-commercial-and-evaluation',
      language: koKR.languageCode,
      width: '100%',
      height: 'auto',
      minRows: 0,
      minCols: 0,
      minSpareRows: 0,
      removeRowPlugin: true,
      undo: true,
      // editor: false,
      readOnly: false,
      wordWrap: true,
      copyable: true,
      copyPaste: true,
      colHeaders: true,
      rowHeaders: false, //버그?:적용안됨..
      // rowHeaderWidth: 0,
      autoColumnSize: true,
      mergeCells: true,
      filters: true,
      dragToScroll: true,
      dropdownMenu: true,
      contextMenu: true,
      comments: false, //contextmenu(댓글기능)
      allowRemoveRow: false, //contextmenu(행삭제)
      allowRemoveColumn: false, //contextmenu(열삭제)
      allowInsertRow: false, //contextmenu(행삽입)
      allowInsertColumn: false, //contextmenu(열삽입)
      manualColumnFreeze: true, //contextmenu(열고정)
      autoWrapRow: true, //마지막 셀 옆에서 다음 셀 처음으로 이동
      autoWrapCol: true, //마지막 셀 아래에서 다음 셀 위로 이동
      fixedColumnsStart: 0,
      columnSorting: true, //열정렬
      manualRowMove: true, //행이동
      manualColumnMove: true, //열이동
      manualRowResize: true, //행조절
      manualColumnResize: true, //열조절
      trimWhitespace: true, //trim후 셀저장
      observeChanges: true, //셀변경 감시
      enterBeginsEditing: true, //엔터시 편집모드 또는 셀이동
      outsideClickDeselects: false, //셀 외부 클릭시 셀선택 해제
      // fixedRowsTop: 1,
      persistentState: false, //열 정렬,위치,크기 등 상태를 로컬스토리지에 저장
      // rowHeights: 30,
      stretchH: 'all',
      // className
      // - Horizontal(htLeft, htCenter, htRight, htJustify)
      // - Vertical(htTop, htMiddle, htBottom)
      className: 'htCenter htMiddle',
      // 추가설정
      // page: 1,
      // pagination: true,
      bakHeight: 'auto',
      init: function () {
        // console.log('grid.init..')
      },
      afterInit: function () {
        // console.log('grid.afterInit..');
      },
      test: function () {
        console.log('test..');
      },
      afterGetRowHeader(row: number, th: any) {
        th.classList.add('htCenter', 'htMiddle');
      }
    },
    options
  );
  // console.log('settings:', settings);
});

onMounted(() => {
  // console.log('onMounted..');

  const hotInstance = grid.value.hotInstance;
  // hotInstance.updateData(paginatedItems.value);
  options.inst = hotInstance;
  options.guid = hotInstance.guid;

  const hotSettings = hotInstance.getSettings();
  if (!hotSettings.backHeight) {
    hotSettings.backHeight = hotSettings.height;
  }

  // 데이터 업데이트
  if (options.pagination) {
    pagination.page = 1;
    pagination.data = options.data;
  }
  updateData();

  // Hook:
  /*
  hotInstance.addHook('', function () {
  });
  hotInstance.addHook('afterChange', function (changes: Array<[]>, source: string) {
    // TODO:
    if (source == 'loadData') {
    } else if (source == 'updateData') {
    }
  });*/
});

const inst = () => {
  return grid.value.hotInstance;
};

defineExpose({
  grid
});
</script>

<style scoped>
.no-data {
  gap: 10px;
  width: 100%;
  padding: 10px;
  color: #555;
  border: 1px solid #f0f0f0;
  /* background: lightgoldenrodyellow; */
  /* height: 300px; */

  ul {
    text-align: left;
    display: inline-block;
  }
}
.show {
  visibility: visible;
}
.hide {
  visibility: hidden;
}
</style>
