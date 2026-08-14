# L05: 调试工具与开发环境

> **课程编号**: L05
> **所属阶段**: Stage 0 - Python 编程基础
> **定位**: 在掌握函数与模块的基础上，学习使用调试工具排查问题，建立良好的调试习惯，提升代码排错能力。

---

## 📋 前置要求

- 掌握 L04 函数与模块（def、参数传递、作用域）
- **补充课程**：可与 L06 并行学习，不影响主线进度

---

## 🎯 学习目标

完成本课后，你应该能够：

- 使用 `pdb` 进行断点调试，单步执行代码
- 使用 `breakpoint()` 内置函数触发调试器
- 使用 `sys.last_traceback` 分析程序崩溃原因
- 理解 `traceback` 模块提供的异常追踪信息
- 配置 Python 调试环境，使用 IDE 内置调试器
- 使用 `uv` 工具链管理项目依赖
- 养成早期调试习惯，避免仅依赖 `print()` 调试

---

## 🚀 快速开始

从仓库根目录执行：

```bash
cd stage0-python-basics/lessons/L05-debugging-tools
```

运行示例：

```bash
uv run python examples/00_pdb_basics.py
uv run python examples/01_breakpoint.py
uv run python examples/02_traceback_analysis.py
```

运行测试：

```bash
uv run pytest tests/ -q
```

---

## 📚 学习路径

```
pdb 基础 → breakpoint() → traceback 分析 → IDE 调试 → uv 工具链
```

建议顺序：

1. 先用 `pdb` 手动调试，理解断点和单步执行
2. 了解 `breakpoint()` 的配置机制
3. 学习分析 `traceback` 信息定位问题
4. 尝试使用 IDE（VS Code/PyCharm）的可视化调试器
5. 学习使用 `uv` 工具链管理项目

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

- [ ] 能使用 `pdb.set_trace()` 设置断点并单步执行
- [ ] 能使用 `breakpoint()` 触发调试器
- [ ] 能阅读 `traceback` 信息定位错误位置
- [ ] 能使用 `sys.last_traceback` 分析崩溃
- [ ] 能在 VS Code 或 PyCharm 中设置断点调试
- [ ] 能使用 `uv` 创建和管理项目

---

## 🔗 前置与后续课程

**前置课程**：
- [L04: 函数与模块](../L04-functions-modules/README.md) - 需要理解函数定义和模块导入

**后续课程**：
- [L06: 异常处理](../L06-exceptions/README.md) - 使用调试技能分析异常

---

## 🔗 下一步

完成本课后继续学习：

- [L06: 异常处理](../L06-exceptions/README.md)

> 📖 **学习路径提示**：L05 是补充课程，可与 L06 并行学习。完成 L05 后继续 L06 的异常处理学习。
