import os
import json
from services.schema_discovery import SchemaDiscovery
from services.document_processor import DocumentProcessor
from services.query_engine import QueryEngine

# Setup Dependencies ---
GEMINI_API_KEY = "GEMINI API KEY"

db_file = "company_with_relations.db"
sqlite_connection_string = f"sqlite:///{db_file}"

schema_service = SchemaDiscovery()
schema_service.schema = schema_service.analyze_database(sqlite_connection_string)

doc_service = DocumentProcessor()
# ... (document ingestion logic is the same)
doc_dir = "test_docs"
files_to_process = [os.path.join(doc_dir, "resume.txt"), os.path.join(doc_dir, "review.docx")]
doc_service.ingest_and_index_documents(files_to_process)

# Initialize the Query Engine ---
print("\n--- Initializing Query Engine ---")
query_engine = QueryEngine(
    schema_service=schema_service, 
    doc_service=doc_service, 
    gemini_api_key=GEMINI_API_KEY,
    db_connection_string=sqlite_connection_string  # Pass the connection string
)

# Run Test Queries ---
test_queries = [
    "How many employees are there?",
    "List the names of all departments"
]
print("\n--- Running Test Queries ---")
for query in test_queries:
    result = query_engine.process_query(query)
    print(f"\nQuery: '{result['query']}'")
    print(f"Type: {result['type']}")
    if result['generated_sql']:
        print(f"Generated SQL: {result['generated_sql']}")
    # Use json.dumps for pretty printing the result
    print(f"Answer: {json.dumps(result['answer'], indent=2)}")
