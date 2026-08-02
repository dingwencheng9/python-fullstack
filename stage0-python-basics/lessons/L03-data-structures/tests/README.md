# tests/ - 单元测试

**用途**：自动验证 L03 的数据结构练习是否掌握。

从本课目录运行：

```bash
uv run pytest tests/ -q
```

从仓库根目录运行：

```bash
uv run pytest stage0-python-basics/lessons/L03-data-structures/tests -q
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_exercises.py` | 正数过滤、词频统计、嵌套字典安全访问、字典合并、生成器表达式、异常边界 |
