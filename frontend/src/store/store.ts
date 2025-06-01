import { create } from 'zustand';
import { type MultiValue, type SingleValue } from 'react-select';
import type { IDocument, Option } from '../queries/types';

export interface SearchState {
  tags: MultiValue<Option>;
  doc_class: SingleValue<Option>;
  keywords: string;
  searchResult: IDocument[];
  setSearchResult: (searchResult: IDocument[]) => void;
  setTags: (tags: MultiValue<Option>) => void;
  setClass: (doc_class: SingleValue<Option>) => void;
  setKeywords: (keywords: string) => void;
}

export const useSearchStore = create<SearchState>((set) => ({
  tags: [],
  doc_class: null,
  keywords: '',
  searchResult: [],
  setSearchResult: (searchResult) => set({ searchResult }),
  setTags: (tags) => set({ tags }),
  setClass: (doc_class) => set({ doc_class }),
  setKeywords: (keywords) => set({ keywords })
}));
