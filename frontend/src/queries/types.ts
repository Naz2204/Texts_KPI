import type { MultiValue, SingleValue } from 'react-select';

export type Option = { value: string; label: string };

export interface IDocument {
  keywords_matched: string[];
  matched_count: number;
  name: string;
  _id: string;
}

export interface IAnalyzedDocument {
  body: string;
  class: string;
  tags: string[];
  topics: string[];
  name: string;
  _id: string;
}

export interface SearchState {
  tags: MultiValue<Option>;
  doc_class: SingleValue<Option>;
  keywords: string;
}
