# examples/ - 示例代码

**用途**：展示 L09 文本文件、路径、JSON 和 CSV 的具体用法。每个示例都可以独立运行。

从本课目录运行：

```bash
uv run python examples/01_read_write.py
```

或进入 examples 目录运行：

```bash
cd stage0-python-basics/lessons/L09-file-operations/examples
python 01_read_write.py
```

## 文件清单

| 文件 | 说明 |
|------|------|
| `01_read_write.py` | 文本文件写入、读取、逐行遍历和追加写入 |
| `02_pathlib.py` | `pathlib.Path` 路径对象、读写、属性和目录遍历 |
| `03_json.py` | JSON 对象和列表的序列化/反序列化 |
| `04_csv_files.py` | CSV 普通读写、`DictReader`、`DictWriter` 和成绩统计 |

> 说明：当前示例默认使用临时目录创建演示文件，运行结束后自动清理，避免在课程目录留下测试文件。
