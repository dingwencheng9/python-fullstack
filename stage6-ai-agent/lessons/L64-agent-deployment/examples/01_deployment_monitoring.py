"""

from __future__ import annotations

L55示例: Agent部署与监控

学习目标:
- FastAPI封装
- 容器化部署
- 监控系统
"""

import time
import logging
from contextlib import contextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. FastAPI封装
print("=== 1. FastAPI封装 ===")

app = FastAPI(title="Agent API", version="1.0")


class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


class QueryResponse(BaseModel):
    result: str
    tokens: int
    duration: float


@contextmanager
def timer() -> float:
    """计时上下文管理器"""
    start = time.time()
    try:
        yield start
    finally:
        pass


@app.post("/agent", response_model=QueryResponse)
async def run_agent(request: QueryRequest):
    """Agent API端点"""
    try:
        with timer() as start:
            # 模拟Agent处理
            result = f"处理查询: {request.query}"
            tokens = len(request.query) * 2

            duration = time.time() - start

            return QueryResponse(result=result, tokens=tokens, duration=duration)
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


print("✅ FastAPI应用已创建")
print("端点: POST /agent")

# 2. 监控指标
print("\n=== 2. 监控指标 ===")


class MetricsCollector:
    """监控指标收集器"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self._lock = False  # 简单锁机制，防止并发问题

    def record_request(self, duration: float, success: bool = True) -> None:
        """记录请求"""
        try:
            if self._lock:
                return

            self._lock = True
            self.request_count += 1
            self.total_duration += duration
            if not success:
                self.error_count += 1
        except Exception as e:
            logger.error(f"记录指标时发生错误: {str(e)}")
        finally:
            self._lock = False

    def get_metrics(self) -> dict[str, Any]:
        """获取指标"""
        try:
            if self._lock:
                return {}

            self._lock = True
            return {
                "total_requests": self.request_count,
                "error_count": self.error_count,
                "error_rate": self.error_count / self.request_count
                if self.request_count > 0
                else 0,
                "avg_duration": self.total_duration / self.request_count
                if self.request_count > 0
                else 0,
            }
        except Exception as e:
            logger.error(f"获取指标时发生错误: {str(e)}")
            return {}
        finally:
            self._lock = False


metrics = MetricsCollector()
print("✅ 监控系统已初始化")


# 3. 健康检查
@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        return {"status": "healthy", "timestamp": time.time(), "metrics": metrics.get_metrics()}
    except Exception as e:
        logger.error(f"健康检查时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="健康检查失败")


print("\n=== 3. 健康检查 ===")
print("端点: GET /health")

# 4. Docker配置示例
print("\n=== 4. Docker配置 ===")

dockerfile = """
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

docker_compose = """
version: '3.8'

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
"""

print("Dockerfile已定义")
print("docker-compose.yml已定义")

# 5. 启动说明
print("\n=== 5. 部署步骤 ===")
print("1. 开发环境:")
print("   uvicorn main:app --reload")
print("\n2. Docker部署:")
print("   docker build -t agent-api .")
print("   docker run -p 8000:8000 agent-api")
print("\n3. 监控:")
print("   curl http://localhost:8000/health")

print("\n✅ 部署与监控示例完成")
