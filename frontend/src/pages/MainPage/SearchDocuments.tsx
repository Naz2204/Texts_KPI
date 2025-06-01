import { useMutation, useQuery } from '@tanstack/react-query';
import { getTagsQuery, searchDocumentsMutation } from '../../queries/queries';
import Select from 'react-select';
import { availableClasses } from '../../config/availableClasses';
import { useSearchStore } from '../../store/store';

export default function SearchDocuments() {
  const {
    tags,
    doc_class,
    keywords,
    setTags,
    setClass,
    setKeywords,
    setSearchResult
  } = useSearchStore();

  const { mutateAsync: search, isPending: isSearching } = useMutation({
    mutationFn: searchDocumentsMutation
  });

  const { data: availableTags, isFetching: areTagsFetching } = useQuery({
    queryKey: ['tags'],
    queryFn: getTagsQuery,
    refetchOnWindowFocus: false
  });

  const handleSearch = async () => {
    const documents = await search({ tags, doc_class, keywords });
    setSearchResult(documents);
  };

  return (
    <div>
      <div>
        <label>Select class</label>
        <Select
          defaultValue={doc_class}
          options={availableClasses}
          onChange={(newClass) => setClass(newClass)}
        />
      </div>
      {!areTagsFetching && (
        <div>
          <label>Select tags</label>
          <Select
            defaultValue={tags}
            isMulti
            options={availableTags}
            onChange={(newTags) => setTags(newTags)}
          />
        </div>
      )}
      <div>
        <label>Enter keywords</label>
        <textarea onChange={(e) => setKeywords(e.target.value)} />
      </div>

      <button disabled={isSearching} onClick={handleSearch}>
        Search
      </button>
    </div>
  );
}
