/**
 * ----------------------------------------------------------------------------------
 * UI 공통스크립트
 * ----------------------------------------------------------------------------------
 */
// import _ from 'lodash';

const ui = {
  init: function (option: { page: { header?: object; init?: Function } }) {
    const page = option.page || {};
    const header = page.header || {};

    // 헤더 초기화
    if (!isEmpty(page)) {
      // console.log('page.header.set:');
      store.page().setHeader(header);
    }

    // 화면 초기화
    Promise.all([max.ui.setCodeInfo()]).then(function () {
      // Input 초기화
      max.ui.inputInit();

      if (isFunction(page.init)) {
        page.init.call(page);
      }
    });
  },
  headInit: function () {},
  menuInit: function () {},
  inputInit: function () {},
  setCodeInfo: function () {
    return new Promise<void>(function (resolve, reject) {
      // resolve();

      // 공통코드 목록
      let codeInfo = max.storage.session.get('codeInfo');
      if (codeInfo == null) {
        try {
          useApi()
            .request({
              method: 'post',
              url: '/api/code/info',
              data: {}
            })
            .then((result: ApiResponse) => {
              let data: Array<{ cd_id: string; cds_id: string; cds_nm: string }> = result.data || [];
              let codeInfo: any = {};
              data.forEach((info, idx) => {
                if (!codeInfo[info.cd_id]) {
                  codeInfo[info.cd_id] = {};
                }
                codeInfo[info.cd_id][info.cds_id] = info.cds_nm;
              });
              max.storage.session.set('codeInfo', codeInfo);
              resolve();
            })
            .catch(ex => {
              console.error('ex.code.info:', ex);
              reject();
            });
        } catch (e) {
          console.error(e);
          reject();
        }
      } else {
        resolve();
      }
    });
  },
  valid: function (option: Object) {
    this.message('valid', option);
  },
  error: function (option: Object) {
    this.message('error', option);
  },
  alert: function (option: Object) {
    this.message('alert', option);
  },
  confirm: function (option: Object) {
    this.message('confirm', option);
  },
  message: function (type: string, option: any) {
    let opt: { type: string; icon?: string; title?: string; content?: string } = { type: type };
    if (typeof option === 'string') {
      opt.content = option;
    } else if (typeof option === 'object') {
      opt = option;
      opt.type = type;
    }

    if (opt.type === 'valid') {
      opt.icon = 'mdi-alert-circle';
      opt.title = '유효성 검사';
    } else if (opt.type === 'error') {
      opt.icon = 'mdi-close-circle';
    }

    if (opt.content) {
      opt.content = opt.content.replaceAll(/\n/g, '<br/>');
    }

    let opts = useMerge(
      {
        type: '',
        icon: '',
        title: '',
        content: '',
        timeout: 0,
        buttons: {
          ok: {
            text: '확인',
            action: function () {}
          },
          cancel:
            opt.type == 'confirm'
              ? {
                  text: '취소',
                  action: function () {}
                }
              : null
        }
      },
      opt
    );
    setTimeout(() => {
      store.page().setMessage(true, opts);
    }, opts.timeout);
  },
  loading: function (isLoading: boolean) {
    store.page().setLoading(isLoading);
  },
  openWinPopup: function (option: object) {
    let opts = useMerge(
      {
        url: '',
        name: 'blank',
        top: 0,
        left: 0,
        width: screen.width,
        height: screen.height,
        fullscreen: 'yes',
        resizable: 'yes',
        location: 'no',
        menubar: 'yes',
        toolbar: 'no',
        status: 'no'
      },
      option
    );

    let options =
      'top=' +
      opts.top +
      ', left=' +
      opts.left +
      ', width=' +
      opts.width +
      ', height=' +
      opts.height +
      ', fullscreen=' +
      opts.fullscreen +
      ', resizable=' +
      opts.resizable +
      ', location=' +
      opts.location +
      ', menubar=' +
      opts.menubar +
      ', toolbar=' +
      opts.toolbar +
      ', status=' +
      opts.status;

    // TODO: post..
    window.open(opts.url, opts.name, options);
  },
  noImage: function (e: MouseEvent) {
    if (e.target instanceof HTMLImageElement) {
      e.target.src = '/src/assets/img/page/no_img.png';
    }
  }
};

export default ui;
