"""

from __future__ import annotations

练习 2: 交互式调试

本练习需要在 Python 3.13 REPL 中完成。

目标：
  - 掌握新 REPL 的多行编辑
  - 使用 Tab 补全探索 API
  - 使用 F1 查看帮助
  - 练习交互式开发工作流

完成标准：
  - 完成所有任务
  - 理解 REPL 新特性的优势
  - 能够高效使用 REPL 进行开发
"""

# ===== 任务说明 =====
# 请在 Python 3.13 REPL 中逐步完成以下任务

TASK_1 = """
任务 1: 探索 datetime 模块 (10 分钟)

步骤:
1. 启动 REPL: python3.13
2. 导入 datetime 模块:
   >>> import datetime
3. 使用 Tab 补全探索模块:
   >>> datetime.  # 按 Tab
4. 找到获取当前时间的方法
5. 使用 F1 查看该方法的详细文档
6. 创建一个格式化时间的函数:
   >>> def format_time(dt):
   ...     return dt.strftime("%Y-%m-%d %H:%M:%S")
7. 测试函数:
   >>> now = datetime.datetime.now()
   >>> format_time(now)

提示:
  - 在多行编辑模式下，可以用 ↑↓ 移动光标
  - 语法高亮让代码更易读
  - F1 快捷键非常实用
"""

TASK_2 = """
任务 2: 创建计算器类 (15 分钟)

步骤:
1. 在 REPL 中定义一个 Calculator 类
2. 实现链式调用方法 (add, subtract, multiply, divide)
3. 测试链式调用:
   >>> calc = Calculator()
   >>> calc.add(10).subtract(3).multiply(2).get_result()

要求:
  - 支持链式调用
  - 除零时抛出异常
  - 记录操作历史

示例代码框架:
>>> class Calculator:
...     def __init__(self):
...         self.result = 0
...         self.history = []
...
...     def add(self, value):
...         # TODO: 实现
...         return self
...
...     # TODO: 实现其他方法
"""

TASK_3 = """
任务 3: JSON 数据处理 (10 分钟)

步骤:
1. 导入 json 模块
2. 创建一个字典:
   >>> data = {
   ...     "name": "Python",
   ...     "version": 3.13,
   ...     "features": ["REPL", "JIT", "Colors"]
   ... }
3. 使用 Tab 补全探索 json 模块的方法
4. 格式化输出 JSON:
   >>> import json
   >>> print(json.dumps(data, indent=2))
5. 创建一个处理 JSON 的函数

任务:
  - 创建 format_json 函数
  - 支持中文输出 (ensure_ascii=False)
  - 自定义缩进
"""

TASK_4 = """
任务 4: 列表和字典推导 (10 分钟)

步骤:
1. 创建各种推导式:
   >>> # 列表推导
   >>> squares = [x**2 for x in range(10)]

   >>> # 字典推导
   >>> square_dict = {x: x**2 for x in range(10)}

   >>> # 集合推导
   >>> even_squares = {x**2 for x in range(10) if x % 2 == 0}

2. 创建一个函数返回所有推导结果

3. 尝试嵌套推导:
   >>> matrix = [[i*j for j in range(5)] for i in range(5)]

任务:
  - 理解不同推导式的使用场景
  - 观察语法高亮的效果
  - 练习多行编辑
"""

TASK_5 = """
任务 5: 交互式帮助系统 (5 分钟)

步骤:
1. 使用直接命令:
   >>> help  # 不需要 help()

2. 查看特定对象的帮助:
   help> list
   help> dict.get
   help> str.format

3. 退出帮助:
   help> quit

4. 尝试 F1 快捷键:
   >>> import os
   >>> os.path.join  # 光标放这里，按 F1

任务:
  - 熟悉帮助系统
  - 对比 F1 和 help 的区别
  - 找到你感兴趣的模块探索
"""


# ===== 参考答案 =====
# 完成练习后可以查看

REFERENCE_SOLUTIONS = """
=== 参考答案 ===

### 任务 1: datetime 处理
>>> import datetime
>>> def format_time(dt):
...     return dt.strftime("%Y-%m-%d %H:%M:%S")
>>>
>>> def get_time_info():
...     now = datetime.datetime.now()
...     return {
...         'formatted': format_time(now),
...         'timestamp': now.timestamp(),
...         'weekday': now.strftime("%A"),
...     }
>>>
>>> get_time_info()

### 任务 2: Calculator 类
>>> class Calculator:
...     def __init__(self):
...         self.result = 0
...         self.history = []
...
...     def add(self, value):
...         self.result += value
...         self.history.append(f'+{value}')
...         return self
...
...     def subtract(self, value):
...         self.result -= value
...         self.history.append(f'-{value}')
...         return self
...
...     def multiply(self, value):
...         self.result *= value
...         self.history.append(f'*{value}')
...         return self
...
...     def divide(self, value):
...         if value == 0:
...             raise ValueError("Cannot divide by zero")
...         self.result /= value
...         self.history.append(f'/{value}')
...         return self
...
...     def get_result(self):
...         return self.result
...
...     def get_history(self):
...         return self.history
>>>
>>> calc = Calculator()
>>> calc.add(10).subtract(3).multiply(2).get_result()
14.0

### 任务 3: JSON 处理
>>> import json
>>> def format_json(data, indent=2):
...     return json.dumps(data, indent=indent, ensure_ascii=False)
>>>
>>> data = {"姓名": "Python", "版本": 3.13}
>>> print(format_json(data))

### 任务 4: 推导式
>>> def demo_comprehensions():
...     return {
...         'squares': [x**2 for x in range(10)],
...         'square_dict': {x: x**2 for x in range(10)},
...         'even_squares': {x**2 for x in range(10) if x % 2 == 0},
...     }
>>>
>>> demo_comprehensions()
"""


def print_tasks():
    """打印所有任务"""
    tasks = [
        ("任务 1: 探索 datetime 模块", TASK_1),
        ("任务 2: 创建计算器类", TASK_2),
        ("任务 3: JSON 数据处理", TASK_3),
        ("任务 4: 列表和字典推导", TASK_4),
        ("任务 5: 交互式帮助系统", TASK_5),
    ]

    print("=" * 70)
    print("练习 2: 交互式调试")
    print("=" * 70)
    print("\n本练习需要在 Python 3.13 REPL 中完成。")
    print("\n启动 REPL:")
    print("  python3.13")
    print()

    for title, task in tasks:
        print(f"\n{title}")
        print("-" * 70)
        print(task)

    print("\n" + "=" * 70)
    print("完成所有任务后，运行以下代码查看参考答案:")
    print("  >>> exec(open('stage2-engineering/lessons/L21-python313-experience/exercises/exercise_02_interactive_debug.py').read())")
    print("  >>> print(REFERENCE_SOLUTIONS)")
    print("=" * 70)


if __name__ == "__main__":
    print_tasks()
