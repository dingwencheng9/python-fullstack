"""示例 3：ThreadPoolExecutor / Future / as_completed。"""

from __future__ import annotations

import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed


def fetch_resource(url: str) -> str:
    """模拟网络请求。"""
    time.sleep(0.05)
    if "bad" in url:
        raise ValueError(f"请求失败: {url}")
    return f"content:{url}"


def demo_submit() -> None:
    """submit 返回 Future，可单独获取结果。"""
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="fetch") as executor:
        future: Future[str] = executor.submit(fetch_resource, "http://example.com")
        print(f"submit result = {future.result()}")


def demo_map() -> None:
    """map 保持输入顺序，但遇到异常会在迭代时抛出。"""
    urls = ["http://a", "http://b", "http://c"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_resource, urls))
    print(f"map results = {results}")


def demo_as_completed() -> None:
    """as_completed 按完成顺序处理结果并隔离异常。"""
    urls = ["http://a", "http://bad", "http://c"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(fetch_resource, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                print(f"{url} -> {future.result()}")
            except ValueError as exc:
                print(f"{url} failed: {exc}")


def main() -> None:
    """运行线程池示例。"""
    demo_submit()
    demo_map()
    demo_as_completed()


if __name__ == "__main__":
    main()
