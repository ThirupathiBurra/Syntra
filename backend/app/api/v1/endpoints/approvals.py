from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.core.config import get_supabase_client
from datetime import datetime

router = APIRouter()

@router.get("")
async def list_approvals():
    """List pending approvals."""
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("approvals").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Failed to fetch approvals: {e}")
        return []

@router.post("/{approval_id}/resolve")
async def resolve_approval(approval_id: str, payload: Dict[str, Any]):
    """Approve or reject a pending approval."""
    supabase = get_supabase_client()
    if not supabase:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    status = payload.get("status")
    if status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    try:
        now = datetime.utcnow().isoformat()
        response = supabase.table("approvals").update({
            "status": status,
            "resolved_by": "Syntra User",
            "resolved_at": now
        }).eq("approval_id", approval_id).execute()
        
        return response.data[0] if response.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
