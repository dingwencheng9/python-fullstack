#!/usr/bin/env python3
"""
L26: HTTP 协议与抓包基础

本文件演示 HTTP 请求的各个组成部分，帮助理解 HTTP 协议结构。
"""

import urllib.request
import json


def fetch_json_api() -> dict:
    """演示 GET 请求获取 JSON 数据"""
    url = "https://httpbin.org/json"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        return data


def post_form_data() -> dict:
    """演示 POST 请求发送表单数据"""
    import urllib.parse

    url = "https://httpbin.org/post"
    data = urllib.parse.urlencode({"name": "Alice", "age": 30}).encode()

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def send_custom_headers() -> dict:
    """演示发送自定义 Headers"""
    url = "https://httpbin.org/headers"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Python-HTTP-Demo/1.0",
            "Accept": "application/json",
            "X-Custom-Header": "custom-value",
        },
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def main():
    """主函数：运行所有 HTTP 请求示例"""
    print("=" * 60)
    print("HTTP 协议请求演示")
    print("=" * 60)

    # 1. GET 请求
    print("\n[1] GET 请求 - 获取 JSON")
    print("-" * 40)
    result = fetch_json_api()
    print("状态: 成功")
    print(f"数据: {json.dumps(result, indent=2)[:200]}...")

    # 2. POST 请求
    print("\n[2] POST 请求 - 发送表单数据")
    print("-" * 40)
    result = post_form_data()
    print("状态: 成功")
    print(f"表单数据: {result.get('form', {})}")

    # 3. 自定义 Headers
    print("\n[3] 自定义 Headers")
    print("-" * 40)
    result = send_custom_headers()
    headers = result.get("headers", {})
    print(f"User-Agent: {headers.get('User-Agent')}")
    print(f"X-Custom-Header: {headers.get('X-Custom-Header')}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
