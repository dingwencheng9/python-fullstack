"""L35 综合项目 - Exercise 1: 项目初始化

任务：创建 FastAPI 项目结构，配置依赖，实现基础应用入口

## 任务描述

创建一个任务管理 API 项目，包含：
1. 项目目录结构
2. FastAPI 应用入口
3. 数据库配置

## 验收标准

- [ ] 创建 app/main.py 入口文件
- [ ] FastAPI 应用可启动
- [ ] 访问 /docs 显示 Swagger UI
- [ ] 有健康检查端点 /health

## 提示

1. 使用 `uv add fastapi uvicorn sqlalchemy` 安装依赖
2. 创建简单的 FastAPI 实例
3. 添加 GET 路由返回 JSON 响应

## 产出

在 solutions/ 目录创建：
- solution_01.py: 完整的项目初始化代码
"""

from __future__ import annotations

# 在下方编写你的代码


def create_project_structure() -> dict[str, str]:
    """返回项目文件结构和内容的字典"""
    return {
        "app/__init__.py": "# App package",
        "app/main.py": "YOUR_CODE_HERE",
        "app/database.py": "YOUR_CODE_HERE",
    }
