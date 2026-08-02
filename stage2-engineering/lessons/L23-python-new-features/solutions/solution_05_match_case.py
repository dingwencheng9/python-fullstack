"""L25 练习5 参考：match/case"""

from __future__ import annotations


def http_status(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "Unknown"
