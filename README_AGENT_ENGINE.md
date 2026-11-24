# MATANGI Agent Engine (prototype)

A compact Python agent runtime designed to sit between MATANGI clients and an OpenAI-compatible model server (for example, vLLM). It is deliberately separate from the CUDA demo in KeggelGPU.

## Architecture

Android / Web client -> authenticated FastAPI -> bounded agent loop -> explicit tool registry -> OpenAI-compatible model endpoint.

KeggelGPU remains an optional CUDA experimentation/benchmark layer. It is not required to run the agent orchestration service and is not currently wired into model inference.

## Run locally

Python 3.11+ recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MODEL_BASE_URL=http://localhost:8000/v1
export MODEL_API_KEY=EMPTY
export MODEL_NAME=your-served-model-name
export ENGINE_API_KEY='replace-with-a-long-random-secret'
uvicorn agent_engine.api:app --host 127.0.0.1 --port 8080
```

Health check: `GET http://127.0.0.1:8080/health`.

Agent request: `POST /v1/agent/run` with header `Authorization: Bearer $ENGINE_API_KEY` and JSON body `{"task":"Calculate (12 + 8) * 3"}`.

## Safety and current limits

- Only registered tools can run; there is no arbitrary shell, browser, or filesystem tool.
- Tool loop is bounded by `AGENT_MAX_STEPS` (default 6).
- The calculator uses a restricted AST parser, not Python eval.
- API key authentication is required for agent requests; keep the service behind HTTPS/reverse proxy in production.
- The model server must already be running and support OpenAI-compatible chat completions and function/tool calling.
- This is a prototype, not production-hardened. Add rate limiting, structured audit logs, per-user quotas, secret rotation, and deployment tests before selling access.
- No GPU acceleration is implemented here. KeggelGPU's existing CUDA vector-add sample remains separate.
