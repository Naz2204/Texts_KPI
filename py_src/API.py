from fastapi import FastAPI, UploadFile
from functions import Functions
app = FastAPI()
functions = Functions()

@app.get('/')
def root():
    return {"Hello": "World"}


@app.post('/upload/text')
async def upload_text(document: UploadFile):
    return {"text": await functions.upload(document)}

@app.post('/upload/topic')
async def upload_tag(name: str, is_root: bool = True, parent_id: str = None):
    return {"name": name, "isRoot": is_root, "parent_id": parent_id}

@app.post('/analyze')
async def analyze(document: UploadFile, number_of_words: int):
    print("10")
    topics, classified, cluster = await functions.analyze(document, number_of_words)
    print(type(topics), topics)
    print(type(classified), classified)
    print(type(cluster), cluster)

    result = {
        "topics": topics,
        "class": classified,
        "tags": cluster
    }
    return result