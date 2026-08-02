# Stage 2: 现代化基础内功

> **阶段编号**: Stage 2  
> **课程数量**: 9 课 (L19-L27)  
> **预计学时**: ~54 小时  
> **前置要求**: Stage 0 + Stage 1（Python 基础与进阶）

---

## 📚 课程列表

| 编号 | 课程名称 | 学时 | 难度 |
|------|----------|------|------|
| L19 | [Pytest 完整实战](lessons/L19-pytest-complete/) | 12h | ⭐⭐⭐⭐ |
| L20 | [现代化工具链](lessons/L20-toolchain/) | 8h | ⭐⭐⭐ |
| L21 | [异步核心进阶](lessons/L21-async-programming/) | 6h | ⭐⭐⭐⭐ |
| L22 | [装饰器深度探索](lessons/L22-decorators/) | 6h | ⭐⭐⭐⭐ |
| L23 | [Python 新特性与版本迁移](lessons/L23-python-new-features/) | 4h | ⭐⭐☆ |
| L24 | [高阶流控与异步协同](lessons/L24-advanced-flow-async/) | 13h | ⭐⭐⭐⭐⭐ |
| L25 | [Python 3.14 极限抽象与算力释放](lessons/L25-extreme-abstraction-performance/) | 10h | ⭐⭐⭐⭐⭐ |
| L26 | [线程与并发](lessons/L26-threading/) | 6h | ⭐⭐⭐⭐ |
| L27 | [工程化综合项目](lessons/L27-engineering-project/) | 5h | ⭐⭐⭐⭐ |

---

## 🎯 学习路径

```
L19 Pytest 完整实战 → L20 现代化工具链 → L21 异步核心进阶
        ↓                ↓                   ↓
L22 装饰器深度探索 ← L23 Python 新特性与版本迁移 → L24 高阶流控
        ↓                                           ↓
L25 Python 3.14 极限抽象与算力释放 ─────────────────────→ L26 线程与并发
        ↓                                           ↓
                 L27 工程化综合项目
```

---

## 📖 学习目标

完成 Stage 2 后，你将掌握：

1. **测试工程化** — 使用 pytest 进行单元测试、集成测试、Mock 与 fixture
2. **工具链生态** — uv、Docker、GitHub Actions 等现代开发工具
3. **异步编程** — asyncio、协程、异步生成器、任务调度
4. **元编程** — 装饰器、描述符、元类、类改造
5. **Python 新特性与版本迁移** — 彩色错误提示、改进 REPL、PEP 695 泛型
6. **高级流控** — 生成器表达式、迭代器协议、上下文管理器
7. **性能优化** — 内存管理、`__slots__`、垃圾回收调优
8. **并发编程** — 线程、同步原语、线程池、GIL 与 free-threading
9. **工程实践** — CLI 工具、数据模型、异步存储、综合项目

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x
- **包管理**: uv
- **测试框架**: pytest

```bash
# 安装依赖
uv sync

# 运行测试
uv run pytest stage2-engineering/lessons/ -v

# 运行单个课程测试
uv run pytest stage2-engineering/lessons/L19-pytest-complete/tests/ -v
```

---

## 📁 课程结构

每个课程包含：

```
L{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码
├── exercises/          # 练习题
├── solutions/          # 参考答案
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

### 前置要求

- **Stage 0**: Python 基础（L01-L10）
- **Stage 1**: Python 进阶
  - L11 + L12: 生成器基础与进阶
  - L13 + L14: 装饰器入门与进阶 ⭐ 重要
  - L16: 异步编程基础 ⭐ 重要

### Stage 1 → Stage 2 知识点映射

| Stage 1 | Stage 2 | 说明 |
|---------|---------|------|
| L11/L12 生成器 | L24 高阶流控 | 生成器深度 |
| L13/L14 装饰器 | L22 装饰器深度 | 装饰器深度 |
| L16 异步基础 | L21 异步进阶 | 异步深度 |
| L08 异常 | L19 Pytest | 测试工程化 |

### 后续课程

- **Stage 3**: Web 开发基础
- **Stage 4**: Web 高级开发
- **Stage 5**: 数据工程

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 9 |
| 示例代码 | ~90 个 |
| 练习题 | ~45 个 |
| 测试用例 | 1370+ |
| 预计学时 | ~54 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 9 个课程的学习
- [ ] 通过所有课程测试（1370+ 测试用例）
- [ ] 完成所有练习题
- [ ] 理解每个课程的核心概念
- [ ] 能够独立完成工程化项目
