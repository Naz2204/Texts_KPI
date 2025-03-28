import pymongo as pm
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    db_client = pm.MongoClient(os.getenv("DB_ADDRESS"))
    db = db_client["Texts"]
    db_collection = db["documents"]

    print("Before delete ", db_collection.find({"body": "BODYA"}).to_list())

    db_collection.delete_many({"body": "BODYA"})

    print("After delete", db_collection.find({"body": "BODYA"}).to_list())

if __name__ == "__main__":
    main()