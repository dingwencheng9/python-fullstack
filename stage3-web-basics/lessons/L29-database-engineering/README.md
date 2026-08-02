# L29: 异步数据持久化与事务原子性

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4-5 小时 | ⭐⭐⭐⭐☆（高级应用）  
> 前置课程：L27 FastAPI、L28 SQL 基础、L19 异步编程  
> 关键词：异步 ORM、SQLAlchemy 2.0、事务、ACID、锁、隔离级别、回滚、Savepoint、批量操作

## 📋 课程定位

Web 应用的可靠性取决于数据持久化的健壮性。本课程聚焦**异步 ORM**与**事务控制**，让你掌握生产级数据持久化能力。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 使用 SQLAlchemy 2.0 异步引擎进行数据库操作
- [ ] 理解并正确使用事务的 ACID 特性
- [ ] 选择合适的隔离级别解决并发问题
- [ ] 使用 Savepoint 实现嵌套事务
- [ ] 处理死锁与锁等待超时
- [ ] 实现批量插入与批量更新
- [ ] 设计幂等的数据操作接口

## 📂 课程结构

```text
L29-database-engineering/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_async_orm.py
│   ├── 02_transaction.py
│   └── 03_batch_operations.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L29-database-engineering
uv sync
uv run pytest tests -v
```

## 🔗 后续课程

- **L30 SQL 进阶 - 高级特性与性能优化**：深入 SQL 高级特性
- **L31 Docker 容器化基础**：部署数据库应用
