"""

from __future__ import annotations

练习 2: 生产级 Docker Compose 检查器

任务：实现 validate_compose_config(config: dict) -> list[str]

要求检查：
1. api 服务必须存在 healthcheck
2. postgres / redis / qdrant 必须配置 volume
3. 所有服务必须有 restart 策略
4. api 必须依赖 postgres/redis/qdrant 的 service_healthy
5. POSTGRES_PASSWORD 不能是硬编码明文，必须使用环境变量表达式

返回值：错误消息列表。无错误返回空列表。
"""

from __future__ import annotations
import re


def validate_compose_config(config: dict) -> list[str]:
    """验证生产级 compose 配置。

    TODO: 实现校验逻辑。
    """
    errors = []

    try:
        services = config.get("services", {})

        # 检查1: api 服务必须存在 healthcheck
        api_service = services.get("api", {})
        if "healthcheck" not in api_service:
            errors.append("API service must have a healthcheck defined")

        # 检查2: postgres / redis / qdrant 必须配置 volume
        required_volume_services = ["postgres", "redis", "qdrant"]
        for service_name in required_volume_services:
            service = services.get(service_name, {})
            if not service.get("volumes"):
                errors.append(f"{service_name} service must have volumes configured")

        # 检查3: 所有服务必须有 restart 策略
        for service_name, service in services.items():
            if "restart" not in service:
                errors.append(f"{service_name} service must have a restart policy")

        # 检查4: api 必须依赖 postgres/redis/qdrant 的 service_healthy
        api_depends_on = api_service.get("depends_on", {})
        required_healthy_deps = ["postgres", "redis", "qdrant"]
        for dep in required_healthy_deps:
            if dep not in api_depends_on:
                errors.append(f"API service must depend on {dep} with service_healthy condition")
            elif api_depends_on.get(dep) != {"condition": "service_healthy"}:
                errors.append(
                    f"API service's dependency on {dep} must use service_healthy condition"
                )

        # 检查5: POSTGRES_PASSWORD 不能是硬编码明文，必须使用环境变量表达式
        postgres_service = services.get("postgres", {})
        env_vars = postgres_service.get("environment", {})
        if "POSTGRES_PASSWORD" in env_vars:
            postgres_password = env_vars["POSTGRES_PASSWORD"]
            if not re.match(r"^\$\{[^}]+\}$", str(postgres_password)):
                errors.append(
                    "POSTGRES_PASSWORD must use environment variable expression (e.g., ${POSTGRES_PASSWORD})"
                )

    except Exception as e:
        errors.append(f"Configuration validation error: {str(e)}")

    return errors
