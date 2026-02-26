import chromadb
from chromadb.config import Settings
from load_pdf import load_pdf
from chunk import chunk_text
from embed import generate_embeddings


def store_embeddings(chunks, embeddings):
    client = chromadb.Client(
        Settings(
            persist_directory="./chroma_db",
            is_persistent=True
        )
    )

    collection = client.get_or_create_collection(name="pdf_collection")

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )

    return collection


if __name__ == "__main__":
    text = load_pdf("data/data.pdf")
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    store_embeddings(chunks, embeddings)

    print("Stored successfully with persistence.")