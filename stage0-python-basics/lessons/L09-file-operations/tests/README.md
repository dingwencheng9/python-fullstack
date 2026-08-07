# tests/ - 单元测试

**用途**：自动验证 L09 的文件读写、日志解析和大文件处理行为。

从本课目录运行：

```bash
uv run pytest tests/ -q
```

从仓库根目录运行：

```bash
uv run pytest stage0-python-basics/lessons/L09-file-operations/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_files.py` | 基础文本读写、编码、二进制文件、上下文管理器、JSON、追加写入、临时文件 |
| `test_large_file.py` | 流式读取、分块读取、空文件、单字节文件和基础 I/O 性能 |
| `test_log_parser.py` | `solutions/01_solution.py` 的日志统计、ERROR 行提取、缺失文件和中文内容 |
| `conftest.py` | 按物理路径加载本课 `solutions`，避免与其他课程同名包冲突 |
