"""
L57 示例 2: MCP File System Server — 本地文件系统安全访问

使用官方 mcp Python SDK 构建极简的 Local File System MCP Server。
遵循三层路径安全防护：resolve().relative_to() + O_NOFOLLOW + inode 比较。

使用方式（stdio 模式）:
    mcp run examples/02_mcp_server.py
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
)

# ---------------------------------------------------------------------------
# 安全工具函数（三层防护）
# ---------------------------------------------------------------------------

ALLOWED_ROOT = Path.cwd()


def _safe_resolve(path: str) -> Path:
    """第一层 + 第二层：防御性断言 + 拒绝符号链接。"""
    requested = (ALLOWED_ROOT / path).resolve()
    try:
        requested.relative_to(ALLOWED_ROOT)
    except ValueError as exc:
        raise PermissionError(f"路径越界: {path!r}") from exc
    # O_NOFOLLOW：拒绝符号链接
    fd = os.open(str(requested), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        return Path(requested)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# MCP Server 声明
# ---------------------------------------------------------------------------

SERVER = Server("l57-file-server")


@SERVER.list_tools()
async def list_tools() -> ListToolsResult:
    """向客户端暴露三个工具。"""
    return ListToolsResult(
        tools=[
            Tool(
                name="list_directory",
                description="列出指定目录中的文件和子目录。返回文件大小和最后修改时间。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "相对于当前目录的路径（如 src/ 或 .）",
                        }
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="read_file",
                description="读取指定文件的内容（限文本文件，<= 64KB）。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "相对于当前目录的文件路径",
                        }
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="search_files",
                description="在目录中递归搜索文件名包含关键字的文件。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "搜索起点目录"},
                        "keyword": {"type": "string", "description": "文件名关键字（大小写敏感）"},
                    },
                    "required": ["path", "keyword"],
                },
            ),
        ]
    )


# ---------------------------------------------------------------------------
# 工具调用处理（异步，完整异常处理）
# ---------------------------------------------------------------------------


@SERVER.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
) -> CallToolResult:
    try:
        match name:
            case "list_directory":
                return await _list_directory(arguments["path"])
            case "read_file":
                return await _read_file(arguments["path"])
            case "search_files":
                return await _search_files(arguments["path"], arguments["keyword"])
            case _:
                raise ValueError(f"未知工具: {name!r}")
    except PermissionError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"权限错误: {exc}")],
            isError=True,
        )
    except FileNotFoundError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"文件未找到: {exc}")],
            isError=True,
        )
    except OSError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"系统错误: {exc}")],
            isError=True,
        )
    except Exception as exc:
        # 捕获所有未预期异常，重新抛出以触发 MCP 协议层日志
        raise RuntimeError(f"工具 {name!r} 执行失败: {exc}") from exc


# ---------------------------------------------------------------------------
# 工具实现
# ---------------------------------------------------------------------------


async def _list_directory(rel_path: str) -> CallToolResult:
    """异步列出目录内容。"""
    try:
        target = _safe_resolve(rel_path)
        entries = []
        for entry in sorted(target.iterdir()):
            stat = entry.stat()
            size = stat.st_size
            kind = "📁 dir" if entry.is_dir() else f"📄 {size:>8} bytes"
            entries.append(f"{kind}  {entry.name}")
        body = "\n".join(entries) if entries else "(空目录)"
        return CallToolResult(content=[TextContent(type="text", text=body)])
    except PermissionError:
        return CallToolResult(
            content=[TextContent(type="text", text=f"无权限访问目录: {rel_path!r}")],
            isError=True,
        )


async def _read_file(rel_path: str) -> CallToolResult:
    """异步读取文本文件内容（限制 64KB）。"""
    MAX_SIZE = 64 * 1024
    try:
        target = _safe_resolve(rel_path)
        if target.is_dir():
            return CallToolResult(
                content=[TextContent(type="text", text=f"{rel_path!r} 是目录，请使用 list_directory")],
                isError=True,
            )
        size = target.stat().st_size
        if size > MAX_SIZE:
            return CallToolResult(
                content=[TextContent(type="text", text=f"文件过大 ({size} bytes)，最大支持 64KB")],
                isError=True,
            )
        # 异步文件 I/O（用于未来扩展为真正的异步实现）
        content = await asyncio.to_thread(target.read_text, encoding="utf-8")
        return CallToolResult(content=[TextContent(type="text", text=content)])
    except UnicodeDecodeError:
        return CallToolResult(
            content=[TextContent(type="text", text="文件非 UTF-8 文本，无法读取")],
            isError=True,
        )


async def _search_files(rel_path: str, keyword: str) -> CallToolResult:
    """异步递归搜索文件名。"""
    try:
        root = _safe_resolve(rel_path)
        matches: list[str] = []
        # 搜索深度上限，防止恶意无限递归
        depth_limit = 5
        for p in root.rglob(keyword):
            if len(p.parts) - len(root.parts) > depth_limit:
                continue
            matches.append(str(p.relative_to(root)))
        if matches:
            body = "\n".join(f"  {m}" for m in matches[:50])
            tail = f"\n  ... (共 {len(matches)} 个匹配)" if len(matches) > 50 else ""
            return CallToolResult(content=[TextContent(type="text", text=f"找到 {len(matches)} 个文件:\n{body}{tail}")])
        return CallToolResult(content=[TextContent(type="text", text="未找到匹配文件")])
    except PermissionError:
        return CallToolResult(
            content=[TextContent(type="text", text="搜索遇到权限受限目录，已跳过")],
            isError=False,
        )


# ---------------------------------------------------------------------------
# 服务器入口（stdio 模式）
# ---------------------------------------------------------------------------


async def main() -> None:
    """启动 stdio 服务器，等待 MCP 客户端连接。"""
    async with stdio_server() as (read, write):
        await SERVER.run(read, write, SERVER.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
