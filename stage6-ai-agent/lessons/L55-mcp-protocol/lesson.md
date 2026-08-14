L55: MCP 协议与标准化工具集成 - 详细教程

> **课程编号**: L55
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 6 小时
> **难度**: ⭐⭐⭐⭐☆（AI Agent 工程化终章）
> **前置课程**: L54 Agent 基础
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L54**: Agent 基础与工具调用（理解 ReAct 模式与工具调用）
- **L56**: LangChain 与应用编排（可选，理解 Chain 基础）

**如果你还没有学习以上课程，建议先完成前置课程。**

---

MCP (Model Context Protocol) 是一种把 AI Agent 与外部工具、资源、提示词连接起来的协议思想。
本课不深绑某个 SDK，而是用 Python 模拟 MCP 的角色模型，帮助你理解协议边界。

## 第一章：Tool Calling 的问题

在 L54 中，我们实现过 Agent 工具调用：

```python
def search_docs(query: str) -> str:
    return "检索结果"

agent.register_tool("search_docs", search_docs)
```python
这种方式简单，但有三个问题：

1. **工具和 Agent 紧耦合** — 工具函数直接写在 Agent 代码里
2. **权限边界模糊** — Agent 能调用什么、不能调用什么，靠代码约定
3. **跨应用复用困难** — 同一个工具很难被多个 Agent/IDE/客户端共享

MCP 的价值在于把工具变成独立服务：

```python
Agent Host ── MCP Client ── MCP Server ── Tools / Resources
```markdown
## 第二章：MCP 的角色模型

### 2.1 Host

Host 是承载用户交互的应用，例如：

- Claude Desktop
- IDE 插件
- 自己写的 Agent Web 应用
- CLI Agent

Host 管理用户会话、权限策略和多个 MCP Client。

### 2.2 Client

Client 是 Host 内部负责和某个 Server 通信的对象。

```text
Host
├── Client A → 文件系统 Server
├── Client B → 数据库 Server
└── Client C → GitHub Server
```python
### 2.3 Server

Server 暴露能力，通常包括：

- **Tools**: 可以执行的动作，如搜索文件、查询数据库、创建 issue
- **Resources**: 可读取上下文，如文件内容、数据库表结构
- **Prompts**: 可复用提示词模板

### 2.4 Tool / Resource / Prompt

| 类型     | 含义       | 示例                  |
| -------- | ---------- | --------------------- |
| Tool     | 执行动作   | `search_files(query)` |
| Resource | 读取上下文 | `file://README.md`    |
| Prompt   | 提示词模板 | `summarize_project`   |

## 第三章：极简协议模拟

我们用纯 Python 数据结构模拟 MCP 协议。

```python
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]

@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]

@dataclass(frozen=True)
class ToolResult:
    content: str
    ok: bool = True
```python
Server 注册工具：

```python
class ToolServer:
    def __init__(self):
        self.tools: dict[str, Callable] = {}
        self.specs: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec, handler: Callable):
        self.specs[spec.name] = spec
        self.tools[spec.name] = handler

    def list_tools(self) -> list[ToolSpec]:
        return list(self.specs.values())

    def call_tool(self, call: ToolCall) -> ToolResult:
        if call.name not in self.tools:
            return ToolResult(f"unknown tool: {call.name}", ok=False)
        result = self.tools[call.name](**call.arguments)
        return ToolResult(str(result))
```python
Client 调用工具：

```python
server = ToolServer()
server.register(
    ToolSpec(
        name="echo",
        description="回显输入文本",
        input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
    ),
    lambda text: text,
)

result = server.call_tool(ToolCall("echo", {"text": "hello"}))
print(result.content)  # hello
```python
## 第四章：本地工具服务器

一个有价值的本地工具：文件搜索。

```python
from pathlib import Path

class FileSearchServer(ToolServer):
    def __init__(self, root: Path):
        super().__init__()
        self.root = root.resolve()
        self.register(
            ToolSpec(
                name="search_files",
                description="在允许目录内搜索文本",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "pattern": {"type": "string", "default": "*.py"},
                    },
                    "required": ["query"],
                },
            ),
            self.search_files,
        )

    def search_files(self, query: str, pattern: str = "*.py") -> str:
        hits: list[str] = []
        for path in self.root.rglob(pattern):
            if not self._is_allowed(path):
                continue
            text = path.read_text(errors="ignore")
            if query in text:
                hits.append(str(path.relative_to(self.root)))
        return "\n".join(hits[:20]) or "no matches"

    def _is_allowed(self, path: Path) -> bool:
        resolved = path.resolve()
        return self.root in resolved.parents or resolved == self.root
```python
关键安全点：`root` 限制。Agent 不能随便读整个磁盘。

## 第五章：Agent 调用 MCP 工具

Mock Agent 可以把工具列表作为上下文：

```python
class AgentToolBridge:
    def __init__(self, server: ToolServer):
        self.server = server

    def describe_tools(self) -> str:
        return "\n".join(
            f"- {tool.name}: {tool.description}"
            for tool in self.server.list_tools()
        )

    def execute(self, tool_name: str, arguments: dict) -> str:
        result = self.server.call_tool(ToolCall(tool_name, arguments))
        if not result.ok:
            return f"工具调用失败: {result.content}"
        return result.content
```python
Agent 看到工具描述后，决定要调用哪个工具。
实际生产里，这一步由 LLM 的 tool calling 能力完成。

## 第六章：生产化边界

### 6.1 权限

MCP Server 必须明确限制权限：

- 文件工具只能访问白名单目录
- 数据库工具只能执行 SELECT 或预定义查询
- GitHub 工具不能默认写入 issue/PR
- 网络工具要限制目标域名

### 6.2 输入校验

所有 tool arguments 都必须通过 schema 校验：

```python
def validate_args(schema: dict, args: dict) -> bool:
    required = schema.get("required", [])
    for key in required:
        if key not in args:
            return False
    return True
```yaml
### 6.3 审计日志

工具调用必须记录：

```python
{
    "tool": "search_files",
    "args": {"query": "FastAPI"},
    "user": "alice",
    "timestamp": "...",
    "ok": True,
}
```

### 6.4 版本兼容

MCP 生态仍在演进。课程建议：

- 学协议模型，不绑定某个 SDK
- 工具 schema 保持简单
- Server 与 Agent 解耦
- 重要工具加权限边界和审计日志

## 第七章：JSON-RPC 2.0 传输层

MCP 使用 JSON-RPC 2.0 作为传输格式。

### 7.1 JSON-RPC 请求/响应格式

```python
import json
from dataclasses import dataclass
from typing import Any

@dataclass
class JSONRPCRequest:
    """JSON-RPC 2.0 请求"""
    jsonrpc: str = "2.0"
    id: str | int | None = None
    method: str = ""
    params: dict[str, Any] | None = None

    def to_json(self) -> str:
        return json.dumps(self, default=str, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "JSONRPCRequest":
        data = json.loads(text)
        return cls(
            id=data.get("id"),
            method=data["method"],
            params=data.get("params"),
        )

@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 响应"""
    jsonrpc: str = "2.0"
    id: str | int | None = None
    result: Any = None
    error: dict[str, Any] | None = None

    def to_json(self) -> str:
        return json.dumps(self, default=str, ensure_ascii=False)

    @classmethod
    def from_json(cls, text: str) -> "JSONRPCResponse":
        data = json.loads(text)
        return cls(
            id=data.get("id"),
            result=data.get("result"),
            error=data.get("error"),
        )
```

### 7.2 MCP 方法映射

| MCP 方法 | JSON-RPC method | 说明 |
| -------- | ---------------- | ---- |
| 初始化 | `initialize` | 客户端连接时握手 |
| 列出工具 | `tools/list` | 获取可用工具列表 |
| 调用工具 | `tools/call` | 执行指定工具 |
| 列出资源 | `resources/list` | 获取可用资源列表 |
| 读取资源 | `resources/read` | 读取资源内容 |
| 列出提示词 | `prompts/list` | 获取可用提示词 |
| 获取提示词 | `prompts/get` | 获取完整提示词 |

### 7.3 初始化握手流程

```python
# 客户端发送初始化请求
client_init = JSONRPCRequest(
    id=1,
    method="initialize",
    params={
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {"subscribe": True},
        },
        "clientInfo": {
            "name": "my-agent",
            "version": "1.0.0",
        },
    },
)

# 服务器响应
server_response = JSONRPCResponse(
    id=1,
    result={
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {},
            "prompts": {},
        },
        "serverInfo": {
            "name": "filesystem-server",
            "version": "1.0.0",
        },
    },
)
```

---

## 第八章：SSE 传输层实现

MCP 推荐使用 Server-Sent Events (SSE) 作为传输层。

### 8.1 SSE 服务器

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

class SSEServer:
    """SSE MCP 服务器"""
    def __init__(self):
        self.tools = {}
        self.subscribers: list[asyncio.Queue] = []

    async def emit(self, event: dict):
        """向所有订阅者发送事件"""
        message = f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        for queue in self.subscribers:
            await queue.put(message)

    async def handle_request(self, request: JSONRPCRequest) -> JSONRPCResponse:
        """处理 JSON-RPC 请求"""
        if request.method == "tools/list":
            return JSONRPCResponse(
                id=request.id,
                result={
                    "tools": [
                        {"name": name, **spec}
                        for name, spec in self.tools.items()
                    ]
                },
            )
        elif request.method == "tools/call":
            result = await self.call_tool(
                request.params["name"],
                request.params.get("arguments", {}),
            )
            return JSONRPCResponse(id=request.id, result=result)
        else:
            return JSONRPCResponse(
                id=request.id,
                error={"code": -32601, "message": f"Unknown method: {request.method}"},
            )

    async def call_tool(self, name: str, args: dict) -> dict:
        """调用工具"""
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        # 实际工具调用逻辑
        return {"content": [{"type": "text", "text": "result"}]}

sse_server = SSEServer()

@app.post("/mcp")
async def handle_mcp(request: Request):
    """处理 MCP JSON-RPC 请求"""
    body = await request.json()
    req = JSONRPCRequest.from_json(json.dumps(body))
    resp = await sse_server.handle_request(req)
    return {"status": "ok", "result": json.loads(resp.to_json())}

@app.get("/mcp/stream")
async def mcp_stream():
    """SSE 流式端点"""
    queue = asyncio.Queue()
    sse_server.subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                message = await queue.get()
                yield message
        except asyncio.CancelledError:
            sse_server.subscribers.remove(queue)
            raise

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
```

### 8.2 SSE 客户端

```python
import httpx
import asyncio
import json

class MCPClient:
    """MCP SSE 客户端"""
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.protocol_version = "2024-11-05"
        self.capabilities = {}

    async def initialize(self) -> dict:
        """初始化握手"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": self.protocol_version,
                        "capabilities": {
                            "tools": {"listChanged": True},
                        },
                        "clientInfo": {
                            "name": "agent-client",
                            "version": "1.0.0",
                        },
                    },
                },
            )
            result = response.json()["result"]
            self.capabilities = result["capabilities"]
            return result

    async def list_tools(self) -> list[dict]:
        """列出可用工具"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {},
                },
            )
            return response.json()["result"]["tools"]

    async def call_tool(self, name: str, args: dict) -> dict:
        """调用工具"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": name,
                        "arguments": args,
                    },
                },
            )
            return response.json()["result"]
```

---

## 第九章：完整 MCP Server 实现

### 9.1 数据库工具 Server

```python
from dataclasses import dataclass
from typing import Any
import sqlite3
from pathlib import Path

@dataclass(frozen=True)
class DatabaseToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]

class DatabaseMCPServer:
    """数据库 MCP Server - 暴露安全的数据库操作"""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.allowed_tables: set[str] = set()
        self._init_connection()

    def _init_connection(self):
        """初始化数据库连接"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        # 获取所有表名
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        self.allowed_tables = {row["name"] for row in cursor.fetchall()}

    def _validate_query(self, query: str) -> bool:
        """SQL 注入防护：只允许 SELECT"""
        query = query.strip().upper()
        # 必须是 SELECT 语句
        if not query.startswith("SELECT"):
            return False
        # 不能包含危险关键字
        dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "TRUNCATE"]
        for keyword in dangerous:
            if keyword in query:
                return False
        # 不能查询系统表
        if "SQLITE_" in query:
            return False
        return True

    def _get_table_schema(self, table: str) -> list[dict]:
        """获取表结构"""
        if table not in self.allowed_tables:
            raise ValueError(f"Table not allowed: {table}")

        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return [
            {"name": row["name"], "type": row["type"]}
            for row in cursor.fetchall()
        ]

    async def execute_query(self, query: str, params: tuple = ()) -> dict:
        """执行查询"""
        if not self._validate_query(query):
            raise ValueError("Query validation failed: only SELECT allowed")

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return {
                "content": [
                    {"type": "text", "text": str(dict(row))}
                    for row in rows
                ],
                "isError": False,
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {e}"}],
                "isError": True,
            }

    def list_tools(self) -> list[DatabaseToolSpec]:
        """列出可用工具"""
        return [
            DatabaseToolSpec(
                name="execute_query",
                description="执行 SELECT 查询（仅读操作）",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL SELECT 语句",
                        },
                        "params": {
                            "type": "array",
                            "description": "查询参数",
                            "default": [],
                        },
                    },
                    "required": ["query"],
                },
            ),
            DatabaseToolSpec(
                name="get_schema",
                description="获取表结构",
                input_schema={
                    "type": "object",
                    "properties": {
                        "table": {
                            "type": "string",
                            "description": "表名",
                        },
                    },
                    "required": ["table"],
                },
            ),
            DatabaseToolSpec(
                name="list_tables",
                description="列出所有可用表",
                input_schema={"type": "object", "properties": {}},
            ),
        ]

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any]
    ) -> dict:
        """调用工具"""
        if name == "execute_query":
            return await self.execute_query(
                arguments["query"],
                tuple(arguments.get("params", [])),
            )
        elif name == "get_schema":
            schema = self._get_table_schema(arguments["table"])
            return {
                "content": [{"type": "text", "text": str(schema)}],
                "isError": False,
            }
        elif name == "list_tables":
            return {
                "content": [{"type": "text", "text": str(list(self.allowed_tables))}],
                "isError": False,
            }
        else:
            raise ValueError(f"Unknown tool: {name}")
```

### 9.2 与 LangChain 集成

```python
from langchain.tools import tool
from langchain_core.tools import StructuredTool

def create_mcp_langchain_tools(server: DatabaseMCPServer) -> list[StructuredTool]:
    """将 MCP Server 工具转换为 LangChain 工具"""

    tools = []

    for spec in server.list_tools():
        # 获取工具函数
        async def make_call(tool_name: str):
            async def _call(**kwargs):
                result = await server.call_tool(tool_name, kwargs)
                if result.get("isError"):
                    raise ValueError(result["content"][0]["text"])
                return "\n".join(c["text"] for c in result["content"])
            return _call

        lc_tool = StructuredTool(
            name=spec.name,
            description=spec.description,
            args_schema=spec.input_schema,
            coroutine=await make_call(spec.name) if False else None,
        )
        tools.append(lc_tool)

    return tools
```

---

## 第十章：生产环境最佳实践

### 10.1 权限模型

```python
from enum import Enum
from dataclasses import dataclass

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"

@dataclass
class ToolPermission:
    """工具权限配置"""
    tool_name: str
    allowed_roles: set[str]
    rate_limit: int  # 每分钟调用次数
    timeout_seconds: int

# 权限配置示例
TOOL_PERMISSIONS = {
    "search_files": ToolPermission(
        tool_name="search_files",
        allowed_roles={"user", "admin"},
        rate_limit=100,
        timeout_seconds=30,
    ),
    "execute_query": ToolPermission(
        tool_name="execute_query",
        allowed_roles={"analyst", "admin"},
        rate_limit=50,
        timeout_seconds=60,
    ),
    "delete_file": ToolPermission(
        tool_name="delete_file",
        allowed_roles={"admin"},  # 仅管理员
        rate_limit=10,
        timeout_seconds=10,
    ),
}

def check_permission(
    user_role: str,
    tool_name: str,
    current_usage: int
) -> bool:
    """检查用户是否有权调用工具"""
    if tool_name not in TOOL_PERMISSIONS:
        return False  # 未知工具默认拒绝

    perm = TOOL_PERMISSIONS[tool_name]

    # 检查角色
    if user_role not in perm.allowed_roles:
        return False

    # 检查频率限制
    if current_usage >= perm.rate_limit:
        return False

    return True
```

### 10.2 审计日志设计

```python
from datetime import datetime
from dataclasses import dataclass, asdict
import json

@dataclass
class AuditLog:
    """审计日志条目"""
    timestamp: str
    user_id: str
    user_role: str
    tool_name: str
    arguments: dict
    result_status: str  # "success" | "error" | "denied"
    execution_time_ms: int
    client_ip: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

class AuditLogger:
    """审计日志记录器"""

    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.current_file = self.storage_path / f"audit_{datetime.now():%Y%m%d}.jsonl"

    def log(self, entry: AuditLog):
        """写入审计日志"""
        self.current_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.current_file, "a", encoding="utf-8") as f:
            f.write(entry.to_json() + "\n")

    def query(
        self,
        user_id: str | None = None,
        tool_name: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[AuditLog]:
        """查询审计日志"""
        results = []
        for log_file in self.storage_path.glob("audit_*.jsonl"):
            with open(log_file, encoding="utf-8") as f:
                for line in f:
                    entry = AuditLog(**json.loads(line))

                    if user_id and entry.user_id != user_id:
                        continue
                    if tool_name and entry.tool_name != tool_name:
                        continue
                    if start_time and datetime.fromisoformat(entry.timestamp) < start_time:
                        continue
                    if end_time and datetime.fromisoformat(entry.timestamp) > end_time:
                        continue

                    results.append(entry)
        return results
```

### 10.3 健康检查与监控

```python
from dataclasses import dataclass
import time

@dataclass
class MCPServerMetrics:
    """MCP 服务器指标"""
    total_requests: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    denied_calls: int = 0
    total_latency_ms: float = 0.0
    start_time: float = field(default_factory=time.time)

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_calls / self.total_requests

    @property
    def avg_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_latency_ms / self.total_requests

    def to_prometheus(self) -> str:
        """导出 Prometheus 格式"""
        return f"""
# HELP mcp_requests_total Total MCP requests
# TYPE mcp_requests_total counter
mcp_requests_total{self._labels()} {self.total_requests}

# HELP mcp_request_duration_seconds Average request duration
# TYPE mcp_request_duration_seconds gauge
mcp_request_duration_seconds{self._labels()} {self.avg_latency_ms / 1000:.3f}

# HELP mcp_success_rate Request success rate
# TYPE mcp_success_rate gauge
mcp_success_rate{self._labels()} {self.success_rate:.3f}
"""

    def _labels(self) -> str:
        return '{service="mcp-server"}'
```

### 10.4 版本兼容性策略

```python
class ProtocolVersion:
    """协议版本管理"""

    SUPPORTED_VERSIONS = ["2024-11-05", "2024-10-01", "2024-06-01"]
    CURRENT_VERSION = "2024-11-05"

    @classmethod
    def negotiate(cls, client_version: str) -> str:
        """协商协议版本"""
        if client_version in cls.SUPPORTED_VERSIONS:
            return client_version

        # 向后兼容：返回最接近的旧版本
        for version in cls.SUPPORTED_VERSIONS:
            if cls._is_compatible(client_version, version):
                return version

        raise ValueError(f"Unsupported protocol version: {client_version}")

    @classmethod
    def _is_compatible(cls, client: str, server: str) -> bool:
        """检查版本兼容性"""
        # 简化版本：只要主版本号相同即可
        return client.split("-")[0] == server.split("-")[0]
```

## 🔗 下一步

完成本课后继续学习：

- [L56: LangChain 基础与应用](../L56-langchain/README.md)

> 📖 **学习路径提示**：L56 将学习 LangChain 的基本用法。
