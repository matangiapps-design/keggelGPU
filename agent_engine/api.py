from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from .config import settings
from .engine import AgentEngine

app = FastAPI(title="MATANGI Agent Engine", version="0.1.0")
engine = AgentEngine()

class RunRequest(BaseModel):
    task: str = Field(min_length=1, max_length=12000)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "matangi-agent-engine"}

@app.post("/v1/agent/run")
async def run_agent(body: RunRequest, authorization: str | None = Header(default=None)):
    if not settings.engine_api_key:
        raise HTTPException(status_code=503, detail="ENGINE_API_KEY is not configured")
    if authorization != f"Bearer {settings.engine_api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        return await engine.run(body.task)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Model backend error: {exc}") from exc
