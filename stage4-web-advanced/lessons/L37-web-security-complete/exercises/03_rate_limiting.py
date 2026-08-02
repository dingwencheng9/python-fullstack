"""

from __future__ import annotations

练习 3: API 限流系统

任务：
实现基于 Redis 的 API 限流系统，防止 API 滥用和 DDoS 攻击。

学习目标：
- 理解限流算法（固定窗口、滑动窗口、令牌桶）
- 使用 Redis 实现分布式限流
- 实现基于用户和 IP 的限流
- 处理限流异常和响应头

预计时间: 60 分钟
难度: ⭐⭐⭐⭐☆
"""

import time

from fastapi import Depends, FastAPI, Request

# ============================================================================
# TODO 1: 定义限流配置
# ============================================================================

# TODO: 创建限流配置类
# class RateLimitConfig(BaseModel):
#     max_requests: int  # 最大请求数
#     window_seconds: int  # 时间窗口（秒）


# ============================================================================
# TODO 2: 实现内存限流器（简化版）
# ============================================================================


class InMemoryRateLimiter:
    """内存限流器（开发环境使用）

    生产环境应使用 Redis 实现分布式限流
    """

    def __init__(self):
        # TODO: 初始化存储结构
        # 提示：使用字典存储 {key: [timestamp1, timestamp2, ...]}
        pass

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, dict]:
        """
        检查是否允许请求

        返回: (是否允许, 限流信息)
        """
        # TODO:
        # 1. 获取当前时间
        # 2. 清理过期的时间戳
        # 3. 检查请求数是否超限
        # 4. 如果允许，记录本次请求时间
        # 5. 返回结果和限流信息

    def reset(self, key: str) -> None:
        """重置限流记录"""
        # TODO: 从存储中删除 key


# ============================================================================
# TODO 3: 实现滑动窗口限流器
# ============================================================================


class SlidingWindowRateLimiter:
    """滑动窗口限流器（更精确）"""

    def __init__(self):
        # TODO: 初始化存储
        pass

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, dict]:
        """
        滑动窗口算法

        原理：维护一个时间戳列表，移除窗口外的记录
        """
        # TODO: 实现滑动窗口逻辑


# ============================================================================
# TODO 4: 实现限流中间件
# ============================================================================

# 全局限流器实例
rate_limiter = InMemoryRateLimiter()


def rate_limit(max_requests: int = 100, window_seconds: int = 60, key_func=None):
    """
    限流装饰器

    参数：
    - max_requests: 时间窗口内最大请求数
    - window_seconds: 时间窗口（秒）
    - key_func: 生成限流 key 的函数
    """

    async def dependency(request: Request):
        # TODO:
        # 1. 生成限流 key（使用 key_func 或默认 IP）
        # 2. 调用限流器检查
        # 3. 如果被限流，抛出 429 异常
        # 4. 设置响应头（X-RateLimit-*）
        pass

    return Depends(dependency)


# ============================================================================
# TODO 5: 实现不同粒度的限流
# ============================================================================


def get_client_ip(request: Request) -> str:
    """获取客户端 IP"""
    # TODO: 从 request 提取 IP
    # 考虑反向代理的情况（X-Forwarded-For）


def get_user_key(request: Request) -> str:
    """获取用户限流 key"""
    # TODO: 从请求中提取用户标识
    # 可以是 token、user_id 等


# ============================================================================
# TODO 6: 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="API 限流练习")


@app.get("/")
async def root() -> dict:
    """公开端点（无限流）"""
    return {"message": "API 限流系统"}


@app.get("/api/limited")
async def limited_endpoint(
    # TODO: 添加限流依赖（10请求/分钟）
) -> dict:
    """限流端点"""
    return {"message": "请求成功", "timestamp": time.time()}


@app.get("/api/strict")
async def strict_endpoint(
    # TODO: 添加严格限流（3请求/分钟）
) -> dict:
    """严格限流端点"""
    return {"message": "请求成功", "timestamp": time.time()}


@app.get("/api/user/{user_id}")
async def user_endpoint(
    user_id: str,
    # TODO: 添加基于用户的限流
) -> dict:
    """基于用户的限流"""
    return {"message": f"用户 {user_id} 的请求", "timestamp": time.time()}


@app.post("/api/reset/{key}")
async def reset_rate_limit(key: str) -> dict:
    """重置限流（管理员功能）"""
    # TODO: 重置指定 key 的限流记录


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 3: API 限流系统")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现内存限流器")
    print("  2. 实现滑动窗口算法")
    print("  3. 创建限流装饰器")
    print("  4. 实现不同粒度的限流（IP、用户）")
    print("  5. 添加限流响应头")
    print("\n测试方法：")
    print("  1. 启动服务: uvicorn exercises.03_rate_limiting:app --reload")
    print("  2. 快速请求测试限流:")
    print("     for i in {1..15}; do curl http://localhost:8000/api/limited; done")
    print("  3. 观察 429 状态码和响应头")
    print("\n限流算法：")
    print("  - 固定窗口: 简单但有突刺问题")
    print("  - 滑动窗口: 更平滑，更精确")
    print("  - 令牌桶: 允许突发流量")
    print("\n生产环境建议：")
    print("  - 使用 Redis 实现分布式限流")
    print("  - 添加监控和告警")
    print("  - 考虑限流降级策略")
    print()
