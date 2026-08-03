# L14: 装饰器进阶

> **课程编号**: L14  
> **所属阶段**: Stage 1 - Python 进阶  
> **预计时长**: 6 小时  
> **难度**: ⭐⭐⭐⭐☆（中高级）  
> **前置课程**: L13 Python 高级特性（入门）  
> **学习目标**: 掌握带参装饰器、装饰器链、类装饰器初步

---

## 📚 课程概述

本课程是 [L13 Python 高级特性（入门）](../L13-advanced-features/) 的进阶补充。

**核心内容**:
- 带参装饰器（装饰器工厂）
- 装饰器链与执行顺序
- 类装饰器初步
- 可选参数装饰器

---

## 🚀 快速开始

```bash
cd stage1-python-intermediate/lessons/L14-decorator-advanced
```

### 1. 阅读课程内容

```bash
cat lesson.md
```

### 2. 运行示例代码

```bash
python examples/01_parameterized_decorators.py
python examples/02_decorator_chaining.py
python examples/03_class_decorators.py
```

### 3. 完成练习题

```bash
python exercises/01_parameterized.py
python exercises/02_chaining.py
python exercises/03_class_decorators.py
```

---

## 📂 课程结构

```
L14-decorator-advanced/
├── README.md           # 本文件
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码
│   ├── 01_parameterized_decorators.py
│   ├── 02_decorator_chaining.py
│   └── 03_class_decorators.py
├── exercises/          # 练习题
│   ├── 01_parameterized.py
│   ├── 02_chaining.py
│   └── 03_class_decorators.py
└── solutions/          # 参考答案
    ├── 01_parameterized.py
    ├── 02_chaining.py
    └── 03_class_decorators.py
```

---

## 🔗 课程衔接

- **前置课程**: [L13 Python 高级特性（入门）](../L13-advanced-features/lesson.md)
- **后续课程**: 
  - [L15 描述符与属性](../L15-descriptors/lesson.md)
  - [L14 并发编程入门](../L14-concurrency-intro/lesson.md)

**Stage 2 衔接**:
- [L20 装饰器深度探索](../../stage2-engineering/lessons/L20-decorators/lesson.md)

---

## 📊 学习路径

```
L13 (入门)  →  L14 (进阶)  →  L13
    │              │
    └──────────────┴──────────▶ L20 (Stage 2)
                                     │
                                     └──────────▶ FastAPI/LangChain 实战
```

---

## 📚 与 L20 的关系

**L14 覆盖**:
- 带参装饰器
- 类装饰器
- 装饰器链

**L20 深度覆盖**:
- 装饰器与类型注解
- @singledispatch
- __init_subclass__
- 装饰器与依赖注入
- 装饰器与中间件

---

**作者**: Python 3.13 全栈课程团队
