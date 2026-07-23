from typing import Any


class ShortTermMemory:
    """对话级短期记忆"""

    def __init__(self):
        self._messages: list[dict[str, str]] = []

    def add_user_message(self, content: str):
        self._messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self._messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> list[dict[str, str]]:
        return self._messages

    def clear(self):
        self._messages.clear()
