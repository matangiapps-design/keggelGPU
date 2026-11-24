"""Small, explicit tool registry. No arbitrary shell or filesystem access by default."""
from typing import Any, Callable

Tool = Callable[[dict[str, Any]], dict[str, Any]]

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[str, Tool]] = {}

    def register(self, name: str, description: str, fn: Tool) -> None:
        if not name.isidentifier():
            raise ValueError("Tool names must be valid identifiers")
        self._tools[name] = (description, fn)

    def schemas(self) -> list[dict[str, Any]]:
        return [{
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {"type": "object", "properties": {}, "additionalProperties": True},
            },
        } for name, (description, _) in self._tools.items()]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            return {"ok": False, "error": f"Tool not allowed: {name}"}
        try:
            return {"ok": True, "result": self._tools[name][1](arguments)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

def default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        "calculator",
        "Evaluate basic arithmetic. Input: {expression: string}. Only numeric arithmetic is supported.",
        _calculate,
    )
    return registry

def _calculate(args: dict[str, Any]) -> dict[str, Any]:
    # Deliberately restricted parser: no eval(), names, imports, or function calls.
    import ast, operator
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
           ast.UAdd: operator.pos, ast.Mod: operator.mod}
    tree = ast.parse(str(args.get("expression", "")), mode="eval")
    def walk(node: ast.AST) -> float:
        if isinstance(node, ast.Expression): return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)): return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops: return ops[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in ops: return ops[type(node.op)](walk(node.operand))
        raise ValueError("Unsupported arithmetic expression")
    value = walk(tree)
    if abs(value) > 1e100: raise ValueError("Result exceeds safety limit")
    return {"value": value}
