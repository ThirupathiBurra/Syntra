-- Migration: 20260704_knowledge_schema.sql
-- Description: Sets up the pgvector extension and schemas for Syntra Enterprise RAG

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents Table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    workspace_id VARCHAR(255) NOT NULL,
    title VARCHAR(512) NOT NULL,
    department VARCHAR(100),
    document_type VARCHAR(50),
    owner VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Document Chunks Table
CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    page_number INTEGER,
    embedding VECTOR(768), -- Gemini text-embedding-004 dimension
    metadata JSONB DEFAULT '{}'::jsonb
);

-- HNSW Index for fast similarity search
CREATE INDEX ON document_chunks USING hnsw (embedding vector_ip_ops) WITH (m = 16, ef_construction = 64);

-- Supabase RPC for similarity search
CREATE OR REPLACE FUNCTION match_document_chunks (
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT,
  filter_workspace_id VARCHAR
)
RETURNS TABLE (
  id UUID,
  document_id UUID,
  content TEXT,
  page_number INT,
  metadata JSONB,
  similarity FLOAT,
  title VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id,
    dc.document_id,
    dc.content,
    dc.page_number,
    dc.metadata,
    1 - (dc.embedding <=> query_embedding) AS similarity,
    d.title
  FROM document_chunks dc
  JOIN documents d ON dc.document_id = d.id
  WHERE d.workspace_id = filter_workspace_id
    AND 1 - (dc.embedding <=> query_embedding) > match_threshold
  ORDER BY dc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
