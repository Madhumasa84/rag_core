from pypdf import PdfReader
import re
from collections import Counter



def clean_text(text: str)-> str:
    """
    Performs basic cleanup of extracted PDF text.

    This includes:
    - Removing common page number formats
    - Removing excessive whitespace
    - Normalizing newline spacing

    Args:
        text (str): Raw extracted text from PDF.

    Returns:
        str: Cleaned and normalized text.
    """
    text=re.sub(r"Page \d+( of \d+)?", "",text) #remove page numbers
    text=re.sub(r"\n\d+\n","\n", text) #remove standalone numbers
    text = re.sub(r"\n\s*\n", "\n", text) #replace multiple newlines
    text = re.sub(r"[ \t]+", " ", text) #replace excess place
    return text.strip()


def remove_repeated_headers_footers(pages: list[str]) -> list[str]:
    """
    Detects and removes repeated headers and footers
    based on frequency across pages.

    Strategy:
    - Extract first and last lines of each page
    - Identify lines that appear frequently
    - Remove those lines from all pages

    Args:
        pages (list[str]): List of page texts.

    Returns:
        list[str]: Cleaned pages without repeated headers/footers.
    """
    header_candidates = []
    footer_candidates = []

    for page in pages:
        lines = page.split("\n")
        if len(lines) > 2:
            header_candidates.append(lines[0].strip())
            footer_candidates.append(lines[-1].strip())

    header_freq = Counter(header_candidates)
    footer_freq = Counter(footer_candidates)

    common_headers = {
        line for line, count in header_freq.items() if count > len(pages) * 0.5
    }
    common_footers = {
        line for line, count in footer_freq.items() if count > len(pages) * 0.5
    }

    cleaned_pages = []

    for page in pages:
        lines = page.split("\n")
        filtered_lines = [
            line for line in lines
            if line.strip() not in common_headers
            and line.strip() not in common_footers
        ]
        cleaned_pages.append("\n".join(filtered_lines))

    return cleaned_pages


def remove_watermark_patterns(text: str) -> str:
    """
    Removes common watermark-like patterns such as:
    - CONFIDENTIAL
    - DRAFT
    - Company names repeated across pages

    This uses regex-based pattern removal.

    Args:
        text (str): Input text.

    Returns:
        str: Text with watermark patterns removed.
    """
    watermark_patterns = [
        r"CONFIDENTIAL",
        r"DRAFT",
        r"Company Name",
    ]

    for pattern in watermark_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    return text


def load_pdf(path: str) -> str:
    """
    Loads a PDF file, removes repeated headers/footers,
    removes watermark patterns, and returns cleaned text.

    Args:
        path (str): Path to the PDF file.

    Returns:
        str: Fully cleaned text extracted from the PDF.
    """

    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            pages.append(extracted)

    pages = remove_repeated_headers_footers(pages)

    text = "\n".join(pages)
    text = remove_watermark_patterns(text)
    text = clean_text(text)

    return text


if __name__ == "__main__":
    pdf_path="data/messydata.pdf"
    text=load_pdf(pdf_path)    
    print(text[:200])