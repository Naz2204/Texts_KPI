import { useState } from 'react';
import SearchDocuments from './SearchDocuments';
import DocumentList from './DocumentList';
import type { IDocument } from '../../queries/store';

export default function MainPage() {
  const [documents, setDocuments] = useState<IDocument[]>([]);

  return (
    <main>
      <SearchDocuments setDocuments={setDocuments} />
      <DocumentList documents={documents} />
    </main>
  );
}
