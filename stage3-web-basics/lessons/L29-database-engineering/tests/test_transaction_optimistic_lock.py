"""L29 Exercise 2: 事务管理与乐观锁 - 测试套件。

测试事务上下文管理器和乐观锁的基础结构。
"""

from __future__ import annotations


class TestExerciseStructure:
    """测试 exercise_02 模块结构和关键元素。"""

    def test_exercise_file_exists(self) -> None:
        """测试 exercise_02 文件存在。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        assert exercise_file.exists(), f"exercise_02 文件应存在: {exercise_file}"

    def test_exercise_file_not_empty(self) -> None:
        """测试 exercise_02 文件非空（验证课程内容存在）。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        assert len(content) > 1000, f"exercise_02 内容过少（{len(content)} 字符），应为完整练习题"

    def test_account_model_in_source(self) -> None:
        """测试 Account 模型在源代码中定义。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        assert "class Account" in content, "Account 类应在 exercise_02 中定义"
        assert "Mapped[" in content, "Account 应使用 SQLAlchemy Mapped 类型注解"

    def test_version_field_for_optimistic_lock(self) -> None:
        """测试 Account 模型包含 version 字段（乐观锁核心）。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        # 检查 version 字段定义
        assert "version" in content, "Account 应包含 version 字段（乐观锁）"

    def test_transaction_scope_function(self) -> None:
        """测试 transaction_scope 上下文管理器定义。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        assert "transaction_scope" in content, "transaction_scope 函数应在 exercise_02 中定义"
        assert "asynccontextmanager" in content, "应使用 @asynccontextmanager 装饰器"

    def test_optimistic_lock_transfer_function(self) -> None:
        """测试乐观锁转账函数存在。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        assert "transfer_with_optimistic_lock" in content, "transfer_with_optimistic_lock 函数应存在"
        assert "from_account_id" in content, "应接受 from_account_id 参数"
        assert "to_account_id" in content, "应接受 to_account_id 参数"
        assert "amount" in content, "应接受 amount 参数"

    def test_exercise_has_todos(self) -> None:
        """测试练习题包含 TODO 标记（学员需完成的部分）。"""
        from pathlib import Path

        exercise_file = Path(__file__).resolve().parent.parent / "exercises" / "exercise_02_transaction_optimistic_lock.py"
        content = exercise_file.read_text()
        assert "# TODO" in content or "TODO" in content, "练习题应包含 TODO 标记"

    def test_solution_02_file_exists(self) -> None:
        """测试 solution_02 参考答案文件存在。"""
        from pathlib import Path

        solution_file = Path(__file__).resolve().parent.parent / "solutions" / "02_transaction_solution.py"
        assert solution_file.exists(), f"solution_02 文件应存在: {solution_file}"
