from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file_path):
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(file_path)
    elif suffix in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    elif suffix in [".md", ".txt"]:
        return Path(file_path).read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def load_text_file(file_path):
    return Path(file_path).read_text(encoding="utf-8")
