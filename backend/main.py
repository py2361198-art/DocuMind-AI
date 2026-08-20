from fastapi import FastAPI, UploadFile, File
from pdf_service import extract_text_from_pdf
from chunking import split_text
from rag import answer_question
import tempfile
import os

app = FastAPI(title="DocuMind AI")

document_chunks = []


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
    global document_chunks

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    content = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:
        temp.write(content)
        temp_path = temp.name

    try:
        text = extract_text_from_pdf(temp_path)
        chunks = split_text(text)

        if not chunks:
            return {
                "error": "No readable text found in PDF"
            }

        document_chunks = chunks

        return {
            "filename": file.filename,
            "characters": len(text),
            "chunks": len(chunks),
            "message": "PDF processed successfully"
        }

    finally:
        os.remove(temp_path)


@app.post("/ask")
async def ask_question(question: str):
    if not document_chunks:
        return {
            "error": "Please upload a PDF first"
        }

    answer = answer_question(
        question,
        document_chunks
    )

    return {
        "question": question,
        "answer": answer
    }
