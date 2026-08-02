# exercises/ - L12 练习题

练习用于把高级特性转成可运行代码。当前练习脚本都带有 `__main__` 自检，可直接运行获取快速反馈。

```bash
cd stage1-python-intermediate/lessons/L12-advanced-features
python exercises/01_decorators.py
```

## 文件清单

| 文件 | 练习目标 | 对应参考答案/测试 |
| ---- | -------- | ----------------- |
| `01_decorators.py` | 实现日志、重试、记忆化和参数验证装饰器 | `solutions/solution_01_decorators.py` / `tests/test_decorators.py` |
| `02_context_managers.py` | 实现事务、计时、输出重定向和延迟资源上下文管理器 | `solutions/solution_02_context_managers.py` / `tests/test_context_managers.py` |

## 建议流程

1. 先运行 `examples/`，观察装饰器和上下文管理器的执行顺序。
2. 完成练习脚本并运行自检。
3. 对照 `solutions/`，比较异常处理和资源清理边界。
4. 运行 pytest 验证参考答案行为。

```bash
uv run pytest tests -q
```

> 注：练习脚本侧重概念自检；pytest 当前验证的是 `solutions/` 中更完整的参考答案实现。
