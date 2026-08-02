# solutions/ - 参考答案

**用途**：提供三个异常处理练习的参考实现，并展示可测试、可复用的错误处理边界。

> ⚠️ 建议先独立完成 exercises，再查看本目录。

## 文件清单

| 文件 | 对应练习 | 说明 |
|------|----------|------|
| `basic_handling.py` | `01_basic_handling.py` | 基础安全包装函数：除法、整数解析、列表索引 |
| `multiple_exceptions.py` | `02_multiple_exceptions.py` | 多异常分流、用户名/年龄输入校验 |
| `custom_exceptions.py` | `03_custom_exceptions.py` | `InvalidAgeError`、`InvalidEmailError` 与注册校验 |
| `__init__.py` | - | 统一导出答案模块和自定义异常类 |

## 使用方式

从课程目录运行：

```bash
python3 - <<'PY'
from solutions import InvalidAgeError, custom_exceptions, multiple_exceptions

print(multiple_exceptions.validate_user_input(" alice ", "25"))

try:
    custom_exceptions.register_user("", -5, "invalid")
except ValueError as exc:
    print(exc)

print(InvalidAgeError.__name__)
PY
```

也可以直接运行测试：

```bash
uv run pytest tests/ -q
```

## 设计说明

- `multiple_exceptions.validate_user_input()` 会规范化用户名，空白用户名视为非法。
- 年龄字符串会转换为整数，并最终以规范化字符串形式返回。
- `custom_exceptions.register_user()` 会收集用户名、年龄、邮箱的多个错误后统一抛出，避免用户反复提交才能发现所有问题。
- `InvalidAgeError` 与 `InvalidEmailError` 继承 `ValueError`，因为它们表达的是“值不符合业务规则”。
