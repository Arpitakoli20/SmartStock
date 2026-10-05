from pathlib import Path
from pypdf import PdfReader


# Project मधील documents folder
DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def read_pdf(pdf_path):
    """
    Reads a PDF and returns all extracted text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_all_pdfs():
    """
    Reads all PDF files from the documents folder.
    """

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    documents = []

    for pdf_file in pdf_files:
        text = read_pdf(pdf_file)

        documents.append(
            {
                "filename": pdf_file.name,
                "text": text,
            }
        )

    return documents


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - PDF READER")
    print("===================================")

    documents = read_all_pdfs()

    print(f"\nPDF files found: {len(documents)}")

    for document in documents:

        print("\n-----------------------------------")
        print(f"File: {document['filename']}")
        print("-----------------------------------")

        print(document["text"][:500])

    print("\n===================================")
    print("PDF reading completed!")
    print("===================================")