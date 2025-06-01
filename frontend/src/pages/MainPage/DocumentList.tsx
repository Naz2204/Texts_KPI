import { Link } from 'react-router';
import { useSearchStore } from '../../store/store';

export default function DocumentList() {
  const { searchResult: documents } = useSearchStore();

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
