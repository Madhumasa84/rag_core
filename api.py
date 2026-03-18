# api.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path

app = FastAPI(title="Document QA API", version="1.0")

# Creating upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
    return {"message": "Document QA API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a document (PDF, PPT, HTML, TXT)
    """
    try:
        # Saves file
        file_path = UPLOAD_DIR / file.filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "filename": file.filename,
            "size": file_path.stat().st_size,
            "message": "File uploaded successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def ask_question(question: str, filename: str = None):
    """
    Ask a question about uploaded document(s)
    """
    return {
        "question": question,
        "filename": filename,
        "answer": "Answer generation will be implemented next",
        "status": "pending"
    }