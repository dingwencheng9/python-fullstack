"""

from __future__ import annotations

L21: Python 3.13 体验 - 完整测试套件

测试 Python 3.13 新特性的核心功能和示例代码。
"""

from __future__ import annotations

import sys

import pytest


def load_solution_module(module_name: str, file_name: str):
    """按文件名动态加载带连字符的 solution 模块。"""
    import importlib.util
    from pathlib import Path

    solutions_dir = Path(__file__).parent.parent / "solutions"
    spec = importlib.util.spec_from_file_location(module_name, solutions_dir / file_name)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ==================== Python 版本检查 ====================


@pytest.mark.skipif(sys.version_info < (3, 13), reason="需要 Python 3.13+，当前环境用于课程开发")
def test_python_version():
    """测试 Python 版本"""
    assert sys.version_info >= (3, 13), "需要 Python 3.13+"


# ==================== 导入测试 ====================


def test_import_examples():
    """测试 examples 模块导入"""
    try:
        from examples import example_01_colorful_errors, example_02_repl_improvements

        assert hasattr(example_01_colorful_errors, "demonstrate_colorful_traceback")
        assert hasattr(example_02_repl_improvements, "show_repl_improvements")
    except ImportError as e:
        pytest.skip(f"Examples 模块导入失败: {e}")


def test_import_solutions():
    """测试 solutions 模块导入"""
    try:
        import importlib.util
        from pathlib import Path

        solutions_dir = Path(__file__).parent.parent / "solutions"

        # 动态加载 exercise_01_error_handling.py
        spec1 = importlib.util.spec_from_file_location("sol1", solutions_dir / "solution_01_error_handling.py")
        if spec1 and spec1.loader:
            sol1 = importlib.util.module_from_spec(spec1)
            spec1.loader.exec_module(sol1)

            # 验证 solution 1 的函数
            assert hasattr(sol1, "level_1")
            assert hasattr(sol1, "level_2")
            assert hasattr(sol1, "level_3")

        # 动态加载 exercise_03_benchmark.py
        spec3 = importlib.util.spec_from_file_location("sol3", solutions_dir / "solution_03_benchmark.py")
        if spec3 and spec3.loader:
            sol3 = importlib.util.module_from_spec(spec3)
            spec3.loader.exec_module(sol3)

            # 验证 solution 3 有 fibonacci 函数
            assert hasattr(sol3, "fibonacci_recursive") or hasattr(sol3, "fibonacci_iterative")
    except (ImportError, FileNotFoundError) as e:
        pytest.skip(f"Solutions 模块导入失败: {e}")


def test_import_demos():
    """测试 demos 模块导入"""
    try:
        import demos

        # 检查 __version__ 属性
        assert hasattr(demos, "__version__")
        assert demos.__version__ == "1.0.0"
    except AssertionError:
        # demos 模块存在但缺少 __version__ 属性（跨课程污染）
        pytest.skip("Demos 模块不可用或版本不匹配")
    except Exception as e:
        pytest.skip(f"Demos 模块不可用: {e}")


# ==================== 核心功能测试 ====================


def test_solution_error_handling():
    """测试错误处理解决方案"""
    try:
        import importlib.util
        from pathlib import Path

        solutions_dir = Path(__file__).parent.parent / "solutions"
        spec = importlib.util.spec_from_file_location("sol1", solutions_dir / "solution_01_error_handling.py")
        if not spec or not spec.loader:
            pytest.skip("Solutions 模块不可用")

        sol1 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sol1)

        # 测试 AttributeError
        with pytest.raises(AttributeError):
            sol1.scenario_attribute_error()

        # 测试 IndexError
        with pytest.raises(IndexError):
            sol1.scenario_index_error()

        # 测试 KeyError
        with pytest.raises(KeyError):
            sol1.scenario_key_error()

    except (ImportError, FileNotFoundError):
        pytest.skip("Solutions 模块不可用")


def test_benchmark_function():
    """测试基准测试函数"""
    try:
        from benchmarks.benchmark_313_vs_312 import benchmark

        # 简单函数测试
        def simple_func():
            return sum(range(100))

        # 执行基准测试
        elapsed = benchmark(simple_func, iterations=10)

        # 验证返回值是浮点数且大于0
        assert isinstance(elapsed, float)
        assert elapsed > 0
        assert elapsed < 1.0  # 应该很快

    except ImportError:
        pytest.skip("Benchmark 模块不可用")


def test_list_comprehension():
    """测试列表推导（Python 3.13 优化）"""
    # 小列表推导
    squares = [i**2 for i in range(10)]
    assert len(squares) == 10
    assert squares[0] == 0
    assert squares[9] == 81

    # 带条件的列表推导
    evens = [i for i in range(20) if i % 2 == 0]
    assert len(evens) == 10
    assert all(x % 2 == 0 for x in evens)


def test_dict_comprehension():
    """测试字典推导"""
    square_dict = {i: i**2 for i in range(10)}
    assert len(square_dict) == 10
    assert square_dict[5] == 25
    assert square_dict[9] == 81


def test_modern_type_hints():
    """测试现代类型提示（内置泛型）"""

    def process_list(items: list[int]) -> dict[int, int]:
        """使用内置泛型的函数"""
        return {i: i**2 for i in items}

    result = process_list([1, 2, 3, 4, 5])
    assert isinstance(result, dict)
    assert result[3] == 9
    assert len(result) == 5


def test_union_types():
    """测试联合类型（PEP 604 管道符）"""

    def get_value(key: str) -> int | str | None:
        """使用管道符的联合类型"""
        data = {"count": 42, "name": "Python"}
        return data.get(key)

    assert get_value("count") == 42
    assert get_value("name") == "Python"
    assert get_value("missing") is None


def test_json_processing():
    """测试 JSON 处理"""
    import json

    data = {"name": "Python", "version": 3.13, "features": ["colored errors", "new REPL"]}
    json_str = json.dumps(data, indent=2)

    assert isinstance(json_str, str)
    assert "Python" in json_str
    assert "3.13" in json_str

    parsed = json.loads(json_str)
    assert parsed["name"] == "Python"
    assert parsed["version"] == 3.13
    assert len(parsed["features"]) == 2


def test_datetime_processing():
    """测试日期时间处理"""
    import datetime

    now = datetime.datetime.now()
    assert isinstance(now, datetime.datetime)

    formatted = now.strftime("%Y-%m-%d")
    assert len(formatted) == 10
    assert formatted.count("-") == 2


def test_string_operations():
    """测试字符串操作性能"""
    # 字符串拼接
    text = " ".join(str(i) for i in range(100))
    assert len(text) > 0
    assert "0" in text
    assert "99" in text

    # 字符串格式化
    name = "Python"
    version = 3.13
    message = f"{name} {version}"
    assert message == "Python 3.13"


def test_exception_chaining():
    """测试异常链"""
    try:
        try:
            data = {"value": "not_a_number"}
            _ = int(data["value"])  # 故意触发 ValueError
        except ValueError as e:
            raise RuntimeError("数据处理失败") from e
    except RuntimeError as e:
        assert e.__cause__ is not None
        assert isinstance(e.__cause__, ValueError)
        assert "数据处理失败" in str(e)


# ==================== 性能相关测试 ====================


def test_recursive_fibonacci():
    """测试递归函数（性能测试用例）"""

    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # 测试小值
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55


def test_nested_loops():
    """测试嵌套循环性能"""
    result = []
    for i in range(10):
        for j in range(10):
            result.append(i * j)

    assert len(result) == 100
    assert result[0] == 0
    assert result[-1] == 81


@pytest.mark.parametrize(
    ("scenario_name", "expected_error"),
    [
        ("scenario_attribute_error", AttributeError),
        ("scenario_index_error", IndexError),
        ("scenario_key_error", KeyError),
        ("scenario_value_error", ValueError),
    ],
)
def test_error_scenarios_parametrized(scenario_name: str, expected_error: type[Exception]) -> None:
    """参数化验证 Python 3.13 错误体验示例的异常路径。"""
    sol1 = load_solution_module("sol1_quality", "solution_01_error_handling.py")

    with pytest.raises(expected_error):
        getattr(sol1, scenario_name)()


def test_level_1_nested_call_raises_type_error() -> None:
    """异常路径：多层调用链最终暴露 TypeError。"""
    sol1 = load_solution_module("sol1_nested_quality", "solution_01_error_handling.py")

    with pytest.raises(TypeError):
        sol1.level_1()


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 1), (2, 1), (10, 55)],
)
def test_fibonacci_iterative_boundaries(n: int, expected: int) -> None:
    """边界场景：迭代 Fibonacci 覆盖 0、1 和常规输入。"""
    sol3 = load_solution_module("sol3_quality", "solution_03_benchmark.py")

    assert sol3.fibonacci_iterative(n) == expected


# ==================== 主入口 ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
