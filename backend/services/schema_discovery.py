# backend/services/schema_discovery.py
from sqlalchemy import create_engine, inspect

class SchemaDiscovery:
    def __init__(self):
        # Initialize the schema attribute to None when the object is created
        self.schema = None

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
                "relationships": []
            }

            for table_name in table_names:
                columns = inspector.get_columns(table_name)
                schema_info["columns"][table_name] = [{'name': c['name'], 'type': str(c['type'])} for c in columns]

                foreign_keys = inspector.get_foreign_keys(table_name)
                for fk in foreign_keys:
                    schema_info["relationships"].append({
                        "from_table": table_name,
                        "from_column": fk['constrained_columns'][0],
                        "to_table": fk['referred_table'],
                        "to_column": fk['referred_columns'][0]
                    })

            # Set the discovered schema on the instance
            self.schema = schema_info
            return schema_info

        except Exception as e:
            print(f"An error occurred: {e}")
            self.schema = {"error": str(e)}
            return self.schema