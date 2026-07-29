# wedding-ceremony-agent — 开发规范

> 本规范由 spec-check 自动生成，基于 spec-dev 轻量级规范开发工作流，确保本项目在每次会话中自动遵循规范开发流程。

## 核心理念

- **省Token优先**：子技能精炼，按需加载
- **复杂度动态路由**：简单任务直接干，复杂任务走流程
- **用户说了算**：用户可随时覆盖阈值设定

## 配置文件

默认生成：`.workbuddy/spec-dev/config.json`

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| max_questions | 5 | 需求规划时最大提问数 |
| skip_questions | false | 跳过提问，智能分析按最优解处理 |
| plan_file_threshold | 5 | 修改文件数超过此值才走技术文档流程 |
| plan_line_threshold | 100 | 修改代码行数超过此值才走技术文档流程 |
| generate_test_report | false | 是否生成测试与验证分析报告 |
| generate_dev_memory | true | 是否生成功能开发记忆 |
| enable_code_review | true | 是否启用代码审查 |

## 复杂度评估

### 简单任务（直接执行）

满足全部条件：
- 预计修改文件数 ≤ plan_file_threshold
- 预计修改代码行数 ≤ plan_line_threshold
- 不涉及架构变更、新模块、多组件协调

### 复杂任务（走完整流程）

满足任一条件：
- 预计修改文件数 > plan_file_threshold
- 预计修改代码行数 > plan_line_threshold
- 涉及新功能开发、架构调整、多模块协调
- 用户明确要求走规范流程

## 完整工作流（复杂任务）

按以下顺序执行，每步读取 `subskills/<技能名>/SKILL.md`：

```
1. 规范检测    → subskills/spec-check/SKILL.md
   检查/创建 CLAUDE.md 或 AGENTS.md

2. 需求规划    → subskills/req-plan/SKILL.md
   提问式澄清需求（受 max_questions / skip_questions 控制）

3. 任务分解    → subskills/task-split/SKILL.md（大型需求时）
   拆解为可独立执行的子任务

4. 技术文档    → subskills/dev-plan/SKILL.md
   生成实施技术文档（plan doc）

5. 执行开发
   按技术文档实施代码变更

6. 测试验证    → subskills/test-verify/SKILL.md（受 generate_test_report 控制）
   生成功能测试与验证分析报告

7. 代码审查    → subskills/code-review/SKILL.md（受 enable_code_review 控制）
   分支对比，评估影响范围与风险

8. 开发记忆    → subskills/dev-memo/SKILL.md（受 generate_dev_memory 控制）
   生成简短精炼的开发记忆
```

## 子技能清单

所有子技能已内置在 `.claude/spec-dev/subskills/` 目录中，无需单独安装：

| 目录 | 技能 | 说明 |
|------|------|------|
| subskills/spec-check/ | 规范检测 | 项目规范文件检测与创建 |
| subskills/req-plan/ | 需求规划 | 提问式需求澄清 |
| subskills/dev-plan/ | 技术文档 | 实施方案生成 |
| subskills/task-split/ | 任务分解 | 大型需求拆解 |
| subskills/test-verify/ | 测试验证 | 测试覆盖分析 |
| subskills/code-review/ | 代码审查 | 分支对比风险评估 |
| subskills/dev-memo/ | 开发记忆 | 精炼开发记录 |

## 快捷访问

直接通过技能名触发子技能，可针对用户输入或引用的内容独立调用：

| 命令 | 子技能路径 | 说明 |
|------|-----------|------|
| /spec-check | subskills/spec-check/SKILL.md | 项目规范文件检测 |
| /req-plan | subskills/req-plan/SKILL.md | 需求规划 |
| /dev-plan | subskills/dev-plan/SKILL.md | 实施技术文档 |
| /task-split | subskills/task-split/SKILL.md | 任务分解 |
| /test-verify | subskills/test-verify/SKILL.md | 测试与验证分析 |
| /code-review | subskills/code-review/SKILL.md | 代码审查 |
| /dev-memo | subskills/dev-memo/SKILL.md | 功能开发记忆 |

用户也可直接描述需求，主技能自动评估复杂度并路由。

## 触发示例

### 主技能（直接描述需求即可触发）
- "用规范开发流程做一个订单管理系统" → 走完整流程
- "帮我写个格式化日期的工具函数" → 简单任务，直接执行
- "我要做个新功能" → 模糊需求，先走需求规划

### 子技能单独触发（命令或自然语言）
- `/spec-check` "检查并创建项目规范文件"
- `/req-plan` "帮我规划一下这个需求"
- `/dev-plan` "生成这个功能的实施方案"
- `/task-split` "把这个大需求拆成子任务"
- `/test-verify` "分析这次改动的测试覆盖"
- `/code-review` "审查一下我的代码改动"
- `/dev-memo` "生成这次开发的记忆文档"

### 口头覆盖阈值
- "跳过提问，直接按最优方案做" → skip_questions=true
- "直接开发，不用走流程" → 强制简单任务模式
- "这次生成测试报告" → 临时开启测试报告
- "代码审查先跳过" → 临时关闭代码审查

## 执行规则

1. 首次在项目中使用时，自动读取配置文件（使用默认值）
2. 每次触发时读取配置，用户可随时修改覆盖
3. 用户明确指示时（如"跳过提问"、"直接开发"、"不走流程"），覆盖配置设定
4. 简单任务跳过所有流程步骤，直接执行开发
5. 子技能内置在 `subskills/` 目录，无需额外安装，按需读取对应 SKILL.md
6. 每个子技能执行完毕后，根据配置决定是否继续下一步

## 项目专属约定

### 技术栈
- **前端**: Vue 3 + TypeScript
- **后端**: Python (FastAPI)
- **数据库**: SQLAlchemy ORM

### 目录结构
- `frontend/` — 前端项目
- `backend/` — 后端项目
- `.claude/` — Claude 配置与技能
- `.workbuddy/` — 工作流配置

### 构建命令
- 后端启动：`cd backend && uvicorn app.main:app --reload`

---

> 提示：配置文件将在首次使用时自动创建于 `.workbuddy/spec-dev/config.json`
