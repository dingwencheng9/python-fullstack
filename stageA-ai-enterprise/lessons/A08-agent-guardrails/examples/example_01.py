"""A08: Agent 安全护栏与内容过滤

本示例演示 Agent 安全护栏与内容过滤 的核心概念和实现。
"""

from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime
from enum import Enum


class Status(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Config:
    enabled: bool = True
    threshold: float = 0.8
    timeout: int = 30


class BaseProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.status = Status.IDLE

    def process(self, data: Any) -> Any:
        if not self.config.enabled:
            raise ValueError("Feature is disabled")
        return {"processed": data, "status": self.status.value}

    def get_status(self) -> Status:
        return self.status


def main():
    config = Config(enabled=True, threshold=0.9, timeout=60)
    processor = BaseProcessor(config)
    result = processor.process("test data")
    print(f"Result: {result}")
    print(f"Status: {processor.get_status()}")


if __name__ == "__main__":
    main()
