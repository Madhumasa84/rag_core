# 📄 PDF Semantic Search (Minimal RAG Core)

## 🔎 Overview

This project implements a **minimal semantic search pipeline** over a PDF document.

The system:
- Extracts and cleans text from PDFs (handles messy documents)
- Converts text into dense vector representations (embeddings)
- Stores them in a vector database (ChromaDB)
- Retrieves relevant chunks using cosine similarity
- **Generates answers using a lightweight decoder model** (Qwen2.5-1.5B) running entirely on **CPU**

This demonstrates production-ready RAG architecture suitable for resource-constrained environments.

---

## 🏗 Architecture

### Pipeline Steps


1. **PDF Processing** — Extract raw text + clean headers/footers/watermarks
2. **Chunking** — Split into overlapping chunks (preserves semantic continuity)
3. **Embedding** — Convert chunks to 384-dim vectors (`all-MiniLM-L6-v2`)
4. **Storage** — Store vectors in ChromaDB (persistent)
5. **Retrieval** — Embed user query → cosine similarity search → Top-K chunks
6. **Generation** — Feed chunks + question to **Qwen2.5-1.5B** → generate grounded answer

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
User Query → Query Embedding
↓
Cosine Similarity Search
↓
Top-K Results
↓
Qwen2.5-1.5B (CPU)
↓
Grounded Answer
---

## ⚙️ How It Works Internally

### Retrieval Layer
- Each text chunk → fixed-size vector (384 dimensions)
- Semantically similar chunks → vectors pointing in similar directions
- Cosine similarity measures angle between vectors
- Query embedded into same vector space → closest vectors returned

### Generation Layer
- Retrieved chunks + question → formatted into prompt
- Qwen2.5-1.5B (1.5B parameters) generates answer **strictly from context**
- Runs entirely on **CPU** — no GPU required
- Model says "I cannot find this information" when answer absent (reduces hallucination)

> Note: No training occurs. Embedding model is pre-trained; decoder is used for inference only.

---

## 🧹 PDF Cleaning Enhancements

To handle unstructured PDFs (headers, footers, page numbers, watermarks), preprocessing removes noise before embedding generation:

- **Frequency-based header/footer detection**
- **Regex-based watermark removal**
- **Page number elimination**
- **Whitespace normalization**

This improves retrieval quality by reducing noise in vector representations.

---

## Decoder-based QA (Qwen2.5-1.5B)

The system was extended with a lightweight decoder model optimized for **CPU inference**.

### Model Selection
Based on evaluation of 5 lightweight models:

| Model                     | Params | CPU Feasible | Hallucination Control | Selected |
|---------------------------|--------|--------------|-----------------------|----------|
| **Qwen2.5-1.5B-Instruct** | 1.5B   | Excellent    | Good                  | **Yes**  |
| Phi-3 Mini 4K             | 3.8B   | Good         | Excellent             | heavier  |
| TinyLlama 1.1B            | 1.1B   | Excellent    | Weaker                | No       |
| Llama 3.2-3B              | 3B     | Limited      | Good                  | No       |
| Mistral 7B                | 7B     | No           | Good                  | No       |

### Why Qwen2.5-1.5B?
- **1.5B parameters** — lightweight enough for CPU
- **32K context window** — handles long document chunks
- **Strong instruction following** — respects "answer only from context"
- **Apache 2.0 license** — commercial use permitted
- **Fast inference on CPU** — optimized for resource-constrained environments

### Performance (CPU)
| Metric                 | Value         |
|------------------------|---------------|
| First load time        | ~2-3 minutes  |
| Inference per question | 10-30 seconds |
| RAM usage              | ~4-6 GB       |
| Context window         | 32,768 tokens |

---


## 🛠 Tech Stack

- **Python** — Core language
- **sentence-transformers** — Embedding model (`all-MiniLM-L6-v2`)
- **ChromaDB** — Vector database (persistent storage)
- **PyPDF** — PDF text extraction
- **Transformers (Hugging Face)** — Qwen2.5-1.5B for answer generation

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
Step 3: Using Qwen2.5-1.5B
python src/generate_answer_qwen.py


📚Key Learnings

Chunk size & overlap - Critical for preserving semantic context

Same embedding model - Must be used for documents and queries

In-memory vs persistent DB - Persistence enables reuse without recomputation

Cosine similarity - Measures direction, not magnitude - ideal for text

Decoder grounding - Lightweight models can run on CPU with proper prompting

Hallucination control - System prompt + low temperature reduces made-up answers


🔮Future Improvements

Sentence-aware chunking (instead of fixed character count)

Metadata filtering (page numbers, document sections)

Batch processing for multiple PDFs

Simple web UI (Streamlit)

Quantization for faster CPU inference

RAGAS evaluation metrics



📂Repository Structure

rag_ini/
│
├── data/                      # PDF files
│   ├── clean.pdf
│   └── messy.pdf
│
├── src/
│   ├── load_pdf.py           # Extraction + cleaning
│   ├── chunk.py              # Text chunking
│   ├── embed.py              # Embedding generation
│   ├── store.py              # ChromaDB storage
│   ├── query.py              # Retrieval only
│   ├── generate_answer.py     # Phi-3 version (backup)
│   └── generate_answer_qwen.py # Qwen2.5-1.5B (CPU)
│
├── requirements.txt
└── README.md