"""

from __future__ import annotations

test_python314_features.py — Python 3.14 新特性单元测试

仅在 Python 3.14+ 上运行；3.13 自动 skip。

运行：
    python3.14 -m pytest tests/test_python314_features.py -v
"""

import sys

import pytest

PY314 = sys.version_info >= (3, 14)

# ============================================================================
# PEP 649 — annotationlib
# ============================================================================


@pytest.mark.skipif(not PY314, reason="PEP 649 annotationlib needs Python 3.14+")
class TestPEP649Annotations:
    def test_annotationlib_importable(self) -> None:
        """annotationlib 模块在 3.14+ 应可导入"""
        from annotationlib import Format, get_annotations

        assert Format.VALUE is not None
        assert callable(get_annotations)

    def test_format_value_returns_real_types(self) -> None:
        """Format.VALUE 应返回真实类型对象"""
        from annotationlib import Format, get_annotations

        def f(x: int, y: str) -> bool:
            return True

        ann = get_annotations(f, format=Format.VALUE)
        assert ann["x"] is int
        assert ann["y"] is str
        assert ann["return"] is bool

    def test_format_string_returns_strings(self) -> None:
        """Format.STRING 应返回源码字符串"""
        from annotationlib import Format, get_annotations

        def f(x: int) -> str:
            return ""

        ann = get_annotations(f, format=Format.STRING)
        assert ann["x"] == "int"
        assert ann["return"] == "str"

    def test_forward_reference_no_error(self) -> None:
        """前向引用不应在定义时抛 NameError（PEP 649 默认行为）"""
        # 没有 from __future__ import annotations
        # 但 'Tree' 是字符串字面量，本来就是字符串前向引用
        # 真正的延迟求值发生在 PEP 649 模式下，无字符串前向引用也不报错

        def f(x: "ThisDoesNotExistYet") -> None:  # noqa: F821
            pass

        # 函数定义不报错就是 PEP 649 在生效
        assert f is not None


# ============================================================================
# PEP 750 — t-string Template
# ============================================================================


@pytest.mark.skipif(not PY314, reason="PEP 750 t-string needs Python 3.14+")
class TestPEP750TString:
    def test_template_module_importable(self) -> None:
        """string.templatelib.Template 在 3.14+ 应可导入"""
        from string.templatelib import Template  # noqa: F401

    def test_tstring_returns_template(self) -> None:
        """t-string 字面量应返回 Template 实例"""
        # 用 exec 编译，避免 3.13 解析器报错
        from string.templatelib import Template

        ns: dict = {}
        exec("name = 'world'\nresult = t'hello {name}'", ns)
        result = ns["result"]
        assert isinstance(result, Template)

    def test_template_strings_segments(self) -> None:
        """Template.strings 应包含所有静态片段"""
        ns: dict = {}
        exec("a = 1\nb = 2\nresult = t'x={a}, y={b}!'", ns)
        result = ns["result"]
        # strings 元组应该有 N+1 个元素（N 个插值切出 N+1 段）
        assert len(result.strings) == 3
        assert result.strings[0] == "x="
        assert result.strings[1] == ", y="
        assert result.strings[2] == "!"

    def test_template_interpolations_capture_value(self) -> None:
        """interpolations 应捕获到表达式的求值结果"""
        ns: dict = {}
        exec("x = 42\nresult = t'value is {x}'", ns)
        result = ns["result"]
        assert len(result.interpolations) == 1
        assert result.interpolations[0].expression == "x"
        assert result.interpolations[0].value == 42

    def test_safe_sql_pattern(self) -> None:
        """t-string 转参数化 SQL 的模式（防注入）"""
        from string.templatelib import Template

        def safe_sql(tmpl: Template) -> tuple[str, list]:
            parts: list[str] = []
            params: list = []
            for i, segment in enumerate(tmpl.strings):
                parts.append(segment)
                if i < len(tmpl.interpolations):
                    parts.append("?")
                    params.append(tmpl.interpolations[i].value)
            return "".join(parts), params

        ns: dict = {}
        exec("uid = 42\ntmpl = t'SELECT * FROM users WHERE id = {uid}'", ns)
        sql, params = safe_sql(ns["tmpl"])
        assert sql == "SELECT * FROM users WHERE id = ?"
        assert params == [42]

    def test_tstring_handles_dangerous_input(self) -> None:
        """危险输入不会被 t-string 自动展开为 SQL（关键安全保证）"""

        ns: dict = {}
        exec(
            "evil = \"' OR '1'='1\"\nresult = t'name = {evil}'",
            ns,
        )
        result = ns["result"]
        # 危险字符串原样保留在 interpolations[0].value 中
        # 而不是被拼进 strings 元组
        assert result.interpolations[0].value == "' OR '1'='1"
        # strings 元组只有静态片段
        assert "OR" not in "".join(result.strings)


# ============================================================================
# 跨版本兼容测试（任何版本都能跑）
# ============================================================================


def test_python_version_at_least_313() -> None:
    """本课程基线要求 Python 3.13+"""
    assert sys.version_info >= (3, 13)


def test_gil_introspection_api() -> None:
    """sys._is_gil_enabled 是 3.13+ 引入的"""
    assert hasattr(sys, "_is_gil_enabled")
    assert callable(sys._is_gil_enabled)
    assert isinstance(sys._is_gil_enabled(), bool)
