import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import accountApi from '@/api/account.api';
import type { LoginResponse, TokenResponse, UserInfo } from '@/types/auth';

export const useAuthStore = defineStore(
  'account',
  () => {
    const user = ref<LoginResponse | null>(null);
    const token = ref<TokenResponse | null>(null);

    const isLogin = computed(() => !!token.value && !!user.value);
    const isAdmin = computed(() => !!user.value && user.value.user_type === 'TA');
    const getUser = computed(() => user.value);
    const getToken = computed(() => token.value);

    function setAccount(newUser: LoginResponse, newToken: TokenResponse) {
      user.value = newUser;
      token.value = newToken;
    }

    function setUser(newUser: LoginResponse) {
      user.value = newUser;
    }

    function setToken(newToken: TokenResponse) {
      token.value = newToken;
    }

    // 나중에 바뀔 속성들 일단 주석 처리
    function setLogin(id: UserInfo['user_id']) {
      if (user.value && user.value.user_id === '1') {
        // user.value.isUser = true;
        return true;
      }
      return false;
    }

    const login = async (param: any) => {
      try {
        const api = useApi();
        const token: TokenResponse = await api.request({
          method: 'post',
          url: '/api/user/login',
          data: param,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        if (token && token.access_token) {
          // 발급된 토큰 설정
          setToken(token);

          // 발급된 토큰으로 사용자 정보 가져오기
          const { status, data } = await accountApi.getAccount();
          if (status === 200) {
            const user = data.user;
            setUser(user);
            // return data.user;
          } else {
            throw new Error('Failed to fetch user data');
          }
        } else {
          throw new Error('Invalid token');
        }
      } catch (error) {
        console.error('Login error:', error);
        throw error;
      }
    };

    const logout = async (forceLogout = false) => {
      return new Promise<void>(async resolve => {
        // 로그아웃시 스토리지 데이터 제거
        max.storage.session.remove('codeInfo');

        if (forceLogout) {
          user.value = null;
          token.value = null;
          resolve();
        } else {
          try {
            await useApi().get('/api/user/logout');
          } catch (ex) {
            console.error('logout.ex', ex);
          } finally {
            user.value = null;
            token.value = null;
            resolve();
          }
        }
      });
    };

    return {
      user,
      token,
      isLogin,
      isAdmin,
      getUser,
      getToken,
      setAccount,
      setUser,
      setToken,
      setLogin,
      login,
      logout
    };
  },
  {
    persist: true
  }
);
