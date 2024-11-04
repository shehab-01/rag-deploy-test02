export interface TaskData {
  search: SearchData;
}

export interface SearchData {
  searchDiv: string;
  searchInput: string | number;
}

export interface RegisterTaskInfo {
  bidNtceNm: string;
  task_nm: string;
  noticeName: string;
  noticeAgencyName: string;
  contactName: string;
  props_end_dtm: string;
  noticeManageName: string;
  all_task_gov_spamt: number;
  all_task_bgn_dt: string;
  all_task_end_dt: string;
  all_task_end_dt2: string;
  sfbdamt_rate: number;
  cash_sfbdamt_rate: number;
}

export interface TaskInfo {
  registerTaskInfo: RegisterTaskInfo;
  userList: any;
}

export interface BidNtceData {
  search: NtceSearchData;
}

export interface NtceSearchData {
  inqryDiv: string;
  inqryEndDt: number;
  inqryBgnDt: number;
  bidNtceNm: number;
  bidNtceNo: number;
}

// src/types/chat.ts
export interface ChatMessage {
  type: 'Q' | 'Ai';
  content: string;
  source: string;
}

export interface ApiRequest {
  question: string;
  directory_name: string;
  question_lang: 'en' | 'ko';
}

export interface ApiResponse {
  data: any; // Update this based on your actual API response type
}

// You can also add enums if needed
export enum MessageType {
  Question = 'Q',
  AI = 'Ai'
}

// Add any other chat-related types here
export type Language = 'en' | 'ko';
