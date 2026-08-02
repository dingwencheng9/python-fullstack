"""

from __future__ import annotations

Python 3.13 体验课程 - 练习题模块

本模块包含 Python 3.13 新特性的练习题。

练习清单：
    - exercise_01_error_handling.py: 错误处理和彩色堆栈练习
    - exercise_02_interactive_debug.py: 交互式调试和 REPL 练习
    - exercise_03_benchmark.py: 性能基准测试练习

使用方法：
    1. 阅读练习文件中的任务说明
    2. 完成 TODO 标记的代码
    3. 运行对应的测试验证：
       ```bash
       pytest tests/test_features.py -v
       ```
    4. 查看 solutions/ 目录中的参考答案

练习目标：
    - 掌握 Python 3.13 彩色错误提示的使用
    - 熟悉新 REPL 的交互式开发工作流
    - 理解 Python 3.13 的性能改进
    - 学会使用现代 Python 特性

学习建议：
    1. 练习1：先运行 examples/example_01_colorful_errors.py 观察效果
    2. 练习2：需要在 Python 3.13 REPL 中完成，体验交互式开发
    3. 练习3：对比 Python 3.12 和 3.13 的性能差异

完成标准：
    - 所有 TODO 已实现
    - 代码可以正常运行
    - 理解 Python 3.13 新特性的优势
"""

__version__ = "1.0.0"
__all__ = [
    "error_handling",
    "interactive_debug",
    "benchmark",
]
