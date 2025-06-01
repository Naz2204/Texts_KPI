import axios from 'axios';
import type { IDocument, SearchState } from './types';
import { baseUrl } from '.';

export const analyzeDocumentMutation = async ({
  file,
  numKeywords
}: {
  file: File;
  numKeywords: number;
}) => {
  const fd = new FormData();
  fd.append('document', file);

  const { data } = await axios.post(
    `${baseUrl}/analyze?number_of_keywords=${numKeywords}`,
    fd
  );

  return data;
};

export const searchDocumentsMutation = async ({
  keywords,
  tags,
  doc_class
}: SearchState) => {
  const body = {
    keywords: keywords
      .replace(/[^a-zA-Z0-9]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim(),
    tags: tags.map((tag) => tag.value),
    doc_class: doc_class?.value
  };

  const { data } = await axios.post<IDocument[]>(`${baseUrl}/find`, body);
  data.sort((doc1, doc2) => doc2.matched_count - doc1.matched_count);
  return data;
};

export const getTagsQuery = async () => {
  const { data } = await axios.get<{ name: string }[]>(baseUrl);
  return data.map((tag) => ({ value: tag.name, label: tag.name }));
};
