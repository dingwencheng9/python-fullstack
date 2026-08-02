"""L11: 生成器与迭代器 - 文件流生成器示例

演示生成器在实际场景中的应用：
1. 大文件逐行流式读取（避免一次性加载到内存）
2. 批量行处理（平衡内存与 I/O 效率）
3. 带过滤条件的行生成器
"""

from __future__ import annotations

import re
from pathlib import Path

# === Part 1: 大文件逐行流式读取 ===


def stream_lines(filepath: str, encoding: str = "utf-8"):
    """逐行流式读取大文件，不会一次性加载全部内容到内存。

    适用场景：日志分析、大型 CSV、DNA 序列文件等超大文件。
    """
    with open(filepath, encoding=encoding) as f:
        for line in f:
            yield line.rstrip("\n")


# 模拟大文件（实际使用时替换为真实文件路径）
DEMO_FILE = Path(__file__).parent / "demo_large.log"
DEMO_FILE.write_text("\n".join(f"Line {i}: INFO message {i % 5}" for i in range(100)))

print("=== Part 1: 流式读取 ===")
line_count = 0
for line in stream_lines(str(DEMO_FILE)):
    line_count += 1
    if line_count <= 3:
        print(f"  {line}")
print(f"  ... (共 {line_count} 行，内存中只保留当前行)")


# === Part 2: 批量行处理生成器 ===


def batched_stream(filepath: str, batch_size: int = 10):
    """批量读取行，每次返回 batch_size 行。

    适用场景：批量写入数据库、网络分批发送等。
    """
    batch: list[str] = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            batch.append(line.rstrip("\n"))
            if len(batch) >= batch_size:
                yield batch
                batch = []
        if batch:
            yield batch  # 最后一批不足 batch_size 的行


print("\n=== Part 2: 批量处理 ===")
for i, batch in enumerate(batched_stream(str(DEMO_FILE), batch_size=10)):
    print(f"  Batch {i + 1}: {len(batch)} 行，首行: {batch[0]}")


# === Part 3: 带过滤条件的行生成器 ===


def filtered_lines(filepath: str, pattern: str):
    """只产出匹配正则表达式的行。

    适用场景：从日志中提取特定错误、搜索关键词等。
    """
    compiled = re.compile(pattern)
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if compiled.search(line):
                yield line.rstrip("\n")


print("\n=== Part 3: 过滤匹配 ===")
print("  匹配 'Line 5' 的行:")
for line in filtered_lines(str(DEMO_FILE), r"Line [5]"):
    print(f"    {line}")


# === Part 4: 生成器管道组合 ===


def lines_to_words(lines):
    """将行拆分为单词流"""
    for line in lines:
        yield from line.split()


def words_matching(lines, substring: str):
    """过滤包含子串的单词"""
    for word in lines:
        if substring in word:
            yield word


print("\n=== Part 4: 生成器管道 ===")
# 组合使用：读取 → 过滤行 → 拆分单词 → 过滤单词
pipeline = words_matching(lines_to_words(stream_lines(str(DEMO_FILE))), substring="INFO")
matched = list(pipeline)
print(f"  包含 'INFO' 的单词: {matched[:5]}...")


# === Part 5: 生成器的内存优势 ===


def count_memory_advantage():
    """对比列表 vs 生成器的内存占用"""
    import sys

    # 列表：一次性分配所有行
    all_lines = [f"Line {i}" for i in range(1000)]
    list_size = sys.getsizeof(all_lines)
    print("\n=== Part 5: 内存对比 ===")
    print(f"  列表存储 1000 行: {list_size:,} bytes")

    # 生成器：只存储生成器对象本身
    gen = (f"Line {i}" for i in range(1000))
    gen_size = sys.getsizeof(gen)
    print(f"  生成器存储 1000 行: {gen_size:,} bytes")
    print(f"  内存节省: {(1 - gen_size / list_size) * 100:.1f}%")


count_memory_advantage()

# 清理演示文件
DEMO_FILE.unlink(missing_ok=True)

print("\n=== 文件流生成器示例完成 ===")
