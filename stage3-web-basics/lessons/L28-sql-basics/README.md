# L28: 数据库基础与 SQL 入门

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4-5 小时 | ⭐⭐⭐☆☆（中级）  
> 前置课程：L26 HTTP 协议  
> 关键词：SQL、PostgreSQL、DDL、DML、DQL、JOIN、索引、事务、ACID、ORM、SQLAlchemy

## 📋 课程定位

数据库是 Web 应用的"记忆"。本课程从 SQL 基础到实战应用，让你掌握数据存储与查询的核心技能。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 使用 DDL 创建、修改、删除数据库对象（表、索引、约束）
- [ ] 使用 DML 进行增删改查操作
- [ ] 使用 DQL 进行复杂查询（子查询、聚合、分组）
- [ ] 理解并使用 JOIN 连接多表
- [ ] 理解事务与 ACID 特性
- [ ] 使用 SQLAlchemy 进行 Python 数据库操作
- [ ] 设计规范的数据库表结构

## 📂 课程结构

```text
L28-sql-basics/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_ddl_basics.py
│   ├── 02_dml_operations.py
│   └── 03_joins.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L28-sql-basics
uv sync
uv run pytest tests -v
```

## 🔗 后续课程

- **L29 异步数据持久化与事务原子性**：深入事务与异步 ORM
- **L30 SQL 进阶 - 高级特性与性能优化**：性能调优与高级 SQL
