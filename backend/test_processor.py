from services.document_processor import DocumentProcessor
import os

doc_dir = "test_docs"
files_to_process = [
    os.path.join(doc_dir, "resume.txt"),
    os.path.join(doc_dir, "review.docx")
]

# Initialize the processor
processor = DocumentProcessor()

# Ingest and index the documents
processor.ingest_and_index_documents(files_to_process)

# Perform a test search
if processor.index:
    print("\n--- Performing a test search ---")
    query = "Who is a Python developer?"
    search_results = processor.search(query)

    print(f"Query: '{query}'")
    print("Search Results:")
    for result in search_results:
        print(f"  - Source: {result['source']}")
        print(f"    Content: '{result['content']}'")
        print(f"    Similarity Score (Distance): {result['distance']:.4f}\n")