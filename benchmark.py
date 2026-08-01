import time
import uuid
import chromadb
from unittest.mock import MagicMock

def generate_data(num_items=1000):
    chunks = [f"This is chunk number {i} with some sample text for benchmarking." for i in range(num_items)]
    embeddings = [[0.1] * 384 for _ in range(num_items)]
    return chunks, embeddings

def run_loop_baseline(chunks, embeddings, collection):
    start = time.time()
    chunk_ids = []
    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        chunk_ids.append(chunk_id)
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[chunk_id]
        )
    return time.time() - start

def run_batch_optimized(chunks, embeddings, collection):
    start = time.time()
    chunk_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=chunk_ids
    )
    return time.time() - start

if __name__ == "__main__":
    chunks, embeddings = generate_data(100)

    # We can use actual ChromaDB in-memory client for testing
    client = chromadb.Client()

    col1 = client.create_collection("baseline")
    loop_time = run_loop_baseline(chunks, embeddings, col1)
    print(f"Loop Insertion Time: {loop_time:.4f} seconds")

    col2 = client.create_collection("optimized")
    batch_time = run_batch_optimized(chunks, embeddings, col2)
    print(f"Batch Insertion Time: {batch_time:.4f} seconds")

    print(f"Improvement: {loop_time / batch_time:.2f}x faster")
