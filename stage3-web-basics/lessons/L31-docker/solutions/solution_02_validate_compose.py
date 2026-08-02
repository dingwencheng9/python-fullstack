"""练习 2 参考答案: Compose 配置校验。"""

from __future__ import annotations


def validate_compose(config: dict) -> list[str]:
    errors: list[str] = []
    services = config.get("services", {})
    if not services:
        return ["missing services"]

    api = services.get("api")
    redis_exists = "redis" in services
    redis = services.get("redis", {})

    if not api:
        errors.append("missing api service")
    else:
        if "ports" not in api:
            errors.append("api must expose ports")
        deps = api.get("depends_on", [])
        depends_on_redis = "redis" in deps if isinstance(deps, list) else "redis" in deps.keys()
        if not depends_on_redis:
            errors.append("api must depend on redis")

    if not redis_exists:
        errors.append("missing redis service")
    elif "volumes" not in redis:
        errors.append("redis should persist data with volume")

    return errors
