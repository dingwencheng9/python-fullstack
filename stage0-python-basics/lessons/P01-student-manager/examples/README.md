# examples/ - 示例代码

**用途**：把“学员管理系统”拆成几个可独立运行的小示例，逐步展示数据模型、管理器、持久化和 CLI 如何组合。

运行方式：

```bash
cd stage0-python-basics/lessons/P01-student-manager
python3 examples/01_student_basics.py
```

也可以批量运行前三个非交互示例：

```bash
for f in examples/0[1-3]_*.py; do python3 "$f"; done
```

`04_cli_demo.py` 是交互式程序，建议单独运行：

```bash
python3 examples/04_cli_demo.py
```

## 文件清单

| 文件 | 重点 |
|------|------|
| `01_student_basics.py` | 普通类、字典存储、添加/查询/列出/删除 |
| `02_class_student.py` | 手动类定义（`__init__`、`__repr__`、`__eq__`），对比 `dataclass` 等价实现 |
| `03_persistence.py` | `pathlib`、`json`、对象与字典互转、异常兜底 |
| `04_cli_demo.py` | 完整命令行菜单、输入解析、CRUD、保存与加载 |

## 学习建议

- 先理解 `Student` 和 `StudentManager` 的职责边界：一个表示数据，一个管理集合。
- 关注 `student_id` 为什么适合作为字典 key。
- `03_persistence.py` 使用临时目录演示保存/加载，避免在仓库中留下 `students.json`。
- CLI 示例更接近真实项目，但代码更长；建议先完成前三个示例再阅读。
