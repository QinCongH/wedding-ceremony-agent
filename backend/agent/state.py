"""Agent 运行时状态（AgentState）。

职责：作为 Agent 运行期的「状态载体」，携带**用户信息**、**鉴权 token** 及自定义元数据，
随 ``agent.run(input_text, state=...)`` 透传给 Agent 及其子组件。

设计要点：
- 对应需求 5：「用户信息通过 AgentState 存储」。
- 与 ``agent.context`` 配合：``context`` 负责请求级传播，
  ``AgentState`` 负责把这些信息以**显式参数**形式交到 Agent 手中，二者互补。
- 使用 ``dataclass``，轻量、可序列化、易扩展（后续可加入 ``session_id``、
  ``conversation_history`` 等字段以支撑动态提示词与工具鉴权）。
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from shared.schemas.user import UserInfo


@dataclass
class AgentState:
    """Agent 单次运行的上下文状态。"""

    #: 当前调用者信息（来自鉴权依赖）
    user: Optional[UserInfo] = None
    #: 当前鉴权 token（来自 context）
    token: Optional[str] = None
    #: 自定义扩展字段，避免频繁改签名
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    # 便捷读写扩展字段
    # ------------------------------------------------------------------ #
    def set(self, key: str, value: Any) -> None:
        """写入扩展字段。"""
        self.metadata[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """读取扩展字段，缺失时返回 ``default``。"""
        return self.metadata.get(key, default)

    # ------------------------------------------------------------------ #
    # 常用派生属性
    # ------------------------------------------------------------------ #
    @property
    def user_id(self) -> Optional[int]:
        """当前用户 ID（未登录时 ``None``）。"""
        return self.user.id if self.user else None

    @property
    def username(self) -> Optional[str]:
        """当前用户名（未登录时 ``None``）。"""
        return self.user.username if self.user else None

    @property
    def is_authenticated(self) -> bool:
        """是否已通过鉴权。"""
        return self.user is not None and self.token is not None

    @classmethod
    def from_context(cls, **extra: Any) -> "AgentState":
        """从 ``agent.context`` 中读取 token 与 user，快速构造状态。

        在 Service 层组装 AgentState 时可直接调用，避免重复取 context。
        """
        from agent.context import get_auth_token, get_auth_user

        return cls(token=get_auth_token(), user=get_auth_user(), metadata=dict(extra))
