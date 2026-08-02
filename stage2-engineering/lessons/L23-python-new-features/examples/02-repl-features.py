"""

from __future__ import annotations

Python 3.13 REPL 功能演示

本脚本包含一些可以在 Python 3.13 REPL 中尝试的示例代码。

运行方式：
    python3.13
    >>> exec(open('examples/02-repl-features.py').read())

或者逐行复制到 REPL 中体验。
"""

import datetime
import json


# 示例 1: 多行函数定义
def greet(name: str, greeting: str = "Hello") -> str:
    """
    生成问候语

    在 REPL 中，你可以：
    - 使用 ↑↓ 在多行中移动
    - 语法高亮让代码更清晰
    """
    return f"{greeting}, {name}!"


# 示例 2: 类定义
class Calculator:
    """简单的计算器类"""

    def __init__(self):
        self.result = 0
        self.history: list[str] = []

    def add(self, value: float) -> "Calculator":
        """加法"""
        self.result += value
        self.history.append(f"+{value}")
        return self

    def subtract(self, value: float) -> "Calculator":
        """减法"""
        self.result -= value
        self.history.append(f"-{value}")
        return self

    def multiply(self, value: float) -> "Calculator":
        """乘法"""
        self.result *= value
        self.history.append(f"*{value}")
        return self

    def divide(self, value: float) -> "Calculator":
        """除法"""
        if value == 0:
            raise ValueError("Cannot divide by zero")
        self.result /= value
        self.history.append(f"/{value}")
        return self

    def get_result(self) -> float:
        """获取结果"""
        return self.result

    def get_history(self) -> list[str]:
        """获取历史记录"""
        return self.history


# 示例 3: JSON 处理
def format_json(data: dict[str, int | str | float | bool | None]) -> str:
    """
    格式化 JSON

    使用 Python 3.10+ 的联合类型语法 (PEP 604)
    支持常见的 JSON 数据类型
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


# 示例 4: 日期时间处理
def get_current_time() -> str:
    """获取当前时间"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_date_info() -> dict[str, int | str]:
    """获取日期信息"""
    now = datetime.datetime.now()
    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "weekday": now.strftime("%A"),
        "timestamp": now.timestamp(),
    }


# 示例 5: 列表推导和生成器
def demo_comprehensions():
    """演示各种推导式"""
    # 列表推导
    squares = [x**2 for x in range(10)]

    # 字典推导
    square_dict = {x: x**2 for x in range(10)}

    # 集合推导
    even_squares = {x**2 for x in range(10) if x % 2 == 0}

    # 生成器表达式
    square_gen = (x**2 for x in range(10))

    return {
        "list": squares,
        "dict": square_dict,
        "set": even_squares,
        "generator": list(square_gen),
    }


# REPL 使用指南
REPL_GUIDE = """
=== Python 3.13 REPL 使用指南 ===

1. 多行编辑：
   - 定义函数或类时，自动进入多行模式
   - ↑↓ 键在多行中移动光标
   - Enter 在当前位置换行
   - Ctrl+D 或空行结束输入

2. 语法高亮：
   - 关键字（蓝色）: def, class, if, for, etc.
   - 字符串（绿色）: "hello", 'world'
   - 数字（黄色）: 123, 3.14
   - 注释（灰色）: # comment

3. 自动补全（Tab 键）：
   >>> import json
   >>> json.  # 按 Tab 查看所有方法
   >>> json.dumps  # 按 Tab 补全

4. F1 交互式帮助：
   >>> import json
   >>> json.dumps  # 将光标放在这里，按 F1
   # 显示详细文档

5. 直接命令：
   >>> help  # 不需要 help()
   >>> exit  # 不需要 exit()
   >>> quit  # 不需要 quit()

6. 历史记录：
   - ↑ 上一条命令
   - ↓ 下一条命令
   - Ctrl+R 搜索历史

7. 编辑快捷键：
   - Ctrl+A 行首
   - Ctrl+E 行尾
   - Ctrl+K 删除到行尾
   - Ctrl+U 删除到行首
   - Ctrl+W 删除前一个单词

=== 实战练习 ===

试试以下操作：

1. 导入模块并探索：
   >>> import datetime
   >>> datetime.  # Tab 补全
   >>> datetime.datetime.now  # F1 查看帮助

2. 定义函数：
   >>> def fibonacci(n):
   ...     if n <= 1:
   ...         return n
   ...     return fibonacci(n-1) + fibonacci(n-2)
   >>> fibonacci(10)

3. 链式调用：
   >>> calc = Calculator()
   >>> calc.add(10).subtract(3).multiply(2).get_result()

4. JSON 处理：
   >>> data = {"name": "Python", "version": 3.13}
   >>> format_json(data)

5. 日期处理：
   >>> get_date_info()

"""


def print_guide():
    """打印使用指南"""
    print(REPL_GUIDE)


if __name__ == "__main__":
    print("=" * 60)
    print("Python 3.13 REPL 功能演示")
    print("=" * 60)
    print("\n建议在 Python 3.13 REPL 中运行此脚本：")
    print("  python3.13")
    print("  >>> exec(open('examples/02-repl-features.py').read())")
    print("\n或者复制代码到 REPL 中逐行体验。")
    print("\n使用 print_guide() 查看完整使用指南。")
    print()

    # 运行示例
    print("### 示例 1: 简单问候")
    print(greet("World"))
    print(greet("Python", "Hi"))

    print("\n### 示例 2: 计算器链式调用")
    calc = Calculator()
    result = calc.add(10).subtract(3).multiply(2).get_result()
    print(f"结果: {result}")
    print(f"历史: {calc.get_history()}")

    print("\n### 示例 3: JSON 格式化")
    data = {"name": "Python", "version": 3.13, "features": ["REPL", "JIT"]}
    print(format_json(data))

    print("\n### 示例 4: 日期时间")
    print(f"当前时间: {get_current_time()}")
    print("日期信息:")
    print(format_json(get_date_info()))

    print("\n### 示例 5: 推导式")
    comprehensions = demo_comprehensions()
    for key, value in comprehensions.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 60)
    print("在 REPL 中试试这些功能吧！")
    print("=" * 60)
