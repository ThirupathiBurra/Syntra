import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("SUPABASE_DB_URL")
if not db_url:
    print("SUPABASE_DB_URL not found in .env")
    exit(1)

# Connect to the database
print(f"Connecting to database...")
try:
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            # Read schema file
            schema_path = os.path.join(os.path.dirname(__file__), "generate_schema.sql")
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            # Execute schema
            print("Executing schema...")
            cur.execute(schema_sql)
            conn.commit()
            print("Schema executed successfully!")
except Exception as e:
    print(f"Error executing schema: {e}")
