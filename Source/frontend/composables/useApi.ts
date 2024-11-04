import axios from 'axios';
import type { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { useRuntimeConfig } from 'nuxt/app';
import { useAuthStore } from '@/store/module/account';
import type { ApiResponse } from '@/types/api';

const env = import.meta.env;
const isDev = process.env.NODE_ENV === 'development';

export const useApi = () => {
  // const config = useRuntimeConfig();
  // const baseURL = config.public.baseApiUrl as string;

  const api = axios.create({
    baseURL: env.VITE_API_URL,
    timeout: 200000
  });

  /**
   * Request Interceptor
   */
  const timeout = 500;
  api.interceptors.request.use(
    async config => {
      max.ui.loading(true);

      // 토큰확인
      const authStore = useAuthStore();
      let token = authStore.token;
      // let token = store.account().token;
      if (token && token.access_token) {
        // ※ 인증서버: 토큰 유효성검사 및 갱신
        // if (!isEmpty(token.refresh_token)) {
        //   let { data } = await axios.post(`${env.VITE_OAUTH_URL}/oauth/token/validate`, token);
        //   let new_token = data.resultData;
        //   if (!isEmpty(new_token) && useHas(new_token, 'access_token') && useHas(new_token, 'refresh_token')) {
        //     token = new_token;
        //     store.account().setToken(token);
        //   }
        // }

        // 헤더설정
        config.headers.Authorization = `Bearer ${token.access_token}`;
      }
      // if (isFunction(config.before)) {
      //   config.before.call(this, config);
      // }

      // 파라미터확인
      if (config.method == 'get') {
        if (isEmpty(config.params)) {
          config.params = useClone(config.data);
        }
        delete config.data;
      }
      return config;
    },
    error => {
      max.ui.loading(false);
      return Promise.reject(error);
    }
  );

  /**
   * Response Interceptor
   */
  api.interceptors.response.use(
    response => {
      max.ui.loading(false);

      // (response): AxiosResponse<ApiResponse> => {
      // console.log('response:', response);
      if (response.data) {
        return response.data;
      }
      return response;
    },
    error => {
      max.ui.loading(false);
      console.log('error:', error);

      if (error.response) {
        const router = useRouter();
        const { status, statusText, data } = error.response;
        // console.log('error:', status, statusText, data);

        // 세션종료: 토큰만료 및 다중로그인 오류처리`
        if (status === 401 || status === 403) {
          if (status === 401) {
            max.ui.error({
              title: '401: Unauthorized',
              content: '세션이 종료되었습니다. \n다시 로그인해 주세요.',
              buttons: {
                ok: {
                  text: '확인',
                  action: function () {
                    router.replace('/');
                  }
                }
              }
            });
          } else {
            max.ui.error({
              title: '403: Forbidden',
              content: '다른 기기 접속으로 인해 로그아웃되었습니다.'
            });

            // 강제 로그아웃
            store
              .account()
              .logout(true)
              .then(result => {
                router.replace('/auth/login');
              })
              .catch(ex => {
                console.error('ex.logout:', ex);
              });
          }
        }
        // 요청오류
        else if (status === 400) {
          let detail = '';
          if (data && data.error) {
            detail = detail.concat('\n' + data.error.type + ': ' + data.error.detail);
          }
          max.ui.error({
            title: '400: BadRequest Error',
            content: '요청 오류입니다. \n다시 시도해 주세요.'.concat(detail)
          });
        }
        // 서버오류
        else if (status === 500) {
          let detail = '';
          if (data && data.error) {
            detail = detail.concat('\n' + data.error.type + ': ' + data.error.detail);
          }
          max.ui.error({
            title: '500: Internal Server Error',
            content: '서버에서 오류가 발생되었습니다. \n다시 시도해 주세요.'.concat(detail)
          });
        }
        // 예외오류
        else {
          let detail = '';
          if (data && isArray(data.detail)) {
            detail = detail.concat('\n' + data.detail[0].msg);
          }
          max.ui.error({
            title: status + ': ' + statusText,
            content: '서버에서 오류가 발생되었습니다. \n다시 시도해 주세요.'.concat(detail)
          });
        }
      } else {
        max.ui.error({
          title: error.name,
          content: error.message
        });
      }

      // throw error.response;
      return Promise.reject(error);
    }
  );

  return api;
};
