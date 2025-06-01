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
      <h1><span>{document.name}</span></h1>
      <div className='metadata-block'>
        <div className='info-block'>
          <label>Document class: </label>
          <span>{document.class}</span>
        </div>
        <div className='info-block'>
          <label>Document tags: </label>
          <span>{document.tags.join(', ')}</span>
        </div>
        <div className='info-block'>
          <label>Document topics: </label>
          <span>{document.topics.join(', ')}</span>
        </div>
        <div className='download-button-wrapper'>
          <button disabled={isPending} onClick={handleDownloadFile}>
            Download file
          </button>
        </div>
      </div>
      <div className='text-area-wrapper'>
        <textarea
          className='document-body-textarea'
          value={document.body}
          disabled

        />
      </div>
    </div>
  );
}
