"""L55 生产健康检查示例

from __future__ import annotations

用于 Docker Compose healthcheck:
    python -m app.healthcheck
"""

from __future__ import annotations

from dataclasses import dataclass
import os
import sys


@dataclass(frozen=True)
class HealthCheckResult:
    """健康检查结果"""

    name: str
    ok: bool
    detail: str


def check_required_env() -> HealthCheckResult:
    """检查生产必需环境变量"""
    required = ["DATABASE_URL", "REDIS_URL", "JWT_SECRET"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        return HealthCheckResult("env", False, f"missing: {', '.join(missing)}")
    return HealthCheckResult("env", True, "required env present")


def check_jwt_secret_strength() -> HealthCheckResult:
    """检查 JWT secret 长度"""
    secret = os.getenv("JWT_SECRET", "")
    if len(secret) < 32:
        return HealthCheckResult("jwt_secret", False, "JWT_SECRET must be >= 32 chars")
    return HealthCheckResult("jwt_secret", True, "secret length ok")


def run_healthchecks() -> list[HealthCheckResult]:
    """运行所有本地健康检查"""
    return [check_required_env(), check_jwt_secret_strength()]


def main() -> int:
    """CLI 入口，返回 0 表示健康"""
    results = run_healthchecks()
    for result in results:
        status = "OK" if result.ok else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
