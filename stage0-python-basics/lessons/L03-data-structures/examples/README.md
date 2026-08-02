# examples/ - 示例代码

**用途**：展示 L03 核心数据结构的具体用法。每个文件都可以独立运行。

从本课目录运行：

```bash
uv run python examples/01_list.py
```

或进入 examples 目录运行：

```bash
cd stage0-python-basics/lessons/L03-data-structures/examples
python 01_list.py
```

## 文件清单

| 文件 | 说明 |
|------|------|
| `01_list.py` | 列表创建、索引、切片、增删改查、列表推导式 |
| `02_dict.py` | 字典创建、访问、增删改、遍历、字典推导式 |
| `03_set_tuple.py` | 集合去重、集合运算、元组解包与不可变性 |
| `04_comprehension_vs_generator.py` | 列表推导式与生成器表达式的内存和行为差异 |
| `05_nested_data_parsing.py` | 嵌套 API 响应解析、`.get()` 防御访问、`match/case`、字典合并 |

> 📝 **浅拷贝陷阱**（原 `06_shallow_copy_trap.py`）：L03 的浅拷贝行为（`a[:]` 和 `list(a)`）在嵌套列表中会出现引用共享问题。该陷阱会在 **L08 异常与调试** 中通过 `copy.deepcopy()` 完整讲解。
