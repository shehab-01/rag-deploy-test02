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
