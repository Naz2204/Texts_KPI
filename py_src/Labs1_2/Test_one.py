import pymongo as pm
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    db_client = pm.MongoClient(os.getenv("DB_ADDRESS"))
    db = db_client["Texts"]
    db_collection = db["topics"]

    print("Before delete ", db_collection.find_one({"name": "TOPIC3"}))

    db_collection.delete_one({"name": "TOPIC3"})

    print("After delete", db_collection.find_one({"name": "TOPIC3"}))

if __name__ == "__main__":
    main()