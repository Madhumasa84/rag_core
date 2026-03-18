# src/processors.py

from .extractors import extract_text
from .chunk import chunk_text
from .embed import generate_embeddings
from .load_pdf import clean_text
import chromadb
from chromadb.config import Settings
import os

def process_and_store(file_path: str, collection_name: str = "default"):
    """
    Process any supported file and store in vector DB
    
    Steps:
    1. Extract text based on file type
    2. Clean the extracted text
    3. Split into chunks
    4. Generate embeddings
    5. Store in ChromaDB
    """
    print(f"Processing: {file_path}")
    
    # Step 1: Extract text
    print("  Extracting text...")
    raw_text = extract_text(file_path)
    
    # Step 2: Clean text
    print("  Cleaning text...")
    cleaned_text = clean_text(raw_text)
    
    # Step 3: Chunk
    print("  Creating chunks...")
    chunks = chunk_text(cleaned_text)
    print(f"  → {len(chunks)} chunks created")
    
    # Step 4: Generate embeddings
    print("  Generating embeddings...")
    embeddings = generate_embeddings(chunks)
    print(f"  → Embedding dimension: {len(embeddings[0])}")
    
    # Step 5: Store in Chroma
    print("  Storing in vector database...")
    client = chromadb.Client(
        Settings(
            persist_directory="./chroma_db",
            is_persistent=True
        )
    )
    
    # Delete existing collection if it exists (for fresh upload)
    try:
        client.delete_collection(collection_name)
    except:
        pass  # Collection doesn't exist, that's fine
    
    collection = client.create_collection(name=collection_name)
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[f"{collection_name}_{i}"]
        )
    
    print(f"Successfully stored {len(chunks)} chunks")
    return collection