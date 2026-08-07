"""

from __future__ import annotations

L32 SSE 服务器推送事件 - CLI 客户端 V2（会话管理版）
=================================================

本模块实现支持会话管理的 CLI 客户端。

核心能力：
1. 会话列表查看
2. 历史会话选择
3. 新会话创建
4. thread_id 管理

作者：Python 3.13 全栈课程
"""

import asyncio
from datetime import datetime

from cli_client import (
    Config,
    SSEParser,
    TerminalRenderer,
)
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

# ============================================================
# 1. 会话管理客户端
# ============================================================


class ConversationManager:
    """
    会话管理器

    **职责**:
    - 获取会话列表
    - 选择会话
    - 创建新会话
    """

    def __init__(self, api_url: str, token: str):
        self.api_url = api_url.replace("/chat", "")  # 去掉 /chat 后缀
        self.token = token
        self.console = Console()

    async def list_conversations(self, limit: int = 20) -> list[dict]:
        """获取会话列表"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/conversations",
                headers={"Authorization": f"Bearer {self.token}"},
                params={"limit": limit},
            )

            if response.status_code != 200:
                return []

            data = response.json()
            return data.get("conversations", [])

    async def get_conversation_detail(self, thread_id: str) -> dict | None:
        """获取会话详情"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/conversations/{thread_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if response.status_code != 200:
                return None

            return response.json()

    def display_conversations(self, conversations: list[dict]):
        """显示会话列表"""
        if not conversations:
            self.console.print("[yellow]没有找到历史会话[/yellow]\n")
            return

        table = Table(
            title="📚 历史会话",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("#", style="dim", width=3)
        table.add_column("Thread ID", style="cyan", width=20)
        table.add_column("消息数", justify="right", width=8)
        table.add_column("Token 数", justify="right", width=10)
        table.add_column("最后更新", width=20)

        for i, conv in enumerate(conversations, 1):
            # 格式化时间
            updated_at = datetime.fromisoformat(conv["updated_at"])
            time_str = updated_at.strftime("%Y-%m-%d %H:%M")

            table.add_row(
                str(i),
                conv["thread_id"][:18] + "...",
                str(conv["total_messages"]),
                str(conv["total_tokens"]),
                time_str,
            )

        self.console.print(table)
        self.console.print()

    def display_conversation_detail(self, detail: dict):
        """显示会话详情"""
        conv = detail["conversation"]
        messages = detail["messages"]

        # 会话信息
        info_text = Text()
        info_text.append("Thread ID: ", style="bold")
        info_text.append(f"{conv['thread_id']}\n", style="cyan")
        info_text.append("消息数: ", style="bold")
        info_text.append(f"{conv['total_messages']}\n")
        info_text.append("Token 数: ", style="bold")
        info_text.append(f"{conv['total_tokens']}\n")
        info_text.append("创建时间: ", style="bold")
        info_text.append(f"{conv['created_at'][:19]}\n", style="dim")

        panel = Panel(
            info_text,
            title="📋 会话详情",
            border_style="cyan",
        )
        self.console.print(panel)
        self.console.print()

        # 最近消息
        self.console.print("[bold]📝 最近消息:[/bold]\n")

        for msg in messages[-10:]:  # 最多显示 10 条
            role_color = "green" if msg["role"] == "user" else "white"
            role_emoji = "👤" if msg["role"] == "user" else "🤖"

            text = Text()
            text.append(f"{role_emoji} {msg['role'].title()}: ", style=f"bold {role_color}")
            text.append(msg["content"][:100], style=role_color)

            if len(msg["content"]) > 100:
                text.append("...", style="dim")

            self.console.print(text)

        self.console.print()


# ============================================================
# 2. 升级的 Agent 客户端
# ============================================================


class AgentChatClientV2:
    """
    Agent 对话客户端 V2

    **新增功能**:
    - thread_id 管理
    - 会话选择
    """

    def __init__(self, config: Config):
        self.config = config
        self.parser = SSEParser()
        self.renderer = TerminalRenderer()
        self.thread_id: str | None = None

    def set_thread_id(self, thread_id: str | None):
        """设置当前 thread_id"""
        self.thread_id = thread_id

    async def chat_stream(self, message: str):
        """流式对话"""
        self.renderer.print_user_message(message)

        try:
            async with httpx.AsyncClient(timeout=self.config.TIMEOUT) as client:
                # 构建请求体
                request_body = {
                    "message": message,
                    "stream": True,
                    "include_history": True,
                }

                # 如果有 thread_id，携带它
                if self.thread_id:
                    request_body["thread_id"] = self.thread_id

                async with client.stream(
                    "POST",
                    self.config.API_URL.replace("/v1/", "/v2/"),  # 使用 V2 API
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.config.JWT_TOKEN}",
                    },
                    json=request_body,
                ) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        self.renderer.print_error(f"HTTP {response.status_code}: {error_text.decode()}")
                        return

                    # 提取 thread_id（首次对话）
                    if not self.thread_id:
                        self.thread_id = response.headers.get("X-Thread-ID")
                        if self.thread_id:
                            self.renderer.print_status(f"新会话已创建: {self.thread_id}")

                    self.renderer.start_agent_message()

                    # 解析 SSE 流
                    async for event_type, data in self.parser.parse_stream(response):
                        await self.handle_event(event_type, data)

                    self.renderer.finish_agent_message()

        except httpx.TimeoutException:
            self.renderer.print_error("请求超时")
        except httpx.ConnectError:
            self.renderer.print_error("无法连接到服务器")
        except Exception as e:
            self.renderer.print_error(f"{type(e).__name__}: {e}")

    async def handle_event(self, event_type: str, data: dict):
        """处理事件"""
        if event_type == "connection":
            pass

        elif event_type == "system":
            # 系统消息（如压缩提示）
            message = data.get("message", "")
            if message:
                self.renderer.print_status(message)

        elif event_type == "token":
            if data.get("event_type") == "on_chat_model_stream":
                if not data.get("is_final"):
                    token = data.get("token", "")
                    self.renderer.append_token(token)
                    await asyncio.sleep(0.01)

        elif event_type == "tool":
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
                self.renderer.console.print("🤖 Agent: ", style="bold white", end="")

        elif event_type == "completion":
            # 显示 Token 统计
            stats = data.get("token_statistics", {})
            if stats:
                self.renderer.console.print()
                text = Text()
                text.append("📊 ", style="dim")
                text.append(f"总 Token: {stats.get('total_tokens', 0)}, ", style="dim")
                text.append(f"平均: {stats.get('avg_tokens_per_message', 0):.1f}", style="dim")
                self.renderer.console.print(text)

        elif event_type == "error":
            self.renderer.print_error(f"{data.get('error_type', 'Error')}: {data.get('error_message', '')}")


# ============================================================
# 3. 交互式 CLI V2
# ============================================================


class InteractiveCLIV2:
    """
    交互式命令行界面 V2

    **新增功能**:
    - 会话选择
    - 历史加载
    """

    def __init__(self):
        self.config = Config()
        # 修改 API URL 为 V2
        self.config.API_URL = self.config.API_URL.replace("/v1/", "/v2/")

        self.client = AgentChatClientV2(self.config)
        self.renderer = TerminalRenderer()
        self.conversation_manager = ConversationManager(
            self.config.API_URL,
            self.config.JWT_TOKEN,
        )

    async def select_conversation(self) -> str | None:
        """
        选择会话

        **返回**: thread_id 或 None（新会话）
        """
        # 获取会话列表
        conversations = await self.conversation_manager.list_conversations()

        if not conversations:
            self.renderer.print_status("没有历史会话，将创建新会话")
            return None

        # 显示会话列表
        self.conversation_manager.display_conversations(conversations)

        # 提示选择
        choice = Prompt.ask(
            "[bold cyan]选择会话[/bold cyan] (输入编号，或按 Enter 创建新会话)",
            default="",
            console=self.renderer.console,
        )

        if not choice.strip():
            return None

        try:
            index = int(choice) - 1
            if 0 <= index < len(conversations):
                thread_id = conversations[index]["thread_id"]

                # 显示会话详情
                detail = await self.conversation_manager.get_conversation_detail(thread_id)
                if detail:
                    self.conversation_manager.display_conversation_detail(detail)

                return thread_id
            self.renderer.print_error("无效的选择")
            return None

        except ValueError:
            self.renderer.print_error("请输入有效的编号")
            return None

    async def run(self):
        """运行交互式 CLI"""
        self.renderer.clear_screen()
        self.renderer.print_header()

        # 选择会话
        self.renderer.print_status("正在加载会话列表...")
        thread_id = await self.select_conversation()

        if thread_id:
            self.client.set_thread_id(thread_id)
            self.renderer.print_status(f"已加载会话: {thread_id}")
        else:
            self.renderer.print_status("开始新会话")

        self.renderer.print_separator()
        self.renderer.console.print()

        # 交互循环
        while True:
            try:
                user_input = Prompt.ask(
                    "[bold green]You[/bold green]",
                    console=self.renderer.console,
                )

                if user_input.lower() in ["exit", "quit", "q"]:
                    self.renderer.print_status("再见！👋")
                    break

                if user_input.lower() == "new":
                    # 创建新会话
                    self.client.set_thread_id(None)
                    self.renderer.print_status("已切换到新会话")
                    continue

                if user_input.lower() == "list":
                    # 列出会话
                    conversations = await self.conversation_manager.list_conversations()
                    self.conversation_manager.display_conversations(conversations)
                    continue

                if not user_input.strip():
                    continue

                await self.client.chat_stream(user_input)

            except KeyboardInterrupt:
                self.renderer.console.print()
                self.renderer.print_status("已中断（Ctrl+C）")
                break
            except EOFError:
                break


# ============================================================
# 4. 主程序
# ============================================================


async def main():
    """主函数"""
    import sys

    if len(sys.argv) > 1:
        # 单次对话模式（简化版）
        message = " ".join(sys.argv[1:])
        client = AgentChatClientV2(Config())
        renderer = TerminalRenderer()

        renderer.clear_screen()
        renderer.print_header()

        await client.chat_stream(message)
    else:
        # 交互式模式
        cli = InteractiveCLIV2()
        await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
