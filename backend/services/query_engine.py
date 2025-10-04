# backend/services/query_engine.py
import google.generativeai as genai
import json
from sqlalchemy import create_engine, text

from .schema_discovery import SchemaDiscovery
from .document_processor import DocumentProcessor

class QueryEngine:
    def __init__(self, schema_service: SchemaDiscovery, doc_service: DocumentProcessor, gemini_api_key: str, db_connection_string: str):
        self.schema_service = schema_service
        self.doc_service = doc_service
        self.db_engine = create_engine(db_connection_string)
        self.cache = {}

        genai.configure(api_key=gemini_api_key)
        self.llm = genai.GenerativeModel('models/gemini-pro-latest')

        # Keywords for classification
        self.sql_keywords = ['department', 'salary', 'employee', 'hired', 'reports to']
        self.doc_keywords = ['skill', 'python', 'performance', 'review', 'resume', 'experience']

    def _classify_query(self, query: str) -> str:
        """Classifies the query as SQL, DOCUMENT, or HYBRID."""
        query_lower = query.lower()
        has_sql_keyword = any(keyword in query_lower for keyword in self.sql_keywords)
        has_doc_keyword = any(keyword in query_lower for keyword in self.doc_keywords)

        if has_sql_keyword and has_doc_keyword:
            return "HYBRID"
        if has_sql_keyword:
            return "SQL"
        if has_doc_keyword:
            return "DOCUMENT"
        
        # Default to SQL for generic questions like "show me..."
        return "SQL"
    
    def _generate_sql_query(self, user_query: str) -> str:
        # ... (this method is unchanged)
        if not self.schema_service.schema:
             return "Error: Database schema has not been discovered yet."
        prompt = f"""
        You are a powerful Text-to-SQL model. Your role is to generate a single, valid SQL query based on the provided database schema and a user's question. 
        Only extract information that can be found in the database schema. Ignore parts of the question that refer to skills or document content.
        Do not provide any explanations or conversational text; only output the SQL query.
        **Database Schema:**
        {json.dumps(self.schema_service.schema, indent=2)}
        **User's Question:**
        "{user_query}"
        **Generated SQL Query:**
        """
        try:
            response = self.llm.generate_content(prompt)
            sql_query = response.text.strip()
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:-3].strip()
            return sql_query
        except Exception as e:
            return f"Error generating SQL query: {e}"

    def _execute_sql_query(self, sql_query: str) -> dict:
        # ... (this method is unchanged)
        banned_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE']
        if any(keyword in sql_query.upper() for keyword in banned_keywords):
            return {"error": "Query contains potentially destructive commands."}
        try:
            with self.db_engine.connect() as connection:
                result = connection.execute(text(sql_query))
                rows = result.fetchall()
                if rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return []
        except Exception as e:
            return {"error": f"Error executing SQL query: {e}"}

    def process_query(self, user_query: str) -> dict:
        """Processes the user query, checking the cache first."""
        if user_query in self.cache:
            print(f"Query found in cache: '{user_query}'")
            cached_result = self.cache[user_query]
            cached_result["cached"] = True # Add the cache flag
            return cached_result

        print(f"Query not in cache. Processing: '{user_query}'")
        query_type = self._classify_query(user_query)
        result = {"query": user_query, "type": query_type, "answer": None, "cached": False}
        
        if query_type == "SQL":
            print(f"Query classified as '{query_type}'.")
            generated_sql = self._generate_sql_query(user_query)
            result["generated_sql"] = generated_sql
            result["answer"] = self._execute_sql_query(generated_sql)
        
        elif query_type == "DOCUMENT":
            print(f"Query classified as '{query_type}'.")
            result["answer"] = self.doc_service.search(user_query, k=1)
            
        elif query_type == "HYBRID":
            print(f"Query classified as '{query_type}'.")
            # 1. Generate and execute the SQL part
            generated_sql = self._generate_sql_query(user_query)
            sql_results = self._execute_sql_query(generated_sql)
            
            # 2. Execute the document search part
            doc_results = self.doc_service.search(user_query, k=1)
            
            # 3. Combine the results
            result["answer"] = {
                "sql_results": sql_results,
                "doc_results": doc_results
            }
            result["generated_sql"] = generated_sql

        self.cache[user_query] = result
        return result