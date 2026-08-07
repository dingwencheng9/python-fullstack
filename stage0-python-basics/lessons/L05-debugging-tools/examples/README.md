# examples/ - 示例代码

**用途**：展示 L05 调试工具的具体用法。每个示例文件都可以独立运行。

从本课目录运行：

```bash
uv run python examples/00_pdb_basics.py
```

## 文件清单

| 文件 | 说明 |
|------|------|
| `00_pdb_basics.py` | pdb.set_trace() 断点调试基础 |
| `01_breakpoint.py` | breakpoint() 内置函数及其配置 |
| `02_traceback_analysis.py` | traceback 模块分析异常信息 |
| `03_ide_debug_demo.py` | IDE 调试技巧演示 |

## 学习建议

1. **先阅读** 示例代码，理解调试工具的使用方法
2. **再运行** `uv run python examples/00_pdb_basics.py`，观察 pdb 输出
3. **尝试修改** 示例代码，自己添加断点调试
