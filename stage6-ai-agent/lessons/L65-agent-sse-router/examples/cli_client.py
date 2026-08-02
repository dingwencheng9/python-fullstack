"""

from __future__ import annotations

L12 AI Agent 编排 - 优雅的 Python CLI 客户端
==============================================

本模块实现 SSE 流式对话的优雅终端客户端。

核心能力：
1. httpx 异步流式消费
2. SSE 协议解析
3. 彩色终端渲染
4. 打字机效果
5. 工具调用可视化

作者：Python 3.13 全栈课程
"""

import asyncio
import json
import sys
from collections.abc import AsyncGenerator
from enum import StrEnum

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

# ============================================================
# 1. 配置
# ============================================================


class Config:
    """客户端配置"""

    API_URL = "http://localhost:8000/api/v1/agent/chat"
    JWT_TOKEN = "demo-token"  # 替换为真实 Token
    TIMEOUT = 60.0

    # 颜色配置
    COLOR_USER = "green"
    COLOR_AGENT = "white"
    COLOR_TOOL = "cyan"
    COLOR_ERROR = "red"
    COLOR_SYSTEM = "yellow"


# ============================================================
# 2. SSE 事件类型
# ============================================================


class EventType(StrEnum):
    """事件类型"""

    CONNECTION = "connection"
    TOKEN = "token"
    TOOL = "tool"
    COMPLETION = "completion"
    ERROR = "error"


# ============================================================
# 3. SSE 流式解析器
# ============================================================


class SSEParser:
    """
    SSE 协议解析器

    **职责**:
    - 解析 SSE 格式数据流
    - 提取 event 和 data
    - 处理不完整行
    """

    def __init__(self):
        self.buffer = ""
        self.current_event = None

    async def parse_stream(
        self,
        response: httpx.Response,
    ) -> AsyncGenerator[tuple[str, dict]]:
        """
        解析 SSE 流

        **输出**: (event_type, data) 元组
        """
        async for chunk in response.aiter_bytes():
            # 解码
            self.buffer += chunk.decode("utf-8")

            # 按行分割
            lines = self.buffer.split("\n")

            # 保留最后一行（可能不完整）
            self.buffer = lines.pop()

            # 处理每一行
            for line in lines:
                line = line.strip()

                if not line:
                    continue

                # 解析 event 行
                if line.startswith("event:"):
                    self.current_event = line.replace("event:", "").strip()

                # 解析 data 行
                elif line.startswith("data:"):
                    data_str = line.replace("data:", "").strip()

                    try:
                        data = json.loads(data_str)
                        event_type = self.current_event or "message"

                        yield (event_type, data)

                        # 重置
                        self.current_event = None

                    except json.JSONDecodeError:
                        # 非 JSON 数据，跳过
                        pass


# ============================================================
# 4. 终端渲染器
# ============================================================


class TerminalRenderer:
    """
    终端渲染器

    **职责**:
    - 彩色输出
    - 打字机效果
    - 工具调用可视化
    - 进度提示
    """

    def __init__(self):
        self.console = Console()
        self.current_message = ""

    def clear_screen(self):
        """清屏"""
        self.console.clear()

    def print_header(self):
        """打印头部"""
        header = Panel(
            "[bold cyan]🤖 AI Agent 流式对话客户端[/bold cyan]\n[dim]实时 SSE 推送 · 打字机效果 · 工具调用可视化[/dim]",
            border_style="cyan",
        )
        self.console.print(header)
        self.console.print()

    def print_user_message(self, message: str):
        """打印用户消息（绿色）"""
        text = Text()
        text.append("👤 You: ", style="bold green")
        text.append(message, style="green")

        self.console.print(text)
        self.console.print()

    def start_agent_message(self):
        """开始 Agent 消息"""
        self.current_message = ""

        text = Text()
        text.append("🤖 Agent: ", style="bold white")

        self.console.print(text, end="")

    def append_token(self, token: str):
        """追加 Token（打字机效果）"""
        self.current_message += token

        # 打印 Token（白色）
        self.console.print(token, style="white", end="")

    def finish_agent_message(self):
        """结束 Agent 消息"""
        self.console.print()  # 换行
        self.console.print()

    def print_tool_call(self, tool_name: str, tool_input: dict):
        """打印工具调用（青色）"""
        self.console.print()  # 换行

        # 工具调用标题
        text = Text()
        text.append("🔧 System: ", style="bold cyan")
        text.append("调用工具 ", style="cyan")
        text.append(f"{tool_name}", style="bold cyan")

        self.console.print(text)

        # 工具参数
        if tool_input:
            params_table = Table(
                show_header=False,
                box=None,
                padding=(0, 2),
            )
            params_table.add_column("Key", style="dim")
            params_table.add_column("Value", style="cyan")

            for key, value in tool_input.items():
                params_table.add_row(f"  {key}:", str(value))

            self.console.print(params_table)

    def print_tool_result(self, success: bool, duration_ms: float):
        """打印工具结果"""
        if success:
            text = Text()
            text.append("  ✅ ", style="green")
            text.append("执行成功", style="green")
            text.append(f" (耗时: {duration_ms:.2f}ms)", style="dim")
            self.console.print(text)
        else:
            text = Text()
            text.append("  ❌ ", style="red")
            text.append("执行失败", style="red")
            self.console.print(text)

        self.console.print()

    def print_error(self, error_message: str):
        """打印错误（红色）"""
        panel = Panel(
            f"[red]❌ 错误: {error_message}[/red]",
            border_style="red",
        )
        self.console.print(panel)
        self.console.print()

    def print_status(self, status: str):
        """打印状态（黄色）"""
        text = Text()
        text.append("ℹ️  ", style="yellow")
        text.append(status, style="yellow")
        self.console.print(text)

    def print_separator(self):
        """打印分隔线"""
        self.console.print("─" * 80, style="dim")


# ============================================================
# 5. SSE 客户端
# ============================================================


class AgentChatClient:
    """
    Agent 对话客户端

    **职责**:
    - 发送对话请求
    - 接收 SSE 流
    - 实时渲染
    """

    def __init__(self, config: Config):
        self.config = config
        self.parser = SSEParser()
        self.renderer = TerminalRenderer()
        self.conversation_id = None

    async def chat_stream(self, message: str):
        """
        流式对话

        **流程**:
        1. 发送请求
        2. 解析 SSE 流
        3. 实时渲染
        """
        # 打印用户消息
        self.renderer.print_user_message(message)

        try:
            async with httpx.AsyncClient(timeout=self.config.TIMEOUT) as client:
                async with client.stream(
                    "POST",
                    self.config.API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.config.JWT_TOKEN}",
                    },
                    json={
                        "message": message,
                        "conversation_id": self.conversation_id,
                        "stream": True,
                    },
                ) as response:
                    # 检查响应状态
                    if response.status_code != 200:
                        error_text = await response.aread()
                        self.renderer.print_error(f"HTTP {response.status_code}: {error_text.decode()}")
                        return

                    # 开始 Agent 消息
                    self.renderer.start_agent_message()

                    # 解析 SSE 流
                    async for event_type, data in self.parser.parse_stream(response):
                        await self.handle_event(event_type, data)

                    # 结束 Agent 消息
                    self.renderer.finish_agent_message()

        except httpx.TimeoutException:
            self.renderer.print_error("请求超时")

        except httpx.ConnectError:
            self.renderer.print_error("无法连接到服务器，请确保服务正在运行")

        except Exception as e:
            self.renderer.print_error(f"{type(e).__name__}: {e}")

    async def handle_event(self, event_type: str, data: dict):
        """
        处理事件

        **事件类型**:
        - connection: 连接建立
        - token: Token 流式生成
        - tool: 工具调用
        - completion: 对话完成
        - error: 错误
        """
        if event_type == EventType.CONNECTION:
            # 连接建立
            self.conversation_id = data.get("conversation_id")

        elif event_type == EventType.TOKEN:
            # Token 流式生成
            if data.get("event_type") == "on_chat_model_stream":
                if not data.get("is_final"):
                    token = data.get("token", "")
                    self.renderer.append_token(token)

                    # 打字机延迟（可选）
                    await asyncio.sleep(0.01)

        elif event_type == EventType.TOOL:
            # 工具调用
            if data.get("event_type") == "on_tool_start":
                self.renderer.print_tool_call(
                    data.get("tool_name", ""),
                    data.get("tool_input", {}),
                )

            elif data.get("event_type") == "on_tool_end":
                self.renderer.print_tool_result(
                    data.get("success", False),
                    data.get("duration_ms", 0.0),
                )

                # 继续 Agent 消息
                self.renderer.console.print("🤖 Agent: ", style="bold white", end="")

        elif event_type == EventType.COMPLETION:
            # 对话完成
            pass

        elif event_type == EventType.ERROR:
            # 错误
            self.renderer.print_error(f"{data.get('error_type', 'Error')}: {data.get('error_message', '')}")


# ============================================================
# 6. 交互式 CLI
# ============================================================


class InteractiveCLI:
    """
    交互式命令行界面

    **功能**:
    - 循环接收用户输入
    - 调用客户端
    - 优雅退出
    """

    def __init__(self):
        self.client = AgentChatClient(Config)
        self.renderer = TerminalRenderer()

    async def run(self):
        """运行交互式 CLI"""
        # 清屏
        self.renderer.clear_screen()

        # 打印头部
        self.renderer.print_header()

        # 打印帮助
        self.renderer.print_status("输入你的问题，或输入 'exit' 退出")
        self.renderer.print_separator()
        self.renderer.console.print()

        # 交互循环
        while True:
            try:
                # 读取用户输入（绿色提示符）
                user_input = Prompt.ask(
                    "[bold green]You[/bold green]",
                    console=self.renderer.console,
                )

                # 退出命令
                if user_input.lower() in ["exit", "quit", "q"]:
                    self.renderer.print_status("再见！👋")
                    break

                # 空输入
                if not user_input.strip():
                    continue

                # 发送消息
                await self.client.chat_stream(user_input)

            except KeyboardInterrupt:
                self.renderer.console.print()
                self.renderer.print_status("已中断（Ctrl+C）")
                break

            except EOFError:
                break


# ============================================================
# 7. 单次对话模式
# ============================================================


async def single_chat(message: str):
    """
    单次对话模式

    **用途**: 脚本调用
    """
    client = AgentChatClient(Config)
    renderer = TerminalRenderer()

    renderer.clear_screen()
    renderer.print_header()

    await client.chat_stream(message)


# ============================================================
# 8. 主程序
# ============================================================


async def main():
    """主函数"""
    import sys

    if len(sys.argv) > 1:
        # 单次对话模式
        message = " ".join(sys.argv[1:])
        await single_chat(message)
    else:
        # 交互式模式
        cli = InteractiveCLI()
        await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)
