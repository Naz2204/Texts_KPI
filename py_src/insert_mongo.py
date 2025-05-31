import pymongo as pm
import os
from dotenv import load_dotenv
from pypdf import PdfReader
from datetime import datetime, UTC


def read_data(filename:str):
    text = ""
    if filename.endswith(".pdf"):
        reader = PdfReader(filename)

        for page in reader.pages:
            text += page.extract_text()
    else:
        with open(filename, "r") as file:
            for row in file.readline():
                text += row

    return text

def load_document(db):
    db = db["documents"]

    filename = "the-yellow-fairy-book-038-the-tinder-box (1).pdf"
    load = read_data(filename)

    file_size = os.stat(filename).st_size
    data_to_load = {
        "body" : load,
        "metadata" : {
            "name" : filename,
            "size" : file_size
        },
        "createdAt": datetime.now(UTC),
        "updatedAt": datetime.now(UTC),
        "tags": ["Grim"],
        "rating": 7,
        "__v": 0
    }

    db.insert_one(data_to_load)

def load_tags(db, data):
    db = db["tags"]

    tags = []

    for i in data:
        tags.append({
            "name": i,
            "createdAt": datetime.now(UTC),
            "updatedAt": datetime.now(UTC)
        })

    db.insert_many(tags)

def load_topics(db, topics):
    db = db["topics"]
    ids = []
    for i in topics:
        if len(i) == 2:
            data = {
                "name": i[0],
                "parent": ids[i[1]],
                "createdAt": datetime.now(UTC),
                "updatedAt": datetime.now(UTC),
                "isRoot": False,
                "__v": 0
            }
            print(data)
        else:
            data = {
                "name": i[0],
                "createdAt": datetime.now(UTC),
                "updatedAt": datetime.now(UTC),
                "isRoot": True,
                "__v": 0
            }

        x = db.insert_one(data).inserted_id
        ids.append(x)

def main():
    load_dotenv()

    db_client = pm.MongoClient(os.getenv("DB_ADDRESS"))
    db = db_client["Texts"]

    #load_document(db)

    #load_tags(db, ["Grim", "Data", "Trash"])

    data = [
        ["Test parent topic4"],
        ["2", 0]
    ]
    load_topics(db, data)

if __name__ == "__main__":
    main()
