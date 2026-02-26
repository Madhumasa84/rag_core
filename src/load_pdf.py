from pypdf import PdfReader

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = ""   

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

if __name__ == "__main__":
    pdf_text = load_pdf("data/data.pdf")  
    print(pdf_text[:200])    