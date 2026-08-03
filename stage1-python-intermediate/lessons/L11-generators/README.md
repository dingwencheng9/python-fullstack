# L11: 迭代器与生成器

> **课程编号**: L11
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 6 小时
> **前置课程**: L04 函数与模块
> **核心内容**: 迭代器协议、`yield`、惰性求值、生成器管道、`itertools`

---

## 🎯 课程定位

本课承接 L10 的类型意识，进入 Python “按需产生数据”的核心能力：迭代器与生成器。它们是处理大文件、无限序列、数据管道和高效组合迭代的基础，也为后续异步流式处理打底。

完成本课后，你将能够：

- 解释可迭代对象、迭代器和生成器之间的关系。
- 手写实现 `__iter__()` / `__next__()`，并正确抛出 `StopIteration`。
- 使用 `yield` 和 `yield from` 构建惰性数据流。
- 使用生成器表达式替代一次性列表，降低内存占用。
- 使用 `itertools` 处理切片、累积、分组、组合、排列和交替合并。
- 识别生成器“一次性消费”、无限迭代器和分块处理中的常见陷阱。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L11-generators

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
python examples/01_generator_basics.py
python examples/02_itertools.py

# 3) 完成练习并自检
python exercises/01_iterator_protocol.py
python exercises/02_generator_exercises.py
python exercises/03_itertools_exercises.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | 生成器基础 | `lesson.md` Part 1-3、`examples/01_generator_basics.py` | `yield` 暂停/恢复、生成器表达式、一次性消费 |
| 2 | 迭代器协议 | Part 4、`exercises/01_iterator_protocol.py` | `__iter__()`、`__next__()`、`StopIteration` |
| 3 | 数据管道 | Part 5、`exercises/02_generator_exercises.py` | 分块、展平、链式惰性处理 |
| 4 | itertools | Part 6、`examples/02_itertools.py`、`exercises/03_itertools_exercises.py` | `islice`、`accumulate`、`groupby`、`zip_longest` |
| 5 | 高级技巧 | Part 7 | `yield from`、`send()`、状态管理 |
| 6 | 测试验证 | `tests/` | 27 个用例覆盖参考答案关键行为 |

---

## 📁 目录结构

| 目录 | 用途 |
| ---- | ---- |
| [examples/](examples/) | 可直接运行的示例：生成器基础与 itertools 常用模式 |
| [exercises/](exercises/) | 3 个动手练习：迭代器协议、生成器函数、itertools 实战 |
| [solutions/](solutions/) | 与测试对齐的参考答案，建议完成练习后再查看 |
| [tests/](tests/) | 27 个 pytest 用例，验证参考答案行为 |
| [lesson.md](lesson.md) | 完整教程与扩展说明 |

---

## ✅ 完成标准

- [ ] 能说明 iterable、iterator、generator 的区别。
- [ ] 能实现至少一个自定义迭代器，并在结束时抛出 `StopIteration`。
- [ ] 能用 `yield` / `yield from` 构建可组合的生成器。
- [ ] 能用 `itertools.islice()` 安全处理无限或大型迭代器。
- [ ] 能解释生成器为什么不能随意 `len()`、索引访问或重复遍历。
- [ ] 本课测试通过：`uv run pytest stage1-python-intermediate/lessons/L11-generators/tests -q`。

---

## 🧪 测试与检查

```bash
# 定向测试
uv run pytest stage1-python-intermediate/lessons/L11-generators/tests -q

# 语法/导入层面检查
python -m py_compile   stage1-python-intermediate/lessons/L11-generators/examples/*.py   stage1-python-intermediate/lessons/L11-generators/exercises/*.py   stage1-python-intermediate/lessons/L11-generators/solutions/*.py   stage1-python-intermediate/lessons/L11-generators/tests/*.py
```

---

## 🔗 下一步

完成本课后继续学习：

- [L12: 生成器进阶](../L12-generator-advanced/README.md)
- 后续 L14 的异步编程会继续使用“惰性流式处理”的思维模型。
