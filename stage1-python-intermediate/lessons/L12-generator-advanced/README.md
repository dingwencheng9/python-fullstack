# L12: 生成器进阶

> **课程编号**: L12  
> **所属阶段**: Stage 1 - Python 进阶  
> **预计时长**: 4 小时  
> **难度**: ⭐⭐⭐☆☆（中级进阶）  
> **前置课程**: L10 类型系统, L11 迭代器与生成器  
> **学习目标**: 掌握 yield from、send() 双向通信、异步生成器

---

## 📚 课程概述

本课程是 [L11 迭代器与生成器](../L11-generators/) 的进阶补充。

**核心内容**:
- `yield from` 委托机制
- `send()` 双向通信
- 异步生成器
- 生成器管道模式

---

## 🚀 快速开始

```bash
cd stage1-python-intermediate/lessons/L12-generator-advanced
```

### 1. 阅读课程内容

```bash
cat lesson.md
```

### 2. 运行示例代码

```bash
python examples/01_yield_from.py
python examples/02_send.py
python examples/03_async_generator.py
```

### 3. 完成练习题

```bash
python exercises/01_yield_from.py
python exercises/02_send.py
python exercises/03_async_generator.py
```

---

## 📂 课程结构

```
L12-generator-advanced/
├── README.md           # 本文件
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码
│   ├── 01_yield_from.py
│   ├── 02_send.py
│   └── 03_async_generator.py
├── exercises/          # 练习题
│   ├── 01_yield_from.py
│   ├── 02_send.py
│   └── 03_async_generator.py
└── solutions/          # 参考答案
    ├── 01_yield_from.py
    ├── 02_send.py
    └── 03_async_generator.py
```

---

## 🔗 课程衔接

- **前置课程**: [L11 迭代器与生成器](../L11-generators/lesson.md)
- **后续课程**: 
  - [L13 Python 高级特性（入门）](../L13-advanced-features/lesson.md)
  - [L14 并发编程入门](../L14-concurrency-intro/lesson.md)

---

## 📊 学习路径

```
L11 (6h)  →  L12 (4h)  →  L12 (5h)
    │            │
    └────────────┴──────────▶ L14 (异步基础)
                           │
                           └─────────▶ L19 (异步进阶)
```

---

**作者**: Python 3.13 全栈课程团队
