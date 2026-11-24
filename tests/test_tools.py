from agent_engine.tools import default_registry

def test_calculator():
    result = default_registry().execute("calculator", {"expression": "(12 + 8) * 3"})
    assert result == {"ok": True, "result": {"value": 60}}

def test_unknown_tool_is_blocked():
    result = default_registry().execute("run_shell", {"command": "id"})
    assert result["ok"] is False
