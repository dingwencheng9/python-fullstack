# L05: 调试工具与开发环境

> **课程编号**: L05
> **所属阶段**: Stage 0 - Python 编程基础
> **前置课程**: L04 函数与模块
> **建议学时**: 4 小时

---

## 概述

本课是 Stage 0 的补充内容，旨在帮助学习者建立良好的调试习惯。在掌握函数和模块的基础上，学习使用专业的调试工具来排查问题，而不是仅依赖 `print()` 语句。

### 为什么需要调试工具？

`print()` 调试的局限性：
- 需要反复添加/删除 print 语句
- 难以查看复杂数据结构的内部状态
- 无法在特定条件下暂停执行
- 对于大型项目效率低下

专业调试工具的优势：
- 可以设置断点，精确控制执行暂停位置
- 可以单步执行，观察每一步的变量变化
- 可以查看调用栈，理解程序执行流程
- 可以修改变量值，测试不同场景

---

## 1. pdb 基础

### 1.1 什么是 pdb

`pdb` 是 Python 标准库提供的交互式调试器（Python Debugger）。它是 Python 内置的调试工具，无需额外安装。

### 1.2 使用 pdb.set_trace()

最简单的方式是在代码中插入断点：

```python
import pdb

def calculate_factorial(n):
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n == 0 or n == 1:
        return 1
    
    pdb.set_trace()  # 程序在这里暂停
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(calculate_factorial(5))
```

运行效果：

```
> /path/to/code.py(8)calculate_factorial()
-> result = 1
(Pdb) n          # 单步执行 next
> /path/to/code.py(9)calculate_factorial()
-> for i in range(2, n + 1):
(Pdb) p result   # 打印变量
1
(Pdb) p n
5
(Pdb) c          # 继续执行 continue
120
```

### 1.3 pdb 常用命令

| 命令 | 简写 | 说明 |
|------|------|------|
| `next` | `n` | 执行下一行，不进入函数 |
| `step` | `s` | 执行下一行，进入函数 |
| `continue` | `c` | 继续执行到下一个断点 |
| `break` | `b` | 设置断点 |
| `print` | `p` | 打印变量值 |
| `list` | `l` | 查看当前代码上下文 |
| `where` | `w` | 查看调用栈 |
| `up` | `u` | 切换到上层栈帧 |
| `down` | `d` | 切换到下层栈帧 |
| `quit` | `q` | 退出调试器 |

### 1.4 使用命令行方式启动 pdb

除了 `set_trace()`，还可以在命令行启动 pdb：

```bash
# 在程序入口处启动
python -m pdb my_script.py

# 或者在异常发生后启动 post-mortem 调试
python -m pdb -c "postmortem" my_script.py
```

---

## 2. breakpoint() 内置函数

### 2.1 Python 3.7+ 的 breakpoint()

`breakpoint()` 是 Python 3.7 引入的内置函数，比 `pdb.set_trace()` 更灵活：

```python
def process_data(data):
    breakpoint()  # 等同于 pdb.set_trace()，但更简洁
    # 处理逻辑...
    return processed
```

### 2.2 配置默认调试器

`breakpoint()` 会调用 `sys.breakpointhook()`，可以通过环境变量配置：

```bash
# 使用 pdb（默认）
export PYTHONBREAKPOINT=pdb.set_trace

# 使用 ipdb（需要 pip install ipdb）
export PYTHONBREAKPOINT=ipdb.set_trace

# 禁用断点（调试代码留在代码中时使用）
export PYTHONBREAKPOINT=
```

### 2.3 在代码中检查断点状态

```python
import sys

def debug_print(*args):
    """仅在调试模式启用时打印"""
    if sys.flags.debug or hasattr(sys, 'gettrace') and sys.gettrace():
        print(*args)
```

---

## 3. traceback 分析

### 3.1 理解异常追踪信息

当程序崩溃时，Python 会输出 traceback 信息：

```python
def level_3():
    raise ValueError("测试错误")

def level_2():
    level_3()

def level_1():
    level_2()

level_1()
```

输出：

```
Traceback (most recent call last):
  File "example.py", line 12, in <module>
    level_1()
  File "example.py", line 10, in level_1
    level_2()
  File "example.py", line 7, in level_2
    level_3()
  File "example.py", line 2, in level_3
    raise ValueError("测试错误")
ValueError: 测试错误
```

### 3.2 使用 traceback 模块

```python
import traceback
import sys

def show_traceback():
    """打印当前异常追踪信息"""
    traceback.print_exc()

try:
    # 可能抛出异常的代码
    1 / 0
except Exception:
    show_traceback()
```

### 3.3 使用 sys.last_traceback

程序崩溃后，可以通过 `sys.last_traceback` 访问最后的异常信息：

```python
import sys

def analyze_crash():
    """在 except 块中使用 sys.last_traceback"""
    if hasattr(sys, 'last_traceback') and sys.last_traceback:
        tb = sys.last_traceback
        print(f"崩溃位置: {tb.tb_frame.f_code.co_filename}:{tb.tb_lineno}")
        print(f"函数名: {tb.tb_frame.f_code.co_name}")
        traceback.print_tb(tb)

try:
    data = {"key": "value"}
    print(data["nonexistent"])  # KeyError
except Exception:
    analyze_crash()
```

### 3.4 使用 traceback.format_exc()

将异常信息格式化为字符串，用于日志记录：

```python
import traceback
import logging

logging.basicConfig(level=logging.ERROR)

def log_exception(func):
    """装饰器：记录函数异常"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logging.error(f"异常在 {func.__name__}:\n{traceback.format_exc()}")
            raise
    return wrapper

@log_exception
def risky_operation():
    # 可能失败的操作
    pass
```

---

## 4. IDE 调试器

### 4.1 VS Code 调试配置

创建 `.vscode/launch.json`：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "module": "mymodule",
            "console": "integratedTerminal"
        }
    ]
}
```

调试步骤：
1. 在代码行号左侧点击，设置断点（红点）
2. 按 F5 启动调试
3. 使用调试工具栏：继续、跳过、单步进入、停止

### 4.2 PyCharm 调试

PyCharm 提供了更强大的调试功能：
- 条件断点：在断点处设置条件表达式
- 日志断点：断点触发时打印信息但不暂停
- 监视点：监控特定变量的值变化
- 远程调试：连接到远程 Python 进程

---

## 5. uv 工具链

### 5.1 uv 简介

`uv` 是一个用 Rust 编写的超快速 Python 包管理器，兼容 pip、pip-tools、pipx、poetry、pyenv 等工具。

### 5.2 创建项目

```bash
# 创建新项目
uv init my-project
cd my-project

# 添加依赖
uv add requests
uv add --dev pytest

# 运行脚本
uv run python main.py

# 运行测试
uv run pytest
```

### 5.3 使用 uv 管理虚拟环境

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
uv sync
```

### 5.4 uv 的优势

| 特性 | pip | uv |
|------|-----|-----|
| 安装速度 | 慢 | 快 10-100 倍 |
| 依赖解析 | 慢 | 快 |
| 锁文件 | 无 | uv.lock |
| Python 版本管理 | pyenv | 内置 |

---

## 6. 调试最佳实践

### 6.1 何时使用调试器 vs print()

| 场景 | 推荐方式 |
|------|----------|
| 快速查看变量值 | `print()` |
| 理解程序执行流程 | 调试器 |
| 排查复杂逻辑错误 | 调试器 |
| 生产环境问题定位 | 日志 + traceback |
| 循环中的问题 | 条件断点 |

### 6.2 调试技巧

**1. 二分查找法**
```python
# 在函数中间添加断点，逐步缩小问题范围
def buggy_function(data):
    # 前半部分正确？
    part1 = process_first_half(data)
    
    breakpoint()  # 检查 part1
    
    # 后半部分有问题？
    result = process_second_half(part1)
    return result
```

**2. 条件断点**
```python
# 在循环中找到特定值
for item in large_list:
    if item.id == target_id:
        print(f"Found: {item}")  # 改用条件断点更高效
    process(item)
```

**3. 事后调试**
```python
import pdb
import traceback

def excepthook(type, value, tb):
    """全局异常钩子，异常时自动进入 pdb"""
    traceback.print_exception(type, value, tb)
    pdb.post_mortem(tb)

sys.excepthook = excepthook
```

### 6.3 调试与测试的关系

- **单元测试**：定义正确行为，用测试验证
- **调试器**：理解错误原因，定位问题位置
- **两者结合**：测试驱动开发（TDD）先用测试定义行为，调试器解决偶发问题

---

## 7. 常见调试场景

### 7.1 变量值不符合预期

```python
import pdb

def calculate(items):
    total = 0
    for item in items:
        pdb.set_trace()  # 逐个检查 item
        total += item.price * item.quantity
    return total
```

### 7.2 函数返回值错误

```python
def find_user(users, user_id):
    pdb.set_trace()  # 检查输入参数
    for user in users:
        if user.id == user_id:
            return user
    return None  # 可能是这里的问题
```

### 7.3 异常信息不明确

```python
try:
    complex_operation()
except Exception as e:
    import traceback
    print(f"异常类型: {type(e).__name__}")
    print(f"异常信息: {e}")
    traceback.print_exc()
    pdb.post_mortem()
```

---

## 8. 课后练习

### 练习 1: pdb 基础

编写一个函数计算斐波那契数列，使用 pdb 单步调试观察变量变化。

### 练习 2: breakpoint() 配置

创建一个脚本，使用 `breakpoint()`，尝试配置不同的调试器（pdb/ipdb）。

### 练习 3: traceback 分析

编写代码捕获异常，使用 `traceback` 模块将异常信息保存到日志文件。

### 练习 4: IDE 调试

使用 VS Code 或 PyCharm 调试一个包含多个函数的 Python 文件，练习设置断点、单步执行、查看变量。

### 练习 5: uv 项目

使用 `uv` 创建一个新项目，添加依赖，运行测试。

---

## 9. 知识点总结

| 知识点 | 级别 | 说明 |
|--------|------|------|
| pdb.set_trace() | L1 | 在代码中插入断点 |
| breakpoint() | L1 | Python 3.7+ 内置断点函数 |
| traceback 模块 | L1 | 异常追踪信息处理 |
| sys.last_traceback | L2 | 访问最后异常信息 |
| 条件断点 | L2 | 在特定条件下触发断点 |
| post_mortem 调试 | L3 | 异常发生后调试 |
| IDE 调试器 | L2 | VS Code/PyCharm 可视化调试 |
| uv 工具链 | L2 | 现代化 Python 包管理 |

---

## 10. 参考资源

- [Python pdb 文档](https://docs.python.org/3/library/pdb.html)
- [Python traceback 文档](https://docs.python.org/3/library/traceback.html)
- [uv 官方文档](https://github.com/astral-sh/uv)
- [VS Code Python 调试](https://code.visualstudio.com/docs/python/debugging)
