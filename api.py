# api.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
from fastapi import Form
from src.processors import process_and_store
import uuid

app = FastAPI(title="Document QA API", version="1.0")
file_registry = {}
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
    Upload and process a document (PDF, PPT, HTML, TXT)
    """
    try:
        # Generate unique ID
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Check if supported
        supported = ['.pdf', '.pptx', '.ppt', '.html', '.htm', '.txt']
        if file_ext not in supported:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Supported: {supported}"
            )
        
        # Save file
        file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size safely
        file_size = os.path.getsize(file_path)
        
        # Process the file
        collection_name = f"doc_{file_id}"
        process_and_store(str(file_path), collection_name)
        
        # Register
        file_registry[file_id] = {
            "filename": file.filename,
            "path": str(file_path),
            "collection": collection_name
        }
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": file_size,
            "message": "File uploaded and processed successfully"
        }
    
    except Exception as e:
        print(f"ERROR: {str(e)}")  # This will show in console
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