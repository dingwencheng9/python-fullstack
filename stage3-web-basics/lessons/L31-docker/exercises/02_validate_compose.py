"""

from __future__ import annotations

练习 2: Compose 配置校验

实现 validate_compose(config: dict) -> list[str]
检查：
1. services 是否存在
2. api 服务是否暴露 ports
3. redis 是否有 volume
4. api 是否依赖 redis
"""


def validate_compose(config: dict) -> list[str]:
    raise NotImplementedError
