"""L31 示例: 模拟 Compose 启动。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Service:
    name: str
    image: str
    ports: str


def start_mock_compose() -> None:
    services = [
        Service("api", "app:latest", "8000:8000"),
        Service("redis", "redis:7-alpine", "6379:6379"),
    ]
    for s in services:
        print(f"Starting {s.name} ({s.image}) on {s.ports}")


if __name__ == "__main__":
    start_mock_compose()
