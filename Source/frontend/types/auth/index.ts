export interface UserInfo {
  user_id: string;
  user_nm: string;
  user_div: string; // 사용자 구분
  user_type: string; // 사용자 유형
  user_pw: string;
  birth_dt: string;
  sex: string;
  nation: string;
  email: string;
  telno: string;
  nrscr_no: number | null;
  use_yn: string;
  org_id: string | null;
  agencyName?: string;
}

export interface LoginResponse {
  email: string;
  telno: string;
  use_yn: string;
  user_id: string;
  user_nm: string;
  user_type: string;
}

export interface TokenResponse {
  token_type: string;
  access_token: string;
}

export interface LoginUser {
  userName: string;
  userPassword: string;
}

export type UserWithoutPassword = Omit<UserInfo, 'userPassword'>;
