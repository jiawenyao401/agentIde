# Agent Native AI Coding IDE

一个可运行的开源级原型：面向 **Agent Native** 的 AI Coding IDE（非单纯 Chat + 编辑器），具备多层架构、Skill、MCP、Memory、多 Agent 与可观测性。

## 1. 项目结构

```text
ai-ide/
├── frontend/                     # Next.js + TypeScript Web IDE
│   ├── app/
│   ├── components/
│   └── lib/
├── backend/
│   ├── app/
│   │   ├── agent/               # AgentCore / planner / router / executor
│   │   ├── api/                 # FastAPI endpoints
│   │   ├── core/                # settings
│   │   ├── mcp/                 # MCP client (lazy schema loading)
│   │   ├── memory/              # episodic/semantic/personality (Chroma)
│   │   ├── observability/       # logger + trace collector
│   │   ├── skills/              # skill loader/matcher/executor/DAG
│   │   ├── tools/               # filesystem/git/shell/browser/sandbox
│   │   └── examples/            # runnable execution demos
│   └── skills/
│       └── build_api/
└── README.md
```

## 2. 架构概览（5层）

1. **IDE Layer**：Next.js + Monaco + Chat/TaskBoard/Trace/Memory 面板。
2. **Agent Orchestrator**：`AgentCore.plan/route/execute` 统一调度。
3. **Skill System**：Markdown + flow.yaml + tools.json，支持 DAG 编排。
4. **MCP Protocol Layer**：`MCPClient` 动态注册工具，按需懒加载 schema。
5. **Tool Layer**：filesystem / git / shell / browser 工具与沙箱。

## 3. 快速启动

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

接口：
- `GET /healthz`
- `POST /api/run`（执行 Agent 流程）
- `GET /api/tools`（查看 MCP 工具 schema）

### Frontend

```bash
cd frontend
npm install
npm run dev
```

打开 `http://localhost:3000`

## 4. 核心能力设计

### AgentCore

`backend/app/agent/core.py`

- `plan(task)`：Planner + Skill Matching + 子 Agent 生成
- `route(task, plan)`：Router（步骤到 MCP tool 的映射）
- `execute(task, plan)`：Executor（逐步调用 MCP + 记录 trace + 写入 memory）

执行链路：

`User Task -> Planner -> Skill Matching -> MCP Tool Selection -> Execute -> Memory Update`

### Skill System

- `SkillLoader`：动态扫描 `backend/skills/*`
- `SkillMatcher`：轻量语义匹配（可替换 embedding）
- `SkillExecutor`：读取 flow.yaml 并执行 DAG 拓扑序
- `SkillGraph`：基于 networkx 校验 DAG

### MCP Layer

`backend/app/mcp/client.py`

- 支持工具注册与统一调用
- `list_tools()` / `call_tool(name, input)`
- **Lazy Loading**：schema 首次访问时才加载

### Memory（三层）

`backend/app/memory/store.py`

- Episodic：任务执行历史
- Semantic：知识归纳
- Personality：Agent 偏好
- 基于 ChromaDB 实现持久化向量检索

### 安全与可观测性

- 工具安全：`WorkspaceSandbox` 限定文件访问范围
- 可观测性：`TraceCollector` 收集耗时、步骤 metadata
- 日志：统一 logger

## 5. 完整执行示例（登录系统）

命令：

```bash
cd backend
python -m app.examples.login_demo
```

系统将执行：
1. 匹配 Skill `build-rest-api`
2. 基于 DAG 生成计划
3. 路由 MCP 工具（filesystem/shell/git）
4. 写入文件产物
5. 触发 commit 动作（若仓库有变更）

## 6. 关键优化落地

1. **MCP Lazy Loading**：tool schema 按需加载，避免上下文膨胀。
2. **Skill 复用**：workflow 固化到 skill 文件，减少 prompt token。
3. **Agent 可观测性**：trace + logs 完整记录执行链路。
4. **Tool 调用安全**：filesystem 受 sandbox 保护。

## 7. 后续可扩展方向

- 将 `SkillMatcher` 升级为 embedding + rerank。
- 增加 Remote MCP Server discovery 与 auth。
- 增加 Multi-Agent 并发调度器（队列 + 依赖图）。
- 接入真实 PR 平台（GitHub/GitLab API）。
- 引入事件总线（Kafka/NATS）实现跨进程工具调用。


## 8. 本地验证清单

建议按以下顺序验证可运行性：

```bash
python -m compileall backend/app
cd backend && pip install -r requirements.txt && uvicorn app.main:app --port 8000
cd frontend && npm install && npm run dev
```

如果你的环境受代理/防火墙限制，依赖安装可能失败（`pip`/`npm` 403），需切换可访问镜像源后再执行。
