"""全局依赖注入。

对应技术文档 §7.1。``get_current_user`` 校验 Bearer token，并将 token 与用户信息
同时存入 ``request.state`` 与 ``agent.context``（contextvars），供下游 Service / Agent 读取。
"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from agent.context import set_auth_token, set_auth_user
from app.core.security import decode_access_token
from app.services.user_service import UserService
from shared.schemas.user import UserInfo

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> UserInfo:
    if creds is None or not creds.credentials:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing_token")

    try:
        payload = decode_access_token(creds.credentials)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid_or_expired_token")

    user = await UserService().get_by_username(payload.get("sub", ""))
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user_not_found")

    # 需求 4：鉴权通过后将 token 及用户信息"存起来"
    request.state.token = creds.credentials
    request.state.user = user
    # 注入 contextvars，供解耦的 Agent 层读取（需求 5）
    set_auth_token(creds.credentials)
    set_auth_user(user)
    return user
