"""L26 示例 1: 原始 HTTP 请求报文"""

from __future__ import annotations

REQUEST = """GET /health HTTP/1.1\r
Host: localhost:8000\r
Accept: application/json\r
\r
"""

RESPONSE = """HTTP/1.1 200 OK\r
Content-Type: application/json\r
Content-Length: 15\r
\r
{"status":"ok"}"""


if __name__ == "__main__":
    print("请求报文:")
    print(REQUEST)
    print("响应报文:")
    print(RESPONSE)
