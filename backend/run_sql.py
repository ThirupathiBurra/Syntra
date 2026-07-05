import psycopg2, os
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv('SUPABASE_DB_URL'))
cur = conn.cursor()
sql = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    document_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    page_number INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(768)
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
"""
cur.execute(sql)
conn.commit()

# Handle Policies (Ignore if exist)
policies = [
    "CREATE POLICY \"Allow public read access on documents\" ON documents FOR SELECT USING (true);",
    "CREATE POLICY \"Allow public insert access on documents\" ON documents FOR INSERT WITH CHECK (true);",
    "CREATE POLICY \"Allow public read access on document_chunks\" ON document_chunks FOR SELECT USING (true);",
    "CREATE POLICY \"Allow public insert access on document_chunks\" ON document_chunks FOR INSERT WITH CHECK (true);"
]
for p in policies:
    try:
        cur.execute(p)
        conn.commit()
    except Exception as e:
        conn.rollback()

# RPC
rpc = """
CREATE OR REPLACE FUNCTION match_document_chunks (
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT,
  filter_workspace_id TEXT
)
RETURNS TABLE (
  chunk_id TEXT,
  document_id TEXT,
  content TEXT,
  similarity FLOAT
)
LANGUAGE sql STABLE
AS $$
  SELECT
    dc.id AS chunk_id,
    dc.document_id,
    dc.content,
    1 - (dc.embedding <=> query_embedding) AS similarity
  FROM document_chunks dc
  JOIN documents d ON d.id = dc.document_id
  WHERE d.workspace_id = filter_workspace_id
    AND 1 - (dc.embedding <=> query_embedding) > match_threshold
  ORDER BY dc.embedding <=> query_embedding
  LIMIT match_count;
$$;
"""
cur.execute(rpc)
conn.commit()

cur.execute("NOTIFY pgrst, 'reload schema';")
conn.commit()
print("Success")
