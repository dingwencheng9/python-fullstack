"""

使用 @singledispatch 实现函数重载（单分派泛函数）。

本文件演示：
- @singledispatch 基本用法
- register() 注册特定类型的实现
- type annotation 风格 vs decorator 风格
- 在类中使用 singledispatch

作者: Python 3.13 全栈课程
日期: 2026-07-13
Python版本: 3.8+
"""

from __future__ import annotations

from functools import singledispatch, singledispatchmethod
from collections.abc import Sequence
from typing import Any


def demo_basic_singledispatch() -> None:
    """演示 @singledispatch 基本用法"""
    print("=" * 50)
    print("1. @singledispatch 基本用法")
    print("=" * 50)

    @singledispatch
    def process(data: Any) -> str:
        """默认实现（处理未知类型）"""
        return f"不支持的类型: {type(data).__name__}"

    # 注册 int 的实现
    @process.register(int)
    def _(data: int) -> str:
        return f"整数: {data} (2倍={data * 2})"

    # 注册 str 的实现
    @process.register(str)
    def _(data: str) -> str:
        return f"字符串: '{data}' (大写={data.upper()})"

    # 注册 list 的实现
    @process.register(list)
    def _(data: list) -> str:
        return f"列表: {len(data)} 个元素, 内容={data}"

    print(process(42))  # 整数: 42 (2倍=84)
    print(process("hello"))  # 字符串: 'hello' (大写=HELLO)
    print(process([1, 2, 3]))  # 列表: 3 个元素, 内容=[1, 2, 3]
    print(process(3.14))  # 不支持的类型: float
    print()


def demo_register_styles() -> None:
    """演示两种 register 风格"""
    print("=" * 50)
    print("2. register 两种风格")
    print("=" * 50)

    # 风格 1: 函数装饰器风格（推荐）
    @singledispatch
    def convert1(data: Any) -> str:
        return str(data)

    @convert1.register(int)
    def _(data: int) -> str:
        return f"int: {data}"

    @convert1.register(float)
    def _(data: float) -> str:
        return f"float: {data:.2f}"

    # 风格 2: lambda 函数风格
    @singledispatch
    def convert2(data: Any) -> str:
        return str(data)

    convert2.register(int, lambda x: f"int: {x}")
    convert2.register(float, lambda x: f"float: {x:.2f}")

    print("装饰器风格:")
    print(f"  convert1(10): {convert1(10)}")
    print(f"  convert1(3.14): {convert1(3.14)}")

    print("lambda 风格:")
    print(f"  convert2(10): {convert2(10)}")
    print(f"  convert2(3.14): {convert2(3.14)}")
    print()


def demo_union_types() -> None:
    """演示处理多种相关类型"""
    print("=" * 50)
    print("3. 使用 register 处理多种相关类型")
    print("=" * 50)

    @singledispatch
    def describe(data: Any) -> str:
        return f"类型 '{type(data).__name__}': {data}"

    # bool 是 int 的子类，所以 bool 会匹配 int
    @describe.register(int)
    def _(data: int) -> str:
        kind = "偶数" if data % 2 == 0 else "奇数"
        return f"整数 {data} 是 {kind}"

    # 注册多个类型：使用 lambda 风格
    describe.register(str, lambda s: f"字符串: 长度={len(s)}")
    describe.register(bytes, lambda b: f"字节: 长度={len(b)}")

    print(describe(10))  # 整数 10 是 偶数
    print(describe(True))  # 整数 True 是 偶数（bool 是 int 子类）
    print(describe("hello"))  # 字符串: 长度=5
    print(describe(b"world"))  # 字节: 长度=5
    print()


def demo_sequence_type() -> None:
    """演示使用抽象基类处理序列类型"""
    print("=" * 50)
    print("4. 使用 Sequence 抽象基类")
    print("=" * 50)

    @singledispatch
    def summarize(data: Any) -> str:
        return f"不支持: {type(data).__name__}"

    # 使用 Sequence 处理 list, tuple, str 等序列类型
    @summarize.register(Sequence)
    def _(data: Sequence) -> str:
        if not data:
            return "空序列"
        return f"序列: {type(data).__name__}, 长度={len(data)}, 首元素={data[0]!r}"

    print(summarize([1, 2, 3]))  # 序列: list, 长度=3, 首元素=1
    print(summarize((4, 5, 6)))  # 序列: tuple, 长度=3, 首元素=4
    print(summarize("Python"))  # 序列: str, 长度=6, 首元素='P'
    print(summarize([]))  # 空序列
    print()


def demo_singledispatchmethod() -> None:
    """演示在类中使用 singledispatch"""
    print("=" * 50)
    print("5. 类中的 singledispatch")
    print("=" * 50)

    class Serializer:
        """序列化器"""

        @singledispatchmethod
        def serialize(self, data: Any) -> str:
            """默认序列化"""
            return str(data)

        @serialize.register
        def _str(self, data: str) -> str:
            return f'"{data}"'

        @serialize.register
        def _int(self, data: int) -> str:
            return f"{data} (int)"

        @serialize.register
        def _list(self, data: list) -> str:
            return f"[{', '.join(self.serialize(item) for item in data)}]"

        @serialize.register(dict)
        def _dict(self, data: dict) -> str:
            pairs = [f"{k!r}: {self.serialize(v)}" for k, v in data.items()]
            return "{" + ", ".join(pairs) + "}"

    s = Serializer()
    print(f"字符串: {s.serialize('hello')}")
    print(f"整数: {s.serialize(42)}")
    print(f"列表: {s.serialize([1, 'two', 3])}")
    print(f"字典: {s.serialize({'a': 1, 'b': 'two'})}")
    print()


def demo_practical_example() -> None:
    """演示实际的序列化场景"""
    print("=" * 50)
    print("6. 实际场景：多格式序列化")
    print("=" * 50)

    from dataclasses import dataclass
    from datetime import datetime

    @dataclass
    class User:
        name: str
        age: int

    @singledispatch
    def to_json(data: Any) -> str:
        """默认：将对象转为 JSON 字符串"""
        import json

        return json.dumps(str(data))

    # 使用 lambda 风格注册，避免 get_type_hints 问题
    to_json.register(str, lambda s: f'"{s}"')
    to_json.register(int, lambda x: str(x))
    to_json.register(float, lambda x: str(x))
    to_json.register(bool, lambda b: "true" if b else "false")

    @to_json.register(list)
    def _list(data: list) -> str:
        items = ", ".join(to_json(item) for item in data)
        return f"[{items}]"

    @to_json.register(dict)
    def _dict(data: dict) -> str:
        pairs = [f"{to_json(k)}: {to_json(v)}" for k, v in data.items()]
        return "{" + ", ".join(pairs) + "}"

    @to_json.register(datetime)
    def _datetime(data: datetime) -> str:
        return f'"{data.isoformat()}"'

    user = User("Alice", 30)
    data = {
        "user": user,
        "active": True,
        "created_at": datetime.now(),
        "roles": ["admin", "editor"],
    }

    print("对象转 JSON:")
    print(to_json(data))
    print()


def main() -> None:
    """主函数"""
    print(">>> @singledispatch 演示\n")

    demo_basic_singledispatch()
    demo_register_styles()
    demo_union_types()
    demo_sequence_type()
    demo_singledispatchmethod()
    demo_practical_example()

    print(">>> 演示完成！")
    print()
    print("要点总结:")
    print("  1. @singledispatch 根据第一个参数类型分派到不同实现")
    print("  2. 使用 @func.register(type) 注册特定类型的实现")
    print("  3. 优先使用抽象基类（如 Sequence）处理相关类型")
    print("  4. 也可在类中使用 singledispatch 模式")


if __name__ == "__main__":
    main()
