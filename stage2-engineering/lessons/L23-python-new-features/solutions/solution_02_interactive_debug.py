"""

from __future__ import annotations

练习 2: 交互式调试 - 参考指南

本练习是交互式任务，在 Python 3.13 REPL 中完成。
以下是完整的操作步骤和参考答案。

===============================================================================
解题思路: Python 3.13 增强的 REPL 提供更好的交互调试体验
===============================================================================

## 步骤 1: 启动 Python 3.13 REPL
```bash
python3.13
```

## 步骤 2: 定义测试函数
```python
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

# 测试
calculate_average([1, 2, 3, 4, 5])  # 应返回 3.0
```

## 步骤 3: 故意触发错误
```python
calculate_average([])  # ZeroDivisionError
```

## 步骤 4: 使用内置调试功能
Python 3.13 的 REPL 特性：
- 彩色语法高亮
- 更好的错误提示
- Tab 补全增强
- 多行编辑改进

## 步骤 5: 使用 pdb 调试
```python
import pdb

def buggy_function(x):
    pdb.set_trace()  # 设置断点
    result = x * 2
    return result + 10

buggy_function(5)
```

## 步骤 6: pdb 常用命令
- `n` (next): 执行下一行
- `s` (step): 进入函数
- `c` (continue): 继续执行
- `p variable`: 打印变量值
- `l` (list): 显示代码
- `q` (quit): 退出调试

## 完成标准
- ✓ 成功在 REPL 中定义并测试函数
- ✓ 触发并观察错误信息
- ✓ 使用 pdb 设置断点并逐步调试
- ✓ 理解 Python 3.13 REPL 的改进

## 参考资源
- Python 3.13 REPL 文档
- pdb 调试器文档
"""

if __name__ == "__main__":
    print(__doc__)
