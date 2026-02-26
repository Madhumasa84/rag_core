<<<<<<< HEAD

=======
PDF Semantic Search (Minimal RAG Core)
Overview

This project implements a minimal semantic search pipeline over a PDF document.

Instead of performing keyword-based search, the system converts text into dense vector representations (embeddings) using a pre-trained Sentence Transformer model. These vectors are stored in a Chroma vector database, enabling similarity-based retrieval using cosine similarity.

This forms the core retrieval component of Retrieval-Augmented Generation (RAG) systems used in modern AI applications.


Architecture


The pipeline follows these steps:

Extract raw text from PDF

Split text into overlapping chunks

Convert each chunk into a 384-dimensional embedding using all-MiniLM-L6-v2

Store embeddings in ChromaDB (persistent storage)

Embed the user query using the same model

Perform cosine similarity search to retrieve top-K relevant chunks

Flow:

PDF → Chunking → Embedding → Vector Storage → Query Embedding → Similarity Search


How It Works Internally

Each text chunk is converted into a fixed-size vector (384 dimensions).

Similar text chunks produce vectors that point in similar directions in high-dimensional space.

Cosine similarity measures the angle between vectors to determine semantic closeness.

The query is embedded into the same vector space and compared against stored vectors.

The most similar vectors (Top-K) are returned as relevant results.

No training occurs during this process; the embedding model is pre-trained and reused for inference.


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


How to Run

First, store the embeddings:

python src/store.py

Then run a query:

python src/query.py


Key Learnings

Importance of chunk size and overlap in preserving semantic context

Need to use the same embedding model for documents and queries

Difference between in-memory and persistent vector databases

Cosine similarity measures vector direction rather than magnitude


Future Improvements

Add LLM to generate answers from retrieved chunks (full RAG system)

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
>>>>>>> 14c5713 (Improved the Readme)
