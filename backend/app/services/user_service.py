"""用户业务逻辑层。

对应技术文档 §4.2 / §5.4。本期从 ``data/users_mock.json`` 读取模拟用户；
后续切换数据库时，仅替换 ``_load_users`` 内部实现即可，对外方法签名不变。
"""

from pathlib import Path

from shared.schemas.user import UserInfo

_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users_mock.json"


class UserService:
    def _load_users(self) -> list[dict]:
        import json

        if not _DATA_PATH.exists():
            return []
        with _DATA_PATH.open(encoding="utf-8") as f:
            return json.load(f)

    def find_user(self, username: str) -> dict | None:
        for u in self._load_users():
            if u["username"] == username:
                return u
        return None

    def authenticate(self, username: str, password: str) -> UserInfo | None:
        """校验用户名/密码，成功返回 ``UserInfo``，失败返回 ``None``。"""
        from app.core.security import verify_password

        raw = self.find_user(username)
        if raw is None:
            return None
        if not verify_password(password, raw["password"]):
            return None
        return self._to_userinfo(raw)

    async def get_by_username(self, username: str) -> UserInfo | None:
        """按用户名获取用户信息（异步签名，便于在依赖中 await 调用）。"""
        raw = self.find_user(username)
        return self._to_userinfo(raw) if raw else None

    @staticmethod
    def _to_userinfo(raw: dict) -> UserInfo:
        return UserInfo(
            id=raw["id"],
            username=raw["username"],
            nickname=raw["nickname"],
            role=raw["role"],
        )
