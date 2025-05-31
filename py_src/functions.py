from utils.readers import read_text
from fastapi import UploadFile
from db_connect import DbConnector


class Functions:
    def __init__(self):
        self._client = DbConnector()

    async def upload(self, document: UploadFile):
        await self._client.check_connection()
        text = await read_text(document)
        return text