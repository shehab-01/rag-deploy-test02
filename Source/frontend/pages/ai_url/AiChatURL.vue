<template>
  <v-row>
    <v-col cols="12">
      <v-row>
        <v-col cols="12" lg="12">
          <Top title="URL 관리">
            <div class="d-flex gap-3 align-center flex-column flex-wrap flex-xl-nowrap flex-sm-row fill-height">
              <v-btn value="01" variant="text" color="primary" id="doc-manage" @click="page.topBtnClick('doc-manage')">문서 관리</v-btn>
              <v-btn value="02" variant="text" color="primary" id="prompt-manage" @click="page.topBtnClick('prompt-manage')">프롬프트 관리</v-btn>
              <v-btn value="03" variant="text" color="primary" id="ai-test" @click="page.topBtnClick('ai-test')">GenAI 테스트</v-btn>
              <!-- <v-btn value="03" variant="text" color="primary" id="ai-test" @click="page.dbTest()">DB 테스트</v-btn> -->
            </div>
          </Top>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" lg="12" style="padding: 0" v-if="data.topBtnId == 'ai-test'">
          <ChatWindow />
        </v-col>
        <v-col cols="12" lg="12" style="padding: 0" v-if="data.topBtnId == 'prompt-manage'">
          <PromptManage />
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
import ChatWindow from '@/components/aiChatUrl/ChatWindow.vue';
import UiParentCard from '@/components/shared/UiParentCard.vue';
// import DocumentManage from '@/components/aiChat/DocumentManage.vue';
import DocumentManage from '@/components/aiChatUrl/DocumentManage.vue';
import Top from '@/components/aiChat/Top.vue';
import PromptManage from '@/components/aiChatUrl/PromptManage.vue';

import type { ChatMessage, ApiRequest, ApiResponse, MessageType, Language } from '@/types/biz';

onMounted(() => {
  max.ui.init({
    page: page
  });
});

const data = reactive({
  search: {},
  topBtnId: 'ai-test'
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
