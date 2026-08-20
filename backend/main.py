from fastapi import FastAPI, UploadFile, File
from pdf_service import extract_text_from_pdf
import tempfile
import os

app = FastAPI(title="DocuMind AI")


@app.get("/")
def home():
    return {
        "message": "DocuMind AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    content = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(content)
        temp_path = temp.name

    try:
        text = extract_text_from_pdf(temp_path)

        return {
            "filename": file.filename,
            "characters": len(text),
            "text_preview": text[:1000]
        }

    finally:
        os.remove(temp_path)
