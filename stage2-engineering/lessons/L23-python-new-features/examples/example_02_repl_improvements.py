"""

from __future__ import annotations

L21 示例 2: Python 3.13 REPL 改进

演示 Python 3.13 的改进交互式解释器功能。
"""

import sys


def show_repl_improvements() -> None:
    """展示 REPL 改进"""

    print("🖥️  Python 3.13 REPL 改进")
    print("=" * 70)
    print(f"\nPython 版本: {sys.version}")
    print()

    improvements = [
        ("多行编辑", "支持多行代码块的编辑和导航"),
        ("语法高亮", "交互式输入时的彩色语法高亮"),
        ("自动缩进", "智能缩进，自动补全代码块"),
        ("历史搜索", "Ctrl+R 反向搜索命令历史"),
        ("括号匹配", "输入时高亮显示匹配的括号"),
        ("粘贴模式", "智能处理多行粘贴"),
    ]

    print("💡 主要改进：")
    for feature, description in improvements:
        print(f"\n  {feature}")
        print(f"    → {description}")


def show_repl_features() -> None:
    """展示 REPL 功能"""

    print("\n\n✨ 新 REPL 功能演示")
    print("=" * 70)

    features = """
1. 多行编辑
   >>> def greet(name):
   ...     return f"Hello, {name}!"
   ...
   >>> greet("Python")
   'Hello, Python!'

   • 可以用方向键在多行间导航
   • 支持块选择和编辑

2. 语法高亮
   >>> x = 42        # 数字显示为橙色
   >>> name = "Alice" # 字符串显示为绿色
   >>> def func():    # 关键字显示为紫色
   ...     pass

3. 自动缩进
   >>> if True:
   ...     # 自动缩进 4 空格
   ...     print("hello")
   ...     if True:
   ...         # 嵌套自动缩进
   ...         print("world")

4. 历史搜索
   • Ctrl+R: 反向搜索历史
   • 上/下箭头: 浏览历史
   • Ctrl+S: 正向搜索历史

5. 括号匹配
   >>> data = {"key": [1, 2, 3]}
              ^                ^
              高亮显示匹配的括号

6. 粘贴模式
   • 粘贴多行代码自动进入粘贴模式
   • 保留原始缩进
   • Ctrl+D 结束粘贴
"""

    print(features)


def compare_old_new() -> None:
    """对比旧版和新版 REPL"""

    print("\n\n🆚 Python 3.12 vs 3.13 REPL 对比")
    print("=" * 70)

    comparison = """
Python 3.12 REPL:
  • 基础行编辑
  • 无语法高亮
  • 基本历史记录
  • 简单自动缩进

Python 3.13 REPL:
  ✅ 多行块编辑
  ✅ 彩色语法高亮
  ✅ 高级历史搜索（Ctrl+R）
  ✅ 智能自动缩进
  ✅ 括号匹配高亮
  ✅ 粘贴模式
  ✅ 更好的错误显示

体验提升:
  • 类似 IPython 的编辑体验
  • 更接近现代代码编辑器
  • 提高交互式编程效率
"""

    print(comparison)


def show_keyboard_shortcuts() -> None:
    """展示键盘快捷键"""

    print("\n\n⌨️  键盘快捷键")
    print("=" * 70)

    shortcuts = [
        ("Ctrl+R", "反向搜索历史"),
        ("Ctrl+S", "正向搜索历史"),
        ("Ctrl+C", "取消当前行"),
        ("Ctrl+D", "退出 REPL（或结束粘贴模式）"),
        ("Ctrl+L", "清屏"),
        ("Alt+Enter", "插入新行（不执行）"),
        ("上/下箭头", "浏览命令历史"),
        ("左/右箭头", "移动光标"),
        ("Home/End", "跳到行首/行尾"),
        ("Ctrl+W", "删除前一个单词"),
    ]

    for shortcut, description in shortcuts:
        print(f"\n  {shortcut:15s} → {description}")


def show_usage_examples() -> None:
    """展示使用示例"""

    print("\n\n📝 实际使用示例")
    print("=" * 70)

    examples = """
示例 1: 探索性编程
  >>> import requests
  >>> response = requests.get("https://api.github.com")
  >>> response.json()  # 用方向键修改 URL 重新尝试
  {...}

示例 2: 快速测试
  >>> def fibonacci(n):
  ...     # 多行编辑，语法高亮
  ...     if n <= 1:
  ...         return n
  ...     return fibonacci(n-1) + fibonacci(n-2)
  ...
  >>> [fibonacci(i) for i in range(10)]
  [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

示例 3: 调试代码
  >>> data = {"users": [{"name": "Alice", "age": 25}]}
  >>> data["users"][0]["name"]  # 括号匹配高亮
  'Alice'
  >>> # Ctrl+R 搜索之前的命令快速修改

示例 4: 学习新 API
  >>> import json
  >>> help(json.dumps)  # 查看文档
  >>> json.dumps({"key": "value"})  # 测试
  '{"key": "value"}'
"""

    print(examples)


def show_tips() -> None:
    """展示使用技巧"""

    print("\n\n💡 使用技巧")
    print("=" * 70)

    tips = [
        "1. 启用 REPL 时使用 python -i 加载脚本",
        "2. 使用 _ 访问上一个表达式的结果",
        "3. 粘贴代码块时自动进入粘贴模式",
        "4. 使用 Ctrl+R 快速查找历史命令",
        "5. 多行编辑时用方向键在行间导航",
        "6. exit() 或 Ctrl+D 退出 REPL",
        "7. help(object) 查看文档",
        "8. dir(object) 查看属性和方法",
    ]

    for tip in tips:
        print(f"  {tip}")


def main() -> None:
    """主函数"""

    show_repl_improvements()
    show_repl_features()
    compare_old_new()
    show_keyboard_shortcuts()
    show_usage_examples()
    show_tips()

    print("\n\n✨ 如何体验：")
    print("  1. 确保安装 Python 3.13")
    print("  2. 在终端运行: python3.13")
    print("  3. 开始交互式编程")
    print("\n🔑 关键改进：")
    print("  • 多行块编辑")
    print("  • 彩色语法高亮")
    print("  • 高级历史搜索")
    print("  • 括号匹配")
    print("  • 类似 IPython 的体验")


if __name__ == "__main__":
    main()
