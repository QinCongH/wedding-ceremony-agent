"""消息业务逻辑层。对应技术文档 §6.2。

本期消息存储使用进程内内存（模拟持久化），后续接入 ``Message`` ORM 与 ``data.db`` 时
仅需替换内部存储实现，对外方法签名保持一致。
"""

from datetime import datetime

from shared.schemas.message import MessageCreate, MessageOut

# 进程内存储：[(id, user_id, content, session_id, created_at), ...]
_store: list[dict] = []
_seq = 0


class MessageService:
    def create(self, content: str, user_id: int, session_id: str | None = None) -> MessageOut:
        global _seq
        _seq += 1
        created_at = datetime.now().isoformat(timespec="seconds")
        record = {
            "id": _seq,
            "user_id": user_id,
            "content": content,
            "session_id": session_id,
            "created_at": created_at,
        }
        _store.append(record)
        return self._to_out(record)

    def get(self, message_id: int) -> dict | None:
        for r in _store:
            if r["id"] == message_id:
                return r
        return None

    def delete(self, message_id: int, user_id: int) -> MessageOut:
        """删除消息，仅允许删除本人消息。"""
        record = self.get(message_id)
        if record is None:
            raise NotFound(message_id)
        if record["user_id"] != user_id:
            raise NotOwner()
        _store.remove(record)
        return self._to_out(record)

    @staticmethod
    def _to_out(record: dict) -> MessageOut:
        return MessageOut(
            id=record["id"],
            user_id=record["user_id"],
            content=record["content"],
            session_id=record["session_id"],
            created_at=record["created_at"],
        )


class NotFound(Exception):
    def __init__(self, message_id: int) -> None:
        self.message_id = message_id
        super().__init__(f"message {message_id} not found")


class NotOwner(Exception):
    """当前用户不是消息所有者。"""
