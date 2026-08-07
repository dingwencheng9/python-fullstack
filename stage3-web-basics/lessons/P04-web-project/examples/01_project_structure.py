"""L35 综合项目 - Exercise 1: 项目初始化

任务：创建 FastAPI 项目结构，配置依赖，实现基础应用入口
"""

# === Step 1: 目录结构 ===
# L35-web-project/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py          <- 本文件
# │   ├── config.py        <- 创建配置
# │   ├── database.py      <- 创建数据库连接
# │   ├── models/          <- 创建模型
# │   ├── schemas/         <- 创建 Pydantic 模型
# │   └── api/             <- 创建 API 路由
# ├── tests/
# ├── docker/
# └── requirements.txt

# === Step 2: requirements.txt ===
# fastapi>=0.100.0
# uvicorn[standard]>=0.23.0
# sqlalchemy>=2.0.0
# pydantic>=2.0.0
# python-jose[cryptography]>=3.3.0
# passlib[bcrypt]>=1.7.4
# python-multipart>=0.0.6
# httpx>=0.24.0
# pytest>=7.0.0
# pytest-asyncio>=0.21.0

# === Step 3: app/main.py ===
from fastapi import FastAPI

app = FastAPI(
    title="任务管理 API",
    description="L35 综合项目示例",
    version="1.0.0",
)


@app.get("/")
async def root():
    """健康检查端点"""
    return {"status": "ok", "message": "任务管理 API 运行中"}


@app.get("/health")
async def health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0",
    }


# === Step 4: 运行验证 ===
# uv add fastapi uvicorn sqlalchemy pydantic
# uv run uvicorn app.main:app --reload
# 访问 http://localhost:8000/docs 查看 Swagger UI
