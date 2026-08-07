"""
L16: 练习 2 测试 - 并发文件处理器
"""

import pytest


@pytest.fixture
def temp_files(tmp_path):
    """创建临时测试文件，返回 (tmp_dir, files_dict)。"""
    files = {
        "file0.txt": "hello world",
        "file1.txt": "python async",
        "file2.txt": "test",
    }
    for name, content in files.items():
        (tmp_path / name).write_text(content)
    return tmp_path, files


@pytest.fixture(autouse=True)
def _inject_module(solutions, request) -> None:
    """注入 file_processor 模块到测试命名空间。"""
    try:
        request.module.__dict__["file_processor"] = getattr(solutions, "solution_02_concurrent_file_processor")
    except (AttributeError, ImportError) as e:
        pytest.fail(f"无法导入 solution_02_concurrent_file_processor: {e}")


@pytest.mark.asyncio
async def test_read_file(tmp_path):
    """测试异步文件读取。"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    result = await file_processor.read_file(test_file)
    assert result == "hello"


@pytest.mark.asyncio
async def test_process_files(temp_files):
    """测试并发处理多个文件。"""
    tmp_dir, files = temp_files
    filenames = [str(tmp_dir / fn) for fn in files.keys()]

    results = await file_processor.process_files(filenames)

    assert len(results) == 3
    for r in results:
        assert "filename" in r
        assert "content" in r


@pytest.mark.asyncio
async def test_count_words_in_files(temp_files):
    """测试统计单词数。"""
    tmp_dir, files = temp_files
    filenames = [str(tmp_dir / fn) for fn in files.keys()]

    word_counts = await file_processor.count_words_in_files(filenames)

    assert len(word_counts) == 3
    assert word_counts[str(tmp_dir / "file0.txt")] == 2  # "hello world"
    assert word_counts[str(tmp_dir / "file1.txt")] == 2  # "python async"
    assert word_counts[str(tmp_dir / "file2.txt")] == 1  # "test"
