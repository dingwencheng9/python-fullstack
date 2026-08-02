# tests/ - L13 单元测试

本目录用于自动验证描述符参考答案。

```bash
cd stage1-python-intermediate/lessons/L13-descriptors
uv run pytest tests -q
```

## 测试覆盖

| 测试文件 | 用例数 | 验证内容 |
| -------- | ------ | -------- |
| `test_descriptors.py` | 7 | 正数验证、范围验证、懒加载缓存、大写转换、类级访问描述符对象 |

## 加载策略

`conftest.py` 使用 `importlib.util.spec_from_file_location()` 按物理路径加载 `solutions/`，避免不同课程中同名 `solutions` 包互相污染。

## 维护提示

- 新增描述符练习时，请同步更新 `solutions/`、本 README 和测试覆盖表。
- 如果更改异常消息，请同步检查 `pytest.raises(..., match=...)` 的正则断言。
