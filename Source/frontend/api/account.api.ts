const PREFIX = '/api/user';

const accountApi = {
  async getAccount() {
    const response = await useApi().request({
      method: 'get',
      url: `${PREFIX}/info`,
      data: {}
    });
    return response;
  },
  async checkEmail(param: object) {
    const response = await useApi().request({
      method: 'post',
      url: `${PREFIX}/check`,
      data: param
    });
    return response;
  },
  async joinAccount(param: object) {
    const response = await useApi().request({
      method: 'post',
      url: `${PREFIX}/join`,
      data: param
    });
    return response;
  },
  async updateAccount(param: object) {
    const response = await useApi().request({
      method: 'post',
      url: `${PREFIX}/update`,
      data: param
    });
    return response;
  },

  //////////////////////////////////////////////////////////////////////////
  async checkPassword(password: string) {
    const params = new URLSearchParams();
    params.append('password', password);
    const response = await useApi().post(`${PREFIX}/check-password`, params);
    return response;
  },
  async changePassword(password: string) {
    const params = new URLSearchParams();
    params.append('password', password);
    const response = await useApi().post(`${PREFIX}/change-password`, params);
    return response;
  },

  /////////////////////////////////////////////////////////////
  async getOrganizationUserList(param: {}) {
    const response = await useApi().request({
      method: 'post',
      url: `${PREFIX}/list`,
      data: param
    });
    return response;
  }
};

export default accountApi;
