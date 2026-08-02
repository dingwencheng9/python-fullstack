# tests/ - 单元测试

**用途**：自动验证 L01 的基础概念是否掌握。

从本课目录运行：

```bash
uv run pytest tests/ -q
```

从仓库根目录运行：

```bash
uv run pytest stage0-python-basics/lessons/L01-python-core/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_01_hello.py` | Hello World、print/input、基础算术、字符串格式化 |
| `test_02_types.py` | 变量赋值、基础类型、None、类型注解、类型转换、f-string |
