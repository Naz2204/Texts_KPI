import { QueryClient } from '@tanstack/react-query';
import axios from 'axios';

const baseUrl = 'http://localhost:8000';
export const queryClient = new QueryClient();

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
