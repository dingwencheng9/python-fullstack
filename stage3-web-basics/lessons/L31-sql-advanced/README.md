# L31: SQL 进阶 - 高级特性与性能优化

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4-5 小时 | ⭐⭐⭐⭐☆（高级）  
> 前置课程：L28 数据库基础  
> 关键词：索引优化、EXPLAIN、JOIN 优化、子查询、窗口函数、CTE、视图、物化视图、分区表

## 📋 课程定位

SQL 不是"查数据"那么简单。本课程深入 SQL 高级特性与性能优化，让你写出高效、准确、优雅的数据库查询。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 使用 EXPLAIN/EXPLAIN ANALYZE 分析查询执行计划
- [ ] 设计合理的索引策略（单列、复合、覆盖索引）
- [ ] 优化 JOIN 查询（嵌套循环、哈希、合并连接）
- [ ] 使用子查询与 CTE 处理复杂业务逻辑
- [ ] 使用窗口函数进行排名、累计、分类统计
- [ ] 设计分区表应对大数据量
- [ ] 避免常见的 SQL 反模式

## 📂 课程结构

```text
L31-sql-advanced/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_explain_plan.py
│   ├── 02_index_optimization.py
│   └── 03_window_functions.py
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L31-sql-advanced
uv sync
uv run pytest tests -v
```

## 🔗 后续课程

- **L29 异步数据持久化**：应用 SQL 优化到异步 ORM
- **L35 Web 基础综合项目**：综合运用数据库技能
