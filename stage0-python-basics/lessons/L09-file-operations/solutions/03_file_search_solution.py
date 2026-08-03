"""L05 练习3: 目录文件搜索 - 参考答案"""

from datetime import datetime, timedelta
from pathlib import Path


def find_by_extension(root_dir: str, extensions: list[str]) -> list[str]:
    """搜索指定目录下所有匹配扩展名的文件。"""
    root = Path(root_dir)
    if not root.is_dir():
        return []
    extensions_lower = [ext.lower() for ext in extensions]
    result = []
    for path in root.rglob("*"):
        if path.is_file():
            path_str = str(path).lower()
            if any(path_str.endswith(ext.lower()) for ext in extensions_lower):
                result.append(str(path))
    return result


def find_large_files(root_dir: str, min_size_bytes: int) -> list[tuple[str, int]]:
    """搜索目录下超过指定大小的文件，按大小降序排列。"""
    root = Path(root_dir)
    if not root.is_dir():
        return []
    result = []
    for path in root.rglob("*"):
        if path.is_file():
            size = path.stat().st_size
            if size >= min_size_bytes:
                result.append((str(path), size))
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def find_recent_files(root_dir: str, days: int = 7) -> list[tuple[str, float]]:
    """搜索最近 N 天内修改过的文件，按修改时间降序排列。"""
    root = Path(root_dir)
    if not root.is_dir():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_ts = cutoff.timestamp()
    result = []
    for path in root.rglob("*"):
        if path.is_file():
            mtime = path.stat().st_mtime
            if mtime >= cutoff_ts:
                result.append((str(path), mtime))
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def find_in_directories(root_dirs: list[str], pattern: str) -> dict[str, list[str]]:
    """在多个目录中搜索匹配模式的文件。

    Args:
        root_dirs: 根目录列表
        pattern: 文件名模式，如 '*.py' 或 '**/*.py'
                 含 ** 时自动使用 rglob 递归搜索，否则仅搜根目录

    Returns:
        {目录: [匹配文件列表], ...}
    """
    result = {}
    for root_dir in root_dirs:
        root = Path(root_dir)
        if root.is_dir():
            if "**" in pattern:
                matches = [str(p) for p in root.glob(pattern) if p.is_file()]
            else:
                matches = [str(p) for p in root.rglob(pattern) if p.is_file()]
            result[root_dir] = matches
        else:
            result[root_dir] = []
    return result
