<template>
  <ModalTemplate
    :isModalOpen="options.open"
    icon=""
    title=""
    description=""
    cancelButtonText="돌아가기"
    confirmButtonText="로그인하기"
    maxWidth="400"
    maxHeight="500"
    @closeModal="options.modal.close()"
    @confirmModal="options.modal.confirm()"
  >
    <template #content>
      <section class="login_modal">
        <section class="">
          <LayoutLogo />
        </section>
        <form @submit.prevent="options.modal.executeLogin">
          <v-row class="mb-4 justify-center">
            <v-col cols="12" class="d-flex justify-center align-center gap-2">
              <v-text-field
                v-model="data.userName"
                @keyup.enter="$refs.pass.select()"
                density="comfortable"
                placeholder="이메일"
                autocomplete="username"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="d-flex justify-center align-center gap-2">
              <v-text-field
                type="password"
                v-model="data.userPassword"
                @keyup.enter="options.modal.executeLogin"
                placeholder="비밀번호"
                autocomplete="current-password"
              ></v-text-field>
            </v-col>
            <v-col cols="12" class="mt-4 flex-row-center gap-2 justify-center">
              <div class="link-container">
                <v-btn @click="options.modal.linkSearchEmail()" class="search-link">아이디(이메일) 찾기</v-btn>
                <span class="separator">|</span>
                <v-btn @click="options.modal.linkSearchEmail()" class="search-link">비밀번호 찾기</v-btn>
                <span class="separator">|</span>
                <v-btn @click="options.modal.linkRegister()" class="search-link">회원가입</v-btn>
              </div>
            </v-col>
          </v-row>
        </form>
      </section>
    </template>
  </ModalTemplate>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/store/module/account';
import type { LoginUser } from '@/types/auth';
import { loginRules } from '@/utils/rules';

const router = useRouter();
const authStore = useAuthStore();

onMounted(() => {
  options.modal.init();
});

const data = reactive<LoginUser & { remember: string | boolean }>({
  userName: '',
  userPassword: '',
  remember: ''
});

const props = defineProps({
  options: {
    type: Object,
    required: true,
    default: {}
  },
  modelValue: null
});
const options = props.options;

options.modal = {
  init(): void {
    // 로그인ID(기억하기)
    let remember = max.storage.local.get('remember');
    if (remember) {
      data.userName = remember;
      data.remember = true;
    } else {
      data.userName = '';
      data.remember = false;
    }
  },
  //타입 수정 필요
  executeLogin(): any {
    const loginData = {
      username: data.userName,
      password: data.userPassword,
      remember: data.remember
    };
    // 유효성검사
    max.util.validate(loginRules, data).then(() => {
      authStore
        .login(loginData)
        .then(() => {
          if (data.remember) {
            max.storage.local.set('remember', data.userName);
          } else {
            max.storage.local.remove('remember');
          }
          data.userName = '';
          data.userPassword = '';
          options.modal.close();
          router.push('/');
        })
        .catch((ex: any) => {
          max.ui.error('회원 정보가 일치하지 않습니다.');
        });
    });
  },
  linkRegister() {
    options.modal.close();
    router.push('/auth/register');
  },
  linkSearchEmail() {
    options.modal.close();
    router.push('/');
  },
  close() {
    options.open = false;
  },
  confirm() {
    // options.open = false;
    options.modal.executeLogin();
  }
};
</script>

<style scoped>
.login_modal {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 5px;
}

.link-container {
  gap: 10px;
  font-size: 0.875rem;
}

.search-link {
  color: #4a4a4a;
  text-decoration: none;
  padding: 5px;
  position: relative;
}

.search-link::after {
  content: '';
  display: block;
  width: 100%;
  height: 1px;
  background: #4a4a4a;
  position: absolute;
  bottom: 0;
  left: 0;
}

.separator {
  color: #4a4a4a;
  padding: 0 5px;
}
</style>
