<template>
  <v-row>
    <v-col cols="4">
      <v-row>
        <v-col cols="12" class="pa-0">
          <v-text-field
            append-icon="mdi-magnify"
            type="search"
            class=""
            label="코드명.."
            v-model="data.search.cd_nm"
            @keyup.enter="page.search"
            @click:append="page.search"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" class="pa-0">
          <grid :options="grid1" />
        </v-col>
      </v-row>
    </v-col>

    <v-col cols="8">
      <v-row>
        <v-col cols="6" class="d-flex">
          <v-label><v-icon color="red" size="x-small">mdi-asterisk</v-icon> 표기영역은 필수 입력 항목입니다.</v-label>
        </v-col>
        <v-col cols="6" class="d-flex justify-end pr-0">
          <v-btn class="mx-1" color="primary" @click="page.btnAdd"><v-icon>mdi-plus</v-icon> 추가</v-btn>
          <v-btn class="mx-1" color="primary" @click="page.btnDelete"><v-icon>mdi-minus</v-icon> 삭제</v-btn>
          <v-btn class="ml-1" color="primary" @click="page.btnSave"><v-icon>mdi-check</v-icon> 저장</v-btn>
        </v-col>
      </v-row>
      <v-form ref="view1">
        <v-row table>
          <v-col cols="2" head>
            <v-label>코드 <v-icon color="red" size="x-small">mdi-asterisk</v-icon></v-label>
          </v-col>
          <v-col cols="4">
            <v-text-field type="text" v-model="data.view1.cd_id" maxlength="5" disabled></v-text-field>
          </v-col>
          <v-col cols="2" head>
            <v-label>코드명 <v-icon color="red" size="x-small">mdi-asterisk</v-icon></v-label>
          </v-col>
          <v-col cols="4">
            <v-text-field type="text" v-model="data.view1.cd_nm" id="cd_nm"></v-text-field>
          </v-col>
        </v-row>
      </v-form>

      <v-row>
        <v-col cols="12" class="pa-0">
          <grid :options="grid2" />
        </v-col>
      </v-row>

      <!-- 상세코드 -->
      <v-row>
        <v-col cols="12" class="d-flex justify-end pr-0">
          <v-btn class="mx-1" color="secondary" @click="page.btnAdd2"><v-icon>mdi-plus</v-icon> 추가</v-btn>
          <v-btn class="mx-1" color="secondary" @click="page.btnDelete2"><v-icon>mdi-minus</v-icon> 삭제</v-btn>
          <v-btn class="ml-1" color="secondary" @click="page.btnSave2"><v-icon>mdi-check</v-icon> 저장</v-btn>
        </v-col>
      </v-row>
      <v-form ref="view2">
        <v-row table>
          <v-col cols="2" head>
            <v-label>상세코드 <v-icon color="red" size="x-small">mdi-asterisk</v-icon></v-label>
          </v-col>
          <v-col cols="10">
            <v-text-field type="text" v-model="data.view2.cds_id" id="cds_id"></v-text-field>
          </v-col>
          <v-col cols="2" head>
            <v-label>상세코드명 <v-icon color="red" size="x-small">mdi-asterisk</v-icon></v-label>
          </v-col>
          <v-col cols="10">
            <v-text-field type="text" v-model="data.view2.cds_nm"></v-text-field>
          </v-col>
          <v-col cols="2" head>
            <v-label>순서</v-label>
          </v-col>
          <v-col cols="10">
            <v-text-field type="text" v-model="data.view2.ord_seq" maxlength="4"></v-text-field>
          </v-col>
          <v-col cols="2" head>
            <v-label>비고</v-label>
          </v-col>
          <v-col cols="10" class="d-flex border-thin">
            <v-text-field type="text" v-model="data.view2.cds_text"></v-text-field>
          </v-col>
        </v-row>
      </v-form>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import UiChildCard from '@/components/shared/UiChildCard.vue';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  search: {
    cd_nm: null
  },
  view1: {
    cd_id: null,
    cd_nm: null
  },
  view2: {
    cd_id: null,
    cds_id: null,
    cds_nm: null,
    ord_seq: null,
    cds_text: null
  }
});
const view1 = ref();
const view2 = ref();

const page = {
  header: { title: '코드정보' },
  init() {},
  // 초기화
  reset() {},
  // 검색
  search() {
    grid1.search();
  },
  // 버튼: 코드
  btnAdd() {
    view1.value.reset();
    grid2.inst.updateData([]);
    document.getElementById('cd_nm').focus();
  },
  btnDelete() {
    // 유효성체크
    if (!data.view1.cd_id) {
      max.ui.valid('삭제할 코드를 목록에서 선택해주세요.');
      return;
    }

    // 확인창
    max.ui.confirm({
      title: '확인',
      content: '코드: ' + data.view1.cd_nm + ' \n코드를 삭제하면 하위 상세코드도 같이 삭제됩니다. \n선택한 코드를 삭제하시겠습니까?',
      buttons: {
        ok: {
          text: '확인',
          action() {
            useApi()
              .request({
                method: 'post',
                url: '/api/code/delete',
                data: data.view1
              })
              .then((result: ApiResponse) => {
                console.log('delete.result:', result);
                max.ui.alert(result.msg);
                grid1.search();
              });
          }
        },
        cancel: {
          text: '취소',
          action() {}
        }
      }
    });
  },
  btnSave() {
    // 유효성체크
    if (isEmpty(data.view1.cd_nm)) {
      max.ui.valid('코드명을 입력하세요.');
      return;
    }
    useApi()
      .request({
        method: 'post',
        url: '/api/code/save',
        data: data.view1
      })
      .then((result: ApiResponse) => {
        console.log('save.result:', result);
        max.ui.alert(result.msg);
        grid1.search();
      });
  },
  // 버튼: 상세코드
  btnAdd2() {
    view2.value.reset();
    document.getElementById('cds_id').focus();
  },
  btnDelete2() {
    // 유효성체크
    if (!data.view1.cd_id) {
      max.ui.valid('코드를 먼저 선택해주세요.');
      return;
    }

    let selected = grid2.inst.getSelected();
    if (!isArray(selected)) {
      max.ui.valid('삭제할 상세코드를 목록에서 선택해주세요.');
      return;
    }

    let data2 = grid2.inst.getSourceDataAtRow(selected[0][0]);
    data2.cd_id = data.view1.cd_id;

    // 확인창
    max.ui.confirm({
      title: '확인',
      content: '상세코드: ' + data2.cds_nm + ' \n선택한 상세코드를 삭제하시겠습니까?',
      buttons: {
        ok: {
          text: '확인',
          action() {
            useApi()
              .request({
                method: 'post',
                url: '/api/code/desc/delete',
                data: data2
              })
              .then((result: ApiResponse) => {
                console.log('delete.result:', result);
                max.ui.alert(result.msg);
                grid2.search();
              });
          }
        },
        cancel: {
          text: '취소',
          action() {}
        }
      }
    });
  },
  btnSave2() {
    // 유효성체크
    if (!data.view1.cd_id) {
      max.ui.valid('코드를 먼저 선택해주세요.');
      return;
    }
    if (isEmpty(data.view2.cds_id)) {
      max.ui.valid('상세코드를 입력하세요.');
      return;
    } else if (isEmpty(data.view2.cds_nm)) {
      max.ui.valid('상세코드명을 입력하세요.');
      return;
    }
    data.view2.cd_id = data.view1.cd_id;

    useApi()
      .request({
        method: 'post',
        url: '/api/code/desc/save',
        data: data.view2
      })
      .then((result: ApiResponse) => {
        console.log('save.result:', result);
        max.ui.alert(result.msg);
        // grid2.search();
      });
  }
};

/**
 * grid1
 */
const grid1 = reactive({
  data: [],
  inst: null,
  width: '100%',
  height: 'auto',
  editor: false,
  // rowHeaders: true,
  // nestedHeaders: [],
  columns: [
      { title: '번호', data: 'rn' },
      { title: '코드그룹', data: 'cd_id' },
      { title: '코드그룹명', data: 'cd_nm' }
    ], // prettier-ignore
  hiddenColumns: {
    columns: []
  },
  afterInit() {
    grid1.inst = this;
    grid1.search();
  },
  afterSelection(row: number, col: number) {
    // let selRow = this.getDataAtRow(row);
    data.view1 = this.getSourceDataAtRow(row);
    view2.value.reset();
    grid2.search();
  },
  search() {
    useApi()
      .request({
        method: 'post',
        url: '/api/code/list',
        data: data.search
      })
      .then((result: ApiResponse) => {
        let rowData = result.data;
        grid1.data = rowData;
      });
  }
});

/**
 * grid2
 */
const grid2 = reactive({
  data: [],
  inst: null,
  width: '100%',
  height: 300,
  editor: false,
  rowHeaders: false,
  columns: [
      { title: '번호', data: 'rn' },
      { title: '코드그룹ID', data: 'cd_id' },
      { title: '코드', data: 'cds_id' },
      { title: '코드명', data: 'cds_nm' },
      { title: '순서', data: 'ord_seq' },
      { title: '비고', data: 'cds_text' },
      { title: '사용여부', data: '' },
    ], // prettier-ignore
  afterInit() {
    grid2.inst = this;
  },
  afterSelection(row: number, col: number) {
    data.view2 = this.getSourceDataAtRow(row);
  },
  search() {
    useApi()
      .request({
        method: 'post',
        url: '/api/code/desc/list',
        data: {
          cd_id: data.view1.cd_id
        }
      })
      .then((result: ApiResponse) => {
        let rowData = result.data;
        grid2.data = rowData;
      });
  }
});
</script>

<style scoped></style>
