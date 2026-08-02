"""

from __future__ import annotations

L18 示例 3: Python 3.13 新特性演示

展示 Python 3.13 的核心新特性和现代化语法。

核心特性：
1. PEP 695: 泛型类型参数语法（Type Parameter Syntax）
2. 改进的 REPL（彩色输出、多行编辑、更智能的补全）
3. Free-threading 考量（3.13t: 无 GIL 并发模型）
4. 改进的错误消息
"""

import sys
from collections.abc import Callable, Sequence

# ============================================================================
# 1. PEP 695: 现代泛型语法（Python 3.13）
# ============================================================================


def first[T](items: list[T]) -> T | None:
    """
    获取列表第一个元素

    PEP 695 语法特点：
    - 使用 [T] 声明类型参数，替代 TypeVar
    - 无需导入 typing.TypeVar
    - 语法更简洁、可读性更强

    线程安全（Python 3.14）：
    - ✅ 此函数为纯函数，无共享状态，线程安全
    """
    return items[0] if items else None


def safe_get[T](items: Sequence[T], index: int, default: T | None = None) -> T | None:
    """
    安全获取序列元素

    泛型约束：
    - 使用 collections.abc.Sequence 而非 list，支持更广泛的类型
    - 返回类型 T | None 使用 PEP 604 管道符

    线程安全（Python 3.14）：
    - ✅ 纯函数，无副作用，线程安全
    """
    try:
        return items[index]
    except (IndexError, TypeError):
        return default


class Container[T]:
    """
    泛型容器类

    PEP 695 类泛型：
    - 使用 [T] 在类名后声明类型参数
    - 实例化时自动推断类型：Container(42) -> Container[int]

    线程安全（Python 3.14）：
    - ⚠️ 实例属性 _items 为可变列表，多线程访问需要加锁
    - 建议：在 Free-threading 环境下使用 threading.Lock 保护
    """

    def __init__(self, *items: T) -> None:
        """初始化容器"""
        self._items: list[T] = list(items)

    def add(self, item: T) -> None:
        """添加元素"""
        # 🔒 线程安全提示（Python 3.14）：
        # 在无 GIL 环境下，list.append() 不保证原子性
        # 多线程场景需使用 threading.Lock:
        #   with self._lock:
        #       self._items.append(item)
        self._items.append(item)

    def get_all(self) -> list[T]:
        """获取所有元素（返回副本）"""
        # 🔒 线程安全实践：返回副本而非原列表引用
        return self._items.copy()

    def __len__(self) -> int:
        """容器大小"""
        return len(self._items)


def process_batch[T](
    items: list[T],
    *,
    transform: Callable[[T], T] | None = None,
) -> list[T]:
    """
    批处理函数

    PEP 695 + 现代类型注解：
    - 使用 Callable[[T], T] 而非旧版 typing.Callable（从 collections.abc 导入）
    - 使用 | None 而非 Optional
    - 强制关键字参数（*, 后的参数）

    线程安全（Python 3.14）：
    - ✅ 纯函数，输入不可变，输出新列表，线程安全
    """
    if transform is None:
        return items.copy()
    return [transform(item) for item in items]


# ============================================================================
# 2. 改进的 REPL 演示
# ============================================================================


def demo_repl() -> None:
    """
    Python 3.13 REPL 改进演示

    新特性：
    1. 🎨 彩色语法高亮（自动检测终端支持）
    2. ✏️ 多行编辑支持（更好的交互体验）
    3. 🔍 更智能的自动补全（基于上下文）
    4. 📝 改进的历史记录（持久化到 ~/.python_history）
    5. 🐛 更好的错误提示（精确到字符位置）

    使用方法：
    1. 终端运行：python3.13
    2. 尝试多行输入、Tab 补全、错误提示
    """
    print("=" * 60)
    print("🎯 Python 3.13 REPL 改进演示")
    print("=" * 60)
    print()

    print("💡 新特性展示：")
    print()
    print("1️⃣  彩色语法高亮")
    print("   $ python3.13")
    print("   >>> def greet(name: str) -> str:")
    print("   ...     return f'Hello, {name}!'")
    print("   (注意：关键字、字符串、函数名会有不同颜色)")
    print()

    print("2️⃣  多行编辑支持")
    print("   - 使用 ↑↓ 键在多行代码间导航")
    print("   - 使用 Ctrl+C 取消当前输入（不退出 REPL）")
    print("   - 使用 Ctrl+D 退出 REPL")
    print()

    print("3️⃣  改进的错误提示")
    print("   >>> result = 1 / 0")
    print("   ZeroDivisionError: division by zero")
    print("   >>> result = 1 / 0")
    print("            ~~~~~~^~~  ← 精确指向错误位置")
    print()

    print("4️⃣  更智能的补全")
    print("   >>> import pathlib")
    print("   >>> p = pathlib.Path('.')  ")
    print("   >>> p.[Tab]  # 会列出所有可用方法和属性")
    print()

    print("✨ 立即体验：")
    print("   终端运行: python3.13")
    print()


# ============================================================================
# 3. Free-threading 并发模型演示（Python 3.14）
# ============================================================================


def demo_free_threading() -> None:
    """
    Free-threading（PEP 703/779）概念演示

    背景：
    - Python 3.13t / 3.14t 是独立的"无 GIL"freethreaded 构建版本
    - PEP 703（3.13）试验性引入；PEP 779（3.14）官方支持但仍非默认
    - 启动方式：python3.13t script.py（不是命令行 flag）
    - 允许真正的并行多线程执行

    关键概念：
    1. 传统 CPython：全局解释器锁（GIL）限制多线程并行
    2. Python 3.14：移除 GIL，支持真正的并行多线程
    3. 线程安全：需要显式保护共享状态

    ⚠️  迁移注意事项：
    - 原本依赖 GIL 保护的代码需要加锁
    - list/dict 的操作不再原子性
    - 需要使用 threading.Lock/RLock 保护共享资源
    """
    print("=" * 60)
    print("🚀 Free-threading（PEP 703/779）概念")
    print("=" * 60)
    print()

    print("📌 什么是 Free-threading？")
    print()
    print("传统 CPython (有 GIL):")
    print("  Thread 1: [█████-----] ")
    print("  Thread 2: [-----█████]  ← GIL 导致交替执行，非真并行")
    print()
    print("Python 3.14 (无 GIL):")
    print("  Thread 1: [██████████] ")
    print("  Thread 2: [██████████]  ← 真正并行执行")
    print()

    print("🔒 线程安全示例：")
    print()
    print("❌ 不安全代码（需要修改）：")
    print("""
    # 在 Free-threading 环境下不安全
    shared_list = []

    def append_item(item):
        shared_list.append(item)  # ⚠️  非原子操作
    """)
    print()

    print("✅ 安全代码（推荐写法）：")
    print("""
    import threading

    shared_list = []
    lock = threading.Lock()

    def append_item(item):
        with lock:
            shared_list.append(item)  # ✅ 锁保护
    """)
    print()

    print("💡 最佳实践：")
    print("  1. 优先使用不可变数据结构")
    print("  2. 使用 queue.Queue 等线程安全容器")
    print("  3. 明确标记共享状态并加锁")
    print("  4. 在注释中说明并发安全性")
    print()

    print("🔧 如何使用 Python 3.14：")
    print("  # 从源码编译")
    print("  $ ./configure --disable-gil")
    print("  $ make")
    print("  $ ./python")
    print()


# ============================================================================
# 4. 现代化最佳实践总结
# ============================================================================


def demonstrate_modern_syntax() -> dict[str, str | int]:
    """
    现代化 Python 语法最佳实践

    ✅ 推荐写法（Python 3.13）：
    - 类型提示：list[str], dict[str, int], str | None
    - 泛型：def func[T](x: T) -> T
    - 路径：pathlib.Path
    - 上下文管理：with 语句
    - 字符串：f-string

    ❌ 避免写法：
    - typing.List/Dict/Optional
    - typing.TypeVar 显式声明
    - os.path 字符串拼接
    - 手动 open/close 文件
    - % 或 .format() 字符串格式化

    线程安全（Python 3.14）：
    - ✅ 返回新字典，无共享状态，线程安全
    """
    # ✅ 使用字典类型注解
    config: dict[str, str | int] = {
        "name": "modern-python",
        "version": "3.13",
        "features": 10,
    }

    return config


# ============================================================================
# 主函数
# ============================================================================


def main() -> None:
    """主函数：演示所有 Python 3.13 新特性"""
    print("🐍 Python 3.13 新特性完整演示")
    print("=" * 60)
    print()

    # 检查 Python 版本
    version = sys.version_info
    print(f"当前 Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version >= (3, 13):
        print("✅ 已安装 Python 3.13+，所有特性可用")
    else:
        print("❌ Python 版本过低，建议升级到 3.13+")
    print()

    # 1. PEP 695 泛型语法演示
    print("=" * 60)
    print("1️⃣  PEP 695 泛型语法")
    print("=" * 60)
    print()

    # 泛型函数
    numbers = [1, 2, 3, 4, 5]
    first_num = first(numbers)
    print(f"first([1, 2, 3, 4, 5]) = {first_num}")

    strings = ["hello", "world", "python"]
    first_str = first(strings)
    print(f'first(["hello", "world", "python"]) = {first_str}')

    # 安全获取
    item = safe_get(numbers, 10, default=0)
    print(f"safe_get(numbers, 10, default=0) = {item}")
    print()

    # 泛型类
    int_container: Container[int] = Container(1, 2, 3)
    int_container.add(4)
    print(f"Container[int]: {int_container.get_all()}")

    str_container: Container[str] = Container("a", "b", "c")
    str_container.add("d")
    print(f"Container[str]: {str_container.get_all()}")
    print()

    # 批处理
    doubled = process_batch(numbers, transform=lambda x: x * 2)
    print(f"process_batch([1,2,3,4,5], transform=lambda x: x*2) = {doubled}")
    print()

    # 2. 改进的 REPL
    demo_repl()

    # 3. Free-threading 概念
    demo_free_threading()

    # 4. 现代化语法总结
    print("=" * 60)
    print("4️⃣  现代化语法最佳实践")
    print("=" * 60)
    print()
    config = demonstrate_modern_syntax()
    print(f"配置示例: {config}")
    print()

    # 总结
    print("=" * 60)
    print("✨ 总结")
    print("=" * 60)
    print()
    print("Python 3.13 核心升级：")
    print("  1. ✅ PEP 695 泛型语法 - 更简洁的类型参数")
    print("  2. ✅ 改进的 REPL - 彩色输出、多行编辑")
    print("  3. ✅ Free-threading - 真正的并行多线程（3.13t）")
    print("  4. ✅ 更好的错误消息 - 精确定位错误位置")
    print()
    print("迁移建议：")
    print("  - 使用内置泛型（list/dict/tuple）而非 typing 模块")
    print("  - 使用 PEP 695 语法声明泛型函数和类")
    print("  - 在并发代码中明确标注线程安全性")
    print("  - 为 Free-threading 环境预留兼容性注释")
    print()


if __name__ == "__main__":
    main()
