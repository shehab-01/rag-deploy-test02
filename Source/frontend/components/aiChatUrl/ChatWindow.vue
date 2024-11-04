<template>
  <v-row>
    <!-- Side Chat List -->
    <v-col cols="12" md="3" sm="2" class="chat-list-col">
      <v-card elevation="10" class="withbg chat-card">
        <v-card-item class="pa-0">
          <div class="d-flex align-center justify-space-between">
            <h5 class="text-h5 mb-6 pl-7 pt-7">채팅 리스트</h5>
            <v-btn class="mr-4" icon variant="text" size="x-small" flat @click="chatList.get_prompt_list()">
              <v-icon>mdi-square-edit-outline</v-icon>
            </v-btn>
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <v-divider />
        <div class="scrollable-container">
          <v-card-text class="scrollable-content" style="padding-top: 0; padding-bottom: 0">
            <template v-for="session in sessions" :key="session.id">
              <div
                class="session-wrapper"
                :class="{
                  'session-item': true,
                  'selected-session': selectedSessionId === session.id
                }"
              >
                <div class="d-flex align-center" style="width: 100%">
                  <div class="chat-info flex-grow-1" style="padding-left: 20px" @click="handleSessionClick(session)">
                    <h3 class="text-truncate">{{ session.title }}</h3>
                    <p class="mt-5 text-truncate">{{ session.prompt_name }}</p>
                    <p class="mt-2 mb-4">{{ new Date(session.created_at).toLocaleString() }}</p>
                  </div>
                  <div class="action-button">
                    <v-btn icon variant="text" size="large" class="mr-4" @click.stop="chatList.session_delete_action(session.id)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>
                </div>
                <v-divider v-if="!isLastSession(session)" />
              </div>
            </template>
          </v-card-text>
        </div>
        <v-divider />
      </v-card>
    </v-col>

    <!-- Main Chat -->
    <v-col cols="12" md="9" sm="10" class="chat-main-col">
      <v-card elevation="10" class="withbg d-flex flex-column chat-card">
        <v-card-item class="pa-0">
          <div class="d-flex align-center justify-space-between">
            <h5 class="text-h5 mb-6 pl-7 pt-7">Main Chat</h5>
            <slot name="action"></slot>
          </div>
        </v-card-item>
        <v-divider />

        <v-card-text ref="chatContainer" class="flex-grow-1 chat-messages">
          <v-row class="justify-center">
            <v-col cols="6" class="pa-0">
              <div class="main-chat">
                <div v-for="(message, index) in messages" :key="index" class="message-wrapper mb-4">
                  <!-- User Message (Q) -->
                  <div v-if="message.type == 'Q'" class="d-flex flex-column align-end">
                    <div class="user-message">
                      <span class="text-wrap">{{ message.content }}</span>
                    </div>
                  </div>

                  <!-- AI Message -->
                  <div v-if="message.type == 'Ai'" class="d-flex flex-column">
                    <span class="ai-response text-title-1 pb-2">GenAI:</span>
                    <!-- <div class="ai-message"> -->
                    <div class="">
                      <!-- <span class="ai-response text-subtitle-2">AI</span> -->
                      <span class="text-wrap">{{ message.content }}</span>
                    </div>
                    <p v-if="message.source" class="source-text mt-1">{{ message.source }}</p>
                  </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="ai-text-action d-flex justify-center align-center pa-4">
          <v-text-field
            class="centered-input"
            hide-details="auto"
            label="Search Ai..."
            @click:append-inner="sendMessage"
            @keyup.enter="sendMessage"
            append-inner-icon="mdi-send"
            v-model="newMessage"
            dense
            outlined
            shaped
            :disabled="!currentSession.isActive"
          ></v-text-field>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>

  <!-- Dialog -->
  <v-dialog v-model="data.prompt_modal" max-width="500">
    <template v-slot:default="{ isActive }">
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">새 채팅</div>
          <v-btn icon="mdi-close" variant="text" @click="isActive.value = false"></v-btn>
        </v-card-title>
        <v-divider class="mb-4"></v-divider>
        <v-card-text>
          <div class="text-medium-emphasis mb-4">Prompt 를 선택하여 GenAI 테스트를 하실 수 있습니다.</div>
          <v-table>
            <tbody>
              <tr>
                <td>프롬프트</td>
                <td>
                  <v-select
                    v-model="data.selectedPrompt"
                    :items="data.promptList"
                    item-title="prompt_name"
                    item-value="prompt_id"
                    variant="outlined"
                    density="compact"
                    hide-details
                    @update:model-value="handlePromptSelection"
                  ></v-select>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
        <v-divider class="mt-2"></v-divider>
        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn class="text-none" rounded="xl" text="취소" @click="isActive.value = false"></v-btn>
          <v-btn class="text-none" rounded="xl" text="채팅 시작하기" color="primary" @click="startNewChat"></v-btn>
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

const theme = useTheme();
const primary = theme.current.value.colors.primary;
const secondary = theme.current.value.colors.secondary;
const colorShadow = ref(['primary', 'secondary', 'info', 'success', 'warning', 'error']);

interface Prompt {
  prompt_id: number;
  prompt_name: string;
}

interface ChatSession {
  id: string | null;
  isActive: boolean;
  prompt_id: number | null;
}

const currentSession = reactive<ChatSession>({
  id: null,
  isActive: false,
  prompt_id: null
});

const messages = ref([]);
const newMessage = ref('');
const chatContainer = ref(null);
let firstChat: Ref<string> = ref('');
let datetime: Ref<string> = ref('');
const sessions = ref([]);
const selectedSessionId = ref(null);

const data = reactive({
  prompt_modal: false,
  promptList: [] as Prompt[],
  selectedPrompt: null as number | null
});

onMounted(() => {
  scrollToBottom();
  chatList.get_session_chat_list();
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

const startNewChat = () => {
  console.log('NEW CHAT');
  currentSession.isActive = true;
  currentSession.prompt_id = data.selectedPrompt;
  messages.value = []; // Clear existing messages
  data.prompt_modal = false; // Close the modal
  currentSession.id = null;
};

const saveMessageToDb = async (sessionId: string, type: string, content: string, source: string = '') => {
  try {
    await useApi().request({
      method: 'post',
      url: '/api/chat/messages',
      data: {
        session_id: sessionId,
        type,
        content,
        source
      }
    });
  } catch (error) {
    console.error('Error saving message:', error);
  }
};

const createSession = async (firstMessage: string) => {
  console.log('Create session api');
  try {
    const response = await useApi().request({
      method: 'post',
      url: '/api/chat/sessions',
      data: {
        title: firstMessage,
        prompt_id: currentSession.prompt_id,
        user_email: 'user@example.com', // You'll need to get this from your auth system
        prompt_name: data.promptList.find(p => p.prompt_id === currentSession.prompt_id)?.prompt_name
      }
    });
    return response.data.id;
  } catch (error) {
    console.error('Error creating session:', error);
    return null;
  }
};

// const api = reactive({
//   search(detectedLanguage: string) {
//     fetch('/api/ai-url/ask', {
//       method: 'POST',
//       body: JSON.stringify({
//         question:newMessage.value
//       }),
//     }).then(response => {
//       console.log(response)
//     })
//   }
// });

const api = reactive({
  async search(detectedLanguage: string) {
    let accumulatedResponse = '';
    let lastProcessedLength = 0;
    let currentSource = '';

    try {
      await useApi().request({
        method: 'post',
        url: '/api/ai-url/ask',
        data: {
          question: newMessage.value,
          session_id: currentSession.id,
          language: detectedLanguage
        },
        responseType: 'text',
        onDownloadProgress: (progressEvent: AxiosProgressEvent) => {
          const response = progressEvent.event?.target instanceof XMLHttpRequest ? progressEvent.event.target.response : '';

          if (response) {
            try {
              // Process only new content
              const newContent = response.slice(lastProcessedLength);
              const lines = newContent.split('\n');
              let contentToAdd = '';

              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  try {
                    const jsonData = JSON.parse(line.slice(6));
                    if (jsonData.content) {
                      contentToAdd += jsonData.content;
                      accumulatedResponse += jsonData.content;
                    }
                    if (jsonData.source) {
                      currentSource = jsonData.source;
                    }
                  } catch (e) {
                    console.error('Error parsing JSON:', e);
                  }
                }
              }

              lastProcessedLength = response.length;

              // Update UI only
              if (contentToAdd) {
                if (messages.value.length > 0 && messages.value[messages.value.length - 1].type === 'Ai') {
                  const lastMessage = messages.value[messages.value.length - 1];
                  if (!lastMessage.content.endsWith(contentToAdd)) {
                    lastMessage.content = accumulatedResponse; // Use accumulated response
                    lastMessage.source = currentSource;
                  }
                } else {
                  messages.value.push({
                    type: 'Ai',
                    content: accumulatedResponse, // Use accumulated response
                    source: currentSource
                  });
                }

                scrollToBottom();
              }
            } catch (error) {
              console.error('Error processing stream:', error);
            }
          }
        }
      });

      // After stream is complete, save the entire accumulated response to database
      if (accumulatedResponse && currentSession.id) {
        await saveMessageToDb(currentSession.id, 'Ai', accumulatedResponse, currentSource);
      }
    } catch (error) {
      console.error('API error:', error);
      messages.value.push({
        type: 'Ai',
        content: 'Error: Could not get response from server',
        source: ''
      });
    } finally {
      newMessage.value = '';
      lastProcessedLength = 0;
    }
  }
});

const chatList = reactive({
  get_prompt_list() {
    data.prompt_modal = true;
    useApi()
      .request({
        method: 'post',
        url: '/api/chat/prompt_list'
      })
      .then((result: ApiResponse) => {
        if (result.status === 200 && Array.isArray(result.data)) {
          data.promptList = result.data;
        } else {
          console.error('Invalid response format:', result);
        }
      });
  },
  get_session_chat_list() {
    useApi()
      .request({
        method: 'post',
        url: '/api/chat/session-list'
      })
      .then((result: ApiResponse) => {
        if (result.status === 200 && Array.isArray(result.data)) {
          // console.log("SEASSION LIST: ", result)
          sessions.value = result.data;
        } else {
          console.error('Invalid response format:', result);
        }
      });
  },

  session_delete_action(session_id: any) {
    console.log(session_id);
    // confirm modal
    max.ui.confirm({
      title: '세션 삭제 하겠습니까?',
      content: '세션 삭제하면 챗 기록들이 다 없어져워.',
      buttons: {
        ok: {
          text: '삭제',
          action() {
            console.log('confirm.ok');
            chatList.session_all_delete(session_id);
          }
        },
        cancel: {
          text: '취소',
          action() {
            console.log('confirm.cancel');
          }
        }
      }
    });
  },
  session_all_delete(session_id: string) {
    useApi()
      .request({
        method: 'post',
        url: '/api/chat/session-delete',
        data: {
          session_id: session_id
        }
      })
      .then((result: ApiResponse) => {
        if (result.status === 200) {
          // console.log("SEASSION LIST: ", result)
          chatList.get_session_chat_list();
          max.ui.alert('세션 삭제 완료.');
        } else {
          console.error('Invalid response format:', result);
        }
      });
  }
});

const handlePromptSelection = (value: number) => {
  console.log('Selected prompt:', value);
  // Add any additional handling logic here
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentSession.isActive) return;

  const messageContent = newMessage.value;
  const detectedLanguage = detectLanguage(messageContent);

  // Add user message to UI
  messages.value.push({ type: 'Q', content: messageContent, source: '' });

  // If this is the first message, create a new session
  if (!currentSession.id) {
    firstChat.value = messageContent;
    datetime.value = new Date().toLocaleString();
    currentSession.id = await createSession(messageContent);
    chatList.get_session_chat_list();
  }

  // Save user message to database
  if (currentSession.id) {
    await saveMessageToDb(currentSession.id, 'Q', messageContent);
  }
  await api.search(detectedLanguage);
};

const isLastSession = (session: any) => {
  return sessions.value.indexOf(session) === sessions.value.length - 1;
};

const handleSessionClick = (session: { id: string }) => {
  selectedSessionId.value = session.id;
  currentSession.id = session.id;
  currentSession.isActive = true;

  console.log(selectedSessionId);
  // You might want to load the messages for this session
  loadSessionMessages(session.id);
};

const loadSessionMessages = async (sessionId: string) => {
  try {
    const response = await useApi().request({
      method: 'post',
      url: '/api/chat/full-chat-list',
      data: {
        session_id: sessionId
      }
    });

    if (response.status === 200 && Array.isArray(response.data)) {
      console.log(response.data);
      messages.value = response.data;
      scrollToBottom();
    }
  } catch (error) {
    console.error('Error loading session messages:', error);
  }
};
</script>

<style scoped>
/* Card and Layout */
.chat-card {
  height: 75vh;
}

.chat-list-col,
.chat-main-col {
  transition: all 0.3s ease;
}

/* Scrollable Containers */
.scrollable-container {
  height: calc(75vh - 75px);
  position: relative;
  overflow: hidden;
}

.scrollable-content {
  height: 100%;
  overflow-y: auto;
  padding: 0;
  margin: 0;
  background-color: white;
}

.chat-messages {
  height: calc(75vh - 180px);
  overflow-y: auto;
}

/* Session Items */
.session-wrapper {
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s ease;
  padding: 8px 0;
  position: relative;
}

.session-item:hover {
  background-color: #f5f5f5;
}

.selected-session {
  background-color: #e3f2fd;
}

/* Action Button */
.action-button {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.session-wrapper:hover .action-button {
  opacity: 1;
}

/* Text Styles */
.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.text-wrap {
  word-wrap: break-word;
  word-break: break-word;
}

.chat-info {
  font-size: 1.2em;
}

.ai-response {
  font-weight: bold;
}

/* Input Styles */
.centered-input {
  max-width: 600px;
  width: 100%;
  padding-bottom: 20px;
}

.centered-input :deep(.v-field__outline),
.centered-input :deep(.v-field__input) {
  border-radius: 50px !important;
}

.ai-text-action {
  width: 100%;
  box-shadow: 0 -4px 6px -1px rgba(211, 211, 211, 0.4);
}

/* Responsive Styles */
@media (max-width: 959px) {
  .chat-card {
    height: auto;
    min-height: 50vh;
  }

  .action-button {
    opacity: 1;
  }

  .chat-list-col {
    margin-bottom: 16px;
  }

  .scrollable-container {
    height: auto;
    max-height: 40vh;
  }

  .chat-messages {
    height: 40vh;
  }

  .ai-text-action {
    padding: 8px !important;
  }
}
/* hide */
/* Custom Scrollbar */
.scrollable-content::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar {
  width: 8px;
  /* display: none;  */
}

.scrollable-content::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.scrollable-content::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.scrollable-content::-webkit-scrollbar-thumb:hover,
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* hide */
/* .scrollable-content,
.chat-messages {
  -ms-overflow-style: none; 
  scrollbar-width: none; 
} */

.message-wrapper {
  width: 100%;
  padding: 0 16px;
}

.user-message {
  background-color: #2196f3;
  color: white;
  padding: 12px 16px;
  border-radius: 18px;
  border-top-right-radius: 4px;
  max-width: 80%;
  margin-left: auto;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 12px;
}

.ai-message {
  background-color: #f5f5f5;
  color: #333;
  padding: 12px 16px;
  border-radius: 18px;
  border-top-left-radius: 4px;
  max-width: 80%;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 12px;
}

.ai-response {
  color: #1976d2;
  font-weight: 500;
  margin-right: 8px;
}

.source-text {
  color: #666;
  font-size: 0.8rem;
  margin-left: 12px;
}

/* Ensure proper word wrapping */
.text-wrap {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>
