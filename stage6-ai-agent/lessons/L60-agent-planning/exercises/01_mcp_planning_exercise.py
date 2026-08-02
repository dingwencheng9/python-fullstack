"""
L57 练习: MCP Server + LangGraph ToolNode 集成

任务目标:
1. 实现一个 MCP Server，提供"读取环境变量"和"执行 Python 表达式"两个工具
2. 在 LangGraph 的 ToolNode 中接入该 MCP Server
3. 演示大模型通过 MCP 协议访问环境信息并进行任务规划

技术要求:
- 使用 mcp.server.Server 构建 MCP Server
- 异步异常处理：PermissionError、FileNotFoundError、OSError、UnicodeDecodeError
- LangGraph StateGraph + ToolNode 模式
- stdio 模式通信

开始编写吧！参考 solutions/01_mcp_planning_solution.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Part 1: MCP Server 实现
# ---------------------------------------------------------------------------

"""
实现一个 MCP Server，提供以下两个工具:

1. get_env(key: str) -> str
   - 读取指定环境变量
   - 如果不存在，返回 "NOT_SET"

2. run_expression(expr: str) -> str
   - 在当前 Python 环境中执行简单的数学表达式
   - 仅支持: + - * / ** () 和整数/浮点数
   - 安全性：使用 ast.literal_eval 安全求值，不允许变量/函数调用
   - 错误时返回 "ERROR: <具体错误信息>"

工具的 inputSchema 定义示例:
    Tool(
        name="get_env",
        description="获取指定环境变量的值",
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "环境变量名"}
            },
            "required": ["key"]
        },
    )
"""

# 在下方开始实现你的 MCP Server
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Part 2: MCP Client（用于测试）
# ---------------------------------------------------------------------------

"""
在下方实现 MCP Client 类，用于连接上面的 Server 并调用工具。
参考 examples/03_langgraph_mcp_integration.py 中的 MCPFileSystemClient
"""


# ---------------------------------------------------------------------------
# Part 3: LangGraph 集成
# ---------------------------------------------------------------------------

"""
完成以下状态定义和节点实现:

@dataclass
class TaskState:
    task: str
    plan: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)
    response: str = ""

实现:
- env_planner_node(state): 使用 LLM 将任务分解为 [get_env / run_expression] 调用步骤
- env_executor_node(state): 通过 MCP Client 执行步骤
- summarize_node(state): 汇总结果

图结构:
    planner → execute → (continue?) → summarize → END
"""


# ---------------------------------------------------------------------------
# 验证函数（请勿修改）
# ---------------------------------------------------------------------------


def verify_implementation() -> dict:
    """验证练习完成情况。运行: python -m exercises/01_mcp_planning_exercise"""
    checks = {
        "MCP Server 定义": False,
        "get_env 工具": False,
        "run_expression 工具": False,
        "异常处理": False,
        "MCP Client": False,
        "LangGraph 图": False,
    }
    import ast

    own_file = __file__
    src = open(own_file, encoding="utf-8").read()
    tree = ast.parse(src)

    # 检查 MCP Server 类/函数
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and "Server" in node.name:
            checks["MCP Server 定义"] = True
        if isinstance(node, ast.FunctionDef):
            if node.name == "get_env":
                checks["get_env 工具"] = True
            if node.name == "run_expression":
                checks["run_expression 工具"] = True
            if any("PermissionError" in str(n) for n in ast.walk(node)):
                checks["异常处理"] = True

    # 检查 LangGraph
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "StateGraph":
            checks["LangGraph 图"] = True
        if isinstance(node, ast.Attribute) and node.attr == "MCPFileSystemClient":
            checks["MCP Client"] = True

    print("练习检查结果:")
    for k, v in checks.items():
        print(f"  {'✅' if v else '❌'} {k}")
    return checks


if __name__ == "__main__":
    verify_implementation()
