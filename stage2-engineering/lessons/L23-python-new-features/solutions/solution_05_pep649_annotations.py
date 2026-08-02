"""

from __future__ import annotations

练习 5 参考答案：PEP 649 + annotationlib
"""

import inspect
import sys
import typing

# ----------------------------------------------------------------------------
# 任务 1：互相引用的二叉树
# ----------------------------------------------------------------------------


class BinaryTreeNode:
    """二叉树节点 — 自引用类型，PEP 649 自动延迟求值"""

    def __init__(self, value: int = 0) -> None:
        self.value = value
        self.left: BinaryTreeNode | None = None
        self.right: BinaryTreeNode | None = None

    def add_left(self, value: int) -> "BinaryTreeNode":
        self.left = BinaryTreeNode(value)
        return self.left

    def add_right(self, value: int) -> "BinaryTreeNode":
        self.right = BinaryTreeNode(value)
        return self.right


# ----------------------------------------------------------------------------
# 任务 2：函数签名描述
# ----------------------------------------------------------------------------


def describe_function(func) -> str:
    """读注解（STRING 模式）+ inspect 签名，组装人类可读描述"""
    if sys.version_info < (3, 14):
        # 3.13 fallback：直接用 inspect
        return f"{func.__name__}{inspect.signature(func)}"

    from annotationlib import Format, get_annotations

    annotations = get_annotations(func, format=Format.STRING)
    sig = inspect.signature(func)

    parts = []
    for name in sig.parameters:
        type_str = annotations.get(name, "Any")
        parts.append(f"{name}: {type_str}")

    return_type = annotations.get("return", "None")
    return f"{func.__name__}({', '.join(parts)}) -> {return_type}"


# ----------------------------------------------------------------------------
# 任务 3：注解中是否含某类型
# ----------------------------------------------------------------------------


def has_type_in_annotations(func, target: type) -> bool:
    """在注解中递归查找 target 类型（包括泛型参数内）"""
    if sys.version_info < (3, 14):
        annotations = func.__annotations__
    else:
        from annotationlib import Format, get_annotations

        annotations = get_annotations(func, format=Format.VALUE)

    def contains(annotation, target: type) -> bool:
        if annotation is target:
            return True
        # 解构泛型如 list[str]、dict[str, int]
        args = typing.get_args(annotation)
        return any(contains(a, target) for a in args)

    return any(contains(ann, target) for ann in annotations.values())


# ----------------------------------------------------------------------------
# 自检
# ----------------------------------------------------------------------------


def main() -> None:
    print("Python:", sys.version_info[:3])

    # 任务 1
    root = BinaryTreeNode(1)
    root.add_left(2).add_left(4)
    root.add_right(3)
    print(f"  Task 1: ✅ 树构造成功，根值={root.value}")

    # 任务 2
    def add(a: int, b: int) -> int:
        return a + b

    sig = describe_function(add)
    print(f"  Task 2: ✅ {sig}")

    # 任务 3
    def fetch(ids: list[int]) -> dict[str, int]:
        return {}

    print(f"  Task 3: ✅ has_type(int) = {has_type_in_annotations(fetch, int)}")
    print(f"           has_type(float) = {has_type_in_annotations(fetch, float)}")


if __name__ == "__main__":
    main()
