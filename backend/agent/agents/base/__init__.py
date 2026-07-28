"""Agent 基础包。

原 ``agent/agents/base.py`` 与目录 ``agent/agents/base/`` 同名导致文件遮蔽目录、
``base/base.py``（示例 Agent）无法被导入。现将抽象基类移入 ``base_agent.py``，
``base/`` 作为正式包对外导出 ``BaseAgent`` 与示例 ``WeddingBaseAgent``。
"""

from agent.agents.base_agent import BaseAgent
from agent.agents.base.base import WeddingBaseAgent

__all__ = ["BaseAgent", "WeddingBaseAgent"]
