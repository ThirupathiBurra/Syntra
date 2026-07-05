import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.schema import CreateTable
from app.repository.models import WorkflowModel, ApprovalModel

print("-- Supabase Schema Initialization for Syntra\n")
print("-- Table: workflows")
print(CreateTable(WorkflowModel.__table__).compile(compile_kwargs={"literal_binds": True}).string.strip() + ";\n")

print("-- Table: approvals")
print(CreateTable(ApprovalModel.__table__).compile(compile_kwargs={"literal_binds": True}).string.strip() + ";\n")

print("-- Row Level Security (RLS) Policies")
print("ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;")
print("ALTER TABLE approvals ENABLE ROW LEVEL SECURITY;")
print("CREATE POLICY \"Allow public read access\" ON workflows FOR SELECT USING (true);")
print("CREATE POLICY \"Allow public insert access\" ON workflows FOR INSERT WITH CHECK (true);")
print("CREATE POLICY \"Allow public update access\" ON workflows FOR UPDATE USING (true);")
print("CREATE POLICY \"Allow public read access\" ON approvals FOR SELECT USING (true);")
print("CREATE POLICY \"Allow public insert access\" ON approvals FOR INSERT WITH CHECK (true);")
print("CREATE POLICY \"Allow public update access\" ON approvals FOR UPDATE USING (true);")
