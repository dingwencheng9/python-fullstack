"""

from __future__ import annotations

练习 3: API 限流系统 - Python 3.13 参考答案

本解决方案展示：
1. Python 3.13 PEP 695 泛型语法
2. match/case 模式匹配
3. asyncio.TaskGroup 并发限流检查
4. Free-threading 线程安全设计

【解题思路】

1. 限流算法选择：
   - 固定窗口：简单但有边界突刺问题
   - 滑动窗口：更精确，本方案采用
   - 令牌桶：允许短时突发，更复杂

2. 滑动窗口实现：
   - 维护时间戳列表
   - 移除窗口外的旧记录
   - 检查剩余配额
   - O(n)时间复杂度，n为窗口内请求数

3. 限流粒度：
   - IP级别：防止单个IP滥用
   - 用户级别：防止账户滥用
   - 端点级别：不同API不同限制

4. 响应设计：
   - 429 Too Many Requests 状态码
   - X-RateLimit-* 响应头
   - Retry-After 告知重试时间

5. 生产优化：
   - 使用Redis实现分布式限流
   - 添加限流监控
   - 实现限流降级

【关键知识点】

- 滑动窗口算法
- FastAPI依赖注入
- HTTP 429状态码
- X-RateLimit响应头标准
- 分布式限流设计
- Python 3.13 PEP 695 泛型语法
- match/case 模式匹配
- asyncio.TaskGroup 并发处理

作者：Python 3.13 全栈课程
"""

import asyncio
import time
from collections.abc import Callable
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from pydantic import BaseModel

# ============================================================================
# 1. 定义限流配置
# ============================================================================


class RateLimitConfig(BaseModel):
    """限流配置"""

    max_requests: int  # 最大请求数
    window_seconds: int  # 时间窗口（秒）


# ============================================================================
# 2. 泛型限流器（Python 3.13 PEP 695 泛型）
# ============================================================================


class RateLimiter[T]:
    """
    泛型限流器（Python 3.13 PEP 695 泛型语法）

    🚀 Python 3.13 PEP 695 特性:
    - 使用 class RateLimiter[T]: 定义泛型类
    - 相比旧语法更简洁直观
    - 类型推断更准确

    🔒 Free-threading 线程安全说明:
    - 内部使用字典存储请求记录
    - 在 asyncio event loop 内是单线程安全的
    - Python 3.14 多线程环境下需要额外的锁保护

    泛型参数:
        T: 限流记录的数据类型（通常是 list[float] 或其他时间戳容器）
    """

    def __init__(self) -> None:
        # 存储结构: {key: [timestamp1, timestamp2, ...]}
        self.requests: dict[str, T] = {}

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, dict[str, Any]]:
        """
        检查是否允许请求（使用 match/case 处理结果）

        🎯 Python 3.10+ match/case 模式匹配
        """
        now = time.time()
        window_start = now - window_seconds

        # 获取或创建记录
        if key not in self.requests:
            self.requests[key] = []  # type: ignore

        # 清理过期记录
        self.requests[key] = [ts for ts in self.requests[key] if ts > window_start]  # type: ignore

        # 检查是否超限
        current_requests = len(self.requests[key])  # type: ignore

        # 使用 match/case 处理限流结果
        match current_requests < max_requests:
            case True:
                # 允许请求，记录时间戳
                self.requests[key].append(now)  # type: ignore
                current_requests += 1
                allowed = True
            case False:
                # 拒绝请求
                allowed = False

        # 计算限流信息
        remaining = max(0, max_requests - current_requests)
        reset_time = int(now + window_seconds)

        info = {
            "limit": max_requests,
            "remaining": remaining,
            "reset": reset_time,
            "retry_after": 0 if allowed else int(window_seconds),
        }

        return allowed, info

    def reset(self, key: str) -> None:
        """重置限流记录"""
        if key in self.requests:
            del self.requests[key]


# ============================================================================
# 3. 实现滑动窗口限流器
# ============================================================================


class SlidingWindowRateLimiter:
    """
    滑动窗口限流器

    🔒 Free-threading 线程安全说明:
    - 字典操作在 asyncio event loop 内是线程安全的
    - Python 3.14 环境下避免跨线程共享
    """

    def __init__(self) -> None:
        self.requests: dict[str, list[float]] = {}

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> tuple[bool, dict[str, Any]]:
        """
        滑动窗口算法（使用 match/case 处理边界情况）

        🎯 Python 3.10+ match/case 模式匹配
        """
        now = time.time()
        window_start = now - window_seconds

        # 初始化或清理过期记录
        if key not in self.requests:
            self.requests[key] = []
        else:
            # 移除窗口外的记录
            self.requests[key] = [ts for ts in self.requests[key] if ts > window_start]

        # 检查配额
        current_count = len(self.requests[key])

        # 使用 match/case 判断是否允许
        match (current_count < max_requests, current_count):
            case (True, _):
                # 允许请求
                self.requests[key].append(now)
                current_count += 1
                allowed = True
            case (False, count) if count >= max_requests:
                # 已达限制
                allowed = False
            case _:
                # 其他情况（不应该发生）
                allowed = False

        # 计算下次重置时间
        if self.requests[key]:
            oldest_request = min(self.requests[key])
            next_reset = int(oldest_request + window_seconds)
        else:
            next_reset = int(now + window_seconds)

        info = {
            "limit": max_requests,
            "remaining": max(0, max_requests - current_count),
            "reset": next_reset,
            "retry_after": 0 if allowed else int(window_seconds - (now - window_start)),
        }

        return allowed, info


# ============================================================================
# 4. 批量限流检查（使用 asyncio.TaskGroup）
# ============================================================================


async def check_rate_limits_batch(
    limiter: SlidingWindowRateLimiter,
    keys: list[str],
    max_requests: int,
    window_seconds: int,
) -> dict[str, dict[str, Any]]:
    """
    批量检查限流状态（使用 asyncio.TaskGroup 并发）

    🚀 Python 3.13 asyncio.TaskGroup:
    - 结构化并发，自动等待所有任务完成
    - 异常安全，任何任务失败会取消其他任务

    Args:
        limiter: 限流器实例
        keys: 限流 key 列表
        max_requests: 最大请求数
        window_seconds: 时间窗口

    Returns:
        限流状态字典
    """
    results: dict[str, dict[str, Any]] = {}

    async def check_single(key: str) -> tuple[str, bool, dict[str, Any]]:
        """检查单个 key 的限流状态"""
        # 模拟异步检查（实际可能查询 Redis）
        await asyncio.sleep(0.01)
        allowed, info = limiter.is_allowed(key, max_requests, window_seconds)
        return (key, allowed, info)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(check_single(key)) for key in keys]

    # 收集结果
    for task in tasks:
        key, allowed, info = task.result()
        results[key] = {
            "allowed": allowed,
            **info,
        }

    return results


# ============================================================================
# 5. 实现限流中间件
# ============================================================================

# 全局限流器实例
rate_limiter = SlidingWindowRateLimiter()


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
    key_func: Callable[[Request], str] | None = None,
):
    """限流装饰器"""

    async def dependency(request: Request, response: Response):
        # 生成限流 key
        key = key_func(request) if key_func else get_client_ip(request)

        # 检查限流
        allowed, info = rate_limiter.is_allowed(key, max_requests, window_seconds)

        # 设置响应头
        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(info["reset"])

        # 如果被限流，抛出异常
        if not allowed:
            response.headers["Retry-After"] = str(info["retry_after"])
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "请求过于频繁",
                    "message": f"每{window_seconds}秒最多{max_requests}个请求",
                    "retry_after": info["retry_after"],
                },
            )

        return info

    return Depends(dependency)


# ============================================================================
# 6. 实现不同粒度的限流（使用 match/case）
# ============================================================================


def get_client_ip(request: Request) -> str:
    """
    获取客户端 IP（使用 match/case 处理不同来源）

    🎯 Python 3.10+ match/case 模式匹配
    """
    # 使用 match/case 处理 IP 获取
    match request.headers.get("X-Forwarded-For"):
        case str(forwarded):
            # 有代理，取第一个 IP
            return forwarded.split(",")[0].strip()
        case None:
            # 无代理，直接取客户端 IP
            match request.client:
                case None:
                    return "unknown"
                case client:
                    return client.host


def get_user_key(request: Request) -> str:
    """获取用户限流 key"""
    # 这里简化处理，实际应从 token 中提取
    return f"user:{request.path_params.get('user_id', 'anonymous')}"


# ============================================================================
# 7. 创建 FastAPI 应用和路由
# ============================================================================

app = FastAPI(title="API 限流练习 - Python 3.13")


@app.get("/")
async def root() -> dict[str, Any]:
    """公开端点（无限流）"""
    return {
        "message": "API 限流系统 (Python 3.13)",
        "endpoints": {
            "/api/limited": "10请求/分钟",
            "/api/strict": "3请求/分钟",
            "/api/user/{user_id}": "基于用户限流",
        },
        "features": [
            "PEP 695 泛型语法",
            "match/case 模式匹配",
            "asyncio.TaskGroup 并发",
            "Free-threading 线程安全",
        ],
    }


@app.get("/api/limited")
async def limited_endpoint(
    rate_info: Annotated[dict, rate_limit(max_requests=10, window_seconds=60)],
) -> dict[str, Any]:
    """限流端点（10请求/分钟）"""
    return {
        "message": "请求成功",
        "timestamp": time.time(),
        "rate_limit": rate_info,
    }


@app.get("/api/strict")
async def strict_endpoint(
    rate_info: Annotated[dict, rate_limit(max_requests=3, window_seconds=60)],
) -> dict[str, Any]:
    """严格限流端点（3请求/分钟）"""
    return {
        "message": "请求成功",
        "timestamp": time.time(),
        "rate_limit": rate_info,
    }


@app.get("/api/user/{user_id}")
async def user_endpoint(
    user_id: str,
    rate_info: Annotated[dict, rate_limit(max_requests=5, window_seconds=60, key_func=get_user_key)],
) -> dict[str, Any]:
    """基于用户的限流（5请求/分钟）"""
    return {
        "message": f"用户 {user_id} 的请求",
        "user_id": user_id,
        "timestamp": time.time(),
        "rate_limit": rate_info,
    }


@app.post("/api/check-batch")
async def check_batch_limits(keys: list[str]) -> dict[str, Any]:
    """
    批量检查限流状态（使用 asyncio.TaskGroup 并发）

    🚀 展示 Python 3.13 TaskGroup 并发检查
    """
    results = await check_rate_limits_batch(
        limiter=rate_limiter,
        keys=keys,
        max_requests=10,
        window_seconds=60,
    )

    return {
        "total": len(keys),
        "results": results,
    }


@app.post("/api/reset/{key}")
async def reset_rate_limit(key: str) -> dict[str, str]:
    """重置限流（管理员功能）"""
    rate_limiter.reset(key)
    return {"message": f"已重置 {key} 的限流记录"}


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    from core.settings import get_settings

    settings = get_settings()
    import uvicorn

    print("=" * 70)
    print("练习 3 参考答案: API 限流系统 - Python 3.13")
    print("=" * 70)
    print("\n特性:")
    print("  ✅ PEP 695 泛型语法: class RateLimiter[T]")
    print("  ✅ match/case: 优雅的限流判断")
    print("  ✅ asyncio.TaskGroup: 批量限流检查")
    print("  ✅ Free-threading 线程安全设计")
    print("\n限流配置：")
    print("  /api/limited -> 10请求/分钟")
    print("  /api/strict -> 3请求/分钟")
    print("  /api/user/{user_id} -> 5请求/分钟（基于用户）")
    print("\n测试命令：")
    print("  # 测试正常请求")
    print("  curl -i http://localhost:8000/api/limited")
    print("\n  # 快速请求触发限流")
    print("  for i in {1..15}; do curl -i http://localhost:8000/api/limited; sleep 0.5; done")
    print("\n  # 批量检查限流状态")
    print('  curl -X POST http://localhost:8000/api/check-batch -H "Content-Type: application/json" -d \'["ip1", "ip2"]\'')
    print("\n  # 观察响应头")
    print("  X-RateLimit-Limit: 最大请求数")
    print("  X-RateLimit-Remaining: 剩余配额")
    print("  X-RateLimit-Reset: 重置时间")
    print("  Retry-After: 重试等待时间")
    print("\n启动服务...\n")

    uvicorn.run(
        app,
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
    )
