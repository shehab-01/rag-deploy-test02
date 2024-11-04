/**
 * ----------------------------------------------------------------------------------
 * 유틸 공통스크립트
 * ----------------------------------------------------------------------------------
 */
// import _ from 'lodash';
// import { helpers } from '@vuelidate/validators';

const util = {
  /**
   * validate
   */
  validate: function (rules: object, data: any) {
    return new Promise<void>(async (resolve, reject) => {
      let messages: Array<any> = [];
      let v$ = useVuelidate(rules, data);
      let valid = await v$.value.$validate();
      // v$.value.$validate().then(result => {});
      v$.value.$errors.forEach((item, idx) => {
        messages.push(item.$message);
      });
      if (messages.length > 0) {
        max.ui.valid(messages.join('\n'));
        reject(messages);
      }
      resolve();
    });
  },
  /**
   * Axios
   */
  axios: async function (options: object) {},
  /**
   * 전체 문자치환
   *
   * @param strString
   * @param strAfter
   * @param strNext
   * @returns
   */
  replaceAll: function (strString: string, strAfter: string, strNext: string) {
    var tmpStr = strString;
    while (tmpStr.indexOf(strAfter) != -1) {
      tmpStr = tmpStr.replace(strAfter, strNext);
    }
    return tmpStr;
  },
  /**
   * 좌측패딩
   */
  lpad: function (str: string, padLen: number, padStr: string) {
    str += '';
    padStr += '';
    if (padStr.length > padLen) {
      return str;
    }
    while (str.length < padLen) {
      str = padStr + str;
    }
    str = str.length >= padLen ? str.substring(0, padLen) : str;
    return str;
  },
  /**
   * 우측패딩
   */
  rpad: function (str: string, padLen: number, padStr: string) {
    str += '';
    padStr += '';
    if (padStr.length > padLen) {
      return str;
    }
    while (str.length < padLen) {
      str += padStr;
    }
    str = str.length >= padLen ? str.substring(0, padLen) : str;
    return str;
  },
  /**
   * 오늘날짜
   * @param separator
   */
  getCurrTime: function () {
    var now: any = new Date();
    var day: any = now.getDate();
    var month: any = now.getMonth() + 1;
    var year = now.getFullYear();
    var hours = this.lpad(now.getHours(), 2, '0');
    var minutes = this.lpad(now.getMinutes(), 2, '0');
    var seconds = this.lpad(now.getSeconds(), 2, '0');

    if (day < 10) {
      day = '0' + day;
    }
    if (month < 10) {
      month = '0' + month;
    }
    now = year + '' + month + '' + day + '_' + hours + '' + minutes + '' + seconds;
    return now;
  },
  /**
   * 오늘날짜
   * @param separator
   */
  getToday: function (separator: string): string {
    let today: any = new Date();
    let day: any = today.getDate();
    let month: any = today.getMonth() + 1;
    let year = today.getFullYear();

    if (day < 10) {
      day = '0' + day;
    }
    if (month < 10) {
      month = '0' + month;
    }
    if (typeof separator === 'undefined') {
      //separator = "-";
      separator = '';
    }
    today = year + separator + month + separator + day;
    return today;
  },
  /**
   * 파일다운로드
   */
  downloadFile: function () {},
  downloadExcel: function (url: string, param: object) {},
  /**
   * 이미지처리
   */
  image: {
    getFileFromUrl: async function (url: string, type: string) {
      if (typeof window === 'undefined') return;
      const ext = url.substr(url.lastIndexOf('.') + 1, url.length).toLowerCase();
      const response = await fetch(url);
      const data = await response.blob();
      const metadata = {
        type: type || 'image/' + ext
      };
      return new File([data], url, metadata);
    }
  }
};

export default util;
