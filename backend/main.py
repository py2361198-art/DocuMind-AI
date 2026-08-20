from fastapi import FastAPI, UploadFile, File
from pdf_service import extract_text_from_pdf
from chunking import split_text
from rag import RAGSystem
import tempfile
import os

app = FastAPI(title="DocuMind AI")

rag_system = RAGSystem()


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

        rag_system.add_documents(chunks)

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

    results = rag_system.search(question)

    return {
        "question": question,
        "relevant_chunks": results
    }
