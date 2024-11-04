<template>
  <!------Sidebar-------->
  <v-navigation-drawer left elevation="0" app class="leftSidebar" v-model="sDrawer">
    <!---Logo part -->
    <div class="pa-5">
      <LayoutLogo />
    </div>
    <!-- ---------------------------------------------- -->
    <!---Navigation -->
    <!-- ---------------------------------------------- -->
    <div>
      <perfect-scrollbar class="scrollnavbar">
        <v-list class="pa-6">
          <!---Menu Loop -->
          <template v-for="(item, i) in sidebarMenu">
            <!---Item Sub Header -->
            <LayoutSidebarNavGroup :item="item" v-if="item.header" :key="item.title" />

            <!---Single Item-->
            <LayoutSidebarNavItem :item="item" v-else class="leftPadding" />
            <!---End Single Item-->
          </template>
        </v-list>
        <div class="pa-4">
          <LayoutSidebarExtraBox />
        </div>
      </perfect-scrollbar>
    </div>
  </v-navigation-drawer>

  <!------Header-------->
  <v-app-bar elevation="0" height="70">
    <div class="d-flex align-center justify-space-between w-100">
      <div>
        <v-btn class="ms-md-3 ms-sm-5 ms-3 text-muted" @click="sDrawer = !sDrawer" icon variant="flat" size="small">
          <Menu2Icon size="20" stroke-width="1.5" />
        </v-btn>
      </div>
      <div>
        <!-- Upgrade button -->
        <v-btn class="mr-2 bg-primary" href="https://adminmart.com/templates/nuxtjs/" target="_blank">Download Free</v-btn>
        <!-- Notification -->
        <LayoutHeaderNotificationDD />
        <!-- User Profile -->
        <LayoutHeaderProfileDD />
      </div>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
import { ref, shallowRef } from 'vue';
import sidebarItems from '@/components/layout/sidebar/sidebarItem';
import { Menu2Icon } from 'vue-tabler-icons';
const sidebarMenu = shallowRef(sidebarItems);
const sDrawer = ref(true);
const innerW = window.innerWidth;
onMounted(() => {
  if (innerW < 950) {
    sDrawer.value = !sDrawer.value;
  }
});
</script>
