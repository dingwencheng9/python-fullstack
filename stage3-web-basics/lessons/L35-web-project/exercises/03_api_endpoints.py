"""L35 综合项目 - Exercise 3: API 端点实现

任务：实现用户和任务的 CRUD API

## 任务描述

使用 FastAPI 实现完整的 RESTful API：
1. 用户注册和登录
2. 任务 CRUD 操作
3. 分页和过滤
4. 错误处理

## 验收标准

- [ ] POST /users 创建用户
- [ ] GET /users/me 获取当前用户
- [ ] POST /tasks 创建任务
- [ ] GET /tasks 列出任务（支持分页和过滤）
- [ ] GET /tasks/{id} 获取单个任务
- [ ] PATCH /tasks/{id} 更新任务
- [ ] DELETE /tasks/{id} 删除任务

## 提示

1. 使用 Depends() 注入数据库会话
2. 使用 HTTPException 处理错误
3. 使用 Pydantic 模型验证输入输出

## 产出

在 solutions/ 目录创建：
- solution_03.py: 完整的 API 端点代码
"""

from __future__ import annotations
