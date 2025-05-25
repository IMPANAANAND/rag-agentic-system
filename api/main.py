import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    from agent.agent import run_agent
except Exception as e:
    print(f"Import Error: {e}")
    traceback.print_exc()
    sys.exit(1)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        result = await run_agent(request.query)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)