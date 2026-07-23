# 婚礼仪式智能体 - 运行文档

## 环境要求

- Python >= 3.11
- pip 或 uv（推荐uv，更快）
- Redis（可选，长期记忆需要）

## 快速开始

### 1. 进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 或使用 uv（推荐）
uv venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# pip
pip install -e ".[dev]"

# uv
uv pip install -e ".[dev]"
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，至少配置以下项：

```env
# 必填：LLM API密钥
LLM_API_KEY=sk-your-actual-key

# 可选：自定义LLM端点（使用Azure/其他兼容API时填写）
LLM_BASE_URL=https://api.openai.com/v1

# 可选：模型选择
LLM_MODEL=gpt-4o
```

### 5. 初始化数据库

```bash
# 首次运行会自动创建SQLite数据库（app/main.py的startup事件）
# 如需使用Alembic迁移：
alembic upgrade head
```

### 6. 启动服务

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 7. 验证服务

```bash
# 健康检查
curl http://localhost:8000/docs

# 测试对话接口
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "帮我规划一场户外婚礼"}'
```

## 开发指南

### 项目结构导航

```
backend/
├── app/          → 修改API接口、业务逻辑
├── agent/        → 修改Agent行为、工具、Prompt
├── shared/       → 修改共享数据结构
└── tests/        → 编写测试
```

### 添加新Agent

1. 在 `agent/agents/` 下创建新文件，继承 `BaseAgent`：

```python
# agent/agents/venue_agent.py
from agent.agents.base import BaseAgent

class VenueAgent(BaseAgent):
    name = "venue"
    description = "场地推荐Agent"

    async def run(self, input_text: str, **kwargs) -> str:
        # 实现逻辑
        return result
```

2. 在 `agent/agents/__init__.py` 中导出

3. 在 `agent/workflow/router.py` 中注册路由

4. 在 `agent/prompts/` 下添加对应的Prompt模板

### 添加新工具

1. 在 `agent/tools/` 下创建新文件：

```python
# agent/tools/booking.py
from agent.tools.registry import ToolRegistry

def book_venue(venue_id: str, date: str) -> str:
    """预订场地"""
    # 实现逻辑
    return f"已预订场地 {venue_id}，日期 {date}"

ToolRegistry.register("book_venue", book_venue)
```

2. 在Agent中通过 `ToolRegistry.get("book_venue")` 调用

### 添加新API接口

1. 在 `app/api/v1/` 下创建路由文件
2. 在 `app/api/v1/router.py` 中注册
3. 在 `app/services/` 下创建对应的Service
4. 在 `shared/schemas/` 下定义请求/响应模型

### 修改Prompt

直接编辑 `agent/prompts/` 下的Markdown文件，无需修改Python代码。

## 测试

```bash
# 运行全部测试
pytest

# 运行指定模块
pytest tests/agents/
pytest tests/api/

# 查看覆盖率
pytest --cov=app --cov=agent --cov-report=html
```

## 数据库迁移

```bash
# 生成迁移脚本（修改ORM模型后执行）
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

## 常见问题

### Q: 启动报错 `ModuleNotFoundError: No module named 'agent'`

确保从 `backend/` 目录启动，或设置 PYTHONPATH：

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn app.main:app --reload
```

### Q: LLM调用超时

在 `.env` 中调整超时配置：

```env
AGENT_TIMEOUT=120
```

### Q: 想切换到PostgreSQL

修改 `.env` 中的 `DATABASE_URL`：

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/wedding
```

同时安装驱动：

```bash
pip install asyncpg
```

## Docker部署（可选）

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e ".[dev]"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t wedding-agent .
docker run -d -p 8000:8000 --env-file .env wedding-agent
```
