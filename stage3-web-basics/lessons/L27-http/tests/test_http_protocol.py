"""L31 HTTP 协议与抓包基础测试。"""

from __future__ import annotations

import pytest
from solutions.solution_01_parse_http_message import parse_request
from solutions.solution_02_build_http_client import build_get_request
from solutions.solution_03_analyze_capture import summarize_status


def test_parse_request_line_and_headers():
    raw = "GET /health HTTP/1.1\r\nHost: localhost\r\nAccept: application/json\r\n\r\n"
    result = parse_request(raw)
    assert result["method"] == "GET"
    assert result["path"] == "/health"
    assert result["headers"]["host"] == "localhost"


def test_parse_request_body_and_content_length():
    raw = "POST /users HTTP/1.1\r\nHost: api\r\nContent-Length: 11\r\n\r\nhello world"
    result = parse_request(raw)
    assert result["body"] == "hello world"


def test_parse_request_invalid_line():
    with pytest.raises(ValueError):
        parse_request("BROKEN\r\n\r\n")


def test_parse_request_content_length_mismatch():
    raw = "POST /x HTTP/1.1\r\nContent-Length: 99\r\n\r\nsmall"
    with pytest.raises(ValueError):
        parse_request(raw)


@pytest.mark.parametrize(
    "host,path,expected",
    [
        ("localhost:8000", "/health", "GET /health HTTP/1.1"),
        ("api.example.com", "users", "GET /users HTTP/1.1"),
    ],
)
def test_build_get_request(host, path, expected):
    req = build_get_request(host, path)
    assert expected in req
    assert f"Host: {host}" in req
    assert req.endswith("\r\n\r\n")


def test_summarize_status():
    lines = [
        "HTTP/1.1 200 OK",
        "HTTP/1.1 404 Not Found",
        "HTTP/1.1 200 OK",
        "not http",
    ]
    assert summarize_status(lines) == {200: 2, 404: 1}


@pytest.mark.parametrize(
    "status_line,code",
    [
        ("HTTP/1.1 200 OK", 200),
        ("HTTP/1.1 422 Unprocessable Entity", 422),
        ("HTTP/2.0 500 Internal Server Error", 500),
    ],
)
def test_summarize_status_parametrized(status_line, code):
    assert summarize_status([status_line]) == {code: 1}
