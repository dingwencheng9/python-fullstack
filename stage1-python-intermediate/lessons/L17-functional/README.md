# L17: 函数式编程

> **课程编号**: L17
> **所属阶段**: Stage 1 - Python 进阶
> **预计时长**: 7 小时
> **前置课程**: L11 迭代器与生成器
> **核心内容**: lambda、`map`/`filter`/`reduce`、函数组合、偏函数、柯里化、生成器与 `itertools`

---

## 🎯 课程定位

本课聚焦 Python 中的函数式编程工具：把函数作为值传递、组合和复用，用惰性迭代处理数据流，并通过偏函数/柯里化减少重复参数。本课承接 L11 的生成器、L12 的装饰器和 L14 的任务组合思维，为数据转换、管道处理和声明式代码风格打基础。

完成本课后，你将能够：

- 使用 `lambda` 编写短小的一次性函数。
- 使用 `map()`、`filter()`、`reduce()` 构建数据处理流程。
- 实现 `compose()` 与 `pipe()`，理解从右到左/从左到右组合的差异。
- 使用 `functools.partial()` 创建特定场景的专用函数。
- 理解柯里化的基本形式和适用边界。
- 使用生成器表达式和 `itertools` 构建惰性、可组合的数据管道。

---

## 🚀 快速开始

从仓库根目录运行：

```bash
cd stage1-python-intermediate/lessons/L17-functional

# 1) 阅读完整教程
less lesson.md

# 2) 运行示例
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done

# 3) 完成练习并自检
python exercises/01_functional_pipeline.py
python exercises/02_data_transformation.py
python exercises/03_compose_decorator.py

# 4) 运行单元测试
uv run pytest tests -q
```

---

## 📚 推荐学习路径

| 顺序 | 内容 | 对应文件 | 重点 |
| ---- | ---- | -------- | ---- |
| 1 | lambda 与高阶函数 | `examples/01_lambda_basics.py` | 函数作为值、排序 key、简单回调 |
| 2 | map/filter/reduce | `examples/02_map_filter_reduce.py` | 数据流转换、过滤、归约 |
| 3 | 函数组合与管道 | `examples/03_composition.py`、`exercises/01_functional_pipeline.py` | `compose` vs `pipe` |
| 4 | 偏函数与柯里化 | `examples/04_partial_functions.py`、`examples/05_currying.py`、`exercises/02_data_transformation.py` | 固定参数、分步传参 |
| 5 | 惰性函数式处理 | `examples/06_generator_functional.py`、`examples/07_itertools_functional.py` | 生成器、`itertools`、内存效率 |
| 6 | 装饰器组合 | `exercises/03_compose_decorator.py` | 用函数式方式组合横切逻辑 |
| 7 | 自动化验证 | `tests/` | 23 个测试用例覆盖核心行为 |

---

## 📁 目录结构

| 路径 | 用途 |
| ---- | ---- |
| [lesson.md](lesson.md) | 完整教程与概念说明 |
| [examples/](examples/) | 可独立运行的示例代码 |
| [exercises/](exercises/) | 学员练习与脚本自检 |
| [solutions/](solutions/) | 参考答案 |
| [tests/](tests/) | pytest 单元测试 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解函数式编程的核心概念。
- [ ] 运行 7 个示例文件，并能解释每个示例的关键输出。
- [ ] 完成 3 个练习文件，并通过脚本自检。
- [ ] 能解释 `compose()`、`pipe()`、`partial()`、柯里化和惰性迭代的适用场景。
- [ ] 通过 `uv run pytest tests -q`。

---

## 🧪 检查命令

```bash
# Python 语法/导入检查
python3 -m py_compile examples/*.py exercises/*.py solutions/*.py tests/*.py

# 示例运行
for f in examples/*.py; do
  echo "== $f =="
  python "$f"
done

# 练习自检
for f in exercises/*.py; do
  echo "== $f =="
  python "$f"
done

# 单元测试
uv run pytest tests -q
```

---

## 🔗 下一步

完成本课后继续学习：

- [L16: 正则表达式](../L16-regex/README.md)
- L16 会聚焦文本匹配、提取、替换和正则表达式调试。
