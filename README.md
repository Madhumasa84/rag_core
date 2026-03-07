# 📄 PDF Semantic Search (Minimal RAG Core)

## 🔎 Overview

This project implements a **minimal semantic search pipeline** over a PDF document.

Instead of performing keyword-based search, the system:

- Converts text into dense vector representations (embeddings)
- Stores them in a vector database (ChromaDB)
- Retrieves relevant chunks using cosine similarity

This demonstrates the core retrieval mechanism used in **Retrieval-Augmented Generation (RAG)** systems.

---

## 🏗 Architecture

### Pipeline Steps

1. Extract raw text from PDF(cleaning is also done)  
2. Split text into overlapping chunks  
3. Convert each chunk into a 384-dimensional embedding (`all-MiniLM-L6-v2`)  
4. Store embeddings in ChromaDB (persistent storage)  
5. Embed the user query using the same model  
6. Perform cosine similarity search to retrieve Top-K relevant chunks  

---

### 🔁 Flow Diagram

PDF(Loading and cleaning)
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


---

## ⚙️ How It Works Internally

- Each text chunk is converted into a fixed-size vector (384 dimensions).
- Semantically similar chunks produce vectors that point in similar directions.
- Cosine similarity measures the angle between vectors.
- The query is embedded into the same vector space.
- The closest vectors (Top-K) are returned as results.

> Note: No training occurs during this process. The embedding model is pre-trained and used only for inference.

---

## 🧹 PDF Cleaning Enhancements

To handle unstructured PDFs (with repeated headers, footers, page numbers, and watermarks), a preprocessing step was added before embedding generation.

Cleaning includes:

Frequency-based header detection

Frequency-based footer detection

Regex-based watermark removal

Page number removal

Whitespace normalization

This improves embedding quality by reducing noise in vector representations.


## Decoder-based QA Extension

The system was extended with a lightweight decoder model to generate answers grounded in the retrieved document context.

Pipeline:

User Query → Vector Retrieval → Context Construction → Decoder Model → Generated Answer

Tested lightweight models:
- Microsoft Phi-3 Mini
- TinyLlama (exploratory)

The decoder generates responses strictly using retrieved document content.

## 🛠 Tech Stack

- Python  
- sentence-transformers (`all-MiniLM-L6-v2`)  
- ChromaDB  
- PyPDF  

---

## 🚀 Installation

```bash
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


📚Key Learnings

Importance of chunk size and overlap in preserving semantic context

Need to use the same embedding model for documents and queries

Difference between in-memory and persistent vector databases

Cosine similarity measures vector direction rather than magnitude


🔮Future Improvements

Add LLM to generate answers from retrieved chunks (Full RAG system)

Implement sentence-aware chunking

Add metadata filtering

Build CLI interface for dynamic querying

📂Repository Structure
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