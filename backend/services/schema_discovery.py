from sqlalchemy import create_engine, inspect

class SchemaDiscovery:
    def analyze_database(self, connection_string: str) -> dict:
        """
        Connects to a database and discovers its schema.
        """
        print(f"Analyzing database with connection string: {connection_string}")
        
        try:
            engine = create_engine(connection_string)
            inspector = inspect(engine)
            table_names = inspector.get_table_names()
            
            schema_info = {
                "tables": table_names,
                "columns": {},
                "relationships": [] # Changed to a list
            }
            
            print(f"Discovered tables: {table_names}")

            for table_name in table_names:
                # Get columns
                columns = inspector.get_columns(table_name)
                schema_info["columns"][table_name] = []
                for column in columns:
                    schema_info["columns"][table_name].append({
                        "name": column['name'],
                        "type": str(column['type'])
                    })
                print(f"  - Discovered columns for '{table_name}'")
                
                # Get foreign key relationships
                foreign_keys = inspector.get_foreign_keys(table_name)
                for fk in foreign_keys:
                    relationship = {
                        "from_table": table_name,
                        "from_column": fk['constrained_columns'][0],
                        "to_table": fk['referred_table'],
                        "to_column": fk['referred_columns'][0]
                    }
                    schema_info["relationships"].append(relationship)
                print(f"  - Discovered relationships for '{table_name}'")

            return schema_info

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": str(e)}