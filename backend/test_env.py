import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

async def main():
    print("Testing Supabase...")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if url and key:
        try:
            supabase = create_client(url, key)
            res = supabase.table("workflows").select("*").limit(1).execute()
            print("Supabase connection SUCCESS")
        except Exception as e:
            print(f"Supabase connection FAILED: {e}")
    else:
        print("Missing Supabase URL/Key")

    print("Testing LLM API Keys...")
    if os.environ.get("GEMINI_API_KEY") != "YOUR_GEMINI_API_KEY_HERE":
        print("GEMINI_API_KEY is present.")
    if os.environ.get("GROQ_API_KEY") != "YOUR_GROQ_API_KEY_HERE":
        print("GROQ_API_KEY is present.")
        
    db_url = os.environ.get("SUPABASE_DB_URL")
    if "[YOUR-PASSWORD]" in db_url:
        print("WARNING: [YOUR-PASSWORD] still present in SUPABASE_DB_URL")

asyncio.run(main())
