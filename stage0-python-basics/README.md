# Stage 0: Python 编程基础

> **课程定位**: 零基础入门
> **课程数量**: 9 课程（全部完成）
> **预计时长**: ~56 小时
> **难度**: ⭐☆☆☆☆ (入门)

---

## 🎯 Stage 概述

**Stage 0** 是为**完全零基础**学员设计的 Python 编程入门课程。通过系统学习 Python 基础语法和编程概念，为后续 Stage 1-6 和专项阶段的高级课程打下坚实基础。

### 适合人群

- ✅ 完全零编程基础
- ✅ 从未接触过 Python
- ✅ 希望系统学习编程
- ✅ 准备进入 Stage 1 的学员

### 学习成果

完成 Stage 0 后，你将能够：

- ✅ 编写 100+ 行的 Python 程序
- ✅ 使用变量、数据类型和运算符
- ✅ 使用控制流程（if/for/while/match-case）
- ✅ 定义和使用函数
- ✅ 使用列表、字典、元组、集合等数据结构
- ✅ 处理文件读写
- ✅ 理解并处理异常
- ✅ 掌握面向对象基础（类、对象、继承）
- ✅ 运用魔术方法自定义行为

---

## 📚 课程列表（9 个）

| 课程    | 标题             | 时长  | 难度      | 核心内容                                      | 状态 |
| ------- | ---------------- | ----- | --------- | -------------------------------------------- | ---- |
| **L01** | Python 核心语法   | 6h    | ⭐☆☆☆☆    | 变量、数据类型、运算符、输入输出、REPL         | ✅   |
| **L02** | 运算符与控制流    | 6h    | ⭐☆☆☆☆    | 算术/比较/逻辑/位运算符、if/elif/else、match-case | ✅   |
| **L03** | 数据结构          | 8h    | ⭐⭐☆☆☆   | list、tuple、dict、set、推导式、enumerate、zip  | ✅   |
| **L04** | 函数与模块        | 8h    | ⭐⭐☆☆☆   | def、参数、返回值、\*args/\*\*kwargs、lambda、模块 | ✅   |
| **L05** | 文件操作          | 8h    | ⭐⭐☆☆☆   | 文件读写、with 语句、路径操作、JSON/CSV       | ✅   |
| **L06** | 面向对象基础       | 6h    | ⭐⭐☆☆☆   | 类、对象、继承、多态、封装、组合              | ✅   |
| **L07** | 魔术方法           | 4h    | ⭐⭐⭐☆☆  | \__init\_\_、\__str\_\_、\__repr\_\_、\__len\_\_ 等 | ✅   |
| **L08** | 异常处理          | 3h    | ⭐⭐☆☆☆   | try/except/finally/else、raise、自定义异常、链式异常 | ✅   |
| **L09** | Python 基础实战   | 6-8h  | ⭐⭐⭐☆☆  | 综合项目：学员管理系统                        | ✅   |

**总计**: ~56 小时

---

## 🎓 学习路径

```
L01 (6h)  →  L02 (6h)  →  L03 (8h)
    ↓
L04 (8h)  →  L05 (8h)  →  L06 (6h)
    ↓
L07 (4h)  →  L08 (3h)  →  L09 (6-8h)
    ↓
Stage 1
```

### 推荐学习计划

**密集学习（4 周）**:

```
Week 1: L01 → L03 (20h)  + 练习 (10h)
Week 2: L04 → L06 (22h)  + 练习 (10h)
Week 3: L07 → L08 (7h)   + 练习 (5h)
Week 4: L09 综合项目 (8h) + 复习 (6h)
```

**轻松学习（8 周）**:

```
Week 1-2: L01 → L02
Week 3-4: L03 → L04
Week 5-6: L05 → L06
Week 7-8: L07 → L09 + 项目
```

---

## 🚀 快速开始

### 1. 检查 Python 版本

```bash
python --version  # 应该 >= 3.13
```

### 2. 进入课程目录

```bash
cd stage0-python-basics
```

### 3. 开始第一课

```bash
cd lessons/L01-python-core
cat README.md
```

### 4. 运行示例代码

```bash
python examples/01_hello_world.py
```

### 5. 完成练习题

```bash
python exercises/01_basic_io.py
```

---

## 📂 课程结构

每个课程包含：

```
LXX-topic-name/
├── README.md           # 课程概览（5 分钟阅读）
├── lesson.md           # 详细教学内容（1-2 小时学习）
├── examples/           # 示例代码（可直接运行）
│   ├── 01_basic.py
│   ├── 02_intermediate.py
│   └── 03_advanced.py
├── exercises/          # 练习题（动手实践）
│   ├── 01_exercise.py
│   ├── 02_exercise.py
│   └── 03_exercise.py
├── solutions/          # 参考答案（完成练习后查看）
│   ├── 01_solution.py
│   ├── 02_solution.py
│   └── 03_solution.py
└── tests/              # 单元测试（验证理解）
    └── test_*.py
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

### 常见问题

**Q: Stage 0 是必须的吗？**
A: 如果你已有 Python 基础，可以跳过。建议先完成毕业测试，80% 以上可直接进入 Stage 1。

**Q: Stage 0 需要多久完成？**
A: 完全零基础：6-8 周（每周 8-10 小时）。有编程经验：2-4 周。

**Q: 可以跳过某些课程吗？**
A: 不建议。Stage 0 课程设计是循序渐进的，跳课可能导致后续困难。

**Q: 练习题太难怎么办？**
A: 先重新阅读 lesson.md，然后查看 examples/，最后参考 solutions/ 学习。

**Q: 完成 Stage 0 后应该做什么？**
A: 完成综合项目（L09），通过毕业测试，然后进入 Stage 1。

---

## 🎁 综合项目

### L09: 学员管理系统

**项目描述**: 开发一个命令行学员管理系统

**功能要求**:

- ✅ 添加学员（姓名、年龄、课程）
- ✅ 删除学员
- ✅ 查询学员
- ✅ 列出所有学员
- ✅ 数据持久化（保存到文件）

**技术要点**:

- 使用 list 和 dict 存储数据
- 使用函数组织代码
- 使用文件操作保存数据
- 使用异常处理错误
- 使用类封装学员信息
- 使用面向对象设计模式

**预计时间**: 6-8 小时

---

## 📚 推荐资源

### 官方文档

- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- [Python 标准库](https://docs.python.org/zh-cn/3/library/)

### 在线练习

- [Python Tutor](https://pythontutor.com/) - 可视化代码执行
- [Exercism Python Track](https://exercism.org/tracks/python) - 编程练习
- [HackerRank Python](https://www.hackerrank.com/domains/python) - 算法练习

### 书籍推荐

- 《Python 编程：从入门到实践》
- 《流畅的 Python》（完成 Stage 0 后阅读）

---

## 🔗 相关文档

- [主 README](../README.md) - 课程总览
- [课程映射表](../COURSE_MAPPING.md) - 完整课程编号

## 📌 导航

- **当前**: Stage 0 - Python 编程基础
- **下一阶段**: [Stage 1 - Python 进阶](../stage1-python-intermediate/README.md) →

---

**作者**: Python 3.13 全栈课程团队

🎉 **欢迎来到 Python 世界！** 🚀
