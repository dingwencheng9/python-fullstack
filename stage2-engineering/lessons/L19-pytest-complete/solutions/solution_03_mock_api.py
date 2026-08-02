"""练习 3 参考答案: mock API 调用。"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch


def fetch_user(user_id: int) -> dict[str, Any]:
    """从示例 API 获取用户；404 时返回空字典。"""
    import requests

    resp = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    if resp.status_code == 404:
        return {}
    return resp.json()


@patch("requests.get")
def test_fetch_user_success(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = fetch_user(1)

    assert result == {"id": 1, "name": "Alice"}
    mock_get.assert_called_once_with("https://api.example.com/users/1", timeout=5)


@patch("requests.get")
def test_fetch_user_not_found(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = fetch_user(999)

    assert result == {}
    mock_get.assert_called_once_with("https://api.example.com/users/999", timeout=5)
