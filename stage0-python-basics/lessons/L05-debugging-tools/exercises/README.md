# exercises/ - 练习题

**用途**：使用调试工具修复代码中的问题。建议先尝试调试，再查看解决方案。

从本课目录运行练习：

```bash
uv run python exercises/01_pdb_practice.py
```

## 文件清单

| 文件 | 说明 |
|------|------|
| `01_pdb_practice.py` | 使用 pdb 调试并修复 calculate_average 和 find_middle_element |
| `02_traceback_practice.py` | 使用 traceback 模块分析异常并实现错误日志 |

## 学习建议

1. **运行练习文件**，观察程序行为
2. **使用 pdb/breakpoint** 单步调试，找到问题
3. **修复代码** 后，再次运行验证
4. **对比 solutions/** 参考实现

## 调试技巧

```bash
# 在练习代码中添加断点调试
python -m pdb exercises/01_pdb_practice.py

# 或者在代码中临时添加 breakpoint()
# breakpoint()
```
