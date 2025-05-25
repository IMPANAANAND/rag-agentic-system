import aiohttp
import json
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .tools import query_mysql_database

async def run_agent(query: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            # Query database directly for simplicity
            db_query = """
            SELECT document_number, title, publication_date, president, abstract
            FROM executive_orders
            WHERE president = %s AND publication_date LIKE %s
            """
            params = ("Joe Biden", "2024%")
            results = query_mysql_database(db_query, params)
            
            if not results:
                return "No executive orders found for President Donald Trump in May 2025."
            
            context = "\n".join([
                f"Document: {r['document_number']}, Title: {r['title']}, "
                f"Date: {r['publication_date']}, President: {r['president']}, "
                f"Abstract: {r['abstract'] or 'No abstract available'}"
                for r in results
            ])
            
            payload = {
                "model": "qwen2.5:0.5b",
                "messages": [
                    {"role": "system", "content": "Summarize executive orders concisely."},
                    {"role": "user", "content": f"Query: {query}\nContext:\n{context}\nSummarize the relevant executive orders."}
                ],
                "stream": False
            }
            
            async with session.post("http://localhost:11434/v1/chat/completions", json=payload) as response:
                if response.status != 200:
                    return f"Error calling Ollama: {await response.text()}"
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    async def main():
        result = await run_agent("What are the new executive orders by President Joe Biden this month and summarize them for me?")
        print(result)
    
    asyncio.run(main())