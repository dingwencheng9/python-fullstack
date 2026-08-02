# examples/03_api_gateway.py
"""
API 网关实现 - 统一的 API 入口

本模块演示微服务架构中的 API 网关模式。
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from typing import Callable

# ==================== 数据模型 ====================


@dataclass
class Route:
    """路由配置"""

    path_pattern: str
    upstream_service: str
    methods: list[str] = field(default_factory=lambda: ["GET"])
    rate_limit: int = 100  # 每分钟请求数

    def match(self, path: str, method: str) -> bool:
        """检查是否匹配路由"""
        if method not in self.methods:
            return False
        pattern = self.path_pattern.replace("*", ".*")
        return bool(re.match(f"^{pattern}$", path))


@dataclass
class Request:
    """请求"""

    path: str
    method: str
    headers: dict = field(default_factory=dict)
    body: dict | None = None
    query_params: dict = field(default_factory=dict)


@dataclass
class Response:
    """响应"""

    status_code: int
    body: dict
    headers: dict = field(default_factory=dict)


# ==================== 限流器 ====================


class RateLimiter:
    """令牌桶限流器"""

    def __init__(self, rate: int, window: int = 60):
        self.rate = rate  # 每窗口允许的请求数
        self.window = window  # 窗口大小（秒）
        self._tokens: dict[str, list[float]] = {}

    def _cleanup_old_tokens(self, client_id: str):
        """清理过期的令牌"""
        if client_id not in self._tokens:
            return

        import time

        now = time.time()
        cutoff = now - self.window

        self._tokens[client_id] = [t for t in self._tokens[client_id] if t > cutoff]

    def is_allowed(self, client_id: str) -> bool:
        """检查是否允许请求"""
        self._cleanup_old_tokens(client_id)

        if client_id not in self._tokens:
            self._tokens[client_id] = []

        return len(self._tokens[client_id]) < self.rate

    def record_request(self, client_id: str):
        """记录请求"""
        import time

        if client_id not in self._tokens:
            self._tokens[client_id] = []
        self._tokens[client_id].append(time.time())

    def get_remaining(self, client_id: str) -> int:
        """获取剩余请求数"""
        self._cleanup_old_tokens(client_id)
        return max(0, self.rate - len(self._tokens.get(client_id, [])))


# ==================== API 网关 ====================


class APIGateway:
    """
    API 网关

    功能：
    1. 路由转发
    2. 认证授权
    3. 限流
    4. 日志记录
    """

    def __init__(self):
        self.routes: list[Route] = []
        self.rate_limiter = RateLimiter(rate=100, window=60)
        self._services: dict[str, Callable] = {}

    def add_route(self, route: Route):
        """添加路由"""
        self.routes.append(route)
        print(f"  [网关] 添加路由: {route.path_pattern} -> {route.upstream_service}")

    def register_service(self, service_name: str, handler: Callable):
        """注册服务处理器"""
        self._services[service_name] = handler
        print(f"  [网关] 注册服务: {service_name}")

    def _match_route(self, request: Request) -> Route | None:
        """匹配路由"""
        for route in self.routes:
            if route.match(request.path, request.method):
                return route
        return None

    async def handle_request(self, request: Request) -> Response:
        """处理请求"""
        # 1. 限流检查
        client_id = request.headers.get("X-Client-ID", "anonymous")
        if not self.rate_limiter.is_allowed(client_id):
            return Response(
                status_code=429, body={"error": "Too Many Requests", "message": "请求过于频繁"}
            )
        self.rate_limiter.record_request(client_id)

        # 2. 路由匹配
        route = self._match_route(request)
        if not route:
            return Response(
                status_code=404,
                body={"error": "Not Found", "message": f"路由 {request.path} 不存在"},
            )

        # 3. 获取服务处理器
        handler = self._services.get(route.upstream_service)
        if not handler:
            return Response(
                status_code=503,
                body={
                    "error": "Service Unavailable",
                    "message": f"服务 {route.upstream_service} 不可用",
                },
            )

        # 4. 调用服务
        try:
            result = await handler(request)
            return Response(
                status_code=200,
                body=result,
                headers={"X-Rate-Limit-Remaining": str(self.rate_limiter.get_remaining(client_id))},
            )
        except Exception as e:
            return Response(
                status_code=500, body={"error": "Internal Server Error", "message": str(e)}
            )


# ==================== 模拟微服务 ====================


async def user_service_handler(request: Request) -> dict:
    """用户服务处理器"""
    await asyncio.sleep(0.05)  # 模拟处理延迟

    if request.path == "/api/users":
        return {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ]
        }
    elif match := __import__("re").match(r"/api/users/(\d+)", request.path):
        user_id = match.group(1)
        return {
            "id": int(user_id),
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com",
        }

    return {"error": "Not Found"}


async def order_service_handler(request: Request) -> dict:
    """订单服务处理器"""
    await asyncio.sleep(0.05)

    return {
        "orders": [
            {"id": 1, "user_id": 1, "amount": 99.99, "status": "completed"},
            {"id": 2, "user_id": 2, "amount": 149.99, "status": "pending"},
        ]
    }


# ==================== 演示 ====================


async def demo_basic_routing():
    """演示基础路由"""
    print("\n" + "=" * 60)
    print("API 网关基础路由演示")
    print("=" * 60)

    # 初始化网关
    gateway = APIGateway()

    # 注册服务
    gateway.register_service("user-service", user_service_handler)
    gateway.register_service("order-service", order_service_handler)

    # 添加路由
    gateway.add_route(Route("/api/users/*", "user-service", methods=["GET"]))
    gateway.add_route(Route("/api/orders", "order-service", methods=["GET"]))

    # 测试请求
    print("\n[1] 请求用户列表")
    request = Request(path="/api/users", method="GET", headers={"X-Client-ID": "web-app"})
    response = await gateway.handle_request(request)
    print(f"    状态码: {response.status_code}")
    print(f"    响应: {response.body}")

    print("\n[2] 请求用户详情")
    request = Request(path="/api/users/123", method="GET", headers={"X-Client-ID": "mobile-app"})
    response = await gateway.handle_request(request)
    print(f"    状态码: {response.status_code}")
    print(f"    响应: {response.body}")

    print("\n[3] 请求不存在的路由")
    request = Request(path="/api/products", method="GET", headers={"X-Client-ID": "web-app"})
    response = await gateway.handle_request(request)
    print(f"    状态码: {response.status_code}")
    print(f"    响应: {response.body}")


async def demo_rate_limiting():
    """演示限流"""
    print("\n" + "=" * 60)
    print("API 网关限流演示")
    print("=" * 60)

    # 创建低限流阈值的网关
    gateway = APIGateway()
    gateway.rate_limiter = RateLimiter(rate=5, window=60)  # 每分钟 5 个请求
    gateway.register_service("user-service", user_service_handler)
    gateway.add_route(Route("/api/users", "user-service", methods=["GET"]))

    print("\n[1] 模拟快速请求（测试限流）")
    for i in range(8):
        request = Request(path="/api/users", method="GET", headers={"X-Client-ID": "test-client"})
        response = await gateway.handle_request(request)
        status = response.status_code
        remaining = response.headers.get("X-Rate-Limit-Remaining", "N/A")
        print(f"    请求 {i + 1}: 状态={status}, 剩余配额={remaining}")


async def main():
    """主函数"""
    await demo_basic_routing()
    await demo_rate_limiting()

    print("\n" + "=" * 60)
    print("API 网关演示完成！")
    print("=" * 60)
    print("\n网关核心功能:")
    print("  1. 路由转发: 路径匹配 -> 服务调用")
    print("  2. 限流保护: 令牌桶算法")
    print("  3. 统一入口: 隐藏后端服务细节")
    print("  4. 认证授权: 可扩展的认证机制")


if __name__ == "__main__":
    asyncio.run(main())
