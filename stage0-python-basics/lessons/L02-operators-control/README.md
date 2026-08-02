# L02: 运算符与控制流

> **课程编号**: L02<br>
> **所属阶段**: Stage 0 - Python 编程基础<br>
> **定位**: 在 L01 的变量与类型基础上，掌握表达式计算、条件分支、循环控制和 Python 3.10+ 模式匹配。

---

## 🎯 学习目标

完成本课后，你应该能够：

- 使用算术、比较、逻辑、位运算和赋值运算符
- 理解 `/`、`//`、`%`、`**`、链式比较和逻辑短路
- 编写 `if/elif/else` 条件分支和三元表达式
- 使用 `while`、`for`、`range()` 完成循环任务
- 使用 `break`、`continue` 和循环 `else` 处理搜索与提前退出场景
- 使用 `match/case` 编写简单模式匹配逻辑
- 完成练习并通过 pytest 验证核心概念

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L02-operators-control
```

运行示例：

```bash
uv run python examples/01_arithmetic.py
uv run python examples/07_for_loop.py
uv run python examples/10_match_case.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

如果你当前环境没有使用 `uv`，也可以临时使用：

```bash
python examples/01_arithmetic.py
python -m pytest tests/ -q
```

---

## 📚 学习路径

```text
1. 阅读 lesson.md，理解运算符与控制流主线
2. 运行 examples/*.py，观察每类语法的输出
3. 完成 exercises/*.py，补全练习函数
4. 对照 solutions/*.py，检查自己的实现
5. 运行 pytest tests/，验证理解
```

建议顺序：

```text
算术运算 → 比较运算 → 逻辑运算 → 赋值运算 → 条件语句 → while → for → break/continue → for-else → match/case → enumerate/zip
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

- [ ] 阅读 `lesson.md`，理解运算符、条件语句和循环
- [ ] 至少运行 8 个示例文件
- [ ] 完成 `exercises/` 中的 6 个练习
- [ ] 能解释逻辑短路为什么能避免错误访问
- [ ] 能解释 `break`、`continue` 和循环 `else` 的区别
- [ ] 能通过 `uv run pytest tests/ -q`

---

## 🔗 下一步

完成本课后继续学习：

- [L03: 数据结构](../L03-data-structures/README.md)
