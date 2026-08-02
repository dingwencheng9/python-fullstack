# tests/ - 单元测试

**用途**：验证 L09 学员管理系统参考答案是否满足核心业务行为，并防止不同 lesson 的同名 `solutions` 包互相污染。

运行方式：

```bash
cd stage0-python-basics/lessons/L10-basics-project
uv run pytest tests/ -q
```

需要查看详细用例名称时：

```bash
uv run pytest tests/ -v
```

## 测试覆盖

| 测试文件 | 验证内容 |
|----------|----------|
| `test_student_manager.py` | `Student` 序列化、CRUD、部分更新、搜索、统计、边界值和参数化场景 |
| `conftest.py` | 按物理路径加载当前课程 `solutions` 包，避免跨课程导入污染 |

## 覆盖重点

- `Student`：创建、`to_dict()`、`from_dict()`、属性一致性。
- `add_student()`：正常添加和重复学号拒绝。
- `get_student()`：存在与不存在两种路径。
- `remove_student()`：成功删除和删除不存在学员。
- `update_student()`：完整更新、部分更新、更新不存在学员。
- `list_students()`：空列表、正常列表、返回副本。
- `search_by_name()`：部分匹配、大小写不敏感、无结果、特殊字符。
- `get_statistics()`：正常统计和空管理器统计。
- 参数化测试：多种学号格式、批量添加删除。

## 后续可扩展

- 增加 JSON 持久化测试，使用 pytest `tmp_path` 避免污染仓库。
- 增加数据验证测试，例如空学号、空姓名、非法年龄。
- 增加排序功能测试，例如按姓名、年龄、学号排序。
- 增加 CLI 命令解析测试，把交互逻辑拆成可测试函数。
