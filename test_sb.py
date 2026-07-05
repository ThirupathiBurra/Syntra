import asyncio
from app.core.config import settings
from supabase import create_client

def test():
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    res = client.table("documents").select("*").limit(1).execute()
    print(res)

test()
