# solutions/ - 参考答案

**用途**：练习完成后的参考答案。

> ⚠️ **建议**：先独立完成 `exercises/`，遇到困难再看 `solutions/`。

## 文件清单

| 文件 | 对应练习 | 说明 |
|------|----------|------|
| `01_solution.py` | `01_log_parser.py` | 日志级别统计与 ERROR 行提取 |
| `02_csv_writer_solution.py` | `02_csv_writer.py` | 使用 `csv.DictWriter` 保存成绩列表 |
| `03_file_search_solution.py` | `03_file_search.py` | 按扩展名/大小/时间搜索文件 |

## 运行方式

从本课目录运行：

```bash
uv run python solutions/01_solution.py
uv run python solutions/02_csv_writer_solution.py
uv run python solutions/03_file_search_solution.py
```

也可以通过测试验证关键行为：

```bash
uv run pytest tests/ -q
```
