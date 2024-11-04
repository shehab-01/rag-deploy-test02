<template>
  <v-row>
    <v-col cols="12" md="12">
      <v-card varient="outlined" elevation="10" class="withbg">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <!-- <v-divider /> -->

        <v-card-text>
          <v-row justify="start" class="mb-5 mt-1 px-8 px-3">
            <!-- Create Prompt template -->
            <v-col cols="12" sm="6" md="4">
              <v-card height="250">
                <v-card-text class="d-flex flex-column h-100">
                  <div>
                    <h2 class="mb-5">프롬프트 생성하기</h2>
                    <p>새로운 프롬프트를 생성합니다.</p>
                  </div>

                  <div class="mt-auto text-right">
                    <v-btn color="primary" @click="prompt_modal.show_modal('create', '')">
                      <v-icon icon="mdi-plus" start></v-icon>프롬프트 생성</v-btn
                    >
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
            <!-- Prompts from DB -->
            <v-col v-for="prompt in prompts" cols="12" sm="6" md="4" :key="prompt.prompt_id">
              <v-card height="250">
                <v-card-text class="d-flex flex-column h-100">
                  <div>
                    <h2 class="mb-5">{{ prompt.prompt_name }}</h2>
                    <p>
                      {{ prompt.description }}
                    </p>
                  </div>

                  <div class="mt-auto text-right">
                    <v-btn color="primary" variant="outlined" @click="prompt_modal.show_modal('view', prompt.prompt_id)">보기</v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <!-- Modal for prompts -->
  <v-dialog v-model="modal.isActive" max-width="70%">
    <template v-slot:default="{ isActive }">
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h4 text-medium-emphasis ps-2">프롬프트 보기</div>
          <v-btn icon="mdi-close" variant="text" @click="isActive.value = false"></v-btn>
        </v-card-title>
        <v-divider class="mb-4"></v-divider>

        <v-card-text style="padding-left: 0; padding-right: 0; padding-bottom: 0">
          <!-- <div class="mb-4">Prompt 를 선택하여 GenAI 테스트를 하실 수 있습니다.</div> -->

          <v-container class="" style="padding: 0">
            <v-row justify="center">
              <v-col cols="6" sm="6">
                <v-col cols="12" sm="12">
                  <!-- <label for="prompt_nm" class="title-font"> 프롬프트 이름</label> -->
                  <p class="title-font">프롬프트 이름</p>
                  <v-text-field
                    class="mb-5"
                    id="prompt_nm"
                    placeholder="프롬프트 이름을 입력해주세요."
                    :readonly="modal.readOnly"
                    v-model="modal.prompt_name"
                    :clearable="false"
                  />
                </v-col>
                <v-col cols="12" sm="12">
                  <!-- <label for="prompt_des">프롬프트 설명</label> -->
                  <p class="title-font">프롬프트 설명</p>
                  <v-textarea
                    class="mb-5"
                    id="prompt_des"
                    variant="outlined"
                    auto-grow
                    rows="5"
                    placeholder="커스텀 프롬프트를 입력해주세요."
                    :readonly="modal.readOnly"
                    v-model="modal.description"
                  ></v-textarea>
                </v-col>

                <h3>GenAI 파라미터 설정</h3>
                <v-container style="padding-left: 0; padding-right: 0; margin-left: 0">
                  <h4>Max Output Tokens</h4>
                  <p>GenAI의 응답 길이를 조절합니다.</p>
                  <v-row justify="center">
                    <v-slider
                      v-model="modal.maxOutToken.value"
                      :max="modal.maxOutToken.max"
                      :min="modal.maxOutToken.min"
                      :step="modal.maxOutToken.step"
                      class="align-center"
                      hide-details
                      thumb-label
                      :readonly="modal.readOnly"
                    >
                      <template v-slot:append>
                        <v-text-field
                          class="centered-input"
                          v-model="modal.maxOutToken.value"
                          style="width: 70px"
                          single-line
                          :clearable="false"
                          readonly
                        ></v-text-field>
                      </template>
                    </v-slider>
                  </v-row>
                </v-container>

                <v-container style="padding-left: 0; padding-right: 0; margin-left: 0">
                  <h4>Temperature</h4>
                  <p>토큰 생성의 랜덤성으로 낮을수록 확신있는 답변, 높을수록 다양한 응답을 생성합니다.</p>
                  <v-row justify="center">
                    <v-slider
                      v-model="modal.temp.value"
                      :max="modal.temp.max"
                      :min="modal.temp.min"
                      :step="modal.temp.step"
                      class="align-center"
                      hide-details
                      thumb-label
                      :readonly="modal.readOnly"
                    >
                      <template v-slot:append>
                        <v-text-field
                          class="centered-input"
                          v-model="modal.temp.value"
                          style="width: 70px"
                          single-line
                          :clearable="false"
                          readonly
                        ></v-text-field>
                      </template>
                    </v-slider>
                  </v-row>
                </v-container>

                <v-container style="padding-left: 0; padding-right: 0; margin-left: 0">
                  <h4>Top P</h4>
                  <p>GenAI가 확률 분포 상위 P%의 단어만 고려하여 다음 토큰을 생성합니다.</p>
                  <v-row justify="center">
                    <v-slider
                      v-model="modal.topP.value"
                      :max="modal.topP.max"
                      :min="modal.topP.min"
                      :step="modal.topP.step"
                      class="align-center"
                      hide-details
                      thumb-label
                      :readonly="modal.readOnly"
                    >
                      <template v-slot:append>
                        <v-text-field
                          class="centered-input"
                          v-model="modal.topP.value"
                          style="width: 70px"
                          single-line
                          :clearable="false"
                          readonly
                        ></v-text-field>
                      </template>
                    </v-slider>
                  </v-row>
                </v-container>
              </v-col>
              <v-col cols="6" sm="6" class="pl-5">
                <v-col cols="12">
                  <CustomTooltip title="프롬프트 동적 변수">
                    <template #default>
                      <div class="d-flex align-center">
                        <h3>프롬프트 동적 변수</h3>
                        <v-btn icon="mdi mdi-help-circle-outline"></v-btn>
                      </div>
                    </template>

                    <template #content>
                      프롬프트 동적 변수를 통해 시스템 정보(에이전트명, 언어, 검색 컨텍스트)를 커스텀 프롬프트에서 활용할 수 있습니다. 설정된
                      동적변수는 커스텀 프롬프트에 '변수명'으로 작성함으로써 맵핑되어 사용됩니다.
                    </template>
                  </CustomTooltip>
                </v-col>

                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="10" md="4">
                      <label for="searchContent">검색 컨텍스트</label>
                    </v-col>
                    <v-col cols="12" md="8">
                      <v-text-field id="searchContent" placeholder="search_content" persistent-placeholder :readonly="modal.readOnly" />
                    </v-col>
                  </v-row>
                </v-col>

                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="10" md="4">
                      <label for="fewshot">Fewshot</label>
                    </v-col>
                    <v-col cols="12" md="8">
                      <v-text-field id="fewshot" placeholder="fewshot_example" persistent-placeholder :readonly="modal.readOnly" />
                    </v-col>
                  </v-row>
                </v-col>

                <v-col cols="12" class="pt-10">
                  <v-row no-gutters>
                    <label for="prompt_detl">프롬프트 입력</label>
                    <v-textarea
                      class="mb-5"
                      id="prompt_detl"
                      variant="outlined"
                      auto-grow
                      rows="18"
                      placeholder="프롬프트를 입력해주세요."
                      :readonly="modal.readOnly"
                      v-model="modal.prompt_content"
                    ></v-textarea>
                  </v-row>
                </v-col>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider class="mt-2"></v-divider>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn class="text-none" text="취소" variant="text" @click="isActive.value = false"></v-btn>
          <v-btn class="text-none" text="완료" color="primary" :disabled="modal.readOnly" @click="prompt.save_new_prompt"></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { useTheme } from 'vuetify';
import type { ApiResponse } from '@/types/api';
import type { AxiosProgressEvent } from 'axios';
import CustomTooltip from '../shared/CustomTooltip.vue';

const theme = useTheme();
const primary = theme.current.value.colors.primary;
const secondary = theme.current.value.colors.secondary;

import UiParentCard from '@/components/shared/UiParentCard.vue';
import { QuestionMarkIcon } from 'vue-tabler-icons';
const colorShadow = ref(['primary', 'secondary', 'info', 'success', 'warning', 'error', 'primary']);

const prompts = ref([]);

const modal = reactive({
  isActive: false,
  readOnly: false,
  promptDynamicVariables: false,
  prompt_name: '',
  description: '',
  prompt_content: '',
  maxOutToken: {
    value: 500,
    min: 0,
    step: 5,
    max: 1024
  },
  temp: {
    value: 0.5,
    min: 0,
    step: 0.05,
    max: 2
  },
  topP: {
    value: 0.5,
    min: 0,
    step: 0.01,
    max: 1.0
  }
});
onMounted(() => {
  prompt.get_prompt_list();
});

const prompt = reactive({
  get_prompt_list() {
    useApi()
      .request({
        method: 'post',
        url: '/api/chat/prompt_list'
      })
      .then((result: ApiResponse) => {
        if (result.status === 200 && Array.isArray(result.data)) {
          prompts.value = result.data;
          console.log(result);
        } else {
          console.error('Invalid response format:', result);
        }
      });
  },

  get_prompt_list_detl(prompt_id: any) {
    // console.log('PROMPOT IT', prompt_id);
    useApi()
      .request({
        method: 'post',
        url: '/api/chat/prompt_detl',
        data: {
          prompt_id: prompt_id
        }
      })
      .then((result: ApiResponse) => {
        if (result.status === 200) {
          // prompts.value = result.data;
          console.log(result.data);
          modal.maxOutToken.value = result.data['max_output_token'];
          modal.temp.value = result.data['temperature'];
          modal.topP.value = result.data['topp'];
          modal.prompt_name = result.data['prompt_name'];
          modal.description = result.data['description'];
          modal.prompt_content = result.data['prompt_content'];
        } else {
          console.error('Invalid response format:', result);
        }
      });
  },

  save_new_prompt() {
    console.log(modal.maxOutToken.value);

    useApi()
      .request({
        method: 'post',
        url: '/api/chat/prompt-save',
        data: {
          prompt_name: modal.prompt_name,
          prompt_content: modal.prompt_content,
          description: modal.description,
          prompt_type: 'user',
          max_output_token: modal.maxOutToken.value,
          temperature: modal.temp.value,
          topP: modal.topP.value
        }
      })
      .then((result: ApiResponse) => {
        if (result.status === 200) {
          // prompts.value = result.data;
          console.log(result.data);
        } else {
          console.error('Invalid response format:', result);
        }
      });
  }
});

const prompt_modal = reactive({
  show_modal(modalType: string, prompt_id: any) {
    if (modalType === 'create') {
      modal.isActive = true;
      modal.readOnly = false;

      // reset
      modal.prompt_name = '';
      modal.description = '';
      modal.prompt_content = '';
      modal.maxOutToken.value = 500;
      modal.temp.value = 0.5;
      modal.topP.value = 0.5;
    }

    if (modalType === 'view') {
      modal.isActive = true;
      modal.readOnly = true;
      console.log(prompt_id);

      prompt.get_prompt_list_detl(prompt_id);
    }
  }
});
</script>

<style scoped>
.centered-input {
  text-align: center;
  background-color: white;
  color: black;
}

span.tooltip {
  color: black;
  background-color: white;
  border-color: white;
  max-width: 200px;
  height: 500px;
}

.title-font {
  font-size: 14px;
  font-weight: bolder;
  padding-bottom: 10px;
  /* color: red; */
}
</style>
