import os

from pypdf import PdfReader


def load_text_file(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def load_pdf_file(file_path):
    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):
        text = page.extract_text()

        if text:
            pages.append(
                {
                    "page_number": page_number,
                    "text": text
                }
            )

    return pages


def load_document(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return {
            "type": "txt",
            "content": load_text_file(file_path)
        }

    if extension == ".pdf":
        return {
            "type": "pdf",
            "content": load_pdf_file(file_path)
        }

    return None