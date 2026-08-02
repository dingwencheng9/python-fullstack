# tests/ - L10 单元测试

本目录测试 `solutions/` 中参考答案的关键行为，共 18 个用例。

```bash
uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
| -------- | -------- |
| `test_type_narrowing.py` | `TypeGuard` 对字符串列表/字典列表的真假判断，以及字符串过滤结果 |
| `test_protocol.py` | `Circle` / `Square` 是否满足 `Drawable`、`Resizable`，以及可调整对象处理边界 |
| `test_generic_constraints.py` | `Container`、`NumberBox` 的读写、数值运算、非法类型与容器合并 |
| `conftest.py` | 使用 `importlib` 按物理路径加载本课 solutions，避免污染全局 `sys.path` |

## 运行建议

- 修改练习或参考答案后先跑本目录测试。
- 若后续增加新练习，请同步补齐：`exercises/`、`solutions/`、`tests/` 和本 README 的映射关系。
