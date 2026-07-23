# 婚礼仪式智能体 - 目录结构说明

## 顶层结构

```
backend/
├── app/                    # FastAPI Web应用层
├── agent/                  # 智能体核心层（与Web层解耦）
├── shared/                 # 共享类型与协议
├── alembic/                # 数据库迁移
├── tests/                  # 测试
├── scripts/                # 运维脚本
├── pyproject.toml          # 项目依赖与工具配置
├── .env.example            # 环境变量模板
└── .gitignore
```

## app/ — FastAPI Web应用层

负责HTTP接口、依赖注入、数据库会话管理。不包含智能体决策逻辑。

```
app/
├── __init__.py
├── main.py                 # FastAPI应用工厂，挂载路由、生命周期事件
├── api/                    # 路由层
│   ├── __init__.py
│   ├── deps.py             # 全局依赖注入（get_db, get_agent等）
│   └── v1/                 # API版本化
│       ├── __init__.py
│       ├── router.py       # 汇总所有子路由
│       ├── chat.py         # 对话接口 POST /api/v1/chat
│       ├── plan.py         # 婚礼方案接口 GET/POST /api/v1/plan
│       └── task.py         # 任务管理接口 GET/POST /api/v1/task
├── core/                   # 核心配置
│   ├── __init__.py
│   ├── config.py           # pydantic-settings，从.env读取所有配置
│   ├── database.py         # SQLAlchemy异步引擎、会话工厂、Base模型
│   └── security.py         # 认证鉴权（预留）
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── db.py               # SQLAlchemy ORM模型（数据库表定义）
│   └── schema.py           # Pydantic请求/响应Schema
├── services/               # 业务逻辑层
│   ├── __init__.py
│   └── chat_service.py     # 编排Agent调用，是API和Agent的桥梁
└── utils/                  # 工具函数
    ├── __init__.py
    └── logger.py           # 日志配置
```

### 关键文件说明

| 文件 | 职责 | 注意事项 |
|------|------|----------|
| `main.py` | 应用入口，`create_app()`工厂模式 | 通过`on_event("startup")`初始化数据库表 |
| `api/deps.py` | FastAPI `Depends`注入 | 将Agent/DB实例注入路由，避免路由直接import实现 |
| `core/config.py` | 所有配置集中管理 | 使用pydantic-settings，支持.env文件 |
| `services/chat_service.py` | API与Agent的桥梁 | 负责组装memory、调用agent、返回结果 |

## agent/ — 智能体核心层

纯决策逻辑，不感知HTTP和数据库。可被API层、CLI、定时任务等多种入口调用。

```
agent/
├── __init__.py
├── agents/                 # Agent定义
│   ├── __init__.py
│   ├── base.py             # Agent基类，定义run()接口
│   ├── coordinator.py      # 协调Agent：意图识别，路由到子Agent
│   ├── planner.py          # 规划Agent：生成婚礼方案
│   └── executor.py         # 执行Agent：调用工具完成具体操作
├── tools/                  # Agent可调用的工具
│   ├── __init__.py
│   ├── registry.py         # 工具注册表，统一管理工具的注册与查找
│   ├── search.py           # 场地/供应商搜索工具
│   └── calendar.py         # 日历查询工具
├── workflow/               # 工作流编排
│   ├── __init__.py
│   ├── graph.py            # 工作流有向图，定义Agent间调用关系
│   └── router.py           # Agent路由器，根据意图分发到对应Agent
├── prompts/                # Prompt模板（Markdown文件）
│   ├── coordinator.md      # 协调Agent的系统Prompt
│   └── planner.md          # 规划Agent的系统Prompt
└── memory/                 # 记忆管理
    ├── __init__.py
    ├── short_term.py       # 短期记忆：对话上下文，内存存储
    └── long_term.py        # 长期记忆：跨会话，数据库持久化
```

### 关键文件说明

| 文件 | 职责 | 注意事项 |
|------|------|----------|
| `agents/base.py` | 定义`BaseAgent`抽象基类 | 所有Agent必须实现`run()`方法 |
| `agents/coordinator.py` | 主入口Agent | 识别用户意图，路由到planner或executor |
| `agents/planner.py` | 方案生成 | 接入LLM，结合Prompt模板生成婚礼方案 |
| `agents/executor.py` | 任务执行 | 调用tools完成搜索、预订等操作 |
| `tools/registry.py` | 工具注册中心 | Agent通过名称查找工具，解耦工具实现 |
| `workflow/graph.py` | 工作流图 | 定义Agent调用链，如 coordinator→planner→executor |
| `workflow/router.py` | 意图路由 | 根据LLM分类结果分发到对应Agent |
| `prompts/*.md` | Prompt外置 | 方便迭代修改，不改Python代码 |
| `memory/short_term.py` | 对话记忆 | 每次对话的上下文历史 |
| `memory/long_term.py` | 持久记忆 | 用户偏好、历史方案等跨会话数据 |

## shared/ — 共享类型与协议

app/和agent/共用的数据结构，避免循环依赖。

```
shared/
├── __init__.py
└── schemas/
    ├── __init__.py
    └── chat.py             # ChatRequest/ChatResponse等共享模型
```

## alembic/ — 数据库迁移

```
alembic/
├── versions/               # 迁移脚本存放目录
├── env.py                  # Alembic环境配置
└── alembic.ini             # Alembic主配置
```

## tests/ — 测试

按应用结构镜像组织。

```
tests/
├── __init__.py
├── api/                    # API接口测试
│   └── __init__.py
├── agents/                 # Agent逻辑测试
│   └── __init__.py
└── services/               # Service层测试
    └── __init__.py
```

## scripts/ — 运维脚本

```
scripts/
├── start.sh                # 启动脚本
└── migrate.sh              # 数据库迁移脚本
```

---

## 调用链路

```
HTTP Request
  → app/api/v1/chat.py (参数校验)
    → app/api/deps.py (依赖注入)
      → app/services/chat_service.py (业务编排)
        → agent/memory/ (加载记忆)
        → agent/agents/coordinator.py (意图识别)
          → agent/workflow/router.py (路由分发)
            → agent/agents/planner.py 或 executor.py
              → agent/tools/ (调用工具)
        → agent/memory/ (保存记忆)
      ← ChatResponse
  ← HTTP Response
```

## 设计原则

1. **Web层与Agent层解耦** — agent/不依赖FastAPI，可被CLI、定时任务等复用
2. **Agent与工具解耦** — Agent只做决策，能力由tools提供，通过registry查找
3. **编排与执行分离** — workflow/只管流程，agents/只管逻辑
4. **Prompt外置** — prompts/目录存放Markdown模板，方便非开发人员修改
5. **配置集中** — 所有配置通过core/config.py读取.env，不硬编码
6. **共享类型隔离** — shared/避免app/和agent/之间循环依赖
