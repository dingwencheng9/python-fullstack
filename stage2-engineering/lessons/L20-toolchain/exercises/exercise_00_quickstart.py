"""练习1: uv 包管理实战"""

from __future__ import annotations

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


async def fetch_python_version() -> dict[str, str]:
    """从Python官网API获取最新版本信息"""
    url = "https://www.python.org/api/v2/downloads/release/?is_published=true&limit=5"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

        if data:
            latest = data[0]
            return {
                "name": latest.get("name", "Unknown"),
                "slug": latest.get("slug", "Unknown"),
                "version": latest.get("version", "Unknown"),
            }
        return {}


def display_environment_info() -> None:
    """显示当前Python环境信息"""
    import sys
    from pathlib import Path

    table = Table(title="Python环境信息", show_header=True, header_style="bold magenta")
    table.add_column("项目", style="cyan", width=20)
    table.add_column("值", style="green")

    table.add_row(
        "Python版本",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )
    table.add_row("解释器路径", sys.executable)
    table.add_row(
        "虚拟环境",
        "是" if hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix else "否",
    )
    table.add_row("工作目录", str(Path.cwd()))

    console.print(table)


async def main() -> None:
    """主函数"""
    console.print("[bold blue]L18 练习0: uv 包管理实战[/bold blue]\n")

    # 显示环境信息
    display_environment_info()
    console.print()

    # 测试 httpx 异步请求
    console.print("[bold yellow]正在获取Python最新版本信息...[/bold yellow]")
    try:
        version_info = await fetch_python_version()
        console.print(f"[bold green]✓ 最新Python版本:[/bold green] {version_info.get('name', 'Unknown')}")
    except Exception as e:
        console.print(f"[bold red]✗ 获取失败:[/bold red] {e}")

    console.print("\n[bold green]✓ 练习完成！你已成功使用 uv 安装的依赖。[/bold green]")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
