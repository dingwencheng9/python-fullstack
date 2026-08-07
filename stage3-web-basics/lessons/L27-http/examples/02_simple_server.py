"""L26 示例 2: 简单 HTTP 服务器。

使用标准库 BaseHTTPRequestHandler 构建原始 HTTP 服务器，
演示 HTTP 请求处理流程。
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8888), HealthHandler)
    print("Server at http://localhost:8888")
    server.handle_request()
