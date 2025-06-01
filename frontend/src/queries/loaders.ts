import type { LoaderFunction } from 'react-router';
import type { IAnalyzedDocument } from './types';
import axios from 'axios';
import { baseUrl } from '.';

export const getAnalyzedFileLoader: LoaderFunction<{ id: string }> = async ({
  params
}) => {
  const { data } = await axios.get<IAnalyzedDocument>(
    `${baseUrl}/find/${params.id}`
  );
  return data;
};
