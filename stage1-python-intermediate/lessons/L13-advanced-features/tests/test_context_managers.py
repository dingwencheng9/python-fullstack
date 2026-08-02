"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L12: 高级特性 - 上下文管理器测试
"""

import pytest


def test_file_manager_read(tmp_path):
    """测试文件管理器读取"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")

    with context_managers.FileManager(str(test_file), "r") as f:
        content = f.read()
        assert content == "hello world"


def test_file_manager_write(tmp_path):
    """测试文件管理器写入"""
    test_file = tmp_path / "test.txt"

    with context_managers.FileManager(str(test_file), "w") as f:
        f.write("test content")

    assert test_file.read_text() == "test content"


def test_transaction_commit():
    """测试事务提交"""
    with context_managers.Transaction() as tx:
        tx.operations.append("op1")
        tx.operations.append("op2")

    assert tx.committed is True
    assert len(tx.operations) == 2


def test_transaction_rollback():
    """测试事务回滚"""
    with pytest.raises(ValueError):
        with context_managers.Transaction() as tx:
            tx.operations.append("op1")
            raise ValueError("错误")

    assert len(tx.operations) == 0


def test_timer(capsys):
    """测试计时器"""
    import time

    with context_managers.Timer("测试操作") as t:
        time.sleep(0.01)

    assert t.elapsed > 0
    captured = capsys.readouterr()
    assert "测试操作" in captured.out
    assert "耗时" in captured.out


def test_managed_resource(capsys):
    """测试资源管理器"""
    with context_managers.managed_resource("test_resource"):
        pass

    captured = capsys.readouterr()
    assert "获取资源: test_resource" in captured.out
    assert "释放资源: test_resource" in captured.out


def test_transaction_context_success(capsys):
    """测试事务上下文成功"""
    ops = []

    with context_managers.transaction_context(ops) as operations:
        operations.append("task1")
        operations.append("task2")

    assert len(ops) == 2
    captured = capsys.readouterr()
    assert "提交 2 个操作" in captured.out


def test_transaction_context_failure(capsys):
    """测试事务上下文失败"""
    ops = []

    with pytest.raises(RuntimeError):
        with context_managers.transaction_context(ops) as operations:
            operations.append("task1")
            raise RuntimeError("失败")

    assert len(ops) == 0
    captured = capsys.readouterr()
    assert "事务回滚" in captured.out
