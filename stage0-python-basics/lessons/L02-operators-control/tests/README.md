# tests/ - 单元测试

**用途**：自动验证 L02 的基础概念是否掌握。

从本课目录运行：

```bash
uv run pytest tests/ -q
```

从仓库根目录运行：

```bash
uv run pytest stage0-python-basics/lessons/L02-operators-control/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_01_operators.py` | 算术、比较、逻辑、位运算、赋值、优先级 |
| `test_02_control_flow.py` | if/elif/else、while、for、range、break、continue |
| `test_03_new_content.py` | enumerate、zip、for-else、match-case |
