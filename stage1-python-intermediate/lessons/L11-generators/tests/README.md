# tests/ - L11 单元测试

本目录测试 `solutions/` 中参考答案的关键行为，共 27 个用例。

```bash
uv run pytest stage1-python-intermediate/lessons/L11-generators/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
| -------- | -------- |
| `test_iterator_protocol.py` | 自定义 FibonacciIterator、Range、Counter 的迭代结果与边界 |
| `test_generator_exercises.py` | 斐波那契生成、递归展平、分块、素数、pairwise 和滑动窗口 |
| `test_itertools_exercises.py` | 截断、累积和、连续分组、组合、排列与不等长交替合并 |
| `conftest.py` | 使用 `importlib` 按物理路径加载本课 solutions，避免污染全局 `sys.path` |

## 维护提示

- 如果新增练习函数，请同步补齐 `solutions/`、`tests/` 和本 README 的映射关系。
- 若测试需要检查练习文件本身，应新增独立加载逻辑，避免和当前“测试参考答案”的策略混淆。
