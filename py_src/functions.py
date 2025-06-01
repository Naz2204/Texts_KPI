from my_utils.document_structure import Document
from my_utils.readers import read_text
from my_utils.writers import write_file
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from db_connect import DbConnector
from my_utils.topic_extraction import find_topic
from my_utils.classify_text import classify
from my_utils.clusterize_texts import assign_new_document_lda, cluster_documents_and_generate_tags_lda
import datetime
from pathlib import Path

class Functions:
    def __init__(self):
        self._client = DbConnector()

    async def analyze(self, document: UploadFile, number_of_words: int) -> str:
        text = await read_text(document)

        topics = find_topic(text, number_of_words)

        classified = classify(text)

        cluster, tags = assign_new_document_lda(text)

        doc = Document(body=text, topics=topics, metadata={"name": document.filename, "size": document.size}, cluster_id=cluster,
                       document_class=classified, createdAt=datetime.datetime.now(datetime.UTC), updatedAt=datetime.datetime.now(datetime.UTC))

        doc_id = await self._client.add_new_document(doc)
        return doc_id

    async def get_tags(self) -> list[str]:
        tags = await self._client.get_all_tags()
        return tags

    async def complex_find(self, search_string: str|None, tags: list[str]|None, doc_class: str|None):
        if search_string:
            keywords = search_string.split(" ")
        else:
            keywords = None
        result = await self._client.get_document_by_complex_filter(tags, keywords, doc_class)
        return result

    async def get_doc_by_id(self, doc_id: str):
        info = await self._client.get_document_by_id(doc_id)
        return info

    @staticmethod
    def _find_all_files(path: Path):
        from pypdf import PdfReader
        import re

        all_docs = []
        for i in path.iterdir():
            if i.is_file():
                if i.suffix not in [".docx", ".doc", ".pdf", ".txt"]: continue

                name = i.name
                doc_class = i.parent.name
                size = i.stat().st_size

                reader = PdfReader(i)
                body = "".join([page.extract_text() for page in reader.pages])

                def clean_text(text):
                    if isinstance(text, str):
                        return re.sub(r'[\ud800-\udfff]', '', text)  # remove surrogate pairs
                    return text

                body = clean_text(body)

                topics = find_topic(body, 5)

                all_docs.append(Document(body=body, topics=topics, metadata={"name": name, "size": size}, document_class=doc_class,
                                         createdAt=datetime.datetime.now(datetime.UTC),
                                         updatedAt=datetime.datetime.now(datetime.UTC)).model_dump(by_alias=True))
            else:
                result = Functions._find_all_files(i)
                all_docs.extend(result)
        return all_docs

    async def load_initial_dataset(self):

        training_data_file_path = Path(__file__).parent / 'training_data'
        all_docs = Functions._find_all_files(training_data_file_path)
        print("Documents parsed")

        await self._client.add_many_documents(all_docs)
        print("Documents inserted")

        texts = await self._client.get_all_documents_texts()
        print("Texts pulled from db")

        cluster_tags, id_cluster_pairs = cluster_documents_and_generate_tags_lda(texts)
        print("Clusterized")

        await self._client.add_clusters_and_tags(cluster_tags)
        print("Clusters saved")

        for i in id_cluster_pairs:
            await self._client.update_document(i[0], i[1])
        print("Documents updated")

    @staticmethod
    def download_file(filename: str, text: str) -> StreamingResponse:
        return write_file(filename, text)


def main():
    import asyncio
    functions = Functions()
    asyncio.run(functions.load_initial_dataset())

if __name__ == "__main__":
    main()