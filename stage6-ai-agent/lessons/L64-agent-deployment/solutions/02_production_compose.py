"""L55 练习 2: 生产级 Docker Compose 检查器 — 参考答案"""

from __future__ import annotations

from typing import Any


def validate_compose_config(config: dict[str, Any]) -> list[str]:
    """
    验证生产级 compose 配置，返回错误列表。

    Args:
        config: Docker Compose 配置字典

    Returns:
        list[str]: 错误信息列表，如果没有错误则返回空列表
    """
    errors: list[str] = []
    services: dict[str, Any] = config.get("services", {})

    # 检查 api 服务
    api: dict[str, Any] | None = services.get("api")
    if not api:
        return ["missing api service"]

    if not api.get("healthcheck"):
        errors.append("api service must define healthcheck")

    # 检查持久化服务和重启策略
    required_services: list[str] = ["postgres", "redis", "qdrant"]
    for service_name in required_services:
        service: dict[str, Any] | None = services.get(service_name)
        if not service:
            errors.append(f"missing {service_name} service")
            continue
        if not service.get("volumes"):
            errors.append(f"{service_name} must define persistent volume")
        if not service.get("restart"):
            errors.append(f"{service_name} must define restart policy")

    # 检查 api 服务的重启策略
    if not api.get("restart"):
        errors.append("api must define restart policy")

    # 检查 api 服务对其他服务的依赖条件
    depends_on: dict[str, Any] = api.get("depends_on", {})
    for service_name in required_services:
        condition: str | None = depends_on.get(service_name, {}).get("condition")
        if condition != "service_healthy":
            errors.append(f"api must wait for {service_name} service_healthy")

    # 检查 postgres 密码是否来自环境变量
    postgres_env: dict[str, Any] = services.get("postgres", {}).get("environment", {})
    password: str = postgres_env.get("POSTGRES_PASSWORD", "")
    if password and "${" not in str(password):
        errors.append("POSTGRES_PASSWORD must come from environment expression")

    return errors
