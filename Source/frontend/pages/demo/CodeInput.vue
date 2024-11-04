<template>
  <v-row>
    <v-col cols="6">
      <UiParentCard title="Code Input">
        <v-row>
          <v-col cols="12">
            <v-row no-gutters>
              <v-col cols="12" md="3">
                <label for="sel1">Code: Select</label>
              </v-col>
              <v-col cols="12" md="9">
                <Code name="sel1" v-model="data.sel1" :option="{ type: 'select', code: 'CD001' }" />
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12">
            <v-row no-gutters>
              <v-col cols="12" md="3">
                <label for="sel1">Code: Radio</label>
              </v-col>
              <v-col cols="12" md="9">
                <Code
                  name="rdo1"
                  v-model="data.rdo1"
                  :option="{ type: 'radio', code: 'CD002', all: '전체' }"
                  @load="page.code_load.rdo1"
                  @change="page.code_change.rdo1"
                />
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12">
            <v-row no-gutters>
              <v-col cols="12" md="3">
                <label for="sel1">Code: Checkbox</label>
              </v-col>
              <v-col cols="12" md="9">
                <Code
                  name="chk1"
                  v-model="data.chk1"
                  :option="{ type: 'checkbox', code: 'CD003' }"
                  @load="page.code_load.chk1"
                  @change="page.code_change.chk1"
                />
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12">
            <v-row no-gutters>
              <v-col cols="12" md="3">
                <label for="sel1">Code: Biz</label>
              </v-col>
              <v-col cols="12" md="9">
                <Code name="biz1" v-model="data.biz1" :option="{ type: 'select', biz: 'task_user' }" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" class="d-flex justify-end pr-0">
            <v-btn class="ml-1" color="info" @click="page.btnOk"><v-icon>mdi-check</v-icon> 확인</v-btn>
          </v-col>
        </v-row>
      </UiParentCard>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import UiParentCard from '@/components/shared/UiParentCard.vue';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  sel1: 'U',
  rdo1: null,
  chk1: null,
  biz1: null
});

const page = {
  init() {},
  btnOk() {
    console.log('data:', toRaw(data));
  },
  // 코드로드
  code_load: {
    rdo1: function (items: object) {
      // console.log('code_load.rdo1:', items);
    },
    chk1: function (items: object) {
      // console.log('code_load.chk1:', items);
    }
  },
  // 코드변경
  code_change: {
    rdo1: function (evt: Event, val: string) {
      // console.log('code_change.rdo1:', evt, val);
    },
    chk1: function (evt: Event, val: string) {
      // console.log('code_change.chk1:', evt, val);
    }
  }
};
</script>

<style scoped></style>
