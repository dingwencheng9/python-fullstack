"""练习 5: 添加缓存优化。

目标：设计一个 GitHub Actions 缓存步骤，用于缓存 uv 下载内容。
"""

from __future__ import annotations

UV_CACHE_STEP = {
    "name": "Cache uv",
    "uses": "actions/cache@v4",
    "with": {
        "path": "~/.cache/uv",
        "key": "uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}",
        "restore-keys": "uv-${{ runner.os }}-",
    },
}


if __name__ == "__main__":
    for key, value in UV_CACHE_STEP.items():
        print(f"{key}: {value}")
