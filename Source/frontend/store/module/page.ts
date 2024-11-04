import { defineStore } from 'pinia';

export default defineStore('page', {
  persist: true,
  // persist: {
  //   storage: persistedState.localStorage
  // },
  state: () => ({
    header: {
      title: '',
      breadcrumb: ''
    },
    message: {
      show: false,
      opts: {
        type: null,
        icon: null,
        title: '',
        content: '',
        buttons: {
          ok: {
            text: '확인',
            action: function () {}
          },
          cancel: {
            text: '취소',
            action: function () {}
          }
        }
      }
    },
    isLoading: false
  }),
  getters: {},
  actions: {
    setHeader(header: object) {
      this.header = header;
    },
    setLoading(isLoading: boolean) {
      this.isLoading = isLoading;
    },
    setMessage(show: boolean, opts: object) {
      this.message.show = false;
      setTimeout(() => {
        this.message.show = show;
        this.message.opts = opts;
      }, 0);
    }
  }
});
