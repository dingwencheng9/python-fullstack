# solutions/ - 参考答案

**用途**：展示函数如何组织成可导入、可测试的参考模块。

> ⚠️ **建议**：先独立完成 `exercises/`，遇到困难再看 `solutions/`。

## 文件清单

| 文件 | 说明 |
|------|------|
| `__init__.py` | 通过相对导入重导出公开 API，并定义 `__all__` |
| `calculator.py` | 计算器函数模块：`add`、`subtract`、`multiply`、`divide` |
| `validators.py` | 数据验证模块：邮箱、手机号、用户名验证 |

## 运行方式

从本课目录运行：

```bash
uv run python solutions/calculator.py
uv run python solutions/validators.py
```

也可以通过测试验证公开 API：

```bash
uv run pytest tests/ -q
```

> 说明：当前 `solutions/` 更偏“模块化组织示范”，与 `exercises/01_functions.py`、`02_modules.py` 不是逐函数完全同名映射。
