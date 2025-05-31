from dotenv import load_dotenv
from pymongo import AsyncMongoClient, errors
import os




class DbConnector:

    def __init__(self):
        self._db_client = DbConnector._open_connection()

    @staticmethod
    def _open_connection():
        load_dotenv()
        client = AsyncMongoClient(os.getenv("DB_ADDRESS"))
        return client

    async def check_connection(self):
        try:
            await self._db_client.admin.command('ping')
            print("MongoDB connection successful!")
        except errors.ConnectionFailure:
            print("MongoDB connection failed.")
