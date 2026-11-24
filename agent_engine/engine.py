import json
import httpx
from .config import settings
from .tools import ToolRegistry, default_registry

class AgentEngine:
    """OpenAI-compatible tool-calling loop with bounded steps and explicit tools."""
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or default_registry()

    async def run(self, task: str) -> dict:
        if not task.strip():
            raise ValueError("task must not be empty")
        messages = [
            {"role": "system", "content": "You are MATANGI Agent, a careful task assistant. Use available tools only when useful. Never claim an action happened unless a tool confirms it. If tools cannot do a task, explain the limitation."},
            {"role": "user", "content": task},
        ]
        headers = {"Authorization": f"Bearer {settings.model_api_key}"}
        payload = {"model": settings.model_name, "messages": messages,
                   "tools": self.registry.schemas(), "tool_choice": "auto", "temperature": 0.2}
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            for step in range(settings.max_steps):
                response = await client.post(f"{settings.model_base_url.rstrip('/')}/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                choice = data["choices"][0]["message"]
                messages.append(choice)
                calls = choice.get("tool_calls") or []
                if not calls:
                    return {"ok": True, "answer": choice.get("content") or "", "steps": step + 1}
                for call in calls:
                    fn = call.get("function", {})
                    try:
                        arguments = json.loads(fn.get("arguments") or "{}")
                    except json.JSONDecodeError:
                        arguments = {}
                        result = {"ok": False, "error": "Tool arguments were not valid JSON"}
                    else:
                        result = self.registry.execute(fn.get("name", ""), arguments)
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(result)})
        return {"ok": False, "answer": "Agent step limit reached. Increase AGENT_MAX_STEPS if appropriate.", "steps": settings.max_steps}
