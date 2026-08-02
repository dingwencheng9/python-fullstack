"""

from __future__ import annotations

练习1: uv 包管理实战 - 标准答案

解题思路：
==========
本练习旨在验证学员能够：
1. 正确配置 Python 3.13 开发环境
2. 使用 uv 工具管理项目依赖
3. 掌握异步编程基础（async/await）
4. 使用现代化的第三方库（httpx、rich）

核心知识点：
- uv 包管理器的使用
- 异步 HTTP 请求（httpx.AsyncClient）
- 终端美化输出（rich.Console）
- 环境信息获取（sys 模块）

实现要点：
1. 使用 httpx 进行异步 HTTP 请求
2. 使用 rich 创建美化的表格输出
3. 异常处理确保程序健壮性
4. 使用 asyncio.run() 启动异步主函数
"""

import httpx
from rich.console import Console
from rich.table import Table

console = Console()


async def fetch_python_version() -> dict[str, str]:
    """从 Python 官网 API 获取最新版本信息

    为什么使用异步请求？
    - 网络 I/O 是典型的异步场景
    - httpx.AsyncClient 提供现代化的异步 API
    - 避免阻塞主线程，提高程序响应性

    为什么使用 context manager (async with)？
    - 自动管理连接的创建和关闭
    - 确保资源正确释放
    - 异常情况下也能正确清理
    """
    url = "https://www.python.org/api/v2/downloads/release/?is_published=true&limit=5"

    async with httpx.AsyncClient() as client:
        # 发送 GET 请求
        response = await client.get(url)

        # 检查响应状态（4xx/5xx 会抛出异常）
        # 为什么需要 raise_for_status？
        # - 及早发现 HTTP 错误
        # - 提供清晰的错误信息
        response.raise_for_status()

        # 解析 JSON 响应
        data = response.json()

        # 提取最新版本信息
        # 为什么检查 data 是否为空？
        # - API 可能返回空列表
        # - 避免 IndexError
        if data:
            latest = data[0]
            return {
                "name": latest.get("name", "Unknown"),
                "slug": latest.get("slug", "Unknown"),
                "version": latest.get("version", "Unknown"),
            }
        return {}


def display_environment_info() -> None:
    """显示当前 Python 环境信息

    为什么需要显示环境信息？
    - 帮助学员验证环境配置
    - 了解当前运行环境
    - 调试环境问题的第一步

    使用 rich.Table 的好处：
    - 自动对齐和格式化
    - 支持颜色和样式
    - 提供专业的终端输出
    """
    import sys
    from pathlib import Path

    # 创建表格
    table = Table(title="Python 环境信息", show_header=True, header_style="bold magenta")
    table.add_column("项目", style="cyan", width=20)
    table.add_column("值", style="green")

    # 添加 Python 版本
    table.add_row(
        "Python 版本",
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )

    # 添加解释器路径
    table.add_row("解释器路径", sys.executable)

    # 检查是否在虚拟环境中
    # 为什么这样检查虚拟环境？
    # - sys.base_prefix: Python 安装的基础路径
    # - sys.prefix: 当前环境的前缀路径
    # - 虚拟环境中这两者不同
    in_venv = hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    table.add_row("虚拟环境", "是" if in_venv else "否")

    # 添加工作目录
    table.add_row("工作目录", str(Path.cwd()))

    # 打印表格
    console.print(table)


async def main() -> None:
    """主函数

    为什么使用 async main？
    - 允许在主函数中使用 await
    - 统一异步编程风格
    - 便于调用其他异步函数

    程序流程：
    1. 打印标题
    2. 显示环境信息
    3. 测试异步 HTTP 请求
    4. 输出结果
    """
    console.print("[bold blue]L18 练习0: uv 包管理实战[/bold blue]\n")

    # 显示环境信息
    display_environment_info()
    console.print()

    # 测试 httpx 异步请求
    console.print("[bold yellow]正在获取 Python 最新版本信息...[/bold yellow]")

    # 为什么需要 try-except？
    # - 网络请求可能失败（超时、连接错误）
    # - API 可能返回错误状态
    # - 确保程序不会因异常而崩溃
    try:
        version_info = await fetch_python_version()

        # 为什么使用 get() 而非直接索引？
        # - 字典可能不包含某个键
        # - get() 提供默认值，避免 KeyError
        console.print(f"[bold green]✓ 最新 Python 版本:[/bold green] {version_info.get('name', 'Unknown')}")
    except Exception as e:
        # 捕获所有异常并显示错误信息
        console.print(f"[bold red]✗ 获取失败:[/bold red] {e}")

    console.print("\n[bold green]✓ 练习完成！你已成功使用 uv 安装的依赖。[/bold green]")


if __name__ == "__main__":
    import asyncio

    # 为什么使用 asyncio.run()？
    # - Python 3.7+ 推荐的启动异步程序的方式
    # - 自动创建和关闭事件循环
    # - 处理信号和清理任务
    asyncio.run(main())
