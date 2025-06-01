from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functions import Functions
from my_utils.document_structure import RequestBody

app = FastAPI()
functions = Functions()

origins = [
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def get_tags():
    return await functions.get_tags()

@app.post('/analyze')
async def analyze(document: UploadFile, number_of_keywords: int):
    return await functions.analyze(document, number_of_keywords)

@app.post('/find')
async def complex_find(request: RequestBody):
    return await functions.complex_find(request.keywords, request.tags, request.doc_class)

@app.get('/find/{doc_id}')
async def find_by_id(doc_id: str):
    document = await functions.get_doc_by_id(doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    else:
        return document

@app.post('/download/{doc_id}')
async def download_document(doc_id: str):
    document = await functions.get_doc_by_id(doc_id)
    print(document["name"])
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    else:
        return Functions.download_file(document["name"], document["body"])
