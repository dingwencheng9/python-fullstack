# examples/ - 示例代码

**用途**：通过可运行脚本观察异常从发生、捕获、转换到输出 traceback 的全过程。

运行方式：

```bash
cd stage0-python-basics/lessons/L06-exceptions
python3 examples/01_basic_try_except.py
```

也可以批量运行：

```bash
for f in examples/*.py; do python3 "$f"; done
```

> `06_exception_chaining.py` 会有意打印 traceback，用于展示异常链和调试信息；这属于预期输出。

## 文件清单

| 文件 | 重点 |
|------|------|
| `01_basic_try_except.py` | `try/except` 基础、捕获单一异常 |
| `02_multiple_except.py` | 多个 `except` 子句、按异常类型分流 |
| `03_else_finally.py` | `else` 成功路径、`finally` 清理路径 |
| `04_raise_exception.py` | 使用 `raise` 主动抛出内置异常 |
| `05_custom_exceptions.py` | 自定义异常类表达业务规则失败 |
| `06_exception_chaining.py` | `raise ... from ...`、异常链、traceback |

## 学习建议

- 先看输出，再回到代码中定位是哪一行触发了异常。
- 对比 `ValueError` 与 `TypeError`：前者通常是“值不合规”，后者通常是“类型不合规”。
- 重点理解 `finally`：无论成功还是失败，清理逻辑都应执行。
- 观察异常链时，关注“根因异常”和“转换后的业务异常”分别提供了什么信息。
