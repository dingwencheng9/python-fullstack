# L04: 函数与模块

> **课程编号**: L04<br>
> **所属阶段**: Stage 0 - Python 编程基础<br>
> **定位**: 在数据结构基础上，学习如何用函数封装逻辑，并用模块/包组织代码，为后续文件操作、面向对象和项目化开发打基础。

---

## 📋 前置要求

- 掌握 L03 数据结构（list、dict、tuple、set）

---

## 🎯 学习目标

完成本课后，你应该能够：

- 定义和调用函数，并理解参数、默认值、返回值和类型注解
- 使用 `*args`、`**kwargs` 处理可变数量参数
- 理解局部作用域、全局作用域和命名空间
- 使用 `if __name__ == "__main__"` 编写可导入、可运行的模块
- 区分模块、包、子包和 `__init__.py` 的作用
- 理解 `import`、`from ... import ...`、别名导入和 `__all__` 的差异
- 将一组相关函数组织成可测试、可复用的小模块

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L04-functions-modules
```

运行示例：

```bash
uv run python examples/00_demo.py
uv run python examples/06_type_annotations.py
uv run python examples/07_lambda.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

如果你当前环境没有使用 `uv`，也可以临时使用：

```bash
python examples/00_demo.py
python -m pytest tests/ -q
```

---

## 📚 学习路径

```text
1. 阅读 lesson.md，理解函数封装和模块组织的主线
2. 运行 examples/*.py，观察函数、模块、包和 __all__ 的行为
3. 完成 exercises/*.py，练习函数实现和模块 API 设计
4. 对照 solutions/*.py，检查参考模块的组织方式
5. 运行 pytest tests/，验证参考答案行为
```

建议顺序：

```text
函数定义 → 参数/返回值 → 作用域 → 模块导入 → 包与 __init__.py → __name__ 入口点 → __all__ 导出控制 → 标准库
```

---

## 📁 目录结构

| 目录 | 用途 |
|------|------|
| [lesson.md](lesson.md) | 完整教程 |
| [examples/](examples/) | 示例代码，可直接运行 |
| [exercises/](exercises/) | 练习题，建议先独立完成 |
| [solutions/](solutions/) | 参考答案模块 |
| [tests/](tests/) | 单元测试，用于验证参考答案 |

---

## ✅ 完成标准

- [ ] 阅读 `lesson.md`，理解函数、模块和包的基本概念
- [ ] 至少运行 5 个示例文件
- [ ] 完成 `exercises/` 中的 2 个练习文件
- [ ] 能解释 `__name__ == "__main__"` 为什么重要
- [ ] 能解释 `__all__` 与下划线私有命名约定的区别
- [ ] 能通过 `uv run pytest tests/ -q`

---

## 🔗 下一步

完成本课后继续学习：

- [L05: 调试工具](../L05-debugging-tools/README.md)
