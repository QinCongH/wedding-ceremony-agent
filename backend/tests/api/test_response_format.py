"""统一响应格式测试。"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_api_response_model_exists():
    """ApiResponse 模型可导入且为泛型。"""
    from shared.schemas.response import ApiResponse

    instance = ApiResponse(data={"key": "value"})
    assert instance.code == 200
    assert instance.message == "ok"
    assert instance.data == {"key": "value"}


@pytest.mark.asyncio
async def test_api_response_error_fields():
    """ApiResponse 错误场景字段正确。"""
    from shared.schemas.response import ApiResponse

    instance = ApiResponse(code=401, message="invalid_token", data=None)
    assert instance.code == 401
    assert instance.message == "invalid_token"
    assert instance.data is None
