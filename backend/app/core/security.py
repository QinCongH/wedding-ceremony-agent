"""认证鉴权工具：JWT 签发/校验、密码校验。

对应技术文档 §5.2。本期用户数据为 JSON 模拟，密码以明文比较；
DB 阶段 `verify_password` 自动识别 bcrypt 哈希走 `passlib` 校验。
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str, extra: dict | None = None, expires_minutes: int | None = None) -> str:
    """签发 JWT。payload 含 sub=username 与过期时间 exp。"""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """校验并解码 JWT，失败抛出 ``jose.JWTError``。"""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def hash_password(plain: str) -> str:
    """生成 bcrypt 哈希（DB 阶段注册/改密使用）。"""
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """校验密码。

    - DB 阶段：``hashed`` 为 bcrypt 哈希，走 ``passlib`` 校验；
    - 模拟阶段：``hashed`` 为明文，直接相等比较。
    """
    if hashed.startswith(("$2a$", "$2b$", "$2y$")):
        return _pwd_context.verify(plain, hashed)
    return plain == hashed
