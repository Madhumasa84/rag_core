# Audit Report

## 1. `api.py` Functionality
`api.py` is a FastAPI application that serves as the entry point for the Document QA system. It implements the following endpoints:
- `GET /` and `GET /health`: Health checks and root messages.
- `POST /upload`: Accepts file uploads (PDF, PPT, HTML, TXT), saves them to an `uploads/` directory, and calls `process_and_store()` to extract text, chunk it, embed it, and store it in a local ChromaDB instance.
- `POST /ask`: Currently a placeholder endpoint that accepts a question but returns a hardcoded "pending" message. It's meant to interface with the answer generation module.

## 2. Hardcoded Values
Throughout the codebase, several values are hardcoded rather than centralized in a configuration file:
- **Paths:**
  - `UPLOAD_DIR = Path("uploads")` in `api.py`.
  - `./chroma_db` in `processors.py`, `query.py`, and `store.py`.
  - Various test paths like `"data/data.pdf"` and `"data/messydata.pdf"` in `__main__` blocks.
- **Chunking Parameters:** `chunk_size = 500` and `overlap = 100` in `chunk.py`.
- **Generation & Retrieval Parameters:**
  - `n_results = 3` (top_k) in `query.py`.
  - `top_k = 3` in `generate_answer_qwen.py`.
  - `max_new_tokens = 300`, `temperature = 0.1`, `top_p = 0.9` in `generate_answer_qwen.py`.
- **Model Names:**
  - Embedding model: `"all-MiniLM-L6-v2"` in `embed.py` and `query.py`.
  - Generation models: `"Qwen/Qwen2.5-1.5B-Instruct"` in `generate_answer_qwen.py` and `"microsoft/Phi-3-mini-4k-instruct"` in `generate_answer.py`.

## 3. `generate_answer.py` Status
`generate_answer.py` (which uses the Phi-3 model) is effectively **dead code**. It is not imported by `api.py` or any other part of the active pipeline. The main server and pipeline rely on `generate_answer_qwen.py`.

## 4. `requirements.txt` Versions
The current versions in `requirements.txt` are **pinned** using strict equality (e.g., `fastapi==0.115.6`, `pypdf==5.1.0`). However, the file is missing crucial dependencies that are used in the codebase (e.g., `torch`, `transformers`, `pytest`), meaning it does not reflect a fully functional environment.
