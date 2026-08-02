"""

from __future__ import annotations

example_05_python314_pep649.py — PEP 649 延迟注解评估（Python 3.14+）

Python 3.14 通过 PEP 649 改变了类型注解的求值时机：默认变成"延迟求值"，
解决了 PEP 563（`from __future__ import annotations`）在运行时类型工具（如
pydantic、typer、dataclass）下的兼容问题。

运行要求：
    python3.14 example_05_python314_pep649.py

如果你只有 Python 3.13，运行后会跳过演示，输出兼容性提示。

教学要点：
    1. PEP 649 解决"前向引用"的天然方式（不再需要 __future__ import）
    2. annotationlib 提供 Format.VALUE / FORWARDREF / STRING 三种访问模式
    3. 与 PEP 563（字符串化）的根本差异：PEP 649 保留对象语义
"""

import sys


def demo_forward_reference() -> None:
    """演示前向引用：类引用自身 / 互相引用"""
    print("=" * 70)
    print("演示 1：前向引用（PEP 649 自动处理）")
    print("=" * 70)

    class Tree:
        # 注意：没有 `from __future__ import annotations`
        # 即便如此，'Tree' 这个前向引用也不会立即报错
        # PEP 649 的核心：注解延迟求值，class 体定义完成后再解析
        def get_child(self) -> "Tree | None":
            return None

        def add_child(self, child: "Tree") -> None:
            pass

    # 注意：__annotations__ 字段在 PEP 649 下保留字符串形式，
    # 真实类型解析需要走 annotationlib（见演示 2）。
    print(f"  Tree.get_child.__annotations__: {Tree.get_child.__annotations__}")
    print("  ✅ 没有抛出 NameError — 前向引用被延迟求值")
    print("  ✅ 不需要 from __future__ import annotations")
    print()


def demo_annotationlib_formats() -> None:
    """演示 annotationlib 的三种 Format 模式"""
    print("=" * 70)
    print("演示 2：annotationlib 三种 Format")
    print("=" * 70)

    if sys.version_info < (3, 14):
        print("  ⚠️ 需要 Python 3.14+，当前", sys.version_info[:3])
        return

    from annotationlib import Format, get_annotations

    class Order:
        def total(self, quantity: int, price: float) -> float:
            return quantity * price

    # Format.VALUE: 默认模式，返回真实类型对象（int、float、自定义类...）
    val = get_annotations(Order.total, format=Format.VALUE)
    print(f"  VALUE 格式：{val}")
    print(f"    - quantity 类型对象：{val['quantity']}, 是 int 类: {val['quantity'] is int}")

    # Format.STRING: 返回源码字符串（适合文档生成、序列化）
    string = get_annotations(Order.total, format=Format.STRING)
    print(f"  STRING 格式：{string}")

    # Format.FORWARDREF: 含未解析符号时返回 ForwardRef，不报错
    fwd = get_annotations(Order.total, format=Format.FORWARDREF)
    print(f"  FORWARDREF 格式：{fwd}")
    print()


def demo_dynamic_annotation() -> None:
    """演示运行时类型工具与 PEP 649 的兼容"""
    print("=" * 70)
    print("演示 3：运行时类型工具兼容（vs PEP 563）")
    print("=" * 70)

    from dataclasses import dataclass

    # PEP 563（不推荐）：注解永远是字符串，dataclass 需要额外解析
    # PEP 649（默认）：注解是真正的类型对象，dataclass 直接可用
    @dataclass
    class User:
        id: int
        name: str
        tags: list[str]

    u = User(1, "Alice", ["admin"])
    print(f"  dataclass 实例：{u}")
    print(f"  注解类型：{User.__annotations__}")
    print("  ✅ id 是 int 类，不是字符串 'int' — 这正是 PEP 649 的核心改进")


def main() -> None:
    print(f"\nPython 版本：{sys.version_info[:3]}\n")
    demo_forward_reference()
    demo_annotationlib_formats()
    demo_dynamic_annotation()


if __name__ == "__main__":
    main()
