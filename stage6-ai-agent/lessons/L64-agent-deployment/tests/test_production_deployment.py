"""L55 生产部署配置测试。"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict

import pytest

LESSON_DIR = Path(__file__).parent.parent
COMPOSE_FILE = LESSON_DIR / "examples" / "02_docker_compose_prod.yml"
ENV_FILE = LESSON_DIR / "examples" / "03_env_example.txt"
HEALTHCHECK_FILE = LESSON_DIR / "examples" / "04_healthcheck.py"


def _load_solution() -> Any:
    """加载解决方案模块。"""
    path = LESSON_DIR / "solutions" / "02_production_compose.py"
    try:
        spec = importlib.util.spec_from_file_location("production_compose", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"无法加载模块: {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module
    except Exception as e:
        raise ImportError(f"加载解决方案模块失败: {e}") from e


def _read_file_safely(file_path: Path) -> str:
    """安全读取文件内容。"""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        return file_path.read_text(encoding="utf-8")
    except Exception as e:
        raise IOError(f"读取文件失败 {file_path}: {e}") from e


def test_compose_file_exists() -> None:
    """生产 compose 文件存在。"""
    try:
        content = _read_file_safely(COMPOSE_FILE)
        assert content.startswith("# L55")
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_compose_contains_required_services() -> None:
    """compose 包含核心服务。"""
    try:
        content = _read_file_safely(COMPOSE_FILE)
        for service in ("api:", "postgres:", "redis:", "qdrant:"):
            assert service in content, f"缺少服务: {service}"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_compose_has_healthchecks() -> None:
    """关键服务都有 healthcheck。"""
    try:
        content = _read_file_safely(COMPOSE_FILE)
        assert content.count("healthcheck:") >= 4, "healthcheck 数量不足"
        assert "service_healthy" in content, "缺少 service_healthy 条件"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_compose_has_persistent_volumes() -> None:
    """数据库/缓存/向量库配置持久化卷。"""
    try:
        content = _read_file_safely(COMPOSE_FILE)
        for volume in ("postgres_data", "redis_data", "qdrant_data"):
            assert volume in content, f"缺少持久化卷: {volume}"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_env_example_contains_required_keys() -> None:
    """env 示例包含生产必需变量。"""
    try:
        content = _read_file_safely(ENV_FILE)
        for key in ("DATABASE_URL", "REDIS_URL", "QDRANT_URL", "JWT_SECRET"):
            assert key in content, f"缺少环境变量: {key}"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_healthcheck_module_runs() -> None:
    """健康检查模块可导入。"""
    try:
        spec = importlib.util.spec_from_file_location("healthcheck", HEALTHCHECK_FILE)
        if spec is None or spec.loader is None:
            raise ImportError(f"无法加载健康检查模块: {HEALTHCHECK_FILE}")
        module = importlib.util.module_from_spec(spec)
        sys.modules["healthcheck"] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        assert hasattr(module, "run_healthchecks"), "健康检查模块缺少 run_healthchecks 函数"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


def test_validate_compose_config_success() -> None:
    """参考答案能接受符合要求的配置。"""
    try:
        module = _load_solution()
        config: Dict[str, Any] = {
            "services": {
                "api": {
                    "healthcheck": {"test": ["CMD", "curl", "-f", "http://localhost:8000/health"]},
                    "restart": "unless-stopped",
                    "depends_on": {
                        "postgres": {"condition": "service_healthy"},
                        "redis": {"condition": "service_healthy"},
                        "qdrant": {"condition": "service_healthy"},
                    },
                },
                "postgres": {
                    "volumes": ["postgres_data:/var/lib/postgresql/data"],
                    "restart": "unless-stopped",
                    "environment": {"POSTGRES_PASSWORD": "${POSTGRES_PASSWORD:?required}"},
                },
                "redis": {"volumes": ["redis_data:/data"], "restart": "unless-stopped"},
                "qdrant": {"volumes": ["qdrant_data:/qdrant/storage"], "restart": "unless-stopped"},
            }
        }
        errors = module.validate_compose_config(config)
        assert errors == [], f"验证失败，发现错误: {errors}"
    except Exception as e:
        pytest.fail(f"测试失败: {e}")


@pytest.mark.parametrize("missing_service", ["postgres", "redis", "qdrant"])
def test_validate_compose_config_missing_service(missing_service: str) -> None:
    """参数化：缺少关键服务会报错。"""
    try:
        module = _load_solution()
        config: Dict[str, Any] = {
            "services": {"api": {"healthcheck": {}, "restart": "unless-stopped"}}
        }
        errors = module.validate_compose_config(config)
        assert any(missing_service in error for error in errors), (
            f"缺少服务 {missing_service} 未被检测到"
        )
    except Exception as e:
        pytest.fail(f"测试失败: {e}")
