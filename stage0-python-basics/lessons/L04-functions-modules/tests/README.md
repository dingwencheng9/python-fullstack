# tests/ - 单元测试

**用途**：自动验证 L04 的参考模块公开 API 是否可用。

从本课目录运行：

```bash
uv run pytest tests/ -q
```

从仓库根目录运行：

```bash
uv run pytest stage0-python-basics/lessons/L04-functions-modules/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_solutions.py` | `solutions` 包导出的计算器函数和验证器函数 |
| `conftest.py` | 按物理路径加载本课 `solutions` 包，避免与其他课程同名包冲突 |
