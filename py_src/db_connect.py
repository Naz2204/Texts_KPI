import datetime
import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient, errors
from my_utils.document_structure import Document, Tag, Cluster
from bson import ObjectId

class DbConnector:

    def __init__(self):
        self._db_client = DbConnector._open_connection()
        self._db = self._db_client["Texts"]

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

    async def add_new_document(self, document: Document) -> str:
        db_collection = self._db["documents"]

        document_id = (await db_collection.insert_one(document.model_dump(by_alias=True))).inserted_id
        return str(document_id)

    async def add_many_documents(self, documents: list[dict]):
        db_collection = self._db["documents"]
        await db_collection.insert_many(documents)

    async def update_document(self, document_id: str, cluster_id: int):
        db_collection = self._db["documents"]
        await db_collection.update_one({"_id": document_id},
                                       {"$set": {"cluster_id": int(cluster_id), "updatedAt": datetime.datetime.now(datetime.UTC)}, "$inc": {"__v": 1}, })

    async def add_clusters_and_tags(self, clusters: dict):

        if not clusters:
            return

        prepared_clusters = []
        for cluster_id, cluster_tags in clusters.items():
            prepared_clusters.append(Cluster(cluster_id=cluster_id, tags=cluster_tags,
                                             createdAt=datetime.datetime.now(datetime.UTC),
                                             updatedAt=datetime.datetime.now(datetime.UTC)).model_dump(by_alias=True))

        db_collection = self._db["clusters"]
        await db_collection.delete_many({})
        await db_collection.insert_many(prepared_clusters)


        unique_tags = set()

        for cluster_tags in clusters.values():
            unique_tags.update(cluster_tags)

        to_push = []
        for tag in unique_tags:
            to_push.append(Tag(name=tag,
                               createdAt=datetime.datetime.now(datetime.UTC),
                               updatedAt=datetime.datetime.now(datetime.UTC)).model_dump(by_alias=True))

        db_collection = self._db["tags"]
        await db_collection.delete_many({})
        await db_collection.insert_many(to_push)

    async def get_all_documents_texts(self) -> list[dict]:
        db_collection = self._db["documents"]
        data = await db_collection.find({}, {"_id": 1, "body": 1}).to_list()
        return data

    async def get_all_tags(self) -> list[str]:
        db_collection = self._db["tags"]

        tags = await db_collection.find({}, {"_id": 0, "name": 1}).to_list()
        return tags

    async def get_document_by_id(self, document_id: str) -> dict:
        db_collection = self._db["documents"]

        document = await db_collection.find_one({"_id": ObjectId(document_id)}, {"createdAt": 0, "updatedAt": 0, "__v": 0})

        if document:
            name = document["metadata"]["name"]
            document["_id"] = str(document["_id"])
            if name is not None:
                document["name"] = name
            else:
                document["name"] = "Unknown"

            document.pop("metadata", None)

            db_collection = self._db["clusters"]

            tags = await db_collection.find_one({"cluster_id": document["cluster_id"]}, {"tags":1})

            if tags:
                document["tags"] = tags["tags"]
            else:
                document["tags"] = []

            document.pop("cluster_id", None)

        return document

    async def get_document_by_complex_filter(self, tags: list[str]|None, keywords: list[str]|None, doc_class: str|None) -> list[dict]:
        cluster_ids = []
        if tags:
            db_collection = self._db["clusters"]
            data = await db_collection.find({
                "tags": {"$all": tags}
            }, {"_id": 0, "cluster_id": 1}).to_list()

            for entry in data:
                cluster_ids.append(entry["cluster_id"])

        if tags and not cluster_ids:
            search_result = []
            print("here")
        else:
            complex_filter = {}

            if cluster_ids:
                complex_filter["cluster_id"] = {"$in": cluster_ids}

            if keywords:
                complex_filter["topics"] = {"$in": keywords}

            if doc_class:
                complex_filter["class"] = doc_class

            db_collection = self._db["documents"]

            data = await db_collection.find(complex_filter, {"_id": 1, "metadata": 1, "topics": 1}).to_list()

            search_result = []
            if data:
                for entry in data:
                    if keywords:
                        matched = list(set(keywords) & set(entry["topics"]))
                        matched_len = len(matched)
                    else:
                        matched = []
                        matched_len = 0

                    search_result.append({
                        "_id": str(entry["_id"]),
                        "name": entry["metadata"]["name"],
                        "keywords_matched": matched,
                        "matched_count": matched_len
                    })

        return search_result
