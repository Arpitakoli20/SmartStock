from pathlib import Path
import chromadb

from pdf_reader import read_all_pdfs


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ChromaDB storage folder
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


def create_chunks(text, chunk_size=500):
    """
    Split document text into smaller chunks.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def build_vector_store():

    print("===================================")
    print("SMARTSTOCK - CHROMADB SETUP")
    print("===================================")

    # Persistent ChromaDB client
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Create or get collection
    collection = client.get_or_create_collection(
        name="smartstock_documents"
    )

    # Read PDFs
    documents = read_all_pdfs()

    document_count = 0
    chunk_count = 0

    for document in documents:

        filename = document["filename"]
        text = document["text"]

        chunks = create_chunks(text)

        print(f"\nFile: {filename}")
        print(f"Chunks created: {len(chunks)}")

        for index, chunk in enumerate(chunks):

            chunk_id = f"{filename}_{index}"

            collection.upsert(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[
                    {
                        "filename": filename,
                        "chunk_index": index
                    }
                ]
            )

            chunk_count += 1

        document_count += 1

    print("\n===================================")
    print("CHROMADB SETUP COMPLETED")
    print("===================================")

    print(f"Documents processed: {document_count}")
    print(f"Total chunks stored: {chunk_count}")
    print(f"ChromaDB location: {CHROMA_DIR}")


if __name__ == "__main__":
    build_vector_store()