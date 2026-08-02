# exercises/ - 练习题

**用途**：巩固文件读取、异常处理和 CSV 写入知识点。建议先独立完成，再查看 `solutions/`。

从本课目录运行练习：

```bash
uv run python exercises/01_log_parser.py
```

## 文件清单

| 文件 | 说明 | 参考答案 |
|------|------|----------|
| `01_log_parser.py` | 日志解析器：统计 INFO/ERROR/WARNING，找出 ERROR 行号与内容 | `solutions/01_solution.py` |
| `02_csv_writer.py` | CSV 写入：使用 `csv.DictWriter` 保存成绩列表 | `solutions/02_csv_writer_solution.py` |
| `03_file_search.py` | 目录文件搜索：按扩展名、大小、修改时间搜索文件 | `solutions/03_file_search_solution.py` |

## 学习路径

1. **01_log_parser.py** — 先练习 `with open(..., encoding="utf-8")`、逐行读取和 `FileNotFoundError` 处理。
2. **02_csv_writer.py** — 再练习 `csv.DictWriter`、表头写入、`newline=""` 和结构化数据保存。

> 说明：练习文件中的 `raise NotImplementedError` 是刻意保留的待实现标记，完成函数后应替换为你的实现。
