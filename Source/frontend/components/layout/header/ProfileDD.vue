<template>
  <!-- ---------------------------------------------- -->
  <!-- notifications DD -->
  <!-- ---------------------------------------------- -->
  <v-menu :close-on-content-click="false">
    <template v-slot:activator="{ props }">
      <v-btn class="profileBtn custom-hover-primary" variant="text" v-bind="props" icon>
        <v-avatar size="35">
          <img src="/images/users/avatar-1.jpg" height="35" alt="user" />
        </v-avatar>
      </v-btn>
    </template>
    <v-sheet rounded="md" width="200" elevation="10" class="mt-2">
      <v-list class="py-0" lines="one" density="compact">
        <v-list-item value="item1" color="primary">
          <template v-slot:prepend>
            <UserIcon stroke-width="1.5" size="20" />
          </template>
          <v-list-item-title class="pl-4 text-body-1" @click="">My Profile</v-list-item-title>
        </v-list-item>
        <v-list-item value="item2" color="primary">
          <template v-slot:prepend>
            <MailIcon stroke-width="1.5" size="20" />
          </template>
          <v-list-item-title class="pl-4 text-body-1" @click="">My Account ({{ data.user.user_nm }})</v-list-item-title>
        </v-list-item>
        <v-list-item value="item3" color="primary">
          <template v-slot:prepend>
            <ListCheckIcon stroke-width="1.5" size="20" />
          </template>
          <v-list-item-title class="pl-4 text-body-1" @click="">My Task</v-list-item-title>
        </v-list-item>
      </v-list>
      <div class="pt-4 pb-4 px-5 text-center">
        <!-- <v-btn to="/auth/login" color="primary" variant="outlined" block>Logout</v-btn> -->
        <v-btn color="primary" variant="outlined" @click="executeLogout()" block>Logout</v-btn>
      </div>
    </v-sheet>
  </v-menu>
</template>

<script setup lang="ts">
import { UserIcon, MailIcon, ListCheckIcon } from 'vue-tabler-icons';
import { useAuthStore } from '@/store/module/account';

const authStore = useAuthStore();

const data = reactive({
  user: authStore.user
});

const router = useRouter();
const executeLogout = () => {
  authStore
    .logout()
    .then(() => {
      router.replace({ path: '/auth/login', query: {} });
    })
    .catch(ex => {
      console.error('ex.logout:', ex);
    });
};
</script>
