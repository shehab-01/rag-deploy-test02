<template>
  <!------Header-------->
  <v-system-bar color="" height="0"></v-system-bar>

  <!------Header-------->
  <!-- https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg -->
  <v-app-bar elevation="10" height="60" color="" image="">
    <template v-slot:prepend>
      <!-- 사이드바 열기(비활성) -->
      <v-app-bar-nav-icon class="text-muted" @click="sidebar = !sidebar" v-if="false"></v-app-bar-nav-icon>
    </template>

    <template v-slot:default>
      <!-- hidden-md-and-down(X) -->
      <div class="d-none d-md-flex w-100">
        <div class="d-flex align-center ma-1">
          <v-app-bar-title></v-app-bar-title>
          <LayoutLogo />
        </div>
        <div class="d-flex" v-if="!sidebar">
          <v-list class="">
            <template v-for="(menu, i) in sidebarMenu">
              <v-menu open-on-hover>
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" class="ma-1" color="default" variant="text" size="default"> {{ menu.header }} </v-btn>
                </template>
                <v-list>
                  <v-list-item
                    :to="item.to"
                    v-for="(item, index) in menu.children"
                    :disabled="item.disabled"
                    :target="item.type === 'external' ? '_blank' : ''"
                  >
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
          </v-list>
        </div>
      </div>
    </template>

    <template v-slot:append>
      <div class="d-flex align-center justify-end" style="width: 200px">
        <LayoutHeaderNotificationDD v-if="false" />
        <LayoutHeaderProfileDD v-if="false" />
        <v-btn variant="outlined" v-if="authStore.isLogin" @click="toggleLogoutButtonState()">로그아웃</v-btn>
        <v-btn variant="outlined" v-else @click="goLoginPage()">로그인</v-btn>
      </div>
    </template>
  </v-app-bar>

  <!-- TODO: breadcrumbs -->
  <v-app-bar elevation="10" height="30" color="" v-if="false">
    <template v-slot:prepend> </template>
  </v-app-bar>

  <!------Sidebar-------->
  <v-navigation-drawer elevation="0" class="leftSidebar" v-model="sidebar" app temporary>
    <div>
      <perfect-scrollbar class="scrollnavbar">
        <div class="pa-5" v-if="false">
          <LayoutLogo />
        </div>
        <v-list class="pa-4">
          <template v-for="(menu, i) in sidebarMenu">
            <LayoutSidebarNavGroup :item="menu" />
            <template v-for="(item, i) in menu.children">
              <LayoutSidebarNavItem :item="item" class="leftPadding" />
            </template>
          </template>
        </v-list>
        <div class="pa-4">
          <LayoutSidebarExtraBox />
        </div>
      </perfect-scrollbar>
    </div>
  </v-navigation-drawer>

  <template>
    <v-dialog v-model="logoutButtonState" max-width="300" persistent>
      <v-card>
        <v-card-text class="wrapper-modal">
          <v-icon color="red" size="x-large">mdi-alert-circle-outline</v-icon>
          <div class="title text-h4 font-weight-bold mt-6">로그아웃을 하시겠어요?</div>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn @click="toggleLogoutButtonState()" class="logout-modal-button outlined-button">돌아가기</v-btn>
          <v-btn @click="executeLogout()" class="logout-modal-button">로그아웃 하기</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  <LoginModal :options="loginModal" />
</template>

<script setup lang="ts">
import sidebarItems from '@/components/layout/sidebar/sidebarItem';
import { useAuthStore } from '@/store/module/account';
import LoginModal from '../modal/LoginModal.vue';

const authStore = useAuthStore();
const router = useRouter();

const logoutButtonState = ref<boolean>(false);

const toggleLogoutButtonState = (): void => {
  logoutButtonState.value = !logoutButtonState.value;
};

const goLoginPage = (): void => {
  loginModal.show();
};

const sidebar = ref<boolean>(false);
const sidebarMenu = shallowRef(sidebarItems);

onMounted(() => {
  // console.log('main.onMounted:');
});

const page = {
  header: {
    title: 'main'
  },
  init() {
    console.log('page.init..');
  },
  test() {
    console.log('page.test..');
  }
};

const executeLogout = (): void => {
  authStore
    .logout()
    .then(() => {
      logoutButtonState.value = !logoutButtonState.value;
      router.replace({ path: '/', query: {} });
    })
    .catch(ex => {
      console.error('ex.logout:', ex);
    });
};

const loginModal = reactive({
  open: false,
  data: {},
  show() {
    this.open = true;
  },
  callback(result: any) {}
});
</script>

<style scoped>
.wrapper-modal {
  text-align: center;
}
.v-card-actions {
  padding: 16px;
}
.title {
  font-size: 1.25rem;
}
.logout-modal-button {
  height: 2.5rem;
  width: auto;
  margin: 0 8px;
  padding: 1rem !important;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem !important;
}
.outlined-button {
  background-color: white !important;
  color: black !important;
  border: 1px solid black !important;
}
.green-button {
  background-color: green !important;
  color: white !important;
}
</style>
