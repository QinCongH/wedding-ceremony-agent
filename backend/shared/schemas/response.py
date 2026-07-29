from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "ok"
    data: T | None = None

    @classmethod
    def success(cls, data: T | None = None, message: str = "ok") -> "ApiResponse[T]":
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, code: int, message: str) -> "ApiResponse[None]":
        return cls(code=code, message=message, data=None)
