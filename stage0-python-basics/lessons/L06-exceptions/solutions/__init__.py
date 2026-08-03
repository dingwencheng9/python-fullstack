"""L08 Exceptions 参考答案包。"""

from . import basic_handling
from . import custom_exceptions
from . import multiple_exceptions
from .custom_exceptions import InvalidAgeError, InvalidEmailError

__all__ = [
    "InvalidAgeError",
    "InvalidEmailError",
    "basic_handling",
    "custom_exceptions",
    "multiple_exceptions",
]
