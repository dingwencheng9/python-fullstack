#!/usr/bin/env python3
"""
HTTP 状态码参考

本文档展示了常见的 HTTP 状态码及其含义，帮助理解 Web 响应。
"""

from enum import Enum
from dataclasses import dataclass

class HTTPStatus(Enum):
    """HTTP 状态码枚举"""

    # 1xx 信息性
    CONTINUE = 100
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    # 3xx 重定向
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304

    # 4xx 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429

    # 5xx 服务器错误
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


@dataclass
class HTTPResponse:
    """模拟 HTTP 响应"""

    status_code: int
    status_text: str
    headers: dict
    body: str | None = None

    @property
    def is_success(self) -> bool:
        """是否成功响应（2xx）"""
        return 200 <= self.status_code < 300

    @property
    def is_redirect(self) -> bool:
        """是否重定向（3xx）"""
        return 300 <= self.status_code < 400

    @property
    def is_client_error(self) -> bool:
        """是否客户端错误（4xx）"""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """是否服务器错误（5xx）"""
        return 500 <= self.status_code < 600

    def __str__(self) -> str:
        return f"{self.status_code} {self.status_text}"


def get_status_description(status_code: int) -> str:
    """获取状态码描述"""
    descriptions = {
        # 2xx 成功
        200: "OK - 请求成功",
        201: "Created - 资源创建成功",
        204: "No Content - 请求成功但无返回内容",
        # 3xx 重定向
        301: "Moved Permanently - 永久重定向",
        302: "Found - 临时重定向",
        304: "Not Modified - 资源未修改，使用缓存",
        # 4xx 客户端错误
        400: "Bad Request - 请求格式错误",
        401: "Unauthorized - 需要认证",
        403: "Forbidden - 无权限访问",
        404: "Not Found - 资源不存在",
        422: "Unprocessable Entity - 请求格式正确但无法处理",
        # 5xx 服务器错误
        500: "Internal Server Error - 服务器内部错误",
        502: "Bad Gateway - 网关错误",
        503: "Service Unavailable - 服务不可用",
        504: "Gateway Timeout - 网关超时",
    }
    return descriptions.get(status_code, "Unknown Status")


def demo_status_codes():
    """演示各种状态码"""
    print("=" * 60)
    print("HTTP 状态码参考")
    print("=" * 60)

    examples = [
        HTTPResponse(200, "OK", {"Content-Type": "application/json"}),
        HTTPResponse(201, "Created", {"Location": "/users/123"}),
        HTTPResponse(301, "Moved Permanently", {"Location": "https://new.example.com"}),
        HTTPResponse(400, "Bad Request", {}, "Invalid input: name is required"),
        HTTPResponse(401, "Unauthorized", {"WWW-Authenticate": "Bearer"}),
        HTTPResponse(403, "Forbidden", {}, "Access denied"),
        HTTPResponse(404, "Not Found", {}, "User not found"),
        HTTPResponse(422, "Unprocessable Entity", {}, '{"errors": {"email": "invalid format"}}'),
        HTTPResponse(500, "Internal Server Error", {}, "Database connection failed"),
        HTTPResponse(503, "Service Unavailable", {"Retry-After": "60"}, "Server is under maintenance"),
    ]

    for response in examples:
        print(f"\n{response}")
        print(f"  描述: {get_status_description(response.status_code)}")
        print("  类型: ", end="")

        if response.is_success:
            print("✅ 成功")
        elif response.is_redirect:
            print("🔄 重定向")
        elif response.is_client_error:
            print("❌ 客户端错误")
        elif response.is_server_error:
            print("🚨 服务器错误")

        if response.body:
            print(f"  响应体: {response.body[:50]}...")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_status_codes()
