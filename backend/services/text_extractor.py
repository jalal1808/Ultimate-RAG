from pathlib import Path
import re
from pypdf import PdfReader
from docx import Document


def extract_text(file_path: Path, extension: str) -> str:
    """Route to correct extractor based on extension"""
    extension = extension.lower().lstrip(".")

    dispatch = {
        "pdf": _extract_pdf,
        "docx": _extract_docx,
        "txt": _extract_txt,
        "md": _extract_txt, 
    }

    if extension not in dispatch:
        raise ValueError(f"Unsupported text extension: {extension}")

    text = dispatch[extension](file_path)
    return _clean(text)


def _extract_pdf(file_path: Path) -> str:
    """Extract text from PDF using pypdf"""
    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:  # skip None pages
            pages_text.append(page_text)

    return "\n\n".join(pages_text)


def _extract_docx(file_path: Path) -> str:
    """Extract text from DOCX using python-docx"""
    doc = Document(file_path)
    paragraphs = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:  # skip blank lines
            paragraphs.append(text)

    return "\n".join(paragraphs)


def _extract_txt(file_path: Path) -> str:
    """Read plain TXT or Markdown file"""
    return Path(file_path).read_text(encoding="utf-8", errors="replace")


def _clean(text: str) -> str:
    """Basic cleanup of extracted text"""
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()