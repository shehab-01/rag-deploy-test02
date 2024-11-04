import { defineStore } from 'pinia';
import accountApi from '@/api/account.api';
const env = import.meta.env;

export default defineStore('accountTest', {
  persist: true,
  state: () => ({
    user: null,
    token: null
  }),
  getters: {
    isLogin(state) {
      return state.token && state.user ? true : false;
    },
    isAdmin(state) {
      return state.user && state.user.adminYn == 'Y' ? true : false;
    },
    getUser(state) {
      return state.user;
    },
    getToken(state) {
      return state.token;
    }
  },
  actions: {
    setAccount(user: object, token: string) {
      this.user = user;
      this.token = token;
    },
    setUser(user: object) {
      this.user = user;
    },
    setToken(token: string) {
      this.token = token;
    },
    setLogin(id: string) {
      if (this.user && this.user.id === id) {
        this.user.isUser = true;
        return true;
      }
      return false;
    },
    /**
     * 로그인
     */
    login(param: object) {
      return new Promise(async (resolve, reject) => {
        useApi()
          .request({
            method: 'post',
            url: '/api/user/login',
            data: param,
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          })
          .then(({ data: token }) => {
            if (token && token.access_token) {
              // 발급된 토큰설정
              this.setToken(token);

              // 발급된 토큰으로 사용자 정보 가져오기
              accountApi
                .getAccount()
                .then(({ status, data }) => {
                  const user = data.user;
                  if (status == 200) {
                    this.setUser(user);

                    resolve(user);
                  } else {
                    reject(user);
                  }
                })
                .catch(ex => {
                  console.error('ex.getAccount:', ex);
                  reject(ex);
                });
            }
          })
          .catch(ex => {
            console.error('ex.login:', ex);
          });
      });
    },
    /**
     * 로그아웃
     */
    logout(forceLogout = false) {
      return new Promise<void>(resolve => {
        // 로그아웃시 스토리지 데이터 제거
        max.storage.session.remove('codeInfo');

        if (forceLogout) {
          this.user = null;
          this.token = null;
          resolve();
        } else {
          useApi()
            .get('/api/user/logout')
            .then(({ data }) => {
              resolve(data);
            })
            .catch(ex => {
              console.error('logout.ex', ex);
            })
            .finally(() => {
              this.user = null;
              this.token = null;
              resolve();
            });
        }
      });
    }
  }
});
