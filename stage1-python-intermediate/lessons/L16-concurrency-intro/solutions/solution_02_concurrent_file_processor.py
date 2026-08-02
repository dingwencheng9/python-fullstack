"""
L14: 练习 2 参考答案 - 并发文件处理器
"""

import asyncio
from pathlib import Path


async def read_file(path: Path) -> str:
    """异步读取文件内容。"""
    return await asyncio.to_thread(path.read_text)


async def process_files(filenames: list[str]) -> list[dict]:
    """异步读取并处理多个文件。"""
    # 创建任务列表
    tasks = [read_file(Path(fn)) for fn in filenames]

    # 并发执行
    contents = await asyncio.gather(*tasks)

    # 构建结果
    return [
        {"filename": fn, "content": content}
        for fn, content in zip(filenames, contents)
    ]


async def count_words_in_files(filenames: list[str]) -> dict[str, int]:
    """统计每个文件的单词数。"""
    # 读取所有文件内容
    tasks = [read_file(Path(fn)) for fn in filenames]
    contents = await asyncio.gather(*tasks)

    # 统计单词数
    return {
        fn: len(content.split())
        for fn, content in zip(filenames, contents)
    }
