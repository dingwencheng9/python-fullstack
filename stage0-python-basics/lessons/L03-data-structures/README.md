# L03: 数据结构

> **课程编号**: L03<br>
> **所属阶段**: Stage 0 - Python 编程基础<br>
> **定位**: 在 L01/L02 的语法基础上，掌握 Python 最常用的四类容器：`list`、`tuple`、`dict`、`set`，并建立“按场景选择数据结构”的意识。

---

## 🎯 学习目标

完成本课后，你应该能够：

- 使用列表完成有序数据的增删改查、切片和推导式转换
- 使用元组表达不可变、有序、固定结构的数据
- 使用字典表达键值映射，并通过 `.get()` 进行安全访问
- 使用集合完成去重、成员检测和集合运算
- 区分可变对象与不可变对象，避免共享引用和浅拷贝陷阱
- 理解列表推导式与生成器表达式的基本差异
- 能根据“有序/可变/是否去重/是否键值映射”选择合适容器

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L03-data-structures
```

运行示例：

```bash
uv run python examples/01_list.py
uv run python examples/02_dict.py
uv run python examples/04_comprehension_vs_generator.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

如果你当前环境没有使用 `uv`，也可以临时使用：

```bash
python examples/01_list.py
python -m pytest tests/ -q
```

---

## 📚 学习路径

```text
1. 阅读 lesson.md，理解四类核心数据结构的定位
2. 运行 examples/*.py，观察每类容器的行为差异
3. 完成 exercises/*.py，补全数据处理函数
4. 对照 solutions/*.py，检查自己的实现
5. 运行 pytest tests/，验证练习结果
```

建议顺序：

```text
list 基础 → tuple 不可变性 → dict 键值映射 → set 去重/集合运算 → 推导式/生成器 → 嵌套数据解析
```

---

## 📁 目录结构

| 目录 | 用途 |
|------|------|
| [lesson.md](lesson.md) | 完整教程 |
| [examples/](examples/) | 示例代码，可直接运行 |
| [exercises/](exercises/) | 练习题，建议先独立完成 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | 单元测试，用于验证理解 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解 list/tuple/dict/set 的适用场景
- [ ] 至少运行 5 个示例文件
- [ ] 完成 `exercises/` 中的 3 个练习
- [ ] 能解释 `list` 与 `set` 成员检测性能差异
- [ ] 能解释浅拷贝与引用赋值的区别
- [ ] 能通过 `uv run pytest tests/ -q`

---

## 🔗 下一步

完成本课后继续学习：

- [L04: 函数与模块](../L04-functions-modules/README.md)
