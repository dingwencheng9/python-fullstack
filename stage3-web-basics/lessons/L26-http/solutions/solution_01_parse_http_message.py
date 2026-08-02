"""练习 1 参考答案：解析 HTTP 请求报文。"""

from __future__ import annotations


def parse_request(raw: str) -> dict:
    head, _, body = raw.partition("\r\n\r\n")
    lines = head.split("\r\n")
    if not lines or len(lines[0].split()) != 3:
        raise ValueError("invalid request line")
    method, path, version = lines[0].split()
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid header: {line}")
        key, value = line.split(":", 1)
        headers[key.lower()] = value.strip()
    length = headers.get("content-length")
    if length is not None and int(length) != len(body.encode()):
        raise ValueError("content-length mismatch")
    return {"method": method, "path": path, "version": version, "headers": headers, "body": body}
