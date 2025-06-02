from io import BytesIO
from docx import Document
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from reportlab.pdfgen import canvas
from os.path import splitext
import urllib.parse

def write_file(filename: str, text: str) -> StreamingResponse:
    _, extension = splitext(filename)
    #
    # response = None
    match extension:
        case ".docx":
            response = write_docx(filename, text)
        case ".pdf":
            response = write_pdf(filename, text)
        case ".txt":
            response = write_txt(filename, text)
        case _:
            raise HTTPException(status_code=415, detail="Unsupported file type")

    return response

def write_docx(filename: str, text: str) -> StreamingResponse:
    file = BytesIO()
    doc = Document()

    doc.add_paragraph(text)
    doc.save(file)

    encoded_name = urllib.parse.quote(filename)
    file.seek(0)
    return StreamingResponse(
        content = file,
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"
        }
    )

def write_txt(filename: str, text: str) -> StreamingResponse:
    file = BytesIO()
    file.write(text.encode('utf-8'))

    encoded_name = urllib.parse.quote(filename)
    file.seek(0)
    return StreamingResponse(
        content = file,
        media_type = "text/plain",
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"
        }
    )

def write_pdf(filename: str, text: str) -> StreamingResponse:
    file = BytesIO()

    canv = canvas.Canvas(file)
    text_object = canv.beginText()
    text_object.setTextOrigin(40, 800)

    lines = text.split('\n')
    for line in lines:
        text_object.textLine(line)

    canv.drawText(text_object)
    canv.showPage()
    canv.save()

    encoded_name = urllib.parse.quote(filename)
    file.seek(0)
    return StreamingResponse(
        content=file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"
        }
    )
