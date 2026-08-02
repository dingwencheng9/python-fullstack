"""
真实异步HTTP客户端（使用 aiohttp）

演示如何使用 aiohttp 进行真实的异步HTTP请求。
这是生产环境推荐的方式。

支持两种运行模式：
- 真实模式（默认）：使用 aiohttp 连接真实网络
- Mock 模式（--mock）：模拟 HTTP 响应，无需网络依赖

⚠️ 注意：需要安装 aiohttp
    uv add aiohttp

作者: Python 3.13 全栈课程
日期: 2026-06-04
Python版本: 3.12+
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from dataclasses import dataclass
from typing import Any

# ============================================
# Mock 数据层
# ============================================


@dataclass
class MockResponse:
    """模拟 HTTP 响应"""

    status: int
    content_type: str
    text: str

    async def json(self) -> dict[str, Any]:
        """模拟 JSON 解析"""
        return json.loads(self.text)

    async def text(self) -> str:
        """模拟获取文本"""
        return self.text


# Mock 数据存储
MOCK_DATA: dict[str, MockResponse] = {}


def _init_mock_data() -> None:
    """初始化 Mock 数据"""
    global MOCK_DATA
    MOCK_DATA = {
        "https://httpbin.org/get": MockResponse(
            status=200,
            content_type="application/json",
            text=json.dumps(
                {
                    "args": {},
                    "headers": {"Host": "httpbin.org"},
                    "origin": "127.0.0.1",
                    "url": "https://httpbin.org/get",
                }
            ),
        ),
        "https://httpbin.org/delay/1": MockResponse(
            status=200,
            content_type="application/json",
            text=json.dumps(
                {
                    "args": {},
                    "headers": {},
                    "origin": "127.0.0.1",
                    "url": "https://httpbin.org/delay/1",
                }
            ),
        ),
        "https://httpbin.org/post": MockResponse(
            status=200,
            content_type="application/json",
            text=json.dumps(
                {
                    "args": {},
                    "data": '{"name": "\\u5f20\\u4e09", "email": "zhangsan@example.com", "age": 25}',
                    "json": {
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "age": 25,
                    },
                    "headers": {"Content-Type": "application/json"},
                    "origin": "127.0.0.1",
                    "url": "https://httpbin.org/post",
                }
            ),
        ),
        # 模拟超时响应
        "https://httpbin.org/delay/10": MockResponse(
            status=200,
            content_type="application/json",
            text=json.dumps({"error": "timeout"}),
        ),
        # 模拟失败响应
        "https://invalid-domain-12345.com": MockResponse(
            status=404,
            content_type="text/html",
            text="Not Found",
        ),
    }

    # 为 jsonplaceholder 生成模拟用户数据
    for user_id in range(1, 11):
        MOCK_DATA[f"https://jsonplaceholder.typicode.com/users/{user_id}"] = (
            MockResponse(
                status=200,
                content_type="application/json",
                text=json.dumps(
                    {
                        "id": user_id,
                        "name": f"用户 {user_id}",
                        "username": f"user{user_id}",
                        "email": f"user{user_id}@example.com",
                        "phone": f"+1-555-{user_id:04d}",
                        "website": f"user{user_id}.example.com",
                    }
                ),
            )
        )


# Mock 模式标志（全局）
_MOCK_MODE = False


def _set_mock_mode(enabled: bool) -> None:
    """设置 Mock 模式"""
    global _MOCK_MODE
    _MOCK_MODE = enabled
    if enabled:
        _init_mock_data()


def _is_mock_mode() -> bool:
    """检查是否为 Mock 模式"""
    return _MOCK_MODE


# ============================================
# aiohttp 导入与 Mock 适配层
# ============================================


class MockSession:
    """模拟 aiohttp.ClientSession"""

    def __init__(self) -> None:
        pass

    async def __aenter__(self) -> "MockSession":
        return self

    async def __aexit__(self, *args: Any) -> None:
        pass

    def get(self, url: str) -> "MockRequest":
        """发起 GET 请求"""
        return MockRequest(url, "GET")

    def post(self, url: str, **kwargs: Any) -> "MockRequest":
        """发起 POST 请求"""
        return MockRequest(url, "POST", json_data=kwargs.get("json"))


class MockRequest:
    """模拟 aiohttp.ClientResponse"""

    def __init__(
        self, url: str, method: str = "GET", json_data: dict[str, Any] | None = None
    ) -> None:
        self.url = url
        self.method = method
        self._json_data = json_data

    async def __aenter__(self) -> "MockRequest":
        return self

    async def __aexit__(self, *args: Any) -> None:
        pass

    @property
    def status(self) -> int:
        if self.url in MOCK_DATA:
            return MOCK_DATA[self.url].status
        return 404

    @property
    def content_type(self) -> str:
        if self.url in MOCK_DATA:
            return MOCK_DATA[self.url].content_type
        return "text/plain"

    async def text(self) -> str:
        if self.url in MOCK_DATA:
            return MOCK_DATA[self.url].text
        return "{}"

    async def json(self) -> dict[str, Any]:
        text = await self.text()
        return json.loads(text)


# 检查 aiohttp 是否已安装
aiohttp_available = True
try:
    import aiohttp
except ImportError:
    aiohttp_available = False
    aiohttp = None  # type: ignore[assignment]


# ============================================
# 示例1: 单个请求
# ============================================


async def fetch_single_url(url: str) -> dict[str, object]:
    """
    发起单个HTTP请求

    Args:
        url: 请求URL

    Returns:
        响应数据
    """
    if _is_mock_mode():
        async with MockSession() as session, session.get(url) as response:
            return {
                "url": url,
                "status": response.status,
                "content_type": response.content_type,
                "text": await response.text(),
            }
    else:
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            return {
                "url": url,
                "status": response.status,
                "content_type": response.content_type,
                "text": await response.text(),
            }


async def demonstrate_single_request() -> None:
    """演示单个请求"""
    print("=" * 60)
    print("1. 单个HTTP请求")
    print("=" * 60)

    # 使用公开的测试API
    url = "https://httpbin.org/get"

    start = time.time()
    result = await fetch_single_url(url)
    elapsed = time.time() - start

    print(f"URL: {result['url']}")
    print(f"状态码: {result['status']}")
    print(f"Content-Type: {result['content_type']}")
    print(f"响应长度: {len(result['text'])} 字节")
    print(f"耗时: {elapsed:.4f}秒")
    print()


# ============================================
# 示例2: 并发请求
# ============================================


async def fetch_url(session: Any, url: str) -> dict[str, object]:
    """
    使用共享session发起请求

    Args:
        session: aiohttp 或 Mock 客户端会话
        url: 请求URL

    Returns:
        响应数据
    """
    print(f"→ 请求: {url}")

    async with session.get(url) as response:
        text = await response.text()
        print(f"← 响应: {url} (状态={response.status})")

        return {
            "url": url,
            "status": response.status,
            "length": len(text),
        }


async def demonstrate_concurrent_requests() -> None:
    """演示并发请求"""
    print("=" * 60)
    print("2. 并发HTTP请求")
    print("=" * 60)

    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    start = time.time()

    # 使用共享session（推荐）
    SessionClass = MockSession if _is_mock_mode() else aiohttp.ClientSession
    async with SessionClass() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"\n完成 {len(results)} 个请求")
    print(f"总耗时: {elapsed:.4f}秒")
    if _is_mock_mode():
        print("✅ Mock 模式：瞬时完成（无真实网络延迟）")
    else:
        print(f"✅ 并发执行，比顺序快 {len(urls)}倍！")
    print()


# ============================================
# 示例3: 超时和错误处理
# ============================================


async def fetch_with_timeout(
    session: Any, url: str, timeout: int = 5
) -> dict[str, object] | None:
    """
    带超时的请求

    Args:
        session: aiohttp 或 Mock 客户端会话
        url: 请求URL
        timeout: 超时时间（秒）

    Returns:
        响应数据，失败返回None
    """
    try:
        if _is_mock_mode():
            async with session.get(url) as response:
                return {
                    "url": url,
                    "status": response.status,
                    "success": True,
                }
        else:
            timeout_obj = aiohttp.ClientTimeout(total=timeout)
            async with session.get(url, timeout=timeout_obj) as response:
                return {
                    "url": url,
                    "status": response.status,
                    "success": True,
                }
    except TimeoutError:
        print(f"✗ 超时: {url}")
        return {"url": url, "success": False, "error": "timeout"}
    except Exception as e:  # 捕获更通用的异常（包括 MockSession 场景）
        error_name = type(e).__name__
        if "ClientError" in error_name or "Error" in error_name:
            print(f"✗ 错误: {url} - {e}")
            return {"url": url, "success": False, "error": str(e)}
        raise


async def demonstrate_timeout_handling() -> None:
    """演示超时处理"""
    print("=" * 60)
    print("3. 超时和错误处理")
    print("=" * 60)

    urls = [
        "https://httpbin.org/get",  # 正常
        "https://httpbin.org/delay/10",  # 会超时
        "https://invalid-domain-12345.com",  # 会失败
    ]

    SessionClass = MockSession if _is_mock_mode() else aiohttp.ClientSession
    async with SessionClass() as session:
        tasks = [fetch_with_timeout(session, url, timeout=2) for url in urls]
        results = await asyncio.gather(*tasks)

    success_count = sum(1 for r in results if r and r.get("success"))
    print(f"\n成功: {success_count}/{len(urls)} 个请求")
    print()


# ============================================
# 示例4: POST请求
# ============================================


async def post_json_data(
    session: Any, url: str, data: dict[str, object]
) -> dict[str, object]:
    """
    发送JSON数据

    Args:
        session: aiohttp 或 Mock 客户端会话
        url: 请求URL
        data: 要发送的数据

    Returns:
        响应数据
    """
    async with session.post(url, json=data) as response:
        return {
            "url": url,
            "status": response.status,
            "response": await response.json(),
        }


async def demonstrate_post_request() -> None:
    """演示POST请求"""
    print("=" * 60)
    print("4. POST请求")
    print("=" * 60)

    url = "https://httpbin.org/post"
    data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
    }

    SessionClass = MockSession if _is_mock_mode() else aiohttp.ClientSession
    async with SessionClass() as session:
        result = await post_json_data(session, url, data)

    print(f"状态码: {result['status']}")
    print(f"发送的数据: {data}")
    print(f"服务器返回: {result['response'].get('json')}")
    print()


# ============================================
# 示例5: 实战 - 批量API调用
# ============================================


async def fetch_user_data(session: Any, user_id: int) -> dict[str, object] | None:
    """获取用户数据"""
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None
    except Exception as e:
        print(f"错误: 用户{user_id} - {e}")
        return None


async def demonstrate_batch_api_calls() -> None:
    """演示批量API调用"""
    print("=" * 60)
    print("5. 实战 - 批量API调用")
    print("=" * 60)

    user_ids = list(range(1, 11))  # 用户ID 1-10

    start = time.time()

    SessionClass = MockSession if _is_mock_mode() else aiohttp.ClientSession
    async with SessionClass() as session:
        tasks = [fetch_user_data(session, uid) for uid in user_ids]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    # 统计结果
    success_results = [r for r in results if r is not None]
    print(f"\n成功获取: {len(success_results)}/{len(user_ids)} 个用户")
    print(f"总耗时: {elapsed:.4f}秒")
    print(f"平均每个请求: {elapsed / len(user_ids):.4f}秒")

    # 显示前3个用户
    print("\n前3个用户:")
    for user in success_results[:3]:
        print(f"  - {user.get('name')} ({user.get('email')})")

    print()


# ============================================
# 主函数
# ============================================


async def main(mock_mode: bool = False) -> None:
    """主函数

    Args:
        mock_mode: 是否使用 Mock 模式
    """
    # 设置 Mock 模式
    _set_mock_mode(mock_mode)

    print("\n" + "=" * 60)
    mode_str = "Mock" if mock_mode else "真实"
    print(f"{mode_str}异步HTTP客户端（aiohttp）")
    print("=" * 60 + "\n")

    if mock_mode:
        print("⚠️  Mock 模式：使用模拟数据，无需网络连接")
        print()

    try:
        await demonstrate_single_request()
        await demonstrate_concurrent_requests()
        await demonstrate_timeout_handling()
        await demonstrate_post_request()
        await demonstrate_batch_api_calls()
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n可能的原因：")
        print("1. 网络连接问题")
        print("2. API服务不可用")
        print("3. aiohttp版本不兼容")
        print("\n💡 尝试使用 Mock 模式：")
        print("   uv run python 07_async_http_real.py --mock")
        return

    print("=" * 60)
    print("演示完成！")
    print("=" * 60)
    print()
    print("💡 要点总结：")
    print("1. 使用 aiohttp.ClientSession 管理连接")
    print("2. 共享session可以复用连接，提高性能")
    print("3. 使用 ClientTimeout 设置超时")
    print("4. 妥善处理异常（TimeoutError, ClientError）")
    print("5. POST请求使用 json 参数自动序列化")
    print()
    print("🚀 生产环境建议：")
    print("- 使用连接池限制并发数")
    print("- 实现重试机制（exponential backoff）")
    print("- 添加请求日志和监控")
    print("- 考虑使用 aiohttp 的限流功能")


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="异步HTTP客户端演示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 真实模式（需要网络）
  uv run python 07_async_http_real.py

  # Mock 模式（无需网络）
  uv run python 07_async_http_real.py --mock
        """,
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="使用 Mock 模式，模拟 HTTP 响应（无需网络连接）",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(mock_mode=args.mock))
