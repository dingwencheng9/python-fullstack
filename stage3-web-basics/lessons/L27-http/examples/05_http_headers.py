#!/usr/bin/env python3
"""
HTTP Headers 参考指南

本文档演示常见的 HTTP Headers 及其用途。
"""

from dataclasses import dataclass

@dataclass
class HTTPHeaders:
    """HTTP Headers 分类参考"""

    # 请求 Headers
    ACCEPT: str = "Accept"  # 客户端可接受的媒体类型
    ACCEPT_LANGUAGE: str = "Accept-Language"  # 可接受的语言
    AUTHORIZATION: str = "Authorization"  # 认证信息
    CONTENT_TYPE: str = "Content-Type"  # 请求体类型
    USER_AGENT: str = "User-Agent"  # 客户端标识
    COOKIE: str = "Cookie"  # 发送 Cookie

    # 响应 Headers
    CONTENT_LENGTH: str = "Content-Length"  # 响应体长度
    CONTENT_ENCODING: str = "Content-Encoding"  # 压缩方式
    SET_COOKIE: str = "Set-Cookie"  # 设置 Cookie
    LOCATION: str = "Location"  # 重定向目标

    # 缓存 Headers
    CACHE_CONTROL: str = "Cache-Control"  # 缓存控制
    ETAG: str = "ETag"  # 资源标识
    LAST_MODIFIED: str = "Last-Modified"  # 最后修改时间
    EXPIRES: str = "Expires"  # 过期时间

    # CORS Headers
    ACCESS_CONTROL_ALLOW_ORIGIN: str = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS: str = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS: str = "Access-Control-Allow-Headers"

    # 安全 Headers
    STRICT_TRANSPORT_SECURITY: str = "Strict-Transport-Security"
    X_CONTENT_TYPE_OPTIONS: str = "X-Content-Type-Options"
    X_FRAME_OPTIONS: str = "X-Frame-Options"


# Content-Type 常用值
CONTENT_TYPES = {
    "json": "application/json",
    "xml": "application/xml",
    "form": "application/x-www-form-urlencoded",
    "multipart": "multipart/form-data",
    "html": "text/html",
    "plain": "text/plain",
    "css": "text/css",
    "javascript": "application/javascript",
    "octet_stream": "application/octet-stream",
}


def demo_headers():
    """演示常用 Headers"""
    print("=" * 70)
    print("HTTP Headers 参考指南")
    print("=" * 70)

    # 请求 Headers 示例
    print("\n📤 请求 Headers 示例:")
    print("-" * 50)
    request_headers = {
        "Host": "api.example.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "Content-Type": "application/json",
        "X-Request-ID": "req-123456",
    }

    for key, value in request_headers.items():
        print(f"  {key}: {value}")

    # 响应 Headers 示例
    print("\n📥 响应 Headers 示例:")
    print("-" * 50)
    response_headers = {
        "HTTP/1.1 200 OK",
        "Content-Type: application/json; charset=utf-8",
        "Content-Length: 1234",
        "Cache-Control: max-age=3600, public",
        "ETag: 'abc123'",
        "Strict-Transport-Security: max-age=31536000; includeSubDomains",
        "Access-Control-Allow-Origin: *",
        "X-Request-ID: req-123456",
    }

    for header in response_headers:
        print(f"  {header}")

    # Content-Type 示例
    print("\n📋 Content-Type 常用值:")
    print("-" * 50)
    for name, value in CONTENT_TYPES.items():
        print(f"  {name}: {value}")

    # Cache-Control 指令
    print("\n🔄 Cache-Control 常用指令:")
    print("-" * 50)
    cache_directives = [
        ("max-age=3600", "缓存有效期 1 小时"),
        ("no-cache", "每次使用前都验证"),
        ("no-store", "完全不缓存"),
        ("private", "仅浏览器缓存"),
        ("public", "可被任何缓存"),
        ("must-revalidate", "过期后必须验证"),
    ]

    for directive, description in cache_directives:
        print(f"  {directive:25} - {description}")

    print("\n" + "=" * 70)


def demo_auth_headers():
    """演示认证 Headers"""
    print("\n" + "=" * 70)
    print("认证 Headers 演示")
    print("=" * 70)

    # Basic Auth
    import base64

    credentials = "alice:password123"
    encoded = base64.b64encode(credentials.encode()).decode()
    basic_auth = f"Basic {encoded}"

    print("\n🔐 Basic Auth:")
    print(f"  Authorization: {basic_auth}")

    # Bearer Token
    bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
    print("\n🎫 Bearer Token:")
    print(f"  Authorization: Bearer {bearer_token[:50]}...")

    # API Key
    api_key = "sk-1234567890abcdef"
    print("\n🔑 API Key:")
    print(f"  X-API-Key: {api_key}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    demo_headers()
    demo_auth_headers()
