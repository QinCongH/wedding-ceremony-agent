from pydantic import BaseModel


class UserInfo(BaseModel):
    """鉴权通过后对外暴露的用户视图（不含敏感字段）。"""

    id: int
    username: str
    nickname: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
