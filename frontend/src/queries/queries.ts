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

export const downloadFileMutation = async (id: string) => {
  try {
    const response = await fetch(`${baseUrl}/download/${id}`, {
      method: 'POST'
    });

    if (!response.ok) throw new Error('Failed to download file');

    const blob = await response.blob();

    // Extract filename from content-disposition header
    const disposition = response.headers.get('Content-Disposition');
    let filename = 'downloaded_file.docx';

    if (disposition) {
      const match = disposition.match(/filename\*?=['"]?UTF-8''([^;'" ]+)/);
      if (match && match[1]) {
        filename = decodeURIComponent(match[1]);
      }
    }

    // Create a temporary link and trigger the download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Download failed:', error);
    alert('Failed to download file.');
  }
};
