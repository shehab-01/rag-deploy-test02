<template>
  <v-row>
    <v-col cols="12">
      <v-row>
        <v-col cols="12" lg="12">
          <Top title="지식 관리">
            <div class="d-flex gap-3 align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height">
              <v-btn value="01" variant="text" color="primary" id="doc-manage" @click="page.topBtnClick('doc-manage')">문서 관리</v-btn>
              <v-btn value="02" variant="text" color="primary" id="prompt-manage" @click="page.topBtnClick('prompt-manage')">프롬프트 관리</v-btn>
              <v-btn value="03" variant="text" color="primary" id="ai-test" @click="page.topBtnClick('ai-test')">GenAI 테스트</v-btn>
              <v-btn value="03" variant="text" color="primary" id="ai-test" @click="page.dbTest()">DB 테스트</v-btn>
            </div>
          </Top>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" lg="12" style="padding: 0" v-if="data.topBtnId == 'ai-test'">
          <MainChat />
        </v-col>
        <v-col cols="12" lg="12" style="padding: 0" v-if="data.topBtnId == 'doc-manage'">
          <DocumentManage />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import Side from '@/components/aiChat/Side.vue';
import SideTest from '@/components/aiChat/SideTest.vue';
import MainChat from '@/components/aiChat/MainChat.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
import DocumentManage from '@/components/aiChat/DocumentManage.vue';
import Top from '@/components/aiChat/Top.vue';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  search: {},
  topBtnId: 'doc-manage'
});

const page = {
  init() {},

  topBtnClick(btnId: string) {
    console.log(btnId);
    data.topBtnId = btnId;
  },
  dbTest() {
    useApi()
      .request({
        method: 'post',
        url: '/api/demo/test/db',
        data: {}
      })
      .then((result: any) => {
        console.log(result);
      });
  }
};
</script>
