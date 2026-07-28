"""鉴权上下文（Auth Context）。

职责：在「请求 / Agent 运行」生命周期内，异步安全地传播**鉴权 token** 与 **用户信息**。

设计要点：
- 使用 ``contextvars.ContextVar`` 而非 ``Request`` 对象，保证 Agent 层与 Web 层解耦——
  Agent 不直接依赖 FastAPI，可在 CLI / 定时任务 / 测试中以纯 Python 方式注入上下文。
- 对应需求 5：「鉴权 token 通过 context 存储」。
- 提供 ``auth_context`` 上下文管理器，进入时写入、退出时自动重置，避免协程/请求之间串号。
"""

from contextvars import ContextVar
from typing import Iterator, Optional

from shared.schemas.user import UserInfo

_auth_token_var: ContextVar[Optional[str]] = ContextVar("auth_token", default=None)
_auth_user_var: ContextVar[Optional[UserInfo]] = ContextVar("auth_user", default=None)


# --------------------------------------------------------------------------- #
# Token
# --------------------------------------------------------------------------- #
def set_auth_token(token: Optional[str]) -> None:
    """写入当前上下文的鉴权 token。"""
    _auth_token_var.set(token)


def get_auth_token() -> Optional[str]:
    """读取当前上下文的鉴权 token；未设置时返回 ``None``。"""
    return _auth_token_var.get()


# --------------------------------------------------------------------------- #
# User
# --------------------------------------------------------------------------- #
def set_auth_user(user: Optional[UserInfo]) -> None:
    """写入当前上下文的用户信息。"""
    _auth_user_var.set(user)


def get_auth_user() -> Optional[UserInfo]:
    """读取当前上下文的用户信息；未设置时返回 ``None``。"""
    return _auth_user_var.get()


# --------------------------------------------------------------------------- #
# 统一上下文管理器
# --------------------------------------------------------------------------- #
class auth_context:
    """一次性注入 token + user 的上下文管理器，退出时自动复位。

    用法::

        with auth_context(token="xxx", user=user_info):
            # 此处 get_auth_token() / get_auth_user() 生效
            ...
        # 退出后自动清空，避免影响后续协程
    """

    def __init__(self, token: Optional[str] = None, user: Optional[UserInfo] = None) -> None:
        self._token = token
        self._user = user
        self._reset_tokens: list = []

    def __enter__(self) -> "auth_context":
        self._reset_tokens.append(_auth_token_var.set(self._token))
        self._reset_tokens.append(_auth_user_var.set(self._user))
        return self

    def __exit__(self, *exc_info: object) -> None:
        _auth_token_var.reset(self._reset_tokens[0])
        _auth_user_var.reset(self._reset_tokens[1])
        self._reset_tokens.clear()
