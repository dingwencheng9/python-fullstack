"""

from __future__ import annotations

练习 5：PEP 649 延迟注解 + annotationlib 实战

⚠️ 本练习需要 Python 3.14+。如果你只装了 Python 3.13，可以读题但跑不通。
   安装方式：`uv python install 3.14`  然后用 `python3.14 stage2-engineering/lessons/L21-python313-experience/exercises/exercise_05_pep649_annotations.py`

任务清单（按提示填空）：
"""

from __future__ import annotations

import sys

# ----------------------------------------------------------------------------
# 任务 1：定义一棵互相引用的二叉树（不使用 from __future__ import annotations）
# ----------------------------------------------------------------------------

# TODO: 定义 BinaryTreeNode 类，包含字段：
#   - value: int
#   - left: BinaryTreeNode | None  ← 自引用，PEP 649 会延迟求值
#   - right: BinaryTreeNode | None
# 写一个 add_left / add_right 方法，返回新增节点便于链式调用。


class BinaryTreeNode:
    pass  # 替换为你的实现


# ----------------------------------------------------------------------------
# 任务 2：用 annotationlib 提取注解为 STRING 格式生成文档
# ----------------------------------------------------------------------------

# TODO: 定义函数 describe_function(func) -> str
#   读取 func 的注解，用 STRING 格式，组装出一行人类可读的签名描述
#   例如对 def add(a: int, b: int) -> int:  应返回 "add(a: int, b: int) -> int"
#   提示：使用 annotationlib.get_annotations(func, format=Format.STRING)
#         以及 inspect.signature 获取参数名顺序。


def describe_function(func) -> str:
    """请实现这个函数"""
    raise NotImplementedError


# ----------------------------------------------------------------------------
# 任务 3：判断注解中是否包含某个类型（VALUE 模式）
# ----------------------------------------------------------------------------

# TODO: 定义 has_type_in_annotations(func, target: type) -> bool
#   返回 True/False，判断 func 的任意注解（参数或返回值）是否引用了 target 这个类
#   例如 has_type_in_annotations(some_func, str) -> True/False
#   提示：用 Format.VALUE，注意泛型如 list[str] 需要 typing.get_args 解构。


def has_type_in_annotations(func, target: type) -> bool:
    raise NotImplementedError


# ----------------------------------------------------------------------------
# 自检
# ----------------------------------------------------------------------------


def main() -> None:
    if sys.version_info < (3, 14):
        print("⚠️ 本练习需要 Python 3.14+，当前", sys.version_info[:3])
        print("   建议安装：uv python install 3.14")
        return

    print("自检：")
    # 任务 1
    try:
        root = BinaryTreeNode()
        print("  Task 1: BinaryTreeNode 已定义", "✅" if root is not None else "❌")
    except Exception as e:
        print(f"  Task 1: ❌ {e}")

    # 任务 2 & 3 自检
    def sample(a: int, b: str) -> bool:
        return True

    try:
        sig = describe_function(sample)
        print(
            f"  Task 2: describe_function -> {sig!r}",
            "✅" if "sample" in sig and "int" in sig else "❌",
        )
    except NotImplementedError:
        print("  Task 2: ⏳ 待实现")

    try:
        result = has_type_in_annotations(sample, int)
        print(f"  Task 3: has_type(int) -> {result}", "✅" if result is True else "❌")
    except NotImplementedError:
        print("  Task 3: ⏳ 待实现")


if __name__ == "__main__":
    main()
