# src/processors.py

import uuid
import chromadb
from chromadb.config import Settings
from .extractors import extract_text
from .chunk import chunk_text
from .embed import generate_embeddings
from .load_pdf import clean_text

def process_and_store(file_path: str, collection_name: str = "default"):
    """
    Process any supported file and store in vector DB
    
    Steps:
    1. Extract text based on file type
    2. Clean the extracted text
    3. Split into chunks
    4. Generate embeddings
    5. Store in ChromaDB using PersistentClient and UUIDs
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
    
    # Step 5: Store in Chroma using updated API
    print("  Storing in vector database...")
    
    # Use PersistentClient (new API - not deprecated)
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if it exists (for fresh upload)
    try:
        client.delete_collection(collection_name)
        print(f"  Removed existing collection: {collection_name}")
    except:
        pass  # Collection doesn't exist, that's fine
    
    # Create new collection
    collection = client.create_collection(name=collection_name)
    
    # Use UUID for unique IDs to avoid collisions
    chunk_ids = []
    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())  # Unique ID per chunk
        chunk_ids.append(chunk_id)
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[chunk_id]
        )
    
    print(f"Successfully stored {len(chunks)} chunks with UUID IDs")
    return collection