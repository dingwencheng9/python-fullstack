"""

from __future__ import annotations

Python 3.13 体验课程 - 演示代码模块

本模块包含 Python 3.13 新特性的演示代码。

模块清单：
    - 01-colored-traceback.py: 彩色错误堆栈演示
    - 02-repl-features.py: REPL 改进功能演示
    - 03-performance-test.py: 性能基准测试

使用方法：
    直接运行各个演示脚本：

    ```bash
    python3.13 stage2-engineering/lessons/L21-python313-experience/examples/example_01_colorful_errors.py
    python3.13 examples/02-repl-features.py
    python3.13 examples/03-performance-test.py
    ```

注意事项：
    - 彩色错误提示需要在支持 ANSI 转义码的终端中运行
    - REPL 功能演示最好在交互式环境中体验
    - 性能测试建议在 Python 3.13 和 3.13 中分别运行以对比

Python 3.13 主要新特性：
    1. 改进的错误消息（彩色化、更清晰的位置标注）
    2. 新的交互式解释器（多行编辑、语法高亮、历史搜索）
    3. 性能优化（JIT 编译器、更快的解释器）
    4. PEP 695 泛型语法（类型参数语法）
    5. Free-threading 支持（实验性，需要特殊构建）
"""

__version__ = "1.0.0"
__all__ = [
    "colored_traceback",
    "repl_features",
    "performance_test",
]
