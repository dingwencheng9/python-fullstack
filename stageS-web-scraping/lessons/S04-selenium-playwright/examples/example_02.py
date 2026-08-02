"""示例代码：Playwright 请求/响应拦截"""
from dataclasses import dataclass


@dataclass
class CapturedRequest:
    url: str
    method: str
    post_data: str | None = None


@dataclass
class CapturedResponse:
    url: str
    status: int
    body: str


async def intercept_api() -> tuple[list[CapturedRequest], list[CapturedResponse]]:
    """拦截页面中的 API 请求和响应。"""
    # TODO: 使用 Playwright route API 拦截
    # route.abort() 可以阻止请求
    # route.fulfill() 可以自定义响应
    requests: list[CapturedRequest] = []
    responses: list[CapturedResponse] = []
    return requests, responses


if __name__ == "__main__":
    print("Playwright API 拦截示例")
