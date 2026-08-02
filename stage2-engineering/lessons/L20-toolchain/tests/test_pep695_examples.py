"""
测试 PEP 695 真实代码示例

验证 tests/04_pep695_real_examples.py 的功能（展平后）
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 动态导入模块（展平后直接放在 tests/ 目录）
module_path = Path(__file__).parent / "04_pep695_real_examples.py"


def test_module_requires_python312() -> None:
    """测试模块需要 Python 3.12+"""
    # PEP 695 需要 Python 3.12+
    assert sys.version_info >= (3, 12), "PEP 695 requires Python 3.12+"


def test_generic_functions() -> None:
    """测试泛型函数"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 get_first
    numbers = [1, 2, 3, 4, 5]
    assert module.get_first(numbers) == 1

    empty_list: list[int] = []
    assert module.get_first(empty_list) is None

    # 测试 get_last
    assert module.get_last(numbers) == 5
    assert module.get_last(empty_list) is None

    # 测试 reverse
    reversed_list = module.reverse(numbers)
    assert reversed_list == [5, 4, 3, 2, 1]
    assert numbers == [1, 2, 3, 4, 5]  # 原列表未修改


def test_constrained_generics() -> None:
    """测试类型约束的泛型"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 add
    assert module.add(10, 20) == 30
    assert module.add(1.5, 2.5) == 4.0

    # 测试 multiply
    assert module.multiply([2, 3, 4]) == 24
    assert module.multiply([1.5, 2.0]) == 3.0


def test_generic_stack() -> None:
    """测试泛型栈"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 Stack[int]
    stack = module.Stack[int]()
    assert stack.is_empty()
    assert stack.size() == 0

    stack.push(10)
    stack.push(20)
    stack.push(30)

    assert stack.size() == 3
    assert not stack.is_empty()
    assert stack.peek() == 30

    assert stack.pop() == 30
    assert stack.size() == 2
    assert stack.peek() == 20


def test_thread_safe_stack() -> None:
    """测试线程安全栈"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 ThreadSafeStack[str]
    stack = module.ThreadSafeStack[str]()
    stack.push("Python")
    stack.push("3.13")

    assert stack.size() == 2
    assert stack.pop() == "3.13"
    assert stack.size() == 1


def test_multi_parameter_generics() -> None:
    """测试多类型参数泛型"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试字典操作
    user_ages = {"Alice": 30, "Bob": 25, "Charlie": 35}

    keys = module.map_keys(user_ages)
    assert set(keys) == {"Alice", "Bob", "Charlie"}

    values = module.map_values(user_ages)
    assert set(values) == {30, 25, 35}

    inverted = module.invert_dict(user_ages)
    assert inverted[30] == "Alice"

    # 测试 Pair
    pair = module.Pair("name", "Alice")
    assert pair.get_key() == "name"
    assert pair.get_value() == "Alice"

    swapped = pair.swap()
    assert swapped.get_key() == "Alice"
    assert swapped.get_value() == "name"


def test_type_aliases() -> None:
    """测试类型别名"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 Point
    point = module.create_point(10, 20)
    assert point == (10, 20)

    # 测试 transform_point
    transformed = module.transform_point(point, lambda x: x * 2)
    assert transformed == (20, 40)


def test_generic_repository() -> None:
    """测试泛型仓储"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 Repository[dict]
    repo = module.Repository[dict[str, str | int]]()

    user1_id = repo.add({"name": "Alice", "age": 30})
    user2_id = repo.add({"name": "Bob", "age": 25})

    assert user1_id == 1
    assert user2_id == 2

    user1 = repo.get(user1_id)
    assert user1 is not None
    assert user1["name"] == "Alice"

    assert len(repo.find_all()) == 2

    # 测试过滤
    young_users = repo.filter(lambda u: u["age"] < 30)  # type: ignore
    assert len(young_users) == 1
    assert young_users[0]["name"] == "Bob"

    # 测试更新
    assert repo.update(user1_id, {"name": "Alice Smith", "age": 31})
    updated_user = repo.get(user1_id)
    assert updated_user is not None
    assert updated_user["age"] == 31

    # 测试删除
    assert repo.delete(user2_id)
    assert repo.get(user2_id) is None


def test_generic_cache() -> None:
    """测试泛型缓存"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 Cache[str, int]
    cache = module.Cache[str, int](max_size=3)

    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)

    assert cache.size() == 3
    assert cache.get("a") == 1
    assert cache.has("b")

    # 测试 FIFO 驱逐
    cache.set("d", 4)
    assert cache.size() == 3
    assert not cache.has("a")  # 'a' 被驱逐

    # 测试清空
    cache.clear()
    assert cache.size() == 0


def test_generic_factory_functions() -> None:
    """测试泛型工厂函数"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 测试 create_list
    result = module.create_list((1, 2, 3))
    assert result == [1, 2, 3]

    # 测试 create_dict
    result_dict = module.create_dict([("a", 1), ("b", 2)])
    assert result_dict == {"a": 1, "b": 2}

    # 测试 map_list
    numbers = [1, 2, 3, 4, 5]
    doubled = module.map_list(numbers, lambda x: x * 2)
    assert doubled == [2, 4, 6, 8, 10]

    strings = module.map_list(numbers, str)
    assert strings == ["1", "2", "3", "4", "5"]

    # 测试 filter_list
    evens = module.filter_list(numbers, lambda x: x % 2 == 0)
    assert evens == [2, 4]


def test_demonstrate_function(capsys: pytest.CaptureFixture[str]) -> None:
    """测试演示函数"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.demonstrate_pep695_syntax()
    captured = capsys.readouterr()

    # 验证输出包含关键内容
    assert "PEP 695" in captured.out
    assert "函数泛型" in captured.out
    assert "类泛型" in captured.out
    assert "类型别名" in captured.out
    assert "泛型仓储" in captured.out


def test_thread_safety_notes(capsys: pytest.CaptureFixture[str]) -> None:
    """测试线程安全说明"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("pep695_examples", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_thread_safety_notes()
    captured = capsys.readouterr()

    # 验证输出包含线程安全说明
    assert "Free-threading" in captured.out
    assert "线程安全" in captured.out
    assert "纯函数" in captured.out
    assert "可变容器" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
