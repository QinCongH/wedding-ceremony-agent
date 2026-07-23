from typing import Any, Callable, Dict


class ToolRegistry:
    _tools: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str, func: Callable):
        cls._tools[name] = func

    @classmethod
    def get(cls, name: str) -> Callable | None:
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls) -> list[str]:
        return list(cls._tools.keys())
