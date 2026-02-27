import chromadb
from sentence_transformers import SentenceTransformer


def query_collection(query_text):
    """
    Embeds the input query and retrieves the most
    semantically similar text chunks from Chroma.

    Args:
        query_text (str): User query string.
        n_results (int): Number of top results to retrieve.

    Returns:
        dict: Query results including documents and similarity scores.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    from chromadb.config import Settings

    client = chromadb.Client(
    Settings(
        persist_directory="./chroma_db",
        is_persistent=True))

    collection = client.get_collection(name="pdf_collection")
    query_embedding = model.encode([query_text])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return results


if __name__ == "__main__":
    results = query_collection("What is this document about?")

    print("Top Results:\n")
    for doc in results["documents"][0]:
        print(doc)