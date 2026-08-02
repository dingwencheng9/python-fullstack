"""L35 综合项目 - Solution 1: 项目初始化"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="任务管理 API",
    description="L35 综合项目 - 任务管理 API 系统",
    version="1.0.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    """健康检查端点"""
    return {"status": "ok", "message": "任务管理 API 运行中"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """详细健康检查"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0",
    }
