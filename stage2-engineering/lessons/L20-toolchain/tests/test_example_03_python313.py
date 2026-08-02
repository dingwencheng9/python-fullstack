"""测试 examples/example_03_python313_features.py - Python 3.13 新特性演示

from __future__ import annotations

测试覆盖:
- PEP 695 泛型函数和类
- 现代化类型注解
- 线程安全注释验证
- 功能正确性测试
"""

# 导入被测试模块
# 动态导入 example_03_python313_features.py
import importlib.util
import sys
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "python313_features",
    Path(__file__).parent.parent / "examples" / "example_03_python313_features.py",
)
features = importlib.util.module_from_spec(spec)
spec.loader.exec_module(features)


class TestPEP695Generics:
    """测试 PEP 695 泛型语法"""

    def test_first_with_integers(self):
        """测试泛型函数 first() - 整数列表"""
        numbers = [1, 2, 3, 4, 5]
        result = features.first(numbers)
        assert result == 1

    def test_first_with_strings(self):
        """测试泛型函数 first() - 字符串列表"""
        words = ["hello", "world", "python"]
        result = features.first(words)
        assert result == "hello"

    def test_first_with_empty_list(self):
        """测试泛型函数 first() - 空列表"""
        empty: list[int] = []
        result = features.first(empty)
        assert result is None

    def test_first_type_inference(self):
        """测试泛型函数的类型推断"""
        # 测试不同类型的列表
        int_list = [1, 2, 3]
        str_list = ["a", "b", "c"]
        float_list = [1.5, 2.5, 3.5]

        assert features.first(int_list) == 1
        assert features.first(str_list) == "a"
        assert features.first(float_list) == 1.5

    def test_safe_get_valid_index(self):
        """测试 safe_get() - 有效索引"""
        items = [10, 20, 30, 40, 50]
        assert features.safe_get(items, 0) == 10
        assert features.safe_get(items, 2) == 30
        assert features.safe_get(items, 4) == 50

    def test_safe_get_invalid_index(self):
        """测试 safe_get() - 无效索引"""
        items = [10, 20, 30]
        result = features.safe_get(items, 10)
        assert result is None

    def test_safe_get_with_default(self):
        """测试 safe_get() - 自定义默认值"""
        items = [10, 20, 30]
        result = features.safe_get(items, 100, default=999)
        assert result == 999

    def test_safe_get_negative_index(self):
        """测试 safe_get() - 负索引"""
        items = [10, 20, 30, 40, 50]
        result = features.safe_get(items, -1)
        assert result == 50

    def test_safe_get_with_tuple(self):
        """测试 safe_get() - 元组输入"""
        items = (100, 200, 300)
        assert features.safe_get(items, 1) == 200

    def test_safe_get_with_string(self):
        """测试 safe_get() - 字符串输入（Sequence）"""
        text = "hello"
        assert features.safe_get(text, 0) == "h"
        assert features.safe_get(text, 4) == "o"


class TestGenericContainer:
    """测试泛型容器类"""

    def test_container_integers(self):
        """测试整数容器"""
        container: features.Container[int] = features.Container(1, 2, 3)
        assert len(container) == 3
        assert container.get_all() == [1, 2, 3]

    def test_container_strings(self):
        """测试字符串容器"""
        container: features.Container[str] = features.Container("a", "b", "c")
        assert len(container) == 3
        assert container.get_all() == ["a", "b", "c"]

    def test_container_add_item(self):
        """测试添加元素"""
        container: features.Container[int] = features.Container(1, 2, 3)
        container.add(4)
        assert len(container) == 4
        assert container.get_all() == [1, 2, 3, 4]

    def test_container_empty_initialization(self):
        """测试空容器初始化"""
        container: features.Container[str] = features.Container()
        assert len(container) == 0
        assert container.get_all() == []

    def test_container_get_all_returns_copy(self):
        """测试 get_all() 返回副本（线程安全）"""
        container: features.Container[int] = features.Container(1, 2, 3)
        items1 = container.get_all()
        items2 = container.get_all()

        # 修改返回的列表不应影响容器
        items1.append(999)
        assert container.get_all() == [1, 2, 3]
        assert items2 == [1, 2, 3]

    def test_container_mixed_types_fail(self):
        """测试类型安全（运行时不强制，但类型检查会报错）"""
        # 注：Python 运行时不强制泛型类型，但这应该被静态类型检查器捕获
        container: features.Container[int] = features.Container(1, 2, 3)
        # 这在运行时不会报错，但 mypy 会警告
        container.add("string")  # type: ignore
        assert len(container) == 4


class TestProcessBatch:
    """测试批处理函数"""

    def test_process_batch_no_transform(self):
        """测试无转换函数"""
        items = [1, 2, 3, 4, 5]
        result = features.process_batch(items)
        assert result == [1, 2, 3, 4, 5]
        # 确保返回的是副本
        assert result is not items

    def test_process_batch_with_transform(self):
        """测试带转换函数"""
        items = [1, 2, 3, 4, 5]
        result = features.process_batch(items, transform=lambda x: x * 2)
        assert result == [2, 4, 6, 8, 10]

    def test_process_batch_string_transform(self):
        """测试字符串转换"""
        words = ["hello", "world", "python"]
        result = features.process_batch(words, transform=lambda s: s.upper())
        assert result == ["HELLO", "WORLD", "PYTHON"]

    def test_process_batch_preserves_original(self):
        """测试原列表不被修改（线程安全）"""
        original = [1, 2, 3]
        result = features.process_batch(original, transform=lambda x: x * 10)
        assert original == [1, 2, 3]  # 原列表未修改
        assert result == [10, 20, 30]


class TestModernSyntax:
    """测试现代化语法示例"""

    def test_demonstrate_modern_syntax(self):
        """测试现代化语法演示函数"""
        config = features.demonstrate_modern_syntax()

        assert isinstance(config, dict)
        assert "name" in config
        assert "version" in config
        assert "features" in config

        assert config["name"] == "modern-python"
        assert config["version"] == "3.13"
        assert config["features"] == 10

    def test_demonstrate_modern_syntax_types(self):
        """测试返回值类型正确"""
        config = features.demonstrate_modern_syntax()

        # 验证类型
        assert isinstance(config["name"], str)
        assert isinstance(config["version"], str)
        assert isinstance(config["features"], int)


class TestDemoFunctions:
    """测试演示函数（不抛出异常即为通过）"""

    def test_demo_repl_runs_without_error(self, capsys):
        """测试 REPL 演示运行无错误"""
        features.demo_repl()
        captured = capsys.readouterr()

        # 验证输出包含关键信息
        assert "Python 3.13 REPL 改进演示" in captured.out
        assert "彩色语法高亮" in captured.out
        assert "多行编辑支持" in captured.out

    def test_demo_free_threading_runs_without_error(self, capsys):
        """测试 Free-threading 演示运行无错误"""
        features.demo_free_threading()
        captured = capsys.readouterr()

        # 验证输出包含关键信息
        assert "Free-threading" in captured.out
        assert "GIL" in captured.out
        assert "线程安全" in captured.out

    def test_main_runs_without_error(self, capsys):
        """测试主函数运行无错误"""
        features.main()
        captured = capsys.readouterr()

        # 验证输出包含所有关键部分
        assert "Python 3.13 新特性完整演示" in captured.out
        assert "PEP 695 泛型语法" in captured.out
        assert "改进的 REPL" in captured.out
        assert "Free-threading" in captured.out


class TestPythonVersionCheck:
    """测试 Python 版本检测"""

    def test_version_info_accessible(self):
        """测试可以访问 sys.version_info"""
        version = sys.version_info
        assert version.major >= 3
        assert version.minor >= 12


class TestTypeAnnotations:
    """测试类型注解正确性（静态检查）"""

    def test_no_typing_module_imports(self):
        """验证未使用 typing 模块的老旧类型"""
        source_file = Path(__file__).parent.parent / "examples" / "example_03_python313_features.py"
        source_code = source_file.read_text()

        # 验证未导入老旧类型
        assert "from typing import List" not in source_code
        assert "from typing import Dict" not in source_code
        assert "from typing import Optional" not in source_code
        assert "from typing import Union" not in source_code
        assert "from typing import TypeVar" not in source_code

    def test_uses_builtin_generics(self):
        """验证使用了内置泛型"""
        source_file = Path(__file__).parent.parent / "examples" / "example_03_python313_features.py"
        source_code = source_file.read_text()

        # 验证使用了内置泛型语法
        assert "list[" in source_code
        assert "dict[" in source_code
        assert " | None" in source_code or "|None" in source_code

    def test_uses_pep695_syntax(self):
        """验证使用了 PEP 695 语法"""
        source_file = Path(__file__).parent.parent / "examples" / "example_03_python313_features.py"
        source_code = source_file.read_text()

        # 验证使用了 PEP 695 泛型语法
        assert "def first[T]" in source_code
        assert "class Container[T]" in source_code


# 集成测试
class TestIntegration:
    """集成测试"""

    def test_complete_workflow(self):
        """测试完整工作流程"""
        # 1. 泛型函数
        numbers = [1, 2, 3, 4, 5]
        first_num = features.first(numbers)
        assert first_num == 1

        # 2. 泛型类
        container: features.Container[int] = features.Container(10, 20, 30)
        container.add(40)
        assert len(container) == 4

        # 3. 批处理
        doubled = features.process_batch(numbers, transform=lambda x: x * 2)
        assert doubled == [2, 4, 6, 8, 10]

        # 4. 现代化语法
        config = features.demonstrate_modern_syntax()
        assert config["name"] == "modern-python"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
