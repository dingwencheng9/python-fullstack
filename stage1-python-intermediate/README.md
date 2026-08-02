# Stage 1: Python 进阶

> **课程定位**: 中级 Python，连接基础与现代化开发
> **课程数量**: 11 课程
> **预计时长**: ~55 小时
> **难度**: ⭐⭐~⭐⭐⭐⭐ (中级)

---

## 🎯 Stage 概述

**Stage 1** 是连接 **Stage 0（Python 基础）** 和 **Stage 2（现代化开发）** 的桥梁课程。通过学习中级 Python 概念和实战项目，为后续高级特性（泛型、异步编程、装饰器工厂）打下坚实基础。

### 适合人群

- ✅ 已完成 Stage 0（Python 编程基础）
- ✅ 掌握 Python 基础语法（变量、控制流、函数、OOP）
- ✅ 希望进阶到现代化 Python 开发
- ✅ 准备学习 FastAPI、异步编程等高级特性

### 学习成果

完成 Stage 1 后，你将能够：

- ✅ 为代码添加完整的类型注解（mypy 兼容）
- ✅ 使用 PEP 695 现代泛型语法
- ✅ 使用生成器处理大数据和无限序列
- ✅ 实现描述符和属性管理
- ✅ 理解闭包并编写装饰器
- ✅ 使用 async/await 进行并发编程
- ✅ 使用函数式编程范式（map/filter/reduce）
- ✅ 使用正则表达式进行文本处理
- ✅ 准备好学习 Stage 2（异步编程、测试驱动开发）

---

## 📚 课程列表（11 个）

| 课程    | 标题                   | 时长  | 难度      | 核心内容                                      | 状态 |
| ------- | ---------------------- | ----- | --------- | -------------------------------------------- | ---- |
| **L10** | Python 类型系统完整指南 | 6h    | ⭐⭐⭐    | 类型注解、Protocol、泛型基础                   | ✅   |
| **L11** | 迭代器与生成器         | 6h    | ⭐⭐⭐    | yield、迭代器协议、惰性计算、itertools       | ✅   |
| **L12** | 生成器进阶             | 4h    | ⭐⭐⭐    | yield from、send()、异步生成器               | ✅   |
| **L13** | Python 高级特性（入门） | 5h    | ⭐⭐⭐    | 闭包基础、装饰器入门、上下文管理器入门      | ✅   |
| **L14** | 装饰器进阶             | 6h    | ⭐⭐⭐⭐  | 带参装饰器、装饰器链、类装饰器              | ✅   |
| **L15** | 描述符与属性           | 5h    | ⭐⭐⭐    | 描述符协议、property、高级属性管理            | ✅   |
| **L16** | 并发编程入门           | 6h    | ⭐⭐⭐⭐  | async/await、asyncio、异步队列               | ✅   |
| **L17** | 函数式编程             | 5h    | ⭐⭐⭐    | Lambda、map/filter/reduce、组合、管道        | ✅   |
| **L18** | 正则表达式             | 2h    | ⭐⭐⭐    | re 模块、模式匹配、文本处理                   | ✅   |

**总计**: 11 课程 | ~55 小时

---

## 🎓 学习路径

### 推荐学习顺序

```
L10 (6h)  →  L11 (6h)  →  L12 (4h)
    ↓
L13 (5h)  →  L14 (6h) →  L15 (5h)
    ↓
L16 (6h)  →  L17 (5h)  →  L18 (2h)
    ↓
Stage 2
```

### 学习计划

**密集学习（6 周）**:

```
Week 1: L10 + L11 (12h) + 练习 (6h)
Week 2: L12 生成器进阶 (4h) + L13 (5h) + 练习 (5h)
Week 3: L14 装饰器进阶 (6h) + L15 (5h) + 练习 (5h)
Week 4: L16 并发编程 (6h) + 练习 (5h)
Week 5: L17 函数式 (5h) + L18 正则 (2h) + 练习 (3h)
Week 6: Stage 1 复习 (4h) + 进入 Stage 2 准备 (4h)
```

**轻松学习（10-12 周）**:

```
Week 1-2: L10 类型系统
Week 3-4: L11 迭代器与生成器
Week 5: L12 生成器进阶
Week 6: L13 Python 高级特性（入门）
Week 7: L14 装饰器进阶
Week 8: L15 描述符与属性
Week 9: L16 并发编程入门
Week 10: L17 函数式编程
Week 11-12: L18 正则 + Stage 1 复习 + Stage 2 准备
```

---

## 🎯 毕业标准

### 必须完成

- [ ] 完成所有 9 个课程
- [ ] 完成每课的练习题
- [ ] 所有代码通过 mypy 类型检查
- [ ] 运行并通过 Stage 1 各课测试

---

## 🚀 快速开始

### 1. 前置要求验证

确保你已完成 Stage 0：

```bash
# 检查 Python 版本
python --version  # 应该 >= 3.13

# 验证 Stage 0 基础知识
uv run pytest stage0-python-basics/lessons -q
```

### 2. 开始第一课

```bash
cd stage1-python-intermediate/lessons/L10-type-system
cat README.md
```

### 3. 运行示例代码

```bash
cd stage1-python-intermediate/lessons/L10-type-system
python examples/01_type_hints_basics.py
```

### 4. 完成练习题

```bash
cd stage1-python-intermediate/lessons/L10-type-system
python exercises/01_type_narrowing.py
```

### 5. 运行测试

```bash
uv run pytest stage1-python-intermediate/lessons/L10-type-system/tests -q
```

---

## 📂 课程结构

每个课程包含：

```
LXX-topic-name/
├── README.md           # 课程概览（5 分钟阅读）
├── lesson.md           # 详细教学内容（1-2 小时学习）
├── examples/           # 示例代码（可直接运行）
│   ├── 01_xxx.py
│   ├── 02_xxx.py
│   └── 03_xxx.py
├── exercises/          # 练习题（动手实践）
│   ├── 01_xxx.py
│   ├── 02_xxx.py
│   └── 03_xxx.py
├── solutions/          # 参考答案（完成练习后查看）
│   ├── 01_xxx.py
│   ├── 02_xxx.py
│   └── 03_xxx.py
└── tests/              # 单元测试（验证理解）
    └── test_xxx.py
```

---

## 💡 学习建议

### 学习方法

1. **先看 README.md**（5 分钟）
   - 了解课程目标
   - 查看核心内容大纲

2. **阅读 lesson.md**（1-2 小时）
   - 系统学习理论知识
   - 理解代码示例
   - 记笔记

3. **运行示例代码**（30 分钟）
   - 逐个运行 examples/
   - 修改代码观察结果
   - 实验不同输入

4. **完成练习题**（1-2 小时）
   - 独立完成 exercises/
   - 先不看答案
   - 遇到困难时查阅 lesson.md

5. **对比参考答案**（30 分钟）
   - 完成练习后查看 solutions/
   - 对比不同实现方式
   - 学习最佳实践

6. **运行测试**（10 分钟）
   - 运行 `pytest tests/ -v`
   - 确保所有测试通过
   - 理解测试用例

### 时间分配

| 活动     | 时间占比 | 说明       |
| -------- | -------- | ---------- |
| 阅读教材 | 30%      | lesson.md  |
| 运行示例 | 20%      | examples/  |
| 练习实践 | 40%      | exercises/ |
| 复习总结 | 10%      | 笔记、测试 |

---

## 🔗 课程衔接

### 从 Stage 0 到 Stage 1

**Stage 0 教了什么**:

- Python 基础语法（变量、控制流、函数）
- 数据结构（list、dict、set）
- 面向对象基础（类、继承）
- 文件操作和异常处理

**Stage 1 在此基础上教什么**:

- 类型系统（让代码更安全）
- 生成器（处理大数据）
- 描述符（元编程基础）
- 装饰器（增强函数功能）
- 异步编程（并发处理）
- 函数式编程（声明式范式）

### 从 Stage 1 到 Stage 2

**Stage 1 教了什么**:

- 类型注解基础（int, str, Optional, Union, Protocol）
- 生成器和迭代器（L11-L12）
- 装饰器和上下文管理器（L13-L14）
- 异步编程基础（L16）
- 函数式编程范式（L17）

**Stage 2 在此基础上教什么**:

- 测试驱动开发（pytest 与 TDD）→ L19
- uv、ruff、mypy 等工程化工具链 → L20
- 高级异步编程与并发模型 → L21
- 装饰器进阶、线程与性能抽象 → L22, L26
- 综合工程项目实践 → L27

---

## 📚 推荐资源

### 官方文档

- [Python typing 模块](https://docs.python.org/zh-cn/3/library/typing.html)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [asyncio 文档](https://docs.python.org/zh-cn/3/library/asyncio.html)
- [正则表达式 HOWTO](https://docs.python.org/zh-cn/3/howto/regex.html)

### 在线练习

- [Real Python - Type Checking](https://realpython.com/python-type-checking/)
- [Real Python - Async Python](https://realpython.com/async-python/)
- [Generator Tricks for Systems Programmers](http://www.dabeaz.com/generators/)

### 书籍推荐

- 《流畅的 Python》（第二版）- Luciano Ramalho
- 《Python 工匠》- piglei

---

## 🔗 相关文档

- [主 README](../README.md) - 课程总览
- [课程映射表](../COURSE_MAPPING.md) - 完整课程编号

## 📌 导航

- ← **上一阶段**: [Stage 0 - Python 编程基础](../stage0-python-basics/README.md)
- **当前**: Stage 1 - Python 进阶
- **下一阶段**: [Stage 2 - 现代工程](../stage2-engineering/README.md) →

---

**作者**: Python 3.13 全栈课程团队

🎉 **欢迎来到 Python 进阶！** 🚀
