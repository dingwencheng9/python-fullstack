"""L55参考答案: Agent部署与监控"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agent API", version="1.0")


class AgentRequest(BaseModel):
    """Agent请求模型"""

    query: str
    session_id: str = "default"


class AgentResponse(BaseModel):
    """Agent响应模型"""

    result: str
    tokens: int
    duration: float


class HealthMetrics:
    """健康检查指标"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_duration = 0.0

    def record_request(self, duration: float, success: bool = True):
        """记录请求"""
        try:
            self.request_count += 1
            self.total_duration += duration
            if not success:
                self.error_count += 1
        except Exception as e:
            logger.error(f"Error recording request metrics: {str(e)}")
            raise

    def get_metrics(self) -> dict[str, Any]:
        """获取健康指标"""
        try:
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
            logger.error(f"Error getting metrics: {str(e)}")
            raise


# 全局指标
metrics = HealthMetrics()


@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Agent API端点"""
    start = time.time()

    try:
        # 模拟Agent处理
        result = f"处理查询: {request.query}"
        tokens = len(request.query) * 2
        duration = time.time() - start

        # 记录成功请求
        metrics.record_request(duration, success=True)

        return AgentResponse(result=result, tokens=tokens, duration=duration)
    except Exception as e:
        # 记录失败请求
        duration = time.time() - start
        metrics.record_request(duration, success=False)
        logger.error(f"Error in agent processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        return {"status": "healthy", "timestamp": time.time(), "metrics": metrics.get_metrics()}
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """获取详细指标"""
    try:
        return metrics.get_metrics()
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
