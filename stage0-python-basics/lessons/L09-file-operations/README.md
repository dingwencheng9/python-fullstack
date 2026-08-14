# L09: 文件操作

> **课程编号**: L09<br>
> **所属阶段**: Stage 0 - Python 编程基础<br>
> **定位**: 在异常处理基础上，学习如何安全、稳定地读写文本、JSON、CSV 和大文件，为后续数据处理、日志分析和项目持久化能力打基础。

---

## 📋 前置要求

- 掌握 L06 异常处理（try/except）
- 理解 L07 面向对象基础中的上下文管理器概念（`with` 语句）
- 可选：了解 L08 魔术方法中的 `__enter__`/`__exit__` 实现

---

## 🎯 学习目标

完成本课后，你应该能够：

- 使用 `open()` 与 `with` 语句安全读写文件
- 理解 `r/w/a/x/b/+` 等常见文件模式
- 始终显式指定 `encoding="utf-8"` 处理文本文件
- 使用 `pathlib.Path` 完成路径拼接、存在性检查和读写操作
- 使用 `json` 模块读写结构化配置数据
- 使用 `csv.reader`、`csv.DictReader`、`csv.DictWriter` 处理表格数据
- 通过流式读取处理大文件，避免一次性读入造成内存压力
- 编写日志解析器并处理文件不存在等异常场景

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L09-file-operations
```

运行示例：

```bash
uv run python examples/01_read_write.py
uv run python examples/03_json.py
uv run python examples/04_csv_files.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

如果你当前环境没有使用 `uv`，也可以临时使用：

```bash
python examples/01_read_write.py
python -m pytest tests/ -q
```

---

## 📚 学习路径

```text
1. 阅读 lesson.md，理解文件读写、路径、编码和结构化文件主线
2. 运行 examples/*.py，观察文本/JSON/CSV 文件的读写方式
3. 完成 exercises/*.py，练习日志解析和 CSV 写入
4. 对照 solutions/*.py，检查参考实现
5. 运行 pytest tests/，验证文件操作和日志解析行为
```

建议顺序：

```text
文本读写 → pathlib 路径操作 → 编码问题 → JSON 文件 → CSV 文件 → 大文件流式处理 → 日志解析练习
```

---

## 📁 目录结构

| 目录 | 用途 |
|------|------|
| [lesson.md](lesson.md) | 完整教程 |
| [examples/](examples/) | 示例代码，可直接运行，默认使用临时目录避免污染课程目录 |
| [exercises/](exercises/) | 练习题，建议先独立完成 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | 单元测试，用于验证文件操作与日志解析 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解文本、JSON、CSV 和大文件处理方法
- [ ] 至少运行 4 个示例文件
- [ ] 完成 `exercises/` 中的 2 个练习
- [ ] 能解释为什么文本文件应显式指定 `encoding="utf-8"`
- [ ] 能解释为什么 CSV 写入建议使用 `newline=""`
- [ ] 能通过 `uv run pytest tests/ -q`

---

## 🔗 下一步

完成本课后继续学习：

- [P01: 学员管理系统](../P01-student-manager/README.md)

> 📖 **里程碑**：P01 是 Stage 0 的综合项目，将整合语法、数据结构、函数、文件操作、OOP 和异常处理知识。

完成本课后继续学习：

- [P01: 学员管理系统](../P01-student-manager/README.md)
