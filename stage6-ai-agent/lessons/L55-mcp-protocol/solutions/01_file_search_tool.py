"""L60 练习 1: 文件搜索工具 — 参考答案（路径穿越防护强化版）

from __future__ import annotations

✅ 防护措施:
1. 使用 Path.resolve().relative_to(ALLOWED_BASE_DIR) 防御性断言
2. 使用 os.open + os.fstat 消除 TOCTOU 竞态条件
3. 符号链接解析后二次校验
"""

from __future__ import annotations

import os
from pathlib import Path


class PathTraversalError(PermissionError):
    """路径穿越攻击被拦截时抛出。"""

    pass


class FileSearchServer:
    """文件搜索服务器，内置路径穿越防护。

    所有文件访问都经过 resolve().relative_to(root) 断言，
    确保无法越权访问 root 目录之外的任何文件。
    """

    def __init__(self, root: Path) -> None:
        """初始化，锁定允许搜索的根目录。

        Args:
            root: 允许搜索的根目录（自动 resolve 为绝对路径）
        """
        self.root = root.resolve()

    def _validate_path(self, path: Path) -> Path:
        """防御性断言：验证路径在 root 内部，返回解析后的安全路径。

        使用 Path.resolve().relative_to(self.root) 断言，
        路径越界时直接抛出 PathTraversalError。

        Args:
            path: 待验证的路径

        Returns:
            解析后的绝对路径（确认在 root 内部）

        Raises:
            PathTraversalError: 路径穿越 root 边界
        """
        resolved = path.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise PathTraversalError(
                f"拒绝访问: 路径 '{path}' 解析为 '{resolved}'，越出允许的根目录 '{self.root}'"
            ) from exc
        return resolved

    def _safe_read_text(self, path: Path) -> str:
        """安全读取文件内容，消除 TOCTOU 竞态条件。

        使用 os.open + O_NOFOLLOW 打开文件后，立即通过 os.fstat 和 os.stat
        比较 inode，确保打开的文件与原始路径指向同一个文件。

        防护机制:
        1. O_NOFOLLOW: 拒绝打开符号链接
        2. inode 比较: 确保 fd 和 path 指向同一个文件（防止 TOCTOU 替换）

        Args:
            path: 已通过 _validate_path 验证的路径

        Returns:
            文件文本内容

        Raises:
            PathTraversalError: 文件被替换或 inode 不匹配
        """
        # 使用 os.open 获取文件描述符（O_NOFOLLOW 防止符号链接）
        try:
            fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
        except OSError as exc:
            # 符号链接会触发 ELOOP 或 EMLINK
            raise PathTraversalError(f"拒绝打开符号链接: {path}") from exc

        try:
            # 通过 fd 获取文件的 inode 信息
            fd_stat = os.fstat(fd)

            # 再次 stat 原始路径，比较 inode（消除 TOCTOU）
            path_stat = os.stat(str(path), follow_symlinks=False)

            # inode 必须一致（同一个文件）
            if (fd_stat.st_dev, fd_stat.st_ino) != (path_stat.st_dev, path_stat.st_ino):
                raise PathTraversalError(f"TOCTOU 防护: 文件被替换（inode 不匹配）: {path}")

            # 读取内容
            with os.fdopen(fd, "r", errors="ignore") as f:
                return f.read()
        except PathTraversalError:
            os.close(fd)
            raise
        except Exception:
            os.close(fd)
            raise

    def search_files(self, query: str, pattern: str = "*.py") -> str:
        """在 root 目录内搜索包含 query 的文件。

        所有搜索结果都经过路径穿越防护验证，
        符号链接指向 root 外部的文件会被自动过滤。

        Args:
            query: 搜索关键词（在文件内容中匹配）
            pattern: 文件名 glob 模式，默认 "*.py"

        Returns:
            匹配文件列表（相对于 root 的路径），最多 20 个；
            无匹配时返回 "no matches"
        """
        hits: list[str] = []
        for path in self.root.rglob(pattern):
            # 防御层 1: resolve().relative_to() 断言
            try:
                safe_path = self._validate_path(path)
            except PathTraversalError:
                continue

            if not safe_path.is_file():
                continue

            # 防御层 2: 安全读取（消除 TOCTOU）
            try:
                content = self._safe_read_text(safe_path)
            except (PathTraversalError, OSError):
                continue

            if query in content:
                hits.append(str(safe_path.relative_to(self.root)))

        return "\n".join(hits[:20]) or "no matches"
