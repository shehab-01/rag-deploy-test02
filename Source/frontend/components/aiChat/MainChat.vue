<template>
  <v-row>
    <!-- Side -->
    <v-col>
      <v-card elevation="10" class="withbg" height="75vh">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <!-- <v-card-title class="text-h6" style="line-height: 1.57">{{ props.title }}</v-card-title> -->
            <h5 class="text-h5 mb-6 pl-7 pt-7">채팅 리스트</h5>
            <v-btn class="mr-4" icon size="x-small" flat><SettingsIcon stroke-width="1.5" /></v-btn>

            <!-- <template v-slot:append> -->
            <slot name="action"></slot>
            <!-- </template> -->
          </div>
        </v-card-item>
        <v-divider />
        <div>
          <v-card-text style="padding-left: 0; padding-right: 0; background-color: aliceblue">
            <!-- <v-row>
              <div class="chat-info" style="padding-left: 25px">
                <h3>What to do if the water doesn't come</h3>
                <p class="mt-5">아이콘 얼음 정수기</p>
                <p class="mt-2">📚🔍 내부지식 검색 답변 v3.0</p>
                <p class="mt-2 mb-4">2024-08-07 12:10:45</p>
              </div>
            </v-row> -->
            <v-row>
              <div class="chat-info" style="padding-left: 25px">
                <h3>{{ firstChat }}</h3>
                <p class="mt-5">아이콘 얼음 정수기</p>
                <p class="mt-2">📚🔍 내부지식 검색 답변 v3.0</p>
                <p class="mt-2 mb-4">{{ datetime }}</p>
              </div>
            </v-row>
          </v-card-text>
        </div>

        <!-- <v-divider /> -->

        <!-- <v-card-text style="padding-left: 0; padding-right: 0">
          <v-row>
            <div class="chat-info" style="padding-left: 25px">
              <h3>Wi-fi 상태확인 어떻게해요?</h3>
              <p class="mt-5">울산교육정보원</p>
              <p class="mt-2">📚🔍 내부지식 검색 답변 v3.0</p>
              <p class="mt-2 mb-4">2024-07-17 17:10:45</p>
            </div>
          </v-row>
        </v-card-text> -->
        <v-divider />
      </v-card>
    </v-col>

    <!-- Main Chat -->
    <v-col cols="9" md="9">
      <v-card elevation="10" class="withbg d-flex flex-column" height="75vh">
        <v-card-item class="pa-0">
          <div class="d-sm-flex align-center justify-space-between">
            <h5 class="text-h5 mb-6 pl-7 pt-7">Main Chat</h5>
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <v-divider />

        <v-card-text ref="chatContainer" class="flex-grow-1 overflow-y-auto">
          <v-row>
            <v-col cols="12" class="pa-0">
              <!-- Chat messages will appear here -->
              <div v-for="(message, index) in messages" :key="index" class="mb-2">
                <!-- Replace nested h4 in p with proper structure -->
                <div v-if="message.type == 'Q'" class="pb-5">
                  <h4>{{ message.type }}: {{ message.content }}</h4>
                </div>
                <p v-if="message.type == 'Ai'" class="pb-5">
                  <span class="ai-response">{{ message.type }}: </span>{{ message.content }}
                </p>
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="ai-text-action d-flex justify-center align-center pa-4">
          <v-text-field
            class="centered-input flex-grow-0"
            hide-details="auto"
            label="Search Ai..."
            @click:append-inner="sendMessage"
            @keyup.enter="sendMessage"
            append-inner-icon="mdi-send"
            v-model="newMessage"
            dense
            outlined
            shaped
          ></v-text-field>
        </v-card-actions>
        <!-- 
        <v-card-actions class="ai-text-action d-flex justify-center align-center" style="margin-bottom: 10px">
          <v-text-field
            hide-details="auto"
            label="Search Ai..."
            @click:append-inner="sendMessage"
            @keyup.enter="sendMessage"
            append-inner-icon="mdi-send"
            v-model="newMessage"
            dense
          ></v-text-field>

          <v-text-field
            class="ai-text-input"
            v-model="newMessage"
            label="Search Ai..."
            append-inner-icon="mdi-send"
            @click:append-inner="sendMessage"
            @keyup.enter="sendMessage"
            hide-details
            dense
          ></v-text-field>
        </v-card-actions> -->
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { useTheme } from 'vuetify';
import test from './Side.vue';
import type { ApiResponse } from '@/types/api';

const theme = useTheme();
const primary = theme.current.value.colors.primary;
const secondary = theme.current.value.colors.secondary;
const colorShadow = ref(['primary', 'secondary', 'info', 'success', 'warning', 'error']);

const messages = ref([]);
const newMessage = ref('');
const chatContainer = ref(null);
let firstChat: Ref<string> = ref('');
let datetime: Ref<string> = ref('');

onMounted(() => {
  scrollToBottom();
});

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.$el.scrollTop = chatContainer.value.$el.scrollHeight;
    }
  });
};

function isEnglish(text: string): boolean {
  // This regex allows English letters, numbers, and common punctuation
  const englishPattern = /^[a-zA-Z0-9\s.,!?'"()-]+$/;
  return englishPattern.test(text);
}

function detectLanguage(text: string): string {
  return isEnglish(text) ? 'en' : 'ko';
}

const sendMessage = () => {
  if (newMessage.value.trim()) {
    // Add human message
    const detectedLanguage = detectLanguage(newMessage.value);
    console.log(detectedLanguage);
    messages.value.push({ type: 'Q', content: newMessage.value, source: '' });
    console.log(messages.value);
    console.log(messages.value.length);
    if (messages.value.length == 1) {
      firstChat.value = messages.value[0]['content'];
      datetime.value = new Date().toLocaleString();
    }
    api.search(detectedLanguage);
    // Simulate AI response
    // messages.value.push({ type: 'Ai', content: 'AI reply to: ' + newMessage.value });

    // setTimeout(() => {
    //   messages.value.push({ type: 'AI', content: 'AI reply to: fsd' + newMessage.value });
    // }, 500);
    scrollToBottom();
  }
};

const api = reactive({
  search(detectedLanguage: string) {
    useApi()
      .request({
        method: 'post',
        url: '/api/demo/ask-ai-assistant',
        data: {
          question: newMessage.value,
          directory_name: 'x_log',
          question_lang: detectedLanguage
        }
      })
      .then((result: any) => {
        // console.log(result);
        // console.log(result['initial_response']);
        // console.log(result['sources']);
        let sources = '';
        for (let i = 0; i < result['sources'].length; i++) {
          if (result['sources'][i]['chunk_type'] == 'parent') {
            // console.log(result['sources'][i]);
            let page = parseInt(result['sources'][i]['page']);
            let pageF: number = page + 1;
            let pafeS: string = pageF.toString();
            sources = sources.concat(pafeS, ', ');
          }
        }

        console.log('SOURCES', sources);
        messages.value.push({ type: 'Ai', content: result['initial_response'], source: sources });

        // let rowData = result.data;
        // grid1.data = rowData;
        newMessage.value = '';
      });
  }
});
</script>

<style scoped>
.v-card-text {
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
}
.chat-info {
  font-size: 1.2em;
}
.ai-res {
  font-size: 1.2em;
}
.ai-response {
  font-weight: bold;
}

.ai-text-input {
  border-radius: 50px;
}

.ai-text-action {
  width: 100%;
}
.centered-input {
  max-width: 600px; /* Adjust this value based on your desired width */
  width: 100%;
  padding-bottom: 20px;
}
.centered-input :deep(.v-field__outline) {
  border-radius: 50px !important;
}
.centered-input :deep(.v-field__input) {
  border-radius: 50px !important;
}
</style>
