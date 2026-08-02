# L09: Python 基础实战（Stage 0 收官项目）

> **课程编号**: L09
>
> **所属阶段**: Stage 0 - Python 编程基础
>
> **建议学习时间**: 6-8 小时
>
> **前置课程**: L01-L08 全部基础课程
>
> **后续课程**: Stage 1 / L10 类型系统

---

## 🎯 课程定位

本课是 Stage 0 的综合收官项目：用一个命令行“学员管理系统”把前面 8 课串起来。

你将把变量、控制流、数据结构、函数、文件读写、模块组织、面向对象和异常处理组合成一个小型但完整的项目。重点不只是“写出几个函数”，而是练习如何把代码组织成可维护、可测试、可扩展的程序。

项目核心能力包括：

- 用手动类定义表达学员数据模型（`__init__`、`__repr__`、`__eq__`）；
- 用字典按 `student_id` 管理对象；
- 实现增、删、改、查、搜索和统计；
- 用 JSON 做简单持久化；
- 用 pytest 验证关键业务行为；
- 为进入 Stage 1 的类型系统、迭代器、并发和工程化实践打基础。

---

## ✅ 学习目标

完成本课后，你应该能够：

1. 设计一个简单数据模型，并在对象和字典之间转换。
2. 使用 `dict[str, Student]` 实现高效查询和更新。
3. 为 CRUD 方法设计清晰的返回值语义，例如成功返回 `True`、失败返回 `False`。
4. 使用可选参数实现“只更新传入字段”的部分更新逻辑。
5. 使用列表推导式完成模糊搜索和统计数据整理。
6. 使用 `pathlib`、`json` 和异常处理实现简单文件持久化。
7. 通过 pytest 用例理解项目的行为边界。
8. 说明一个小项目的 README、examples、exercises、solutions、tests 如何协同。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage0-python-basics/lessons/L10-basics-project
python3 examples/01_student_basics.py
python3 examples/02_class_student.py
python3 examples/03_persistence.py
uv run pytest tests/ -q
```

`examples/04_cli_demo.py` 是交互式命令行示例，可单独运行：

```bash
python3 examples/04_cli_demo.py
```

进入后输入 `help` 查看命令，输入 `exit` 退出。

如果不使用 `uv`，也可以在已安装 pytest 的环境中运行：

```bash
python3 -m pytest tests/ -q
```

---

## 📚 推荐学习路径

1. 阅读 `lesson.md` 的项目概述，先明确最终要实现的功能。
2. 运行 `examples/01_student_basics.py`，观察最小可用的对象管理方式。
3. 运行 `examples/02_class_student.py`，理解如何手动实现类的等价功能。
4. 运行 `examples/03_persistence.py`，观察对象列表如何保存为 JSON 并恢复。
5. 可选运行 `examples/04_cli_demo.py`，体验完整 CLI 交互。
6. 完成 `exercises/01_student_manager.py` 中的 TODO。
7. 对照 `solutions/student_manager.py`，比较自己的实现和参考答案。
8. 运行 `uv run pytest tests/ -q`，确认所有核心行为通过。

> 说明：`exercises/01_student_manager.py` 是 TODO 练习模板，直接运行时需要你先补全方法体。

---

## 📁 目录结构

| 目录/文件 | 用途 |
|-----------|------|
| `lesson.md` | 项目需求、实现步骤、测试要点和扩展挑战 |
| [examples/](examples/) | 从基础模型到 CLI 的分步示例 |
| [exercises/](exercises/) | 学员管理器 TODO 练习 |
| [solutions/](solutions/) | 学员管理器参考答案 |
| [tests/](tests/) | pytest 行为验证 |

---

## ✅ 完成标准

- [ ] 能解释 `Student` 类的手动实现（`__init__`、`__repr__`、`__eq__`）与 `dataclass` 的等价关系。
- [ ] 能独立实现 `add_student()`、`get_student()`、`remove_student()`、`update_student()`。
- [ ] 能实现 `list_students()` 返回列表副本，而不是暴露内部字典。
- [ ] 能实现不区分大小写的姓名模糊搜索。
- [ ] 能计算总人数、平均年龄、最小年龄、最大年龄。
- [ ] 能说明 JSON 持久化的基本流程。
- [ ] `uv run pytest tests/ -q` 全部通过。

---

## 🧭 Stage 0 收官检查

如果你能完成本项目，说明你已经具备继续 Stage 1 的基础：

- 能读懂并拆解一个小型项目需求；
- 能把函数、类、数据结构和异常处理组合起来；
- 能用测试判断实现是否满足预期；
- 能通过 README 和示例快速定位学习材料。

---

## 🔗 下一步

恭喜完成 Stage 0！继续进入 [Stage 1: Python 进阶 / L10 类型系统](../../../stage1-python-intermediate/lessons/L10-type-system/README.md)。
