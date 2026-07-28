"""鉴权链路冒烟测试：登录 + 受保护接口 + 消息增删 + 鉴权错误码。

运行：backend/ 下 `python scripts/smoke_auth.py`（venv）。
不依赖外部 LLM，仅验证 Web 层与鉴权链路。
"""

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def main() -> int:
    client = TestClient(app)
    base = "/api/v1"
    failures = []

    def check(name: str, cond: bool) -> None:
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            failures.append(name)

    # 1) 错误密码登录 -> 401
    r = client.post(f"{base}/user/login", json={"username": "alice", "password": "wrong"})
    check("login wrong password -> 401", r.status_code == 401)

    # 2) 正确登录 -> 200 + token
    r = client.post(f"{base}/user/login", json={"username": "alice", "password": "alice123"})
    check("login correct -> 200", r.status_code == 200)
    token = r.json().get("access_token", "")
    check("login returns token", bool(token))
    check("token_type bearer", r.json().get("token_type") == "bearer")

    headers = {"Authorization": f"Bearer {token}"}

    # 3) 无 token 访问受保护接口 -> 401
    r = client.post(f"{base}/message", json={"content": "hi"})
    check("message no token -> 401", r.status_code == 401)

    # 4) 带 token 发送消息 -> 201
    r = client.post(f"{base}/message", json={"content": "hello", "session_id": "s1"}, headers=headers)
    check("message with token -> 201", r.status_code == 201)
    msg_id = r.json().get("id")
    check("message user_id == alice.id(1)", r.json().get("user_id") == 1)

    # 5) 删除本人消息 -> 200
    r = client.delete(f"{base}/message/{msg_id}", headers=headers)
    check("delete own message -> 200", r.status_code == 200)

    # 6) 删除不存在消息 -> 404
    r = client.delete(f"{base}/message/999999", headers=headers)
    check("delete missing -> 404", r.status_code == 404)

    # 7) bob 不能删 alice 的消息 -> 403
    rb = client.post(f"{base}/user/login", json={"username": "bob", "password": "bob123"})
    bob_headers = {"Authorization": f"Bearer {rb.json()['access_token']}"}
    rm = client.post(f"{base}/message", json={"content": "bob msg"}, headers=bob_headers)
    bob_msg_id = rm.json()["id"]
    # alice 尝试删 bob 的消息
    r = client.delete(f"{base}/message/{bob_msg_id}", headers=headers)
    check("delete others message -> 403", r.status_code == 403)

    # 8) 篡改 token -> 401
    r = client.post(f"{base}/message", json={"content": "x"}, headers={"Authorization": "Bearer tampered.token.here"})
    check("tampered token -> 401", r.status_code == 401)

    # 9) 接口清单存在
    r = client.get("/openapi.json")
    paths = r.json().get("paths", {})
    check("openapi has /user/login", f"{base}/user/login" in paths)
    check("openapi has /message", f"{base}/message" in paths)

    if failures:
        print(f"\nFAILED {len(failures)}: {failures}")
        return 1
    print("\nALL PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
