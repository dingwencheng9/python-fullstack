# solutions/ - 参考解答

**用途**：展示调试练习的参考解决方案。

> ⚠️ **建议**：先自己调试尝试，遇到困难再看 `solutions/`。

## 文件清单

| 文件 | 说明 |
|------|------|
| `01_pdb_solution.py` | calculate_average 和 find_middle_element 的正确实现 |
| `02_traceback_solution.py` | 错误日志和异常处理的参考实现 |

## 运行方式

```bash
uv run python solutions/01_pdb_solution.py
uv run python solutions/02_traceback_solution.py
```

## 验证方式

```bash
uv run pytest tests/ -q
```
