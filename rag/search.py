import chromadb

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


def search_documents(query, n_results=3):

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_collection(
        name="smartstock_documents"
    )

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    print("===================================")
    print("SMARTSTOCK - DOCUMENT SEARCH")
    print("===================================")

    print(f"\nQuery: {query}")

    print("\nSearch Results:")
    print("-----------------------------------")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        print(f"\nResult {i}")
        print(f"File: {metadata['filename']}")
        print(f"Content:\n{document}")


if __name__ == "__main__":

    query = "What was the previous price of Paracetamol?"

    search_documents(query)