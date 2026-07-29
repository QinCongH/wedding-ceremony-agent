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


@pytest.mark.asyncio
async def test_http_exception_returns_unified_format(client):
    """HTTPException 返回 {code, message, data} 格式。"""
    async with client:
        resp = await client.post("/api/v1/chat")  # 需鉴权，未带 token 触发 401
        body = resp.json()
        assert "code" in body
        assert "message" in body
        assert "data" in body
        assert body["code"] == 401
        assert body["data"] is None


@pytest.mark.asyncio
async def test_validation_error_returns_unified_format(client):
    """请求体验证错误返回 {code, message, data} 格式。"""
    async with client:
        resp = await client.post("/api/v1/user/login", json={})
        body = resp.json()
        assert "code" in body
        assert "message" in body
        assert "data" in body
        assert body["code"] == 422
        assert body["data"] is None
