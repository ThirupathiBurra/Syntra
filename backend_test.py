import asyncio
import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
print("API Key:", api_key[:5] if api_key else "None")
genai.configure(api_key=api_key)

print("Starting embed_content...")
try:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=["test"],
        task_type="retrieval_document"
    )
    print("Done:", len(result['embedding']))
except Exception as e:
    print("Error:", e)
