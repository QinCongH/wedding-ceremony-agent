from typing import Any


class WorkflowGraph:
    """定义Agent间的调用图"""

    def __init__(self):
        self._nodes: dict[str, Any] = {}
        self._edges: dict[str, list[str]] = {}

    def add_node(self, name: str, agent: Any):
        self._nodes[name] = agent

    def add_edge(self, from_node: str, to_node: str):
        self._edges.setdefault(from_node, []).append(to_node)

    def get_next(self, node: str) -> list[str]:
        return self._edges.get(node, [])
