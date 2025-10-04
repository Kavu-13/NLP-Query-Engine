from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

from services.schema_discovery import SchemaDiscovery
from services.document_processor import DocumentProcessor
from services.query_engine import QueryEngine

# --- Configuration ---
# You would normally load these from a config file or environment variables
GEMINI_API_KEY = "AIzaSyAIom_ftRgc4UDla78mWeG8xBwSQvPEyvs" # Use Your GEMINI API KEY

# Create a dummy db for startup. This will be replaced by the user's db.
DB_FILE = "company_with_relations.db"
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"
DOCS_DIR = "uploaded_docs"
os.makedirs(DOCS_DIR, exist_ok=True)

# --- Application Setup ---
app = FastAPI(
    title="NLP Query Engine API",
    description="API for querying structured and unstructured employee data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Service Initialization ---
# Initialize services that will be used across the application
schema_service = SchemaDiscovery()
doc_service = DocumentProcessor()
# The Query Engine needs the other services and connection strings to be initialized
query_engine = QueryEngine(
    schema_service=schema_service,
    doc_service=doc_service,
    gemini_api_key=GEMINI_API_KEY,
    db_connection_string=DB_CONNECTION_STRING
)

# --- API Models ---
# Define the structure of our request and response data
class ConnectionRequest(BaseModel):
    connection_string: str

class QueryRequest(BaseModel):
    query: str

# --- API Endpoints ---
@app.post("/api/connect-database")
async def connect_database(request: ConnectionRequest):
    """Connects to a database and discovers its schema."""
    global query_engine # Use the global engine instance
    
    connection_string = request.connection_string
    schema_info = schema_service.analyze_database(connection_string)
    schema_service.schema = schema_info # Store the discovered schema

    # Re-initialize the Query Engine with the new connection string
    query_engine = QueryEngine(
        schema_service=schema_service,
        doc_service=doc_service,
        gemini_api_key=GEMINI_API_KEY,
        db_connection_string=connection_string
    )
    
    return {"status": "success", "schema": schema_info}

@app.post("/api/upload-documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Uploads documents for processing and indexing."""
    file_paths = []
    for file in files:
        file_path = os.path.join(DOCS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        file_paths.append(file_path)
    
    # Ingest and index the new documents
    doc_service.ingest_and_index_documents(file_paths)
    
    return {"status": "success", "indexed_files": [os.path.basename(p) for p in file_paths]}

@app.post("/api/query")
async def process_user_query(request: QueryRequest):
    """Processes a natural language query."""
    result = query_engine.process_query(request.query)
    return result

@app.get("/")
def read_root():
    return {"message": "Welcome to the NLP Query Engine API. Go to /docs for the API interface."}
