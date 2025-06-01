import { useLoaderData } from 'react-router';
import type { IAnalyzedDocument } from '../queries/types';
import { useMutation } from '@tanstack/react-query';
import { downloadFileMutation } from '../queries/queries';

export default function ResultPage() {
  const document = useLoaderData<IAnalyzedDocument>();

  const { mutateAsync: downloadFile, isPending } = useMutation({
    mutationFn: downloadFileMutation
  });

  const handleDownloadFile = async () => {
    await downloadFile(document._id);
  };

  return (
    <div className='document-viewer-container'>
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
      <div>
        <button disabled={isPending} onClick={handleDownloadFile}>
          Download file
        </button>
      </div>
      <textarea
        style={{
          width: '100%',
          height: '100%',
          resize: 'none'
        }}
        value={document.body}
        disabled
      />
    </div>
  );
}
