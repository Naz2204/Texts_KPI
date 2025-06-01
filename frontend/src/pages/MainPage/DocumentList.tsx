import { Link } from 'react-router';
import type { IDocument } from '../../queries/store';

interface Params {
  documents: IDocument[];
}

export default function DocumentList({ documents }: Params) {
  return (
    <ul>
      {documents.map((doc) => (
        <li key={doc._id}>
          <Link to={`/${doc._id}`}>{doc.name}</Link>
          {!!doc.keywords_matched.length && (
            <p>Matches by: {doc.keywords_matched.join(',')}</p>
          )}
        </li>
      ))}
    </ul>
  );
}
