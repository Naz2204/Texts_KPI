import SearchDocuments from './SearchDocuments';
import UploadDocument from './UploadDocument';

export default function Header() {
  return (
    <header>
      <SearchDocuments />
      <UploadDocument />
    </header>
  );
}
