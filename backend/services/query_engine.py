import google.generativeai as genai
import json
from sqlalchemy import create_engine, text

from .schema_discovery import SchemaDiscovery
from .document_processor import DocumentProcessor

class QueryEngine:
    def __init__(self, schema_service: SchemaDiscovery, doc_service: DocumentProcessor, gemini_api_key: str, db_connection_string: str):
        self.schema_service = schema_service
        self.doc_service = doc_service
        
        # Database engine to execute queries
        self.db_engine = create_engine(db_connection_string)

        genai.configure(api_key=gemini_api_key)
        self.llm = genai.GenerativeModel('models/gemini-pro-latest')

        self.sql_keywords = [
            'count', 'average', 'sum', 'total', 'max', 'min', 'list', 'show me',
            'how many', 'what is the', 'who are the', 'salary', 'department',
            'employee', 'employees', 'hired', 'reports to'
        ]

    def _classify_query(self, query: str) -> str:
        query_lower = query.lower()
        for keyword in self.sql_keywords:
            if keyword in query_lower:
                return "SQL"
        return "DOCUMENT"
    
    def _generate_sql_query(self, user_query: str) -> str:
        if not self.schema_service.schema:
             return "Error: Database schema has not been discovered yet."
        prompt = f"""
        You are a powerful Text-to-SQL model. Your role is to generate a single, valid SQL query based on the provided database schema and a user's question. 
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
        """Executes a SQL query and returns the result."""
        # Safety check: Prevent destructive commands
        banned_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'TRUNCATE']
        if any(keyword in sql_query.upper() for keyword in banned_keywords):
            return {"error": "Query contains potentially destructive commands."}

        try:
            with self.db_engine.connect() as connection:
                result = connection.execute(text(sql_query))
                rows = result.fetchall()
                # Format the result as a list of dictionaries
                if rows:
                    columns = result.keys()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    return []
        except Exception as e:
            return {"error": f"Error executing SQL query: {e}"}


    def process_query(self, user_query: str) -> dict:
        """Processes the user query, generates SQL if needed, and executes it."""
        query_type = self._classify_query(user_query)
        result = {"query": user_query, "type": query_type, "generated_sql": None, "answer": None}
        
        if query_type == "SQL":
            print(f"Query classified as '{query_type}'. Generating and executing SQL...")
            generated_sql = self._generate_sql_query(user_query)
            result["generated_sql"] = generated_sql
            
            # Execute the generated SQL
            if "Error" not in generated_sql:
                result["answer"] = self._execute_sql_query(generated_sql)
            else:
                result["answer"] = {"error": generated_sql}
        
        elif query_type == "DOCUMENT":
            print(f"Query classified as '{query_type}'. Searching indexed documents...")
            result["answer"] = self.doc_service.search(user_query)

        return result