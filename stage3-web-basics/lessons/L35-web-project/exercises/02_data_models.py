"""L35 综合项目 - Exercise 2: 数据模型设计

任务：定义 User 和 Task 数据模型

## 任务描述

使用 SQLAlchemy 2.0 定义数据模型：
1. User 模型：id, username, email, hashed_password, is_active, created_at
2. Task 模型：id, title, description, completed, user_id, created_at, updated_at
3. 建立 User 和 Task 之间的一对多关系

## 验收标准

- [ ] User 模型定义正确
- [ ] Task 模型定义正确
- [ ] 外键关系正确
- [ ] 可以创建表

## 提示

1. 使用 SQLAlchemy 2.0 的 Mapped 类型注解
2. 定义 relationship 时使用 back_populates
3. 使用 cascade="all, delete-orphan" 实现级联删除

## 产出

在 solutions/ 目录创建：
- solution_02.py: 完整的数据模型代码
"""

from __future__ import annotations
