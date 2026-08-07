"""L05 调试工具与环境 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
调试课程的目标是让学员使用 pdb/breakpoint/traceback 调试并修复代码。
"""

import importlib.util
from pathlib import Path

import pytest
import traceback as tb_module


EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pdb_module():
    """加载 exercises/01_pdb_practice.py"""
    return _load_exercise_module("_test_pdb", EXERCISES_DIR / "01_pdb_practice.py")


@pytest.fixture(scope="module")
def traceback_module():
    """加载 exercises/02_traceback_practice.py"""
    return _load_exercise_module("_test_traceback", EXERCISES_DIR / "02_traceback_practice.py")


# ============================================================
# 01_pdb_practice.py 测试
# ============================================================


class TestPdbPractice:
    """测试 pdb 练习：学员应该修复 calculate_average 和 find_middle_element"""

    def test_calculate_average_normal(self, pdb_module) -> None:
        """测试正常情况下的平均值计算"""
        func = getattr(pdb_module, "calculate_average", None)
        assert func is not None, "请定义 calculate_average 函数"

        result = func([1, 2, 3, 4, 5])
        assert result == 3.0, f"calculate_average([1,2,3,4,5]) 应返回 3.0，实际得到 {result}"

    def test_calculate_average_single_element(self, pdb_module) -> None:
        """测试单元素列表"""
        func = getattr(pdb_module, "calculate_average", None)
        assert func is not None, "请定义 calculate_average 函数"

        assert func([10]) == 10.0

    def test_calculate_average_decimal(self, pdb_module) -> None:
        """测试小数结果"""
        func = getattr(pdb_module, "calculate_average", None)
        assert func is not None, "请定义 calculate_average 函数"

        result = func([1, 2, 3])
        assert result == 2.0, f"calculate_average([1,2,3]) 应返回 2.0，实际得到 {result}"

    def test_calculate_average_empty_raises(self, pdb_module) -> None:
        """测试空列表应该抛出异常或返回 None"""
        func = getattr(pdb_module, "calculate_average", None)
        assert func is not None, "请定义 calculate_average 函数"

        # 学员可能选择抛出异常或返回 None/特殊值
        try:
            result = func([])
            # 如果没抛异常，应该返回合理的特殊值
            assert result is None, "空列表应返回 None 或抛出异常"
        except (ValueError, ZeroDivisionError) as e:
            # 这是正确的实现方式
            assert "空" in str(e) or "zero" in str(e).lower()

    def test_find_middle_element_normal(self, pdb_module) -> None:
        """测试正常情况下的中间元素查找"""
        func = getattr(pdb_module, "find_middle_element", None)
        assert func is not None, "请定义 find_middle_element 函数"

        result = func([1, 2, 3, 4, 5])
        assert result == 3, f"find_middle_element([1,2,3,4,5]) 应返回 3，实际得到 {result}"

    def test_find_middle_element_even_length(self, pdb_module) -> None:
        """测试偶数长度列表（选择靠左或靠右都可以）"""
        func = getattr(pdb_module, "find_middle_element", None)
        assert func is not None, "请定义 find_middle_element 函数"

        # 偶数长度时，下取整得到索引 1，值为 2
        result = func([1, 2, 3, 4])
        assert result in [2, 3], f"偶数长度列表应返回中间偏左(2)或偏右(3)的元素，实际得到 {result}"

    def test_find_middle_element_empty_raises(self, pdb_module) -> None:
        """测试空列表应该抛出异常"""
        func = getattr(pdb_module, "find_middle_element", None)
        assert func is not None, "请定义 find_middle_element 函数"

        with pytest.raises((ValueError, IndexError)):
            func([])


# ============================================================
# 02_traceback_practice.py 测试
# ============================================================


class TestTracebackPractice:
    """测试 traceback 练习"""

    def test_save_error_log(self, traceback_module) -> None:
        """测试错误日志保存函数"""
        func = getattr(traceback_module, "save_error_log", None)
        assert func is not None, "请定义 save_error_log 函数"

        # 函数应该存在且可调用
        # 实际保存逻辑由学员实现
        # 如果函数需要路径参数，让学员自己修改
        # 这里只验证函数可调用
        assert callable(func)

    def test_analyze_error_exists(self, traceback_module) -> None:
        """测试 analyze_error 函数存在"""
        func = getattr(traceback_module, "analyze_error", None)
        assert func is not None, "请定义 analyze_error 函数"
        assert callable(func)

    def test_process_user_data_valid(self, traceback_module) -> None:
        """测试正常数据处理"""
        func = getattr(traceback_module, "process_user_data", None)
        assert func is not None, "请定义 process_user_data 函数"

        # 有效数据不应抛异常
        data = {"name": "Alice", "email": "alice@example.com"}
        try:
            func(data)
        except Exception as e:
            pytest.fail(f"有效数据不应抛出异常，但抛出了: {e}")

    def test_process_user_data_missing_field(self, traceback_module) -> None:
        """测试缺失字段应抛异常"""
        func = getattr(traceback_module, "process_user_data", None)
        assert func is not None, "请定义 process_user_data 函数"

        # 缺少 email 字段应该抛出异常
        incomplete_data = {"name": "Bob"}
        with pytest.raises((ValueError, KeyError), match="email"):
            func(incomplete_data)


# ============================================================
# 调试工具概念测试（不依赖学员实现）
# ============================================================


class TestTracebackModuleConcepts:
    """测试学员对 traceback 模块的理解"""

    def test_traceback_print_exc_no_raise(self) -> None:
        """测试 traceback.print_exc 不会抛出异常"""
        try:
            1 / 0
        except ZeroDivisionError:
            # 这不应该抛出异常
            tb_module.print_exc()

    def test_traceback_format_exc_returns_string(self) -> None:
        """测试 traceback.format_exc 返回字符串"""
        try:
            int("not_a_number")
        except ValueError:
            result = tb_module.format_exc()
            assert isinstance(result, str)
            assert "ValueError" in result

    def test_traceback_format_string_contains_error(self) -> None:
        """测试 traceback.format_exc 返回包含错误的字符串"""
        try:
            raise ValueError("test error")
        except ValueError:
            tb = tb_module.format_exc()
            assert isinstance(tb, str)
            assert "ValueError" in tb
            assert "test error" in tb

    def test_exception_in_function_captured(self) -> None:
        """测试函数中的异常能被正确捕获"""
        def inner_function() -> None:
            raise RuntimeError("inner error")

        def outer_function() -> str | None:
            try:
                inner_function()
            except RuntimeError as e:
                return str(e)
            return None

        result = outer_function()
        assert result == "inner error"
