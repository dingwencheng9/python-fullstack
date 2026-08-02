# exercises/ - 练习题

**用途**：巩固函数与模块知识点。建议先独立完成，再查看 `solutions/`。

从本课目录运行练习：

```bash
uv run python exercises/01_functions.py
```

## 文件清单

| 文件 | 说明 | 参考答案/验证 |
|------|------|---------------|
| `01_functions.py` | 函数基础：阶乘、斐波那契、最大值、过滤偶数 | 可运行文件内自测；相关基础函数也可参考 `solutions/calculator.py` 的函数组织方式 |
| `02_modules.py` | 模块与包：`__all__`、公开/私有 API、`dataclass`、入口点 | 可运行文件内自测；相关模块 API 可参考 `solutions/validators.py` 和 `solutions/__init__.py` |

## 学习路径

1. **01_functions.py** — 先关注函数参数、返回值、递归终止条件和异常处理。
2. **02_modules.py** — 再关注模块 API 设计、`__all__`、数据类和入口点模式。

> 说明：L04 的 `solutions/` 当前提供的是“模块组织参考答案”，不是对 `exercises/` 每个函数的逐行一一对应答案。
