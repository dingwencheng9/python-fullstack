"""projects/ 下多项目测试隔离。

from __future__ import annotations

每个项目都有自己的 app/scraper/pipeline 等顶层包。批量运行
`pytest projects/` 时，前一个项目导入的同名包会留在 sys.modules，
导致后续项目导入到错误模块。
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys

PROJECT_MODULE_PREFIXES = (
    "app",
    "scraper",
    "pipeline",
    "tests",
)

logger = logging.getLogger(__name__)


def _project_root_for_path(path: Path) -> Path | None:
    """返回 projects/<project-name> 根目录。"""
    try:
        parts = path.parts
        if "projects" not in parts:
            return None
        idx = parts.index("projects")
        if len(parts) <= idx + 1:
            return None
        return Path(*parts[: idx + 2])
    except Exception as e:
        logger.warning(f"Error determining project root for path {path}: {e}")
        return None


def _clear_project_modules() -> None:
    """清理项目级顶层包缓存。"""
    try:
        modules_to_remove = []
        for module_name in list(sys.modules):
            if any(
                module_name == prefix or module_name.startswith(f"{prefix}.")
                for prefix in PROJECT_MODULE_PREFIXES
            ):
                modules_to_remove.append(module_name)

        for module_name in modules_to_remove:
            try:
                sys.modules.pop(module_name, None)
            except Exception as e:
                logger.warning(f"Error removing module {module_name} from sys.modules: {e}")
    except Exception as e:
        logger.warning(f"Error clearing project modules: {e}")


def _setup_project_path(path: Path) -> None:
    try:
        project_root = _project_root_for_path(path)
        if project_root is None:
            return

        _clear_project_modules()

        try:
            project_path = str(project_root.resolve())
            sys.path[:] = [p for p in sys.path if p != project_path]
        except Exception as e:
            logger.warning(f"Error resolving project path {project_root}: {e}")
    except Exception as e:
        logger.warning(f"Error setting up project path for {path}: {e}")


def pytest_collect_file(file_path: Path, parent: object) -> None:
    """收集测试文件前切换项目 import path。"""
    try:
        if file_path.name.startswith("test_"):
            _setup_project_path(file_path)
    except Exception as e:
        logger.warning(f"Error in pytest_collect_file for {file_path}: {e}")


def pytest_runtest_setup(item: object) -> None:
    """每个测试运行前重新确认项目 import path。"""
    try:
        fspath = getattr(item, "fspath", None)
        if fspath is not None:
            _setup_project_path(Path(str(fspath)))
    except Exception as e:
        logger.warning(f"Error in pytest_runtest_setup: {e}")
