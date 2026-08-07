"""L14 solutions 模块初始化

导出所有练习参考答案。
"""

from .solution_01_parameterized_decorators import rate_limit, deprecated, memoize
from .solution_02_decorator_chaining import log, timer, retry, cache
from .solution_03_class_decorators import CallCounter, singleton, validate, Memoized
from .solution_04_optional_params import log as optional_log, timed, when, debug_timed

__all__ = [
    # 练习 1
    "rate_limit",
    "deprecated",
    "memoize",
    # 练习 2
    "log",
    "timer",
    "retry",
    "cache",
    # 练习 3
    "CallCounter",
    "singleton",
    "validate",
    "Memoized",
    # 练习 4
    "optional_log",
    "timed",
    "when",
    "debug_timed",
]
