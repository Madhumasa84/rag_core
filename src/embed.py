from sentence_transformers import SentenceTransformer
from load_pdf import load_pdf
from chunk import chunk_text

def generate_embeddings(chunks):
    """
    Converts text chunks into dense vector embeddings
    using a pre-trained Sentence Transformer model.

    Args:
        chunks (list[str]): List of text chunks.

    Returns:
        list[list[float]]: List of embedding vectors.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    return embeddings

if __name__ == "__main__":
    text=load_pdf("data/data.pdf")
    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    print(f"Total embeddings: {len(embeddings)}")
    print(f"Embeddings dimension: {len(embeddings[0])}")
    