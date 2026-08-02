"""L26 选读：match/case 模式匹配示例（Python 3.10+）。

from __future__ import annotations

⚠️ 这是 Stage 2 的**选读补充**，不是 L26 任何练习的必需答案。
match/case 已在 Stage 0 L03 / L04 入门，本文件作为 Python 3.13 基线下的更简短示例保留。
"""

from __future__ import annotations


def http_status(code: int) -> str:
    """根据 HTTP 状态码返回简短描述。"""
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "Unknown"
