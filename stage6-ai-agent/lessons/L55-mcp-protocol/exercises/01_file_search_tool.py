"""

from __future__ import annotations

练习 1: 文件搜索工具

实现 FileSearchServer:

1. 初始化时接收 root 目录
2. 提供 search_files(query: str, pattern: str = "*.py") -> str
3. 只能搜索 root 内部文件，不能越权访问
4. 返回最多 20 个匹配文件路径
5. 没有结果时返回 "no matches"

提示:
- 使用 Path.rglob(pattern)
- 用 path.resolve() 检查是否在 root 内部
"""

from pathlib import Path


class FileSearchServer:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def search_files(self, query: str, pattern: str = "*.py") -> str:
        raise NotImplementedError
