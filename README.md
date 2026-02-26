PDF Semantic Search (Minimal RAG Core)
Overview

This project implements a minimal semantic search pipeline over a PDF document.

Instead of performing keyword-based search, the system converts text into dense vector representations (embeddings) using a pre-trained Sentence Transformer model. These vectors are stored in a Chroma vector database, enabling similarity-based retrieval using cosine similarity.

This demonstrates the core retrieval component used in Retrieval-Augmented Generation (RAG) systems.

Architecture
Pipeline Steps

Extract raw text from PDF

Split text into overlapping chunks

Convert each chunk into a 384-dimensional embedding using all-MiniLM-L6-v2

Store embeddings in ChromaDB (persistent storage)

Embed the user query using the same model

Perform cosine similarity search to retrieve Top-K relevant chunks

Flow Diagram
PDF
  ↓
Chunking
  ↓
Embedding (MiniLM)
  ↓
Chroma Vector DB
  ↓
Query Embedding
  ↓
Cosine Similarity Search
  ↓
Top-K Results
How It Works Internally

Each text chunk is converted into a fixed-size vector (384 dimensions).

Semantically similar chunks produce vectors that point in similar directions in high-dimensional space.

Cosine similarity measures the angle between vectors to determine semantic closeness.

The query is embedded into the same vector space and compared against stored vectors.

The most similar vectors (Top-K) are returned as relevant results.

Note: No training occurs during this process. The embedding model is pre-trained and used only for inference.

Tech Stack

Python

sentence-transformers (all-MiniLM-L6-v2)

ChromaDB

PyPDF

Installation
git clone <repo_url>
cd rag_ini
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Usage
Step 1: Store Embeddings
python src/store.py
Step 2: Query the System
python src/query.py
Key Learnings

Importance of chunk size and overlap in preserving semantic context

Need to use the same embedding model for documents and queries

Difference between in-memory and persistent vector databases

Cosine similarity measures vector direction rather than magnitude

Future Improvements

Add LLM to generate answers from retrieved chunks (Full RAG system)

Implement sentence-aware chunking

Add metadata filtering

Build CLI interface for dynamic querying

Repository Structure
rag_ini/
│
├── data/
├── src/
│   ├── load_pdf.py
│   ├── chunk.py
│   ├── embed.py
│   ├── store.py
│   └── query.py
├── requirements.txt
└── README.md