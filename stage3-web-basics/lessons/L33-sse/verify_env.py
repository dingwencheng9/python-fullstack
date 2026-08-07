#!/usr/bin/env python3
"""L32 SSE 环境验证脚本。

基础示例与测试只要求 FastAPI/SSE 所需的核心依赖；V2 生产化示例使用的
PostgreSQL、Redis、OpenTelemetry exporter 等按可选依赖处理，缺失时只给出
安装提示，不阻断基础课程学习。
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Dependency:
    """依赖项说明。"""

    import_name: str
    description: str
    package_name: str | None = None

    @property
    def install_name(self) -> str:
        """返回 pip/uv 使用的包名。"""
        return self.package_name or self.import_name


CORE_DEPENDENCIES = [
    Dependency("fastapi", "核心框架"),
    Dependency("uvicorn", "ASGI 服务器", "uvicorn[standard]"),
    Dependency("httpx", "HTTP 客户端"),
    Dependency("pydantic", "数据验证"),
]

OPTIONAL_DEPENDENCIES = [
    Dependency("asyncpg", "V2 PostgreSQL checkpoint 后端"),
    Dependency("redis", "V2 Redis 缓存/会话层"),
    Dependency("opentelemetry", "基础可观测性 API", "opentelemetry-api"),
    Dependency(
        "opentelemetry.exporter.otlp.proto.grpc.trace_exporter",
        "OTLP gRPC trace exporter",
        "opentelemetry-exporter-otlp-proto-grpc",
    ),
    Dependency(
        "opentelemetry.instrumentation.fastapi",
        "opentelemetry.exporter.otlp",
        "FastAPI 自动埋点",
        "opentelemetry-instrumentation-fastapi",
    ),
    Dependency("rich", "CLI 终端渲染"),
    Dependency("langchain_core", "checkpoint_system.py 类型接口", "langchain-core"),
    Dependency("langgraph", "checkpoint_system.py 检查点接口"),
]


def can_import(import_name: str) -> bool:
    """判断模块是否可导入；父包缺失时 find_spec 可能抛 ModuleNotFoundError。"""
    try:
        return importlib.util.find_spec(import_name) is not None
    except ModuleNotFoundError:
        return False


def missing_dependencies(dependencies: Iterable[Dependency]) -> list[Dependency]:
    """检查依赖是否可 import，并打印状态。"""
    missing = []
    for dep in dependencies:
        if can_import(dep.import_name):
            print(f"  ✅ {dep.import_name:48} - {dep.description}")
        else:
            print(f"  ⚠️  {dep.import_name:48} - {dep.description}")
            missing.append(dep)
    return missing


def print_install_hint(title: str, missing: list[Dependency]) -> None:
    """输出安装建议。"""
    if not missing:
        return
    packages = " ".join(dep.install_name for dep in missing)
    print()
    print(title)
    print(f"  uv add {packages}")


def check_optional_services() -> None:
    """尽力检查 PostgreSQL/Redis 服务连通性；失败不作为基础课程错误。"""
    print()
    print("🔌 可选外部服务连通性（失败不阻断基础示例）：")

    if not can_import("asyncpg"):
        print("  ⚠️  PostgreSQL - 跳过，未安装 asyncpg")
    else:
        import asyncio

        import asyncpg

        async def test_postgres() -> None:
            try:
                conn = await asyncpg.connect(
                    "postgresql://postgres:password@localhost:5432/agent_db",
                    timeout=2,
                )
                version = await conn.fetchval("SELECT version()")
                await conn.close()
                print(f"  ✅ PostgreSQL - {version.split(',')[0]}")
            except Exception as exc:
                print(f"  ⚠️  PostgreSQL - 未连接本地 V2 服务：{exc}")

        asyncio.run(test_postgres())

    if not can_import("redis"):
        print("  ⚠️  Redis - 跳过，未安装 redis")
    else:
        import redis as redis_lib

        try:
            client = redis_lib.Redis(host="localhost", port=6379, socket_connect_timeout=2)
            client.ping()
            print("  ✅ Redis - 连接成功")
        except Exception as exc:
            print(f"  ⚠️  Redis - 未连接本地 V2 服务：{exc}")


def main() -> int:
    """执行环境验证。"""
    print("=" * 80)
    print("🔍 L32 SSE 环境验证")
    print("=" * 80)
    print()
    print(f"✓ Python 版本: {sys.version.split()[0]}")

    print()
    print("📦 核心依赖（基础示例/测试需要）：")
    missing_core = missing_dependencies(CORE_DEPENDENCIES)

    print()
    print("📦 可选依赖（V2 生产化示例需要）：")
    missing_optional = missing_dependencies(OPTIONAL_DEPENDENCIES)

    print_install_hint("核心依赖缺失，请先安装：", missing_core)
    print_install_hint("可选依赖缺失；仅运行 app_v2/checkpoint_system 时再安装：", missing_optional)

    check_optional_services()

    print()
    print("=" * 80)
    if missing_core:
        print("❌ 核心依赖不完整：基础 SSE 示例可能无法运行")
        return 1
    print("✅ 核心环境验证通过：可运行基础 SSE 示例与测试")
    if missing_optional:
        print("ℹ️  V2 可选依赖未完全安装；这不影响基础课程路径")
    else:
        print("✅ V2 可选依赖也已安装；可尝试 app_v2.py / checkpoint_system.py")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
