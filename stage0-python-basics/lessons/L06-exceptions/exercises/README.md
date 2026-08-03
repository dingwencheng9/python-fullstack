# exercises/ - 练习题

**用途**：通过三个递进练习掌握基础异常捕获、多异常分流和自定义异常设计。

运行方式：

```bash
cd stage0-python-basics/lessons/L09-exceptions
python3 exercises/01_basic_handling.py
```

## 文件清单

| 文件 | 任务 | 对应答案 |
|------|------|----------|
| `01_basic_handling.py` | 实现 `safe_divide`、`safe_parse_int`、`safe_getitem` | `solutions/basic_handling.py` |
| `02_multiple_exceptions.py` | 处理数字转换、除零、类型错误，并校验用户输入 | `solutions/multiple_exceptions.py` |
| `03_custom_exceptions.py` | 定义年龄/邮箱异常，完成用户注册校验 | `solutions/custom_exceptions.py` |

## 建议完成顺序

1. 先完成 `01_basic_handling.py`：练习最小可用的 `try/except`。
2. 再完成 `02_multiple_exceptions.py`：针对不同异常给出不同返回或错误信息。
3. 最后完成 `03_custom_exceptions.py`：把业务规则失败表达成清晰的异常类型。

## 验证方式

完成后运行：

```bash
uv run pytest tests/ -q
```

## 实现提示

- 捕获异常时尽量写具体类型，例如 `except ZeroDivisionError`。
- `safe_*` 函数遇到预期错误时可以返回 `None`，但不要吞掉和任务无关的异常。
- 用户名建议先 `strip()` 再判断是否为空。
- 注册用户时可以收集多个校验错误，再一次性抛出 `ValueError`，这样用户能看到完整反馈。
