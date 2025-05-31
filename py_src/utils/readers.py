from io import BytesIO
from docx import Document
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader


async def docx_reader(file: UploadFile):
    reader = Document(BytesIO(await file.read()))
    text = "".join([para.text for para in reader.paragraphs])
    print(text)
    return text

async def pdf_reader(file: UploadFile):
    reader = PdfReader(BytesIO(await file.read()))
    text = "".join([page.extract_text() for page in reader.pages])
    print(text)
    return text

async def txt_reader(file: UploadFile):
    data = await file.read()
    text = data.decode("utf-8")
    print(text)
    return text

async def read_text(document: UploadFile) -> str:
    match document.content_type:
        case "application/pdf":
            text = await pdf_reader(document)
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = await docx_reader(document)
        case "text/plain":
            text = await txt_reader(document)
        case _:
            raise HTTPException(status_code=415, detail="Unsupported file type")
    return text