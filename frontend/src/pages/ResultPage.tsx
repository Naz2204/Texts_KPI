import { useLoaderData } from 'react-router';
import type { IAnalyzedDocument } from '../queries/types';

export default function ResultPage() {
  const document = useLoaderData<IAnalyzedDocument>();

  return (
    <div style={{ height: '90vh' }}>
      <div>
        <label>Document name: </label>
        <span>{document.name}</span>
      </div>
      <div>
        <label>Document class: </label>
        <span>{document.class}</span>
      </div>
      <div>
        <label>Document tags: </label>
        <span>{document.tags.join(', ')}</span>
      </div>
      <div>
        <label>Document topics: </label>
        <span>{document.topics.join(', ')}</span>
      </div>
      <textarea
        style={{
          width: '100%',
          height: '100%',
          resize: 'none'
        }}
        disabled>
        {document.body}
      </textarea>
    </div>
  );
}
