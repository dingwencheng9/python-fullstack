"""练习 2 参考答案：可测试的线程池并发下载器。"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


def fetch_url(url: str) -> str:
    """模拟网络请求；测试可通过 monkeypatch 注入替代实现。"""
    time.sleep(0.05)
    return f"data:{url}"


def parallel_download(urls: list[str], max_workers: int = 5) -> dict[str, str]:
    """并发下载 URL，返回成功结果字典，失败 URL 会被记录并跳过。

    设计要点：
    - 真实 I/O 封装在模块级 ``fetch_url`` 中，便于测试替换。
    - 工作线程只返回结果；主线程集中写入 ``results``，避免共享写入竞态。
    - 单个 URL 失败不让整批任务崩溃，但通过 warning 日志保留上下文。
    """
    if max_workers <= 0:
        msg = "max_workers 必须大于 0"
        raise ValueError(msg)

    results: dict[str, str] = {}
    if not urls:
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as exc:
                logger.warning("下载失败 url=%s 原因=%s", url, exc)
    return results
