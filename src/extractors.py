# src/extractors.py

from pypdf import PdfReader
import os

def extract_from_pdf(path: str) -> str:
    """Extract text from PDF file"""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text(path: str) -> str:
    """
    Universal extractor - detects file type and extracts text
    Currently supports PDF only. PPT/HTML/TXT coming next.
    """
    ext = os.path.splitext(path)[1].lower()
    
    if ext == '.pdf':
        return extract_from_pdf(path)
    else:
        # For now, raise error for unsupported types
        raise ValueError(f"File type {ext} not yet supported. Currently only PDF works.")