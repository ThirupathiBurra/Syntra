-- Migration: 20260705_workflows_approvals.sql
-- Description: Creates the workflows and approvals tables for dynamic AI orchestration.

CREATE TABLE IF NOT EXISTS workflows (
    workflow_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT NOT NULL,
    department VARCHAR,
    tags JSONB DEFAULT '[]'::jsonb,
    nodes JSONB NOT NULL,
    dependencies JSONB NOT NULL,
    confidence FLOAT,
    estimated_duration VARCHAR,
    estimated_cost VARCHAR,
    risks JSONB DEFAULT '[]'::jsonb,
    requires_human_approval BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    execution_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS approvals (
    approval_id VARCHAR PRIMARY KEY,
    workflow_id VARCHAR REFERENCES workflows(workflow_id) ON DELETE CASCADE,
    session_id VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    summary TEXT,
    context JSONB DEFAULT '{}'::jsonb,
    status VARCHAR DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR
);
