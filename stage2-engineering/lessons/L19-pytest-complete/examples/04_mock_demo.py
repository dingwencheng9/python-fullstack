"""L17 示例 4: mock 使用"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


def fetch_data(url: str) -> dict:
    import requests

    resp = requests.get(url, timeout=5)
    return resp.json()


@patch("requests.get")
def test_fetch_data(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_get.return_value = mock_response

    result = fetch_data("https://api.example.com/data")
    assert result["status"] == "ok"
    mock_get.assert_called_once()
