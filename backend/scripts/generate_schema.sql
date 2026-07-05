-- Supabase Schema Initialization for Syntra

-- ==========================================
-- 1. Workflows Table
-- Stores generated workflow graphs and metadata
-- ==========================================
CREATE TABLE IF NOT EXISTS workflows (
    workflow_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    department TEXT NOT NULL,
    tags JSONB DEFAULT '[]'::jsonb,
    
    nodes JSONB NOT NULL,
    dependencies JSONB NOT NULL,
    
    confidence DOUBLE PRECISION NOT NULL,
    estimated_duration TEXT NOT NULL,
    estimated_cost TEXT NOT NULL,
    risks JSONB DEFAULT '[]'::jsonb,
    requires_human_approval BOOLEAN NOT NULL DEFAULT false,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER NOT NULL DEFAULT 1,
    execution_count INTEGER NOT NULL DEFAULT 0
);

-- ==========================================
-- 2. Approvals Table
-- Tracks pause events where the system waits for human input
-- ==========================================
CREATE TABLE IF NOT EXISTS approvals (
    approval_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    node_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'rejected')),
    context_data JSONB DEFAULT '{}'::jsonb,
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by TEXT
);

-- ==========================================
-- 3. Row Level Security (RLS)
-- Enables secure public/authenticated access if Supabase anon key is used
-- ==========================================
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE approvals ENABLE ROW LEVEL SECURITY;

-- Allow public access for Hackathon/Demo purposes. 
-- In production, replace 'true' with 'auth.uid() = user_id'
CREATE POLICY "Allow public read access on workflows" ON workflows FOR SELECT USING (true);
CREATE POLICY "Allow public insert access on workflows" ON workflows FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update access on workflows" ON workflows FOR UPDATE USING (true);
CREATE POLICY "Allow public delete access on workflows" ON workflows FOR DELETE USING (true);

CREATE POLICY "Allow public read access on approvals" ON approvals FOR SELECT USING (true);
CREATE POLICY "Allow public insert access on approvals" ON approvals FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update access on approvals" ON approvals FOR UPDATE USING (true);
CREATE POLICY "Allow public delete access on approvals" ON approvals FOR DELETE USING (true);

-- ==========================================
-- 4. Indexes for Performance
-- ==========================================
CREATE INDEX IF NOT EXISTS idx_workflows_created_at ON workflows(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_approvals_status ON approvals(status);
CREATE INDEX IF NOT EXISTS idx_approvals_workflow_id ON approvals(workflow_id);

-- ==========================================
-- 5. Documents & Vectors
-- ==========================================
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

-- RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access on documents" ON documents FOR SELECT USING (true);
CREATE POLICY "Allow public insert access on documents" ON documents FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access on document_chunks" ON document_chunks FOR SELECT USING (true);
CREATE POLICY "Allow public insert access on document_chunks" ON document_chunks FOR INSERT WITH CHECK (true);

-- RPC for Vector Similarity Search
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
