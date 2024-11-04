import type { ResponseExpItem } from '../exp';

export interface ApiResponse {
  status: number;
  msg?: string;
  data?: any;
  content?: any;
}

export interface ExpApiResponse {
  status: number;
  msg?: string;
  data?: ResponseExpItem[];
}
