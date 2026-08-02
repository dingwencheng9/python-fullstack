"""L17 练习 5 参考：CI 缓存。"""

from __future__ import annotations

# 在 .github/workflows/ci.yml 中添加：
# - name: Cache uv
#   uses: actions/cache@v4
#   with:
#     path: ~/.cache/uv
#     key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
