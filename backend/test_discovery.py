from services.schema_discovery import SchemaDiscovery
import sqlite3
import os

db_file = "company_with_relations.db"
# Delete old DB file if it exists to ensure a clean test
if os.path.exists(db_file):
    os.remove(db_file)

# --- Create a more complex dummy SQLite database ---
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# Create a 'departments' table
cursor.execute("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
""")
# Create an 'employees' table with a foreign key to departments
cursor.execute("""
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    salary REAL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments (id)
);
""")
conn.commit()
conn.close()
# --- End of database creation ---

# Connection string for our new SQLite database
sqlite_connection_string = f"sqlite:///{db_file}"

# Run the analysis
discovery_service = SchemaDiscovery()
schema = discovery_service.analyze_database(sqlite_connection_string)

print("\n--- Final Discovered Schema ---")
import json
print(json.dumps(schema, indent=2))