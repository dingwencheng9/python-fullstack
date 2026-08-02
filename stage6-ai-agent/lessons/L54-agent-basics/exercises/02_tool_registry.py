"""练习 2: 工具注册器。

from __future__ import annotations

实现一个工具注册器，支持注册和调用工具。
"""

from collections.abc import Callable
from typing import Any


# ========================================
# 📝 练习：实现工具注册器
#
# 🎯 目标：掌握 Agent 工具系统的核心机制
#
# 📌 要求：
# 1. 实现 ToolRegistry 类，管理工具注册和调用
# 2. 支持通过装饰器注册工具
# 3. 支持通过名称调用工具
# 4. 提供工具列表和描述查询
# 5. 处理工具调用错误
#
# 💡 实现提示：
# - 使用字典存储 {tool_name: tool_function}
# - 装饰器应该保存函数的 __name__ 和 __doc__
# - 调用时需要验证工具是否存在
# - 可以添加参数验证
#
# ✅ 验收标准：
# - 可以注册和调用工具
# - 工具名称正确映射
# - 错误处理合理
# - 支持查询工具列表
# ========================================


class ToolRegistry:
    """工具注册器

    管理 Agent 可用的工具集合。

    Examples:
        >>> registry = ToolRegistry()
        >>> @registry.register
        ... def add(a: int, b: int) -> int:
        ...     '''加法工具'''
        ...     return a + b
        >>> registry.call("add", a=1, b=2)
        3
        >>> "add" in registry.list_tools()
        True
    """

    def __init__(self) -> None:
        """初始化工具注册器"""
        # 👉 TODO: 初始化工具字典
        # self._tools: dict[str, Callable] = {}
        raise NotImplementedError

    def register(self, func: Callable) -> Callable:
        """注册工具（装饰器）

        Args:
            func: 要注册的工具函数

        Returns:
            原函数（不改变函数行为）

        Examples:
            >>> registry = ToolRegistry()
            >>> @registry.register
            ... def multiply(x: int, y: int) -> int:
            ...     return x * y
            >>> registry.call("multiply", x=3, y=4)
            12
        """
        # 👉 TODO: 实现工具注册
        # 1. 获取函数名: func.__name__
        # 2. 存储到 self._tools 字典
        # 3. 返回原函数
        raise NotImplementedError

    def call(self, tool_name: str, **kwargs: Any) -> Any:
        """调用工具

        Args:
            tool_name: 工具名称
            **kwargs: 工具参数

        Returns:
            工具执行结果

        Raises:
            ValueError: 如果工具不存在

        Examples:
            >>> registry = ToolRegistry()
            >>> @registry.register
            ... def greet(name: str) -> str:
            ...     return f"Hello, {name}!"
            >>> registry.call("greet", name="Alice")
            'Hello, Alice!'
        """
        # 👉 TODO: 实现工具调用
        # 1. 检查工具是否存在: if tool_name not in self._tools
        # 2. 如果不存在，抛出 ValueError
        # 3. 获取工具函数并调用: self._tools[tool_name](**kwargs)
        # 4. 返回结果
        raise NotImplementedError

    def list_tools(self) -> list[str]:
        """列出所有已注册的工具

        Returns:
            工具名称列表

        Examples:
            >>> registry = ToolRegistry()
            >>> @registry.register
            ... def tool1():
            ...     pass
            >>> @registry.register
            ... def tool2():
            ...     pass
            >>> sorted(registry.list_tools())
            ['tool1', 'tool2']
        """
        # 👉 TODO: 返回工具名称列表
        # return list(self._tools.keys())
        raise NotImplementedError

    def get_tool_info(self, tool_name: str) -> dict[str, str]:
        """获取工具信息

        Args:
            tool_name: 工具名称

        Returns:
            包含 name 和 description 的字典

        Raises:
            ValueError: 如果工具不存在

        Examples:
            >>> registry = ToolRegistry()
            >>> @registry.register
            ... def search(query: str) -> str:
            ...     '''搜索工具'''
            ...     return f"Results for {query}"
            >>> info = registry.get_tool_info("search")
            >>> info["name"]
            'search'
            >>> "搜索" in info["description"]
            True
        """
        # 👉 TODO: 实现工具信息获取
        # 1. 检查工具是否存在
        # 2. 获取函数的 __doc__ 作为描述
        # 3. 返回 {"name": tool_name, "description": func.__doc__ or ""}
        raise NotImplementedError


if __name__ == "__main__":
    print("=" * 60)
    print("🛠️  工具注册器练习")
    print("=" * 60)

    print("\n💡 完成上述类后，取消下面的注释测试：")
    print()

    # # 创建注册器
    # registry = ToolRegistry()
    #
    # # 注册工具
    # @registry.register
    # def calculate(operation: str, a: float, b: float) -> float:
    #     """计算器工具：支持加减乘除"""
    #     if operation == "add":
    #         return a + b
    #     elif operation == "subtract":
    #         return a - b
    #     elif operation == "multiply":
    #         return a * b
    #     elif operation == "divide":
    #         return a / b if b != 0 else 0
    #     else:
    #         raise ValueError(f"Unknown operation: {operation}")
    #
    # @registry.register
    # def get_weather(city: str) -> str:
    #     """天气查询工具（模拟）"""
    #     return f"{city} 的天气：晴，25°C"
    #
    # # 测试工具调用
    # print("✅ 测试工具调用:")
    # result1 = registry.call("calculate", operation="add", a=10, b=5)
    # print(f"  calculate(add, 10, 5) = {result1}")
    #
    # result2 = registry.call("get_weather", city="北京")
    # print(f"  get_weather(北京) = {result2}")
    #
    # # 列出所有工具
    # print("\n📋 已注册的工具:")
    # for tool_name in registry.list_tools():
    #     info = registry.get_tool_info(tool_name)
    #     print(f"  - {info['name']}: {info['description']}")
    #
    # # 测试错误处理
    # print("\n⚠️  测试错误处理:")
    # try:
    #     registry.call("nonexistent_tool")
    # except ValueError as e:
    #     print(f"  ✅ 正确捕获错误: {e}")

    print("\n" + "=" * 60)
    print("📚 参考资源:")
    print("   - LangChain Tools 文档")
    print("   - Python 装饰器教程")
    print("=" * 60)
