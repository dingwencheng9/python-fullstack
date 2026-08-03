"""
L05 练习3: 目录文件搜索

难度: ⭐⭐ (中等)
预计时间: 25 分钟
知识点: os.listdir、pathlib.Path、文件过滤、递归搜索

任务描述:
遍历目录，搜索满足条件的文件（如特定扩展名、大小超过阈值等）。
"""

from pathlib import Path


# ========================================
# 👉 TODO 1: 搜索特定扩展名的文件
# ========================================


def find_by_extension(root_dir: str, extensions: list[str]) -> list[str]:
    """搜索指定目录下所有匹配扩展名的文件。

    Args:
        root_dir: 根目录路径
        extensions: 扩展名列表，如 ['.py', '.md']

    Returns:
        所有匹配文件的绝对路径列表
    """
    # 提示:
    # 1. 使用 Path(root_dir).rglob('*') 递归遍历
    # 2. 检查每个路径是否为文件（.is_file()）
    # 3. 检查扩展名是否在 extensions 列表中
    # 4. 返回所有匹配文件的绝对路径（str 或 Path）

    # 扩展名应统一转为小写以支持不区分大小写匹配
    # 使用 str(path).lower().endswith(ext.lower()) 忽略大小写

    # 💡 扩展:
    # - 支持 * 通配符匹配
    # - 支持排除特定子目录
    # - 支持返回相对路径而非绝对路径

    root = Path(root_dir)
    matches: list[str] = []
    exts = [e.lower() for e in extensions]
    for p in root.rglob("*"):
        try:
            if p.is_file():
                name = str(p.name).lower()
                for ext in exts:
                    if name.endswith(ext.lower()):
                        matches.append(str(p))
                        break
        except OSError:
            continue
    return matches


# ========================================
# 👉 TODO 2: 搜索超过指定大小的文件
# ========================================


def find_large_files(root_dir: str, min_size_bytes: int) -> list[tuple[str, int]]:
    """搜索目录下超过指定大小的文件。

    Args:
        root_dir: 根目录路径
        min_size_bytes: 最小文件大小（字节）

    Returns:
        [(文件路径, 大小字节数), ...] 按大小降序排列
    """
    # 提示:
    # 1. 遍历目录（可使用 os.walk 或 pathlib.rglob）
    # 2. 检查每个文件的大小（path.stat().st_size）
    # 3. 过滤出超过 min_size_bytes 的文件
    # 4. 按大小降序排序返回

    # 💡 扩展:
    # - 支持 max_size_bytes 过滤
    # - 支持显示人类可读的大小（KB/MB/GB）
    # - 支持排除特定目录（如 .git）

    root = Path(root_dir)
    results: list[tuple[str, int]] = []
    for p in root.rglob("*"):
        try:
            if p.is_file():
                size = p.stat().st_size
                if size >= min_size_bytes:
                    results.append((str(p), size))
        except OSError:
            continue
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ========================================
# 👉 TODO 3: 搜索最近修改的文件
# ========================================


def find_recent_files(root_dir: str, days: int = 7) -> list[tuple[str, float]]:
    """搜索最近 N 天内修改过的文件。

    Args:
        root_dir: 根目录路径
        days: 天数（默认7天）

    Returns:
        [(文件路径, 修改时间戳), ...] 按修改时间降序排列
    """
    # 提示:
    # 1. 使用 datetime.now() - timedelta(days=days) 计算截止时间
    # 2. 使用 path.stat().st_mtime 获取修改时间戳
    # 3. 比较时间戳，过滤出 recent_time > cutoff_time 的文件
    # 4. 排序并返回

    # 💡 扩展:
    # - 支持 hours 参数（精确到小时）
    # - 支持同时搜索最近修改和最近创建的文件
    # - 支持忽略特定文件（如 __pycache__）

    from datetime import datetime

    cutoff = datetime.now().timestamp() - days * 86400
    root = Path(root_dir)
    results: list[tuple[str, float]] = []
    for p in root.rglob("*"):
        try:
            if p.is_file():
                mtime = p.stat().st_mtime
                if mtime >= cutoff:
                    results.append((str(p), mtime))
        except OSError:
            continue
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# ========================================
# 👉 TODO 4: 递归合并多目录搜索结果
# ========================================


def find_in_directories(root_dirs: list[str], pattern: str) -> dict[str, list[str]]:
    """在多个目录中搜索匹配模式的文件。

    Args:
        root_dirs: 根目录列表
        pattern: 文件名模式，如 '*.py' 或 'test_*.py'

    Returns:
        {目录: [匹配文件列表], ...}
    """
    # 提示:
    # 1. 对每个 root_dir 调用 Path(root_dir).glob(pattern)
    # 2. 将结果按目录分组
    # 3. 返回字典 {root_dir: [files...]}

    # 💡 扩展:
    # - 支持递归 glob（rglob）
    # - 支持返回统计摘要（总文件数、总大小等）

    out: dict[str, list[str]] = {}
    for rd in root_dirs:
        p = Path(rd)
        matches: list[str] = []
        try:
            for f in p.rglob(pattern):
                if f.is_file():
                    matches.append(str(f))
        except OSError:
            matches = []
        out[rd] = matches
    return out


# ========================================
# 测试代码
# ========================================

if __name__ == "__main__":
    import tempfile

    # 创建临时测试目录结构
    test_dir = tempfile.mkdtemp()
    print(f"创建测试目录: {test_dir}")

    # 创建测试文件
    test_files = [
        "script.py",
        "data.txt",
        "README.md",
        "subdir/nested.py",
        "subdir/image.png",
    ]

    for f in test_files:
        path = Path(test_dir) / f
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("test content" * 100)  # 写入一些内容

    # 测试 1: 按扩展名搜索
    print("\n=== 测试 1: 搜索 .py 文件 ===")
    try:
        py_files = find_by_extension(test_dir, [".py"])
        print(f"找到 {len(py_files)} 个 .py 文件")
        for f in py_files:
            print(f"  - {Path(f).relative_to(test_dir)}")
    except NotImplementedError:
        print("  (TODO: 未实现)")

    # 测试 2: 搜索大文件
    print("\n=== 测试 2: 搜索 >500 字节的文件 ===")
    try:
        large_files = find_large_files(test_dir, 500)
        print(f"找到 {len(large_files)} 个大文件")
        for f, size in large_files:
            print(f"  - {Path(f).relative_to(test_dir)}: {size} bytes")
    except NotImplementedError:
        print("  (TODO: 未实现)")

    # 清理
    import shutil

    shutil.rmtree(test_dir)
    print(f"\n清理测试目录: {test_dir}")
