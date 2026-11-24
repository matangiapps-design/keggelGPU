from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    model_base_url: str = os.getenv("MODEL_BASE_URL", "http://localhost:8000/v1")
    model_api_key: str = os.getenv("MODEL_API_KEY", "EMPTY")
    model_name: str = os.getenv("MODEL_NAME", "Qwen/Qwen3.6-27B")
    engine_api_key: str = os.getenv("ENGINE_API_KEY", "")
    max_steps: int = int(os.getenv("AGENT_MAX_STEPS", "6"))
    request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", "90"))

settings = Settings()
