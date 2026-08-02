# exercises/ - 练习题

**用途**：通过一个综合 TODO 练习，把 Stage 0 的核心知识串成完整的学员管理器。

运行方式：

```bash
cd stage0-python-basics/lessons/L10-basics-project
python3 exercises/01_student_manager.py
```

> 注意：练习文件中的方法体需要你先补全；未完成 TODO 时，直接运行只能看到占位逻辑带来的异常或非预期结果。

## 文件清单

| 文件 | 任务 | 对应答案 |
|------|------|----------|
| `01_student_manager.py` | 实现 `Student` 与 `StudentManager` 的增删改查、搜索和统计 | `solutions/student_manager.py` |

## 建议完成顺序

1. 完成 `add_student()`：先处理重复学号。
2. 完成 `get_student()`：练习 `dict.get()`。
3. 完成 `remove_student()`：练习存在性判断和删除。
4. 完成 `update_student()`：只更新非 `None` 的字段。
5. 完成 `list_students()`：返回 `list(self.students.values())`。
6. 完成 `search_by_name()`：使用小写转换做不区分大小写的部分匹配。
7. 对照参考答案补充 `get_statistics()`（如果你想挑战测试覆盖的完整版本）。

## 验证方式

完成后运行：

```bash
uv run pytest tests/ -q
```

## 实现提示

- 内部数据结构建议固定为 `dict[str, Student]`。
- `list_students()` 应返回新的列表，避免调用方直接改坏内部状态。
- `update_student()` 的 `name=None` 和 `age=None` 表示“不更新该字段”。
- 搜索时可以先计算 `keyword = name.lower()`，再遍历所有学员。
- 如果你想让练习版本完全通过测试，需要实现参考答案中的 `get_statistics()`。
