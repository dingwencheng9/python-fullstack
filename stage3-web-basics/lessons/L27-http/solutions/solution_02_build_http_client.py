"""练习 2 参考答案：构造 HTTP GET 请求。"""

from __future__ import annotations


def build_get_request(host: str, path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: application/json\r\nConnection: close\r\n\r\n"
