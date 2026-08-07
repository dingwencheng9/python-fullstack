"""
L16: 练习 2 - 并发文件处理器

使用异步 I/O 异步读取并处理多个文件。
"""

import asyncio
from pathlib import Path


async def read_file(path: Path) -> str:
    """异步读取文件内容。

    Args:
        path: 文件路径

    Returns:
        文件内容字符串
    """
    # 在后台线程中读取文件内容以避免阻塞事件循环
    return await asyncio.to_thread(path.read_text)


async def process_files(filenames: list[str]) -> list[dict]:
    """异步读取并处理多个文件。

    Args:
        filenames: 文件名列表

    Returns:
        包含文件名和内容的字典列表
    """
    # 并发读取所有文件并返回包含文件名和内容的字典列表
    tasks = [asyncio.create_task(read_file(Path(fn))) for fn in filenames]
    contents = await asyncio.gather(*tasks)
    return [{"filename": fn, "content": content} for fn, content in zip(filenames, contents)]


async def count_words_in_files(filenames: list[str]) -> dict[str, int]:
    """统计每个文件的单词数。

    Args:
        filenames: 文件名列表

    Returns:
        文件名到单词数的映射
    """
    results = await process_files(filenames)
    mapping: dict[str, int] = {}
    for r in results:
        content = r["content"]
        # 使用简单的空白分割统计单词数；空字符串计为 0
        count = 0 if content.strip() == "" else len(content.split())
        mapping[r["filename"]] = count
    return mapping


# === 验证 ===

if __name__ == "__main__":

    async def main():
        # 创建测试文件
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)

        (test_dir / "file1.txt").write_text("hello world")
        (test_dir / "file2.txt").write_text("python async programming")
        (test_dir / "file3.txt").write_text("")

        try:
            # 测试 process_files
            results = await process_files([
                "test_files/file1.txt",
                "test_files/file2.txt",
            ])
            assert len(results) == 2
            assert results[0]["content"] == "hello world"
            assert results[1]["content"] == "python async programming"
            print("✅ process_files 测试通过")

            # 测试 count_words_in_files
            word_counts = await count_words_in_files([
                "test_files/file1.txt",
                "test_files/file2.txt",
                "test_files/file3.txt",
            ])
            assert word_counts["test_files/file1.txt"] == 2
            assert word_counts["test_files/file2.txt"] == 3
            assert word_counts["test_files/file3.txt"] == 0
            print("✅ count_words_in_files 测试通过")

            print("\n✅ 所有测试通过！")

        finally:
            # 清理测试文件
            for f in test_dir.glob("*.txt"):
                f.unlink()
            test_dir.rmdir()

    asyncio.run(main())
