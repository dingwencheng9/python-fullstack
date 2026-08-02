"""练习 2：用线程池实现并发下载器。"""

from __future__ import annotations

import time


def fetch_url(url: str) -> str:
    """模拟网络请求；测试时可以 monkeypatch 替换。"""
    time.sleep(0.05)
    return f"data:{url}"


def parallel_download(urls: list[str], max_workers: int = 5) -> dict[str, str]:
    """并发下载 URL，失败的 URL 应被跳过。"""
    # TODO: 导入并使用 ThreadPoolExecutor、submit 和 as_completed 实现。
    # 提示：future_to_url = {executor.submit(fetch_url, url): url for url in urls}
    raise NotImplementedError
