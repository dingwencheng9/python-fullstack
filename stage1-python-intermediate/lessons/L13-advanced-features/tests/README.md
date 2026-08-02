# tests/ - L12 单元测试

本目录测试 `solutions/` 中参考答案的关键行为，共 16 个用例。

```bash
uv run pytest stage1-python-intermediate/lessons/L12-advanced-features/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
| -------- | -------- |
| `test_decorators.py` | 计时输出、重试成功/失败、参数验证、记忆化缓存和调用计数 |
| `test_context_managers.py` | 文件读写、事务提交/回滚、计时器输出、资源获取/释放和事务上下文 |
| `conftest.py` | 使用 `importlib` 按物理路径加载本课 solutions，避免污染全局 `sys.path` |

## 维护提示

- 如果新增练习函数，请同步补齐 `solutions/`、`tests/` 和本 README 的映射关系。
- 若测试需要检查练习文件本身，应新增独立加载逻辑，避免和当前“测试参考答案”的策略混淆。
