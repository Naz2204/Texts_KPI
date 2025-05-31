from utils.readers import read_text
from fastapi import UploadFile
from db_connect import DbConnector
from utils.topic_extraction import find_topic
from utils.classify_text import classify
from utils.clusterize_texts import assign_new_document_lda, cluster_documents_and_generate_tags_lda

class Functions:
    def __init__(self):
        self._client = DbConnector()

    async def upload_to_db(self, document: UploadFile):
        await self._client.check_connection()
        text = await read_text(document)

        return text

    async def analyze(self, document: UploadFile, number_of_words: int) -> tuple[list[str], str, list[str]]:
        text = await read_text(document)

        topics = find_topic(text, number_of_words)

        classified = classify(text)

        cluster, tags = assign_new_document_lda(text)

        return topics, classified, tags