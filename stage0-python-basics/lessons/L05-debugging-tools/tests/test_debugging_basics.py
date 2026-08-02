"""L05 测试: 调试工具基础

测试对 pdb、breakpoint() 和 traceback 模块的理解。
"""

import pytest
import traceback as tb_module

# 导入练习模块
import solutions  # type: ignore


class TestPdbBasics:
    """pdb 基础测试"""

    def test_calculate_average_normal(self):
        """测试正常情况下的平均值计算"""
        result = solutions.calculate_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calculate_average_empty_raises(self):
        """测试空列表应该抛出异常"""
        with pytest.raises(ValueError, match="列表不能为空"):
            solutions.calculate_average([])

    def test_find_middle_element_normal(self):
        """测试正常情况下的中间元素查找"""
        result = solutions.find_middle_element([1, 2, 3, 4, 5])
        assert result == 3  # 中间是第3个元素

    def test_find_middle_element_even_length(self):
        """测试偶数长度列表返回靠左中间元素"""
        result = solutions.find_middle_element([1, 2, 3, 4])
        assert result == 3  # 索引 2，值为 3

    def test_find_middle_element_empty_raises(self):
        """测试空列表应该抛出异常"""
        with pytest.raises(ValueError, match="列表不能为空"):
            solutions.find_middle_element([])


class TestTracebackModule:
    """traceback 模块测试"""

    def test_traceback_print_exc(self):
        """测试 traceback.print_exc 不会抛出异常"""
        try:
            1 / 0
        except ZeroDivisionError:
            # 这不应该抛出异常，直接调用 print_exc()
            tb_module.print_exc()

    def test_traceback_format_exc(self):
        """测试 traceback.format_exc 返回字符串"""
        try:
            int("not_a_number")
        except ValueError:
            result = tb_module.format_exc()
            assert isinstance(result, str)
            assert "ValueError" in result

    def test_exception_in_function(self):
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


class TestTracebackFormat:
    """traceback 格式化测试"""

    def test_traceback_format_string(self):
        """测试 traceback.format_exc 返回包含异常的字符串"""
        try:
            raise ValueError("test error")
        except ValueError:
            tb = tb_module.format_exc()
            assert isinstance(tb, str)
            assert "ValueError" in tb
            assert "test error" in tb


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
