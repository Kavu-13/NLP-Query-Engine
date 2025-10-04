import os
from pypdf import PdfReader
import docx
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class DocumentProcessor:
    def __init__(self):
        model_path = './models/all-MiniLM-L6-v2'
        self.model = SentenceTransformer(model_path)
        print("SentenceTransformer model loaded from local path.")
        
        # Initialize the FAISS index and a mapping to store chunk data
        self.index = None
        self.chunk_map = []

    def _read_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def _read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    def _chunk_text(self, text: str) -> list[str]:
        chunks = text.split('\n\n')
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def ingest_and_index_documents(self, file_paths: list[str]):
        """
        Processes documents, creates embeddings, and builds a FAISS index.
        """
        all_chunks = []
        for file_path in file_paths:
            try:
                _, file_ext = os.path.splitext(file_path)
                file_ext = file_ext.lower()
                if file_ext == ".pdf": text = self._read_pdf(file_path)
                elif file_ext == ".docx": text = self._read_docx(file_path)
                elif file_ext == ".txt":
                    with open(file_path, 'r') as f: text = f.read()
                else: continue
                
                chunks = self._chunk_text(text)
                print(f"Successfully processed and chunked {file_path} into {len(chunks)} chunks.")
                
                for chunk in chunks:
                    # Store chunk content and its source file
                    all_chunks.append({"source": file_path, "content": chunk})
            
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
        
        # Now, create embeddings for all chunks together
        if not all_chunks:
            print("No chunks were created. Nothing to index.")
            return

        contents = [item['content'] for item in all_chunks]
        embeddings = self.model.encode(contents)

        # Build the FAISS index
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.chunk_map = all_chunks

        print(f"\nFAISS index built successfully with {self.index.ntotal} vectors.")

    def search(self, query: str, k: int = 3) -> list[dict]:
        """
        Searches the FAISS index for the most relevant chunks.
        """
        if not self.index:
            return []
        
        # Create an embedding for the query
        query_embedding = self.model.encode([query])
        
        # Search the index
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            # This 'if' statement is also indented
            if idx != -1 and distances[0][i] < 1.0:
                # This 'append' is indented even further
                results.append({
                    "source": self.chunk_map[idx]['source'],
                    "content": self.chunk_map[idx]['content'],
                    "distance": float(distances[0][i])
                })
        return results