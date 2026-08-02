"""

from __future__ import annotations

L55练习: Agent部署与监控

任务: 实现Agent的生产部署和监控系统
"""

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import time

app = FastAPI()


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
        """
        记录请求

        参数:
            duration: 请求耗时
            success: 是否成功
        """
        try:
            # 增加请求计数
            self.request_count += 1

            # 如果失败，增加错误计数
            if not success:
                self.error_count += 1

            # 累加耗时
            self.total_duration += duration
        except Exception as e:
            # 记录错误但不中断程序
            print(f"Error recording request metrics: {str(e)}")
            # 即使记录失败，也不应该影响主流程

    def get_metrics(self) -> dict:
        """
        获取健康指标

        返回格式:
        {
            "total_requests": int,
            "error_count": int,
            "error_rate": float,
            "avg_duration": float
        }
        """
        try:
            # 处理除零情况
            if self.request_count == 0:
                return {
                    "total_requests": 0,
                    "error_count": 0,
                    "error_rate": 0.0,
                    "avg_duration": 0.0,
                }

            # 计算指标
            error_rate = self.error_count / self.request_count
            avg_duration = self.total_duration / self.request_count

            return {
                "total_requests": self.request_count,
                "error_count": self.error_count,
                "error_rate": round(error_rate, 4),
                "avg_duration": round(avg_duration, 4),
            }
        except Exception as e:
            # 记录错误并返回默认值
            print(f"Error getting metrics: {str(e)}")
            return {"total_requests": 0, "error_count": 0, "error_rate": 0.0, "avg_duration": 0.0}


# 创建全局指标收集器
metrics = HealthMetrics()


@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Agent API端点

    要求:
    1. 处理请求
    2. 记录指标
    3. 返回结果
    """
    # 记录开始时间
    start_time = time.time()

    try:
        # 模拟 Agent 处理（实际应调用真实 Agent）
        result = f"回答: 关于 '{request.query}' 的处理结果"
        tokens = len(request.query) * 2  # 模拟 token 计算

        # 计算耗时
        duration = time.time() - start_time

        # 记录成功请求
        metrics.record_request(duration, success=True)

        # 返回响应
        return AgentResponse(result=result, tokens=tokens, duration=duration)

    except Exception as e:
        # 记录失败请求
        duration = time.time() - start_time
        metrics.record_request(duration, success=False)

        # 记录错误日志
        print(f"Error processing agent request: {str(e)}")

        # 重新抛出异常
        raise


@app.get("/health")
async def health_check():
    """
    健康检查端点

    要求:
    1. 返回服务状态
    2. 返回性能指标
    3. 返回时间戳
    """
    try:
        # 获取当前指标
        current_metrics = metrics.get_metrics()
        error_rate = current_metrics.get("error_rate", 0)

        # 判断健康状态
        if error_rate < 0.1:
            status = "healthy"
        elif error_rate < 0.3:
            status = "degraded"
        else:
            status = "unhealthy"

        # 返回健康检查结果
        return {
            "status": status,
            "metrics": current_metrics,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        # 记录错误日志
        print(f"Error in health check: {str(e)}")

        # 返回错误状态
        return {
            "status": "unhealthy",
            "metrics": {
                "total_requests": 0,
                "error_count": 0,
                "error_rate": 1.0,
                "avg_duration": 0.0,
            },
            "timestamp": datetime.now().isoformat(),
        }


@app.get("/metrics")
async def get_metrics():
    """
    获取详细指标

    要求:
    1. 请求统计
    2. 错误统计
    3. 性能指标
    """
    try:
        # 获取基础指标
        current_metrics = metrics.get_metrics()

        # 计算额外统计
        total_requests = current_metrics["total_requests"]
        error_count = current_metrics["error_count"]
        success_count = total_requests - error_count

        # 构建详细响应
        return {
            "summary": {
                "total_requests": total_requests,
                "success_requests": success_count,
                "failed_requests": error_count,
                "success_rate": 1.0 - current_metrics["error_rate"] if total_requests > 0 else 0.0,
            },
            "performance": {
                "avg_duration_seconds": current_metrics["avg_duration"],
                "total_duration_seconds": metrics.total_duration,
            },
            "errors": {"count": error_count, "rate": current_metrics["error_rate"]},
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        # 记录错误日志
        print(f"Error getting metrics: {str(e)}")

        # 返回默认值
        return {
            "summary": {
                "total_requests": 0,
                "success_requests": 0,
                "failed_requests": 0,
                "success_rate": 0.0,
            },
            "performance": {"avg_duration_seconds": 0.0, "total_duration_seconds": 0.0},
            "errors": {"count": 0, "rate": 0.0},
            "timestamp": datetime.now().isoformat(),
        }
