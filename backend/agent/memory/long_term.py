from typing import Any


class LongTermMemory:
    """跨会话长期记忆，持久化到数据库"""

    def __init__(self):
        # TODO: 接入数据库存储
        pass

    async def save(self, key: str, value: Any):
        pass

    async def load(self, key: str) -> Any | None:
        return None

    async def search(self, query: str) -> list[Any]:
        return []
