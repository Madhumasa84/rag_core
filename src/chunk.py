def chunk_text(text:str, chunk_size: int =500, overlap:int=100):
    """
    Splits input text into overlapping character-based chunks.

    Overlapping ensures semantic continuity between chunks.

    Args:
        text (str): Input cleaned text.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of overlapping characters.

    Returns:
        list[str]: List of text chunks.
    """
    chunks=[]
    start=0
    while start < len(text):
        end = start +chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

if __name__=="__main__":
    from load_pdf import load_pdf

    text =load_pdf("data/data.pdf")
    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}")
    print(chunks[0])