from fastapi import FastAPI

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
