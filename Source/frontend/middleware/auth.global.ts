import { useAuthStore } from '@/store/module/account';

export default defineNuxtRouteMiddleware(async (to, from) => {
  const authStore = useAuthStore();
  const isLoggedIn = false;

  // console.log('to.path:', to.path);
  // console.log('process.client:', process.client);

  // 로그인 체크를 하지않을 예외경로 추가
  if (to.path === '/auth/login' || to.path === '/auth/register') {
    return;
  }

  // 로그인인 경우 스킵
  // if (store.account().isLogin) {
  //   return;
  // }
  if (authStore.isLogin) {
    return;
  }

  // 로그인이 아닌경우 로그인 페이지로..
  // return navigateTo('/auth/login', { external: true });
});
