const lowercaseOnly = helpers.regex('lowercaseOnly', /^[a-z]+$/);

export const loginRules = {
  userName: {
    required: helpers.withMessage('이메일을 입력해주세요', required)
    // 관리자 계정때문에 적용하면 안됨.
    // email: helpers.withMessage('이메일 형식으로 입력해주세요.', email)
  },
  userPassword: {
    required: helpers.withMessage('비밀번호를 입력해주세요.', required)
  }
};

export const CheckUserEmailRules = {
  user_id: {
    required: helpers.withMessage('이메일을 입력해주세요', required),
    email: helpers.withMessage('이메일 형식으로 입력해주세요', email)
  }
};

export const RegisterUserRules = {
  user_id: {
    required: helpers.withMessage('이메일을 입력해주세요', required),
    email: helpers.withMessage('이메일 형식으로 입력해주세요', email)
  },
  agencyName: {
    required: helpers.withMessage('소속 기관을 입력해주세요', required)
  },
  user_pw: {
    required: helpers.withMessage('비밀번호를 입력해주세요', required)
  },
  user_nm: {
    required: helpers.withMessage('이름을 입력해주세요', required)
  },
  birth_dt: {
    required: helpers.withMessage('생일을 입력해주세요', required)
  },
  telno: {
    required: helpers.withMessage('전화번호를 입력해주세요', required)
  },
  nrscr_no: {
    required: helpers.withMessage('연구자 번호를 입력해주세요', required)
  }
};
export const OpenAgencyModalRules = {
  user_id: {
    required: helpers.withMessage('이메일을 입력해주세요', required),
    email: helpers.withMessage('이메일 형식으로 입력해주세요', email)
  },
  user_nm: {
    required: helpers.withMessage('이름을 입력해주세요', required)
  }
};

//TODO
//왜 이렇게 해도 안되는지 모르겠다 타입이 안맞나?
export const SearchOrganizationRules = {
  agencySearchInput: {
    required: helpers.withMessage('기업ID를 입력해주세요', required),
    lowercaseOnly: helpers.withMessage('영어 소문자만 입력 가능합니다', lowercaseOnly)
  }
};

export const CheckOrganizationRules = {
  org_id: {
    required: helpers.withMessage('기관ID를 입력해주세요', required)
    // lowercaseOnly: helpers.withMessage('영어 소문자만 입력 가능합니다', lowercaseOnly)
  }
};

export const RegisterAgencyRules = {
  org_id: {
    required: helpers.withMessage('기관 ID를 입력해주세요', required)
  },
  org_nm: {
    required: helpers.withMessage('기관명을 입력해주세요', required)
  },
  brno: {
    required: helpers.withMessage('사업자 등록번호를 입력해주세요', required)
  },
  // cpno: {
  //   required: helpers.withMessage('법인 등록번호를 입력해주세요', required)
  // },
  // address: {
  //   required: helpers.withMessage('기본 주소를 입력해주세요', required)
  // },
  // addr2: {
  //   required: helpers.withMessage('상세 주소를 입력해주세요', required)
  // },
  homeurl: {
    required: helpers.withMessage('홈페이지를 입력해주세요', required)
  },
  ceo_nm: {
    required: helpers.withMessage('대표자 성명를 입력해주세요', required)
  },
  ceo_email: {
    required: helpers.withMessage('대표자 이메일을 입력해주세요', required)
  },
  mgt_nm: {
    required: helpers.withMessage('기관 책임자 성명을 입력해주세요', required)
  },
  mgt_email: {
    required: helpers.withMessage('기관 책임자 이메일을 입력해주세요', required)
  }
};
