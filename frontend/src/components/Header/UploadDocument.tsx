import { useRef, useState, type ChangeEventHandler } from 'react';
import { allowedFileTypes } from '../../config/allowedFileTypes';
import { useMutation } from '@tanstack/react-query';
import { analyzeDocumentMutation } from '../../queries/store';

export default function UploadDocument() {
  const { mutateAsync: analyzeFile, isPending } = useMutation({
    mutationFn: analyzeDocumentMutation
  });

  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const keywordsAmountInputRef = useRef<HTMLInputElement>(null);

  const handleSelectFile = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleUploadFile: ChangeEventHandler<HTMLInputElement> = (e) => {
    const file = e.target.files?.item(0);
    if (file) {
      setFile(file);
      e.target.value = '';
    }
  };

  const handleAnalyzeFile = async () => {
    const numKeywords = keywordsAmountInputRef.current?.value || 4;

    const res = await analyzeFile({
      file: file!,
      numKeywords: +numKeywords
    });

    console.log(res);
  };

  return (
    <div>
      <input
        type="file"
        hidden
        ref={fileInputRef}
        onChange={handleUploadFile}
        accept={allowedFileTypes}
      />
      <button disabled={isPending} onClick={handleSelectFile}>
        Upload document
      </button>
      {file && (
        <div>
          <p>{file.name}</p>
          <label>How many keywords to extract?</label>
          <input type="number" defaultValue={4} ref={keywordsAmountInputRef} />
          <button onClick={handleAnalyzeFile}>Analyze document</button>
        </div>
      )}
    </div>
  );
}
