"""全仓库 pytest 配置 - 集中化 solution/example 加载。

课程测试目录下不再有 conftest.py，所有 solution/example 加载由本文件集中处理。
"""

from __future__ import annotations

# 兼容性别名：在导入任何课程代码之前设置
import sys as _sys

# python-jose 使用 'from jose import jwt'，但课程代码使用 'import jwt'
# 添加 jwt 别名以兼容两种导入方式
try:
    from jose import jwt as _jwt
    if "jwt" not in _sys.modules:
        _sys.modules["jwt"] = _jwt
except ImportError:
    pass

from collections.abc import Generator  # noqa: TC003  # 运行时用于 fixture 返回类型注解
import importlib.util
import logging
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Literal

import pandas as pd  # noqa: TC002  # 用于类型注解
import pytest

logger = logging.getLogger(__name__)

# 追踪 sys.modules 写入（用于调试 conftest.py 注册问题）
_orig_setitem = sys.modules.__setitem__
_trace_keys = {"tests.conftest", "conftest"}
def _trace_setitem(key, value):
    if key in _trace_keys or key.endswith(".conftest"):
        import traceback
        logger.warning(f"[SYSMODULES SET] {key!r} = {value} (file={getattr(value, '__file__', 'N/A')})")
        for line in traceback.format_stack()[-5:]:
            logger.warning(f"  {line.strip()}")
    return _orig_setitem(key, value)
# 注意：暂不激活，避免影响 pytest 自身行为
# sys.modules.__setitem__ = _trace_setitem

# 已加载的 modules 缓存
_LOADED_MODULES: dict[str, ModuleType] = {}

# 仓库根目录（动态向上查找，确保无论 pytest rootdir 在哪都正确）
_REPO_ROOT: Path | None = None

# Lesson 映射缓存（延迟初始化）
_LESSON_MAP: dict[Path, tuple[Path, Literal["solutions"] | Literal["examples"]]] | None = None


def load_exercise_module(name: str, file_path: Path) -> ModuleType:
    """按物理路径加载模块，不污染 sys.path。

    这是所有课程测试共用的模块加载函数。
    在根 conftest.py 中定义，确保所有课程的测试都能访问。
    """
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _get_exercises_dir(lesson_dir: Path) -> Path | None:
    """从 lesson 目录获取 exercises 子目录路径。

    Stage 0 课程使用 exercises/ 作为练习目录。
    """
    exercises_dir = lesson_dir / "exercises"
    if exercises_dir.is_dir():
        return exercises_dir
    return None


# ============================================================================
# Stage 0 Exercises 专用 Fixture 工厂
# ============================================================================

# L01 exercises 模块映射
_L01_EXERCISES = {
    "hello": "01_hello_practice.py",
    "io": "02_io_practice.py",
    "types": "03_type_basics.py",
    "conversion": "04_type_conversion.py",
    "fstring": "05_fstring_practice.py",
}

# L02 exercises 模块映射
_L02_EXERCISES = {
    "arithmetic": "01_arithmetic_conditions.py",
    "logical": "02_logical_operators.py",
    "bitwise": "03_bitwise_operations.py",
    "loops": "04_loops.py",
    "match": "05_match_case.py",
    "comprehensive": "06_comprehensive.py",
}

# L04 exercises 模块映射
_L04_EXERCISES = {
    "functions": "01_functions.py",
    "modules": "02_modules.py",
}

# L05 exercises 模块映射
_L05_EXERCISES = {
    "pdb": "01_pdb_practice.py",
    "traceback": "02_traceback_practice.py",
}

# L06 exercises 模块映射
_L06_EXERCISES = {
    "basic_handling": "01_basic_handling.py",
    "multiple_exceptions": "02_multiple_exceptions.py",
    "custom_exceptions": "03_custom_exceptions.py",
}

# L07 exercises 模块映射
_L07_EXERCISES = {
    "oop_basics": "01_oop_basics.py",
    "inheritance": "02_inheritance_practice.py",
    "property": "03_property_practice.py",
}

# L08 exercises 模块映射
_L08_EXERCISES = {
    "fraction": "01_fraction.py",
    "set_class": "02_set_class.py",
    "callable": "03_callable.py",
}

# L09 exercises 模块映射
_L09_EXERCISES = {
    "log_parser": "01_log_parser.py",
    "csv_writer": "02_csv_writer.py",
    "file_search": "03_file_search.py",
}


def _discover_lesson_exercises(lesson_dir: Path) -> dict[str, str]:
    """发现 lesson 下 exercises/ 目录中的所有 .py 文件。

    返回 {module_name: filename} 映射。
    """
    exercises_dir = _get_exercises_dir(lesson_dir)
    if exercises_dir is None:
        return {}

    modules = {}
    for py_file in exercises_dir.glob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "__init__.py":
            continue
        # 去掉 .py 后缀和数字前缀（如 01_hello → hello）
        stem = py_file.stem
        cleaned = re.sub(r"^\d+_", "", stem)
        modules[cleaned] = py_file.name
        modules[stem] = py_file.name  # 也保留原始名称

    return modules


def _find_repo_root() -> Path:
    """动态向上查找仓库根目录。

    当 pytest rootdir 是 lesson 目录时，conftest.py 的 __file__ 会指向 lesson 目录，
    因此需要向上查找包含 stage*/ 目录的真正仓库根。
    """
    conf_dir = Path(__file__).resolve().parent
    # 向上查找直到找到包含 stage*/ 目录的目录
    for parent in [conf_dir, *list(conf_dir.parents)]:
        stage_dirs = list(parent.glob("stage*"))
        # 排除 __pycache__ 等
        stage_dirs = [d for d in stage_dirs if d.is_dir() and d.name.startswith("stage")]
        if stage_dirs:
            return parent
    # Fallback: 使用 conftest 所在目录
    return conf_dir


def _discover_lessons() -> dict[Path, tuple[Path, Literal["solutions"] | Literal["examples"]]]:
    """发现所有包含 tests/ 和 solutions/ 或 examples/ 的 lesson 目录。

    使用延迟初始化避免在 pytest 启动时扫描所有目录。
    """
    global _REPO_ROOT, _LESSON_MAP  # noqa: PLW0603

    # 延迟初始化：只在首次调用时扫描
    if _LESSON_MAP is not None:
        return _LESSON_MAP

    _REPO_ROOT = _find_repo_root()

    lessons: dict[Path, tuple[Path, Literal["solutions"] | Literal["examples"]]] = {}
    for stage_dir in sorted(_REPO_ROOT.iterdir()):
        if not stage_dir.is_dir() or not stage_dir.name.startswith("stage"):
            continue
        lessons_dir = stage_dir / "lessons"
        if not lessons_dir.is_dir():
            continue
        for lesson_dir in sorted(lessons_dir.iterdir()):
            if not lesson_dir.is_dir() or not (lesson_dir.name.startswith("L") or lesson_dir.name.startswith("P")):
                continue
            tests_dir = lesson_dir / "tests"
            solutions_dir = lesson_dir / "solutions"
            examples_dir = lesson_dir / "examples"
            if tests_dir.is_dir():
                if solutions_dir.is_dir():
                    lessons[lesson_dir] = (solutions_dir, "solutions")
                elif examples_dir.is_dir():
                    lessons[lesson_dir] = (examples_dir, "examples")

    _LESSON_MAP = lessons
    logger.info(f"发现 {len(_LESSON_MAP)} 个课程测试目录 (repo_root={_REPO_ROOT})")
    return _LESSON_MAP


def _get_lesson_map() -> dict[Path, tuple[Path, Literal["solutions"] | Literal["examples"]]]:
    """获取 lesson 映射（延迟初始化）。"""
    if _LESSON_MAP is None:
        _discover_lessons()
    return _LESSON_MAP or {}


def _get_lesson_dir(file_path: str) -> Path | None:
    """从测试文件路径获取对应的 lesson 目录。"""
    try:
        parts = Path(file_path).resolve().parts
        if "lessons" not in parts or "tests" not in parts:
            return None
        tests_index = parts.index("tests")
        if tests_index < 2:
            return None
        lesson_dir = Path(*parts[:tests_index])
        if lesson_dir.name.startswith("L") or lesson_dir.name.startswith("P"):
            return lesson_dir.resolve()
        return None
    except Exception:
        return None


def _load_modules(  # noqa: PLR0912, PLR0915
    lesson_dir: Path, target_dir: Path, module_type: Literal["solutions"] | Literal["examples"]
) -> ModuleType:
    """加载指定 lesson 的 solutions 或 examples 包。

    子模块始终注册到 sys.modules（支持 `from solutions.xxx import X`）。
    Bare 模块名（sys.modules["solutions"]）只在 lesson 只有一个模块目录时才注册，
    以避免 solutions/ 和 examples/ 同时存在时的命名冲突。

    无法导入的模块会被跳过（可能是缺少可选依赖如 fastapi 等）。
    """
    cache_key = f"{lesson_dir.resolve()}::{module_type}"
    if cache_key in _LOADED_MODULES:
        return _LOADED_MODULES[cache_key]

    # 检查 lesson 是否同时有 solutions/ 和 examples/
    # 创建虚拟包对象
    package = ModuleType(module_type)
    package.__path__ = [str(target_dir)]
    package.__package__ = module_type

    # 将 target_dir 加入 sys.path（仅在必要时）
    if str(target_dir) not in sys.path:
        sys.path.insert(0, str(target_dir))

    # 加载所有 .py 文件（排除 __init__.py 和 conftest.py）
    # 注意：跳过 conftest.py 是为了避免 "Plugin already registered" 错误：
    # lesson conftest.py 被 pytest 自动加载为 plugin，如果通过本函数 exec_module
    # 加载，其 __name__ 为 "tests.conftest"，pytest 后续用全路径导入时会报错。
    for sub_file in sorted(target_dir.glob("*.py")):
        if sub_file.stem.startswith("_") or sub_file.name == "conftest.py":
            continue
        if sub_file.name == "__init__.py":
            continue  # 单独处理（见下方）

        # DEBUG
        logger.warning(f"[DEBUG _load_modules] loading: {sub_file} (name={sub_file.name}, __name__=solutions.{sub_file.stem})")

        # 使用 importlib 加载模块
        sub_name = sub_file.stem
        # 完整模块名（支持 `from solutions.solution_01 import X`）
        full_name = f"{module_type}.{sub_name}"
        spec = importlib.util.spec_from_file_location(
            full_name,
            sub_file,
            submodule_search_locations=[str(target_dir)],
        )
        if spec is None or spec.loader is None:
            continue

        try:
            module = importlib.util.module_from_spec(spec)
            # 使用模块自身的 __name__ 注册，让 SQLAlchemy 等库在类定义阶段
            # 解析 Mapped[T] 注解时能通过 sys.modules[module.__name__] 找到它
            sys.modules[module.__name__] = module
            # DEBUG: 追踪 tests.conftest 注册
            if module.__name__ == "tests.conftest":
                import traceback
                logger.warning(f"[DEBUG CRITICAL] tests.conftest registered! module={module}, __file__={getattr(module, '__file__', 'N/A')}")
                for line in traceback.format_stack()[-10:]:
                    logger.warning(f"  {line.strip()}")
            # DEBUG
            logger.warning(f"[DEBUG sys.modules] set {module.__name__} = {module} (file={getattr(module, '__file__', 'N/A')})")
            spec.loader.exec_module(module)
        except Exception as e:
            # 跳过因缺少可选依赖（如 sqlalchemy/fastapi 等）而无法加载的文件。
            # 也跳过 MappedAnnotationError 等解析错误。
            logger.debug(f"跳过 {sub_file.name}: {type(e).__name__}: {e}")
            # 撤销已注册的条目
            sys.modules.pop(module.__name__, None)
            continue

        # 添加子模块本身到虚拟包上
        setattr(package, sub_file.stem, module)

        # 同时注册去数字前缀的别名（如 01_xxx → xxx），兼容测试中的裸名引用
        cleaned = re.sub(r"^\d+_", "", sub_file.stem)
        if cleaned and cleaned != sub_file.stem and not hasattr(package, cleaned):
            setattr(package, cleaned, module)

        # 将子模块的所有公共属性也添加到虚拟包上
        for attr_name in dir(module):
            if attr_name.startswith("_"):
                continue
            if not hasattr(package, attr_name):
                setattr(package, attr_name, getattr(module, attr_name))

    # 如果有 __init__.py，执行它以获取 re-exports（__all__ 声明的符号）
    init_file = target_dir / "__init__.py"
    if init_file.is_file():
        full_init_name = module_type  # e.g. "solutions"
        # __init__.py 的 spec
        init_spec = importlib.util.spec_from_file_location(full_init_name, init_file)
        if init_spec:
            try:
                init_mod = importlib.util.module_from_spec(init_spec)
                # 复用已有的 package 对象（保留已注入的子模块属性）
                init_mod.__path__ = package.__path__
                init_mod.__package__ = package.__package__
                init_mod.__dict__.update(package.__dict__)  # 继承已有属性
                sys.modules[full_init_name] = init_mod
                init_spec.loader.exec_module(init_mod)
                # 同步回 package
                package.__dict__.update(init_mod.__dict__)
            except Exception as e:
                logger.debug(f"执行 {init_file} 失败: {e}")

    _LOADED_MODULES[cache_key] = package

    # 总是注册 bare 模块名：pytest_runtest_setup 会根据 lesson 的主要 module_type
    # 覆盖为正确值，dual_mode 下两侧都需要 bare key（lesson 的两种测试可能导入不同包）
    sys.modules[module_type] = package

    return package


def _get_module_type(file_path: str) -> Literal["solutions"] | Literal["examples"] | None:
    """根据测试文件内容判断它从哪个模块导入。

    扫描测试文件的头部（最多前 50 行），检查是否有
    `from solutions.` 或 `from examples.` 导入语句。
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        lines = content.split("\n")[:50]
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("from solutions.", "import solutions.")):
                return "solutions"
            if stripped.startswith(("from examples.", "import examples.")):
                return "examples"
        return None
    except Exception:
        return None


# 当前活跃的 lesson 目录（用于 fixture）
_CURRENT_LESSON: Path | None = None


def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: list[pytest.Item]) -> None:
    """收集阶段钩子（模块加载由 fixture 驱动以确保正确隔离）。

    不在此处预加载所有 lesson 的模块。
    如果在此预加载，`sys.modules["solutions"]` 会被设为最后一个 lesson 的包，
    而 module-scoped fixture 在每个测试模块 setup 时才运行（此时 import 已完成）。
    正确的做法：让 _lesson_fixture_injector 在每个测试模块 setup 时按需加载。
    """


def pytest_pycollect_makemodule(module_path: Path, parent: object) -> None:
    """在每个测试模块被 import 之前加载对应的 solutions/examples 模块。

    对于同时有 solutions/ 和 examples/ 的 lesson，两个目录都会被加载，
    确保不同测试文件能从不同目录导入。
    """
    global _CURRENT_LESSON  # noqa: PLW0603

    lesson_dir = _get_lesson_dir(str(module_path))
    if lesson_dir is None:
        return

    lesson_dir_abs = lesson_dir.resolve()
    if lesson_dir_abs not in _get_lesson_map():
        return

    target_dir, primary_type = _get_lesson_map()[lesson_dir_abs]

    # 加载 LESSON_MAP 中的主要模块类型
    try:
        if lesson_dir_abs != _CURRENT_LESSON:
            _load_modules(lesson_dir_abs, target_dir, primary_type)
            _CURRENT_LESSON = lesson_dir_abs
    except Exception as e:
        logger.warning(f"加载 {lesson_dir_abs} 失败: {e}")

    # 如果 lesson 同时有 solutions/ 和 examples/，也加载另一个
    # 以支持同一 lesson 中不同测试文件从不同目录导入
    solutions_dir = lesson_dir_abs / "solutions"
    examples_dir = lesson_dir_abs / "examples"
    if solutions_dir.is_dir() and examples_dir.is_dir():
        other_dir = examples_dir if target_dir == solutions_dir else solutions_dir
        other_type = "examples" if target_dir == solutions_dir else "solutions"
        cache_key = f"{lesson_dir_abs}::{other_type}"
        if cache_key not in _LOADED_MODULES:
            try:
                _load_modules(lesson_dir_abs, other_dir, other_type)
            except Exception as e:
                logger.warning(f"加载 {lesson_dir_abs} {other_type} 失败: {e}")


def pytest_configure(config: object) -> None:
    """pytest 初始化 - 清理可能冲突的模块。"""
    for module_name in list(sys.modules):
        if module_name in ("solutions", "examples") or module_name.startswith(
            ("_test_solutions", "_test_examples", "solution_", "example_", "tests.conftest")
        ):
            sys.modules.pop(module_name, None)


def _inject_solutions_attrs(lesson_dir: Path, mapping: dict[str, str]) -> None:
    """将 solutions 包子模块注入到测试模块的命名空间。"""
    pkg = sys.modules.get("solutions")
    if not pkg:
        return
    lesson_name = lesson_dir.name
    for local_name, attr_name in mapping.items():
        val = getattr(pkg, attr_name, None)
        if val is None:
            continue
        for test_mod in list(sys.modules.values()):
            if getattr(test_mod, "__file__", "") and lesson_name in str(getattr(test_mod, "__file__", "")):
                test_mod.__dict__[local_name] = val


def _load_examples_submodule(name: str, examples_dir: Path) -> ModuleType:
    """从 examples_dir 动态加载子模块（使用唯一名称避免 sys.modules 冲突）。"""
    src = examples_dir / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"examples.{name}", src)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 {name}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"examples.{name}"] = mod
    spec.loader.exec_module(mod)
    return mod


# ============================================================================
# Lesson-specific autouse fixtures（统一注入，避免各 lesson conftest.py
# 作为 pytest plugin 注册到同一 "tests.conftest" 名称导致的冲突）
# ============================================================================

# 追踪每个测试模块替换前的 sys.modules 原始值，用于 teardown 时恢复
_MODULE_STATE: dict[str, ModuleType | None] = {}


@pytest.fixture(scope="module", autouse=True)
def _lesson_fixture_injector(  # noqa: PLR0912, PLR0915
    request: pytest.FixtureRequest,
) -> Generator[None]:
    """根据 lesson 目录注入对应的子模块到测试模块命名空间。

    在各测试模块的 setup 阶段运行，将 solutions/examples 子模块
    注入到 request.module.__dict__，让测试代码能直接访问。
    同时将 sys.modules["solutions"] 临时替换为当前 lesson 的包，
    这样 `from solutions import X` 能正确解析到当前 lesson 的 solutions。
    在 teardown 阶段恢复原始 sys.modules 值，不污染后续 lesson。
    """
    fspath = getattr(request.module, "__file__", None)
    if not fspath:
        yield
        return
    # 始终从测试文件路径重新计算 lesson 目录（避免 LESSON_MAP key 不匹配）
    lesson_dir = _get_lesson_dir(fspath)
    if lesson_dir is None:
        yield
        return

    lesson_name = lesson_dir.name

    # 按需加载当前 lesson 的模块（替换预加载策略，避免 fixture 运行前
    # sys.modules["solutions"] 就被设为最后一个 lesson 的包）
    lesson_dir_abs = lesson_dir.resolve()
    orig_module: ModuleType | None = None
    active_module_type: str | None = None
    if lesson_dir_abs in _get_lesson_map():
        _target_dir, module_type = _get_lesson_map()[lesson_dir_abs]
        cache_key = f"{lesson_dir_abs}::{module_type}"
        # 如果缓存为空（移除了预加载），按需加载
        if cache_key not in _LOADED_MODULES:
            _load_modules(lesson_dir_abs, _target_dir, module_type)
        pkg = _LOADED_MODULES.get(cache_key)
        if pkg is not None:
            orig_module = sys.modules.get(module_type)
            active_module_type = module_type
            sys.modules[module_type] = pkg

        # 同时加载 dual-mode 的另一个目录（如果存在）
        solutions_dir = lesson_dir_abs / "solutions"
        examples_dir = lesson_dir_abs / "examples"
        if solutions_dir.is_dir() and examples_dir.is_dir():
            other_dir = examples_dir if _target_dir == solutions_dir else solutions_dir
            other_type = "examples" if _target_dir == solutions_dir else "solutions"
            other_cache_key = f"{lesson_dir_abs}::{other_type}"
            if other_cache_key not in _LOADED_MODULES:
                _load_modules(lesson_dir_abs, other_dir, other_type)

    if "L06" in lesson_name:
        pkg = sys.modules.get("solutions")
        if pkg:
            request.module.__dict__["solutions_pkg"] = pkg
            for sub in ("basic_handling", "custom_exceptions", "multiple_exceptions"):
                val = getattr(pkg, sub, None)
                if val is not None:
                    request.module.__dict__[sub] = val

    # ================================================================
    # Stage 0 exercises 加载（exercises/ 目录是 Stage 0 特有的练习模式）
    # ================================================================
    elif "L01-python-core" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L01_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L02-operators-control" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L02_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L04-functions-modules" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L04_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L05-debugging-tools" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L05_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L06-exceptions" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L06_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L07-oop-basics" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L07_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L08-magic-methods" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L08_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "L09-file-operations" in lesson_name:
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir:
            for key, filename in _L09_EXERCISES.items():
                try:
                    mod = load_exercise_module(f"_test_{key}", exercises_dir / filename)
                    request.module.__dict__[f"{key}_module"] = mod
                except Exception as e:
                    logger.debug(f"加载 {filename} 失败: {e}")

    elif "P01" in lesson_name:
        # P01 独立分支：lesson_name 含 "L01"，必须放在 L10 之前
        _inject_solutions_attrs(lesson_dir, {
            "Student": "Student",
            "StudentManager": "StudentManager",
            "student_manager": "student_manager",
        })

    elif "L10" in lesson_name:
        pkg = sys.modules.get("solutions")
        if pkg:
            gc = getattr(pkg, "solution_03_generic_constraints", None)
            if gc:
                request.module.__dict__["generic_constraints"] = gc
        examples_dir = lesson_dir / "examples"
        ex_map = {
            "type_narrowing": "05_type_narrowing.py",
            "protocol": "02_protocol_typing.py",
        }
        for sub, _filename in ex_map.items():
            try:
                mod = _load_examples_submodule(sub, examples_dir)
                request.module.__dict__[sub] = mod
            except (ImportError, FileNotFoundError, OSError):
                pass

    elif "L11" in lesson_name or "L12" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "generator_exercises": "solution_02_generator_exercises",
            "iterator_protocol": "solution_01_iterator_protocol",
            "itertools_exercises": "solution_03_itertools_exercises",
        })

    elif "L13" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "context_managers": "solution_02_context_managers",
            "decorators": "solution_01_decorators",
        })

    elif "L14" in lesson_name or "L15" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "descriptors": "solution_01_descriptors",
            "property_desc": "solution_02_property",
            "property_": "solution_02_property",
        })

    elif "L16" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "async_basics": "solution_01_async_basics",
            "rate_limiter": "solution_03_async_rate_limiter",
            "file_processor": "solution_02_concurrent_file_processor",
        })

    elif "L17" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "compose_decorator": "solution_03_compose_decorator",
            "data_transformation": "solution_02_data_transformation",
            "functional_pipeline": "solution_01_functional_pipeline",
        })

    elif "L18" in lesson_name:
        _inject_solutions_attrs(lesson_dir, {
            "validation": "solution_01_validation",
            "extraction": "solution_02_extraction",
            "log_parser": "solution_03_log_parser",
        })

    elif "L22" in lesson_name:
        pkg = sys.modules.get("solutions")
        examples_dir = lesson_dir / "examples"
        if pkg:
            try:
                ex_01 = _load_examples_submodule("example_01_async_generators", examples_dir)
                ex_02 = _load_examples_submodule("example_02_context_managers", examples_dir)
                ex_03 = _load_examples_submodule("example_03_taskgroup_exceptions", examples_dir)
                pkg.example_01_async_generators = ex_01
                pkg.example_02_context_managers = ex_02
                pkg.example_03_taskgroup_exceptions = ex_03
                request.module.__dict__["example_01_async_generators"] = ex_01
            except (AttributeError, ImportError, FileNotFoundError):
                pass

    elif "L24" in lesson_name:
        pkg = sys.modules.get("solutions")
        examples_dir = lesson_dir / "examples"
        if pkg:
            try:
                ex_01 = _load_examples_submodule("example_01_async_generators", examples_dir)
                ex_02 = _load_examples_submodule("example_02_context_managers", examples_dir)
                ex_03 = _load_examples_submodule("example_03_taskgroup_exceptions", examples_dir)
                ex_04 = _load_examples_submodule("example_04_pep695_generics", examples_dir)
                pkg.example_01_async_generators = ex_01
                pkg.example_02_context_managers = ex_02
                pkg.example_03_taskgroup_exceptions = ex_03
                pkg.example_04_pep695_generics = ex_04
                request.module.__dict__["example_01_async_generators"] = ex_01
                request.module.__dict__["example_02_context_managers"] = ex_02
                request.module.__dict__["example_03_taskgroup_exceptions"] = ex_03
                request.module.__dict__["example_04_pep695_generics"] = ex_04
            except (AttributeError, ImportError, FileNotFoundError):
                pass

    elif "L36" in lesson_name:
        examples_dir = lesson_dir / "examples"
        try:
            bb = _load_examples_submodule("01_backpressure_basics", examples_dir)
            pb = _load_examples_submodule("02_production_backpressure", examples_dir)
            request.module.__dict__["backpressure_basics"] = bb
            request.module.__dict__["production_backpressure"] = pb
        except (AttributeError, ImportError, FileNotFoundError):
            pass

    elif "L56" in lesson_name:
        pkg = sys.modules.get("solutions")
        if pkg:
            ps = getattr(pkg, "prompt_solution", None)
            if ps:
                request.module.__dict__["prompt_solution"] = ps

    yield  # teardown 阶段

    # 恢复 sys.modules 原始状态
    if active_module_type is not None:
        if orig_module is not None:
            sys.modules[active_module_type] = orig_module
        else:
            sys.modules.pop(active_module_type, None)


# ============================================================================
# Lesson-specific data fixtures（集中在根 conftest 提供，避免 lesson conftest 冲突）
# ============================================================================

@pytest.fixture
def tmp_storage_path(tmp_path: Path) -> Path:
    """返回临时目录作为存储测试路径（L25 专用）。"""
    return tmp_path / "storage"


@pytest.fixture
def sample_orders_path() -> Path:
    """返回测试订单 CSV 文件路径（L47 专用）。"""
    lesson_root = _REPO_ROOT / "stage5-data-engineering" / "lessons" / "L47-pandas"
    path = lesson_root / "data" / "sample_orders.csv"
    if not path.exists():
        pytest.fail(f"测试数据文件不存在: {path}")
    return path


@pytest.fixture
def small_orders_df() -> pd.DataFrame:
    """创建小型测试订单 DataFrame（L47 专用）。"""
    import numpy as np
    import pandas as pd

    n_rows = 1000
    rng = np.random.default_rng(42)
    data = {
        "order_id": [f"ORD{i:06d}" for i in range(n_rows)],
        "user_id": rng.integers(1, 100, n_rows),
        "product_id": rng.integers(1, 50, n_rows),
        "quantity": rng.integers(1, 21, n_rows),
        "price": rng.uniform(10.0, 1000.0, n_rows),
        "order_date": pd.date_range(start="2023-01-01", periods=n_rows),
        "status": rng.choice(["pending", "completed", "cancelled"], n_rows),
        "payment_method": rng.choice(
            ["credit_card", "debit_card", "paypal", "cash"], n_rows
        ),
    }
    df = pd.DataFrame(data)
    missing_indices = rng.choice(n_rows, size=int(n_rows * 0.05), replace=False)
    df.loc[missing_indices, "price"] = np.nan
    anomaly_indices = rng.choice(n_rows, size=int(n_rows * 0.01), replace=False)
    df.loc[anomaly_indices, "quantity"] = -1
    return df


# ============================================================================
# L36 专用 examples fixture wrapper
# ============================================================================

class _ExamplesWrapper:
    """包装 L36 examples 子模块，模拟 examples 包的属性访问。"""

    __slots__ = ("backpressure_basics", "production_backpressure")

    def __init__(self, bb, pb) -> None:
        self.backpressure_basics = bb
        self.production_backpressure = pb


class _L61ExamplesWrapper:
    """包装 L61 examples 子模块，模拟 examples 包的属性访问。"""

    __slots__ = (
        "basic_agent_node_01",
        "human_in_the_loop_03",
        "multi_agent_demo",
        "supervisor_router_02",
    )

    def __init__(
        self,
        basic_agent: object,
        human_loop: object,
        multi_agent: object,
        supervisor: object,
    ) -> None:
        self.basic_agent_node_01 = basic_agent
        self.human_in_the_loop_03 = human_loop
        self.multi_agent_demo = multi_agent
        self.supervisor_router_02 = supervisor

    def __getattr__(self, name: str) -> object:
        raise AttributeError(f"module 'examples' has no attribute '{name}'")


@pytest.fixture(scope="module")
def solutions() -> ModuleType:
    """返回当前 lesson 的 solutions 包。"""
    if "solutions" in sys.modules:
        return sys.modules["solutions"]
    raise RuntimeError("solutions 模块未加载，请检查 conftest.py 配置")


@pytest.fixture(scope="module")
def examples(request: pytest.FixtureRequest) -> _ExamplesWrapper | _L61ExamplesWrapper | ModuleType:
    """返回当前 lesson 的 examples 包。

    - L36: 返回 _ExamplesWrapper（包含 backpressure_basics, production_backpressure）
    - L61: 返回 _L61ExamplesWrapper（包含多 Agent 相关模块）
    - 其他 lesson: 返回 sys.modules["examples"]
    """
    fspath = getattr(request.module, "__file__", None) or ""
    lesson_dir = _get_lesson_dir(fspath)

    if lesson_dir:
        if "L36" in lesson_dir.name:
            examples_dir = lesson_dir / "examples"
            bb = _load_examples_submodule("01_backpressure_basics", examples_dir)
            pb = _load_examples_submodule("02_production_backpressure", examples_dir)
            return _ExamplesWrapper(bb, pb)

        if "L61" in lesson_dir.name:
            examples_dir = lesson_dir / "examples"
            basic = _load_examples_submodule("basic_agent_node_01", examples_dir)
            human_loop = _load_examples_submodule("human_in_the_loop_03", examples_dir)
            multi_agent = _load_examples_submodule("multi_agent_demo", examples_dir)
            supervisor = _load_examples_submodule("supervisor_router_02", examples_dir)
            return _L61ExamplesWrapper(basic, human_loop, multi_agent, supervisor)

    if "examples" in sys.modules:
        return sys.modules["examples"]
    raise RuntimeError("examples 模块未加载，请检查 conftest.py 配置")


# ============================================================================
# Stage 0 Exercises Fixtures（集中定义，替代各课程测试文件内的本地 fixtures）
# ============================================================================
# 这些 fixtures 在根 conftest.py 中定义，确保跨课程运行时 pytest 能正确解析。

def _make_exercise_fixture(lesson_pattern: str, module_key: str, filename: str):
    """工厂函数：为指定 exercise 文件创建 fixture。

    Args:
        lesson_pattern: lesson 目录名匹配模式（如 "L01-python-core"）
        module_key: fixture 名称中的模块键（如 "hello" → hello_module）
        filename: exercises/ 目录下的文件名
    """
    fixture_name = f"{module_key}_module"

    @pytest.fixture(scope="module")
    def exercise_fixture(request: pytest.FixtureRequest) -> ModuleType:
        """加载 exercises/{filename}"""
        fspath = getattr(request.module, "__file__", None) or ""
        lesson_dir = _get_lesson_dir(fspath)
        if lesson_dir is None or lesson_pattern not in lesson_dir.name:
            raise pytest.skip(f"不在 {lesson_pattern} 课程中，跳过此 fixture")
        exercises_dir = _get_exercises_dir(lesson_dir)
        if exercises_dir is None:
            raise pytest.skip("找不到 exercises/ 目录")
        file_path = exercises_dir / filename
        if not file_path.exists():
            raise pytest.fail(f"练习文件不存在: {file_path}")
        return load_exercise_module(f"_test_{module_key}", file_path)

    exercise_fixture.__name__ = fixture_name
    return exercise_fixture


# L01 Exercises Fixtures
hello_module = _make_exercise_fixture("L01-python-core", "hello", "01_hello_practice.py")
io_module = _make_exercise_fixture("L01-python-core", "io", "02_io_practice.py")
types_module = _make_exercise_fixture("L01-python-core", "types", "03_type_basics.py")
conversion_module = _make_exercise_fixture("L01-python-core", "conversion", "04_type_conversion.py")
fstring_module = _make_exercise_fixture("L01-python-core", "fstring", "05_fstring_practice.py")

# L02 Exercises Fixtures
arithmetic_module = _make_exercise_fixture("L02-operators-control", "arithmetic", "01_arithmetic_conditions.py")
logical_module = _make_exercise_fixture("L02-operators-control", "logical", "02_logical_operators.py")
bitwise_module = _make_exercise_fixture("L02-operators-control", "bitwise", "03_bitwise_operations.py")
loops_module = _make_exercise_fixture("L02-operators-control", "loops", "04_loops.py")
match_module = _make_exercise_fixture("L02-operators-control", "match", "05_match_case.py")
comprehensive_module = _make_exercise_fixture("L02-operators-control", "comprehensive", "06_comprehensive.py")

# L04 Exercises Fixtures
functions_module = _make_exercise_fixture("L04-functions-modules", "functions", "01_functions.py")
modules_module = _make_exercise_fixture("L04-functions-modules", "modules", "02_modules.py")

# L05 Exercises Fixtures
pdb_module = _make_exercise_fixture("L05-debugging-tools", "pdb", "01_pdb_practice.py")
traceback_module = _make_exercise_fixture("L05-debugging-tools", "traceback", "02_traceback_practice.py")

# L06 Exercises Fixtures (额外)
basic_handling_module = _make_exercise_fixture("L06-exceptions", "basic_handling", "01_basic_handling.py")
multiple_exceptions_module = _make_exercise_fixture("L06-exceptions", "multiple_exceptions", "02_multiple_exceptions.py")
custom_exceptions_module = _make_exercise_fixture("L06-exceptions", "custom_exceptions", "03_custom_exceptions.py")

# L07 Exercises Fixtures
oop_basics_module = _make_exercise_fixture("L07-oop-basics", "oop_basics", "01_oop_basics.py")
inheritance_module = _make_exercise_fixture("L07-oop-basics", "inheritance", "02_inheritance_practice.py")
property_module = _make_exercise_fixture("L07-oop-basics", "property", "03_property_practice.py")

# L08 Exercises Fixtures
fraction_module = _make_exercise_fixture("L08-magic-methods", "fraction", "01_fraction.py")
set_class_module = _make_exercise_fixture("L08-magic-methods", "set_class", "02_set_class.py")
callable_module = _make_exercise_fixture("L08-magic-methods", "callable", "03_callable.py")

# L09 Exercises Fixtures
log_parser_module = _make_exercise_fixture("L09-file-operations", "log_parser", "01_log_parser.py")
csv_writer_module = _make_exercise_fixture("L09-file-operations", "csv_writer", "02_csv_writer.py")
file_search_module = _make_exercise_fixture("L09-file-operations", "file_search", "03_file_search.py")
