# tests/ - 单元测试

**用途**：验证 L08 异常处理参考答案是否满足预期行为，并防止不同 lesson 的同名 `solutions` 包互相污染。

运行方式：

```bash
cd stage0-python-basics/lessons/L09-exceptions
uv run pytest tests/ -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_exceptions.py` | 基础异常捕获、多异常处理、输入规范化、自定义异常和注册校验 |
| `conftest.py` | 按物理路径加载当前课程 `solutions` 包，避免跨课程导入污染 |

## 覆盖重点

- `safe_divide()`：正常除法、除零、负数、小数结果。
- `safe_parse_int()`：合法整数、负数、非法字符串、浮点数字符串。
- `safe_getitem()`：正常索引、负索引、越界索引。
- `process_number()`：数字转换失败、除零、类型错误。
- `validate_user_input()`：用户名去空白、空用户名、非法年龄、年龄范围。
- 自定义异常：`InvalidAgeError`、`InvalidEmailError` 及顶层导出。
- `register_user()`：成功注册与多个错误一次性收集。

## 后续可扩展

- 增加文件读写场景，验证 `finally` 或上下文管理器释放资源。
- 增加异常链测试，检查 `__cause__` 是否保留根因异常。
- 增加参数化测试，减少重复用例并覆盖更多边界值。
