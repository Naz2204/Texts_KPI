import { useMutation, useQuery } from '@tanstack/react-query';
import {
  getTagsQuery,
  searchDocumentsMutation,
  type IDocument
} from '../../queries/store';
import Select, { type MultiValue, type SingleValue } from 'react-select';
import {
  useReducer,
  type ChangeEventHandler,
  type Dispatch,
  type SetStateAction
} from 'react';
import { availableClasses } from '../../config/availableClasses';

interface Params {
  setDocuments: Dispatch<SetStateAction<IDocument[]>>;
}

type Option = { value: string; label: string };

export type SearchState = {
  tags: MultiValue<Option>;
  doc_class: SingleValue<Option>;
  keywords: string;
};

type Action =
  | { type: 'SET_TAGS'; payload: MultiValue<Option> }
  | { type: 'SET_CLASS'; payload: SingleValue<Option> }
  | { type: 'SET_KEYWORDS'; payload: string };

const initialState: SearchState = {
  tags: [],
  doc_class: availableClasses[0],
  keywords: ''
};

function reducer(state: SearchState, action: Action): SearchState {
  switch (action.type) {
    case 'SET_TAGS':
      return { ...state, tags: action.payload };
    case 'SET_CLASS':
      return { ...state, doc_class: action.payload };
    case 'SET_KEYWORDS':
      return { ...state, keywords: action.payload };
    default:
      return state;
  }
}

export default function SearchDocuments({ setDocuments }: Params) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const { mutateAsync: search, isPending: isSearching } = useMutation({
    mutationFn: searchDocumentsMutation
  });

  const { data: tags, isFetching: areTagsFetching } = useQuery({
    queryKey: ['tags'],
    queryFn: getTagsQuery,
    refetchOnWindowFocus: false
  });

  const handleSelectClass = (newClass: SingleValue<Option>) =>
    dispatch({ type: 'SET_CLASS', payload: newClass });

  const handleSelectTags = (newTags: MultiValue<Option>) =>
    dispatch({ type: 'SET_TAGS', payload: newTags });

  const handleSetKeywords: ChangeEventHandler<HTMLTextAreaElement> = (e) =>
    dispatch({ type: 'SET_KEYWORDS', payload: e.target.value });

  const handleSearch = async () => {
    const documents = await search(state);
    setDocuments(documents);
  };

  return (
    <div>
      <div>
        <label>Select class</label>
        <Select
          defaultValue={state.doc_class}
          options={availableClasses}
          onChange={handleSelectClass}
        />
      </div>
      {!areTagsFetching && (
        <div>
          <label>Select tags</label>
          <Select
            defaultValue={state.tags}
            isMulti
            options={tags}
            onChange={handleSelectTags}
          />
        </div>
      )}
      <div>
        <label>Enter keywords</label>
        <textarea onChange={handleSetKeywords} />
      </div>

      <button disabled={isSearching} onClick={handleSearch}>
        Search
      </button>
    </div>
  );
}
