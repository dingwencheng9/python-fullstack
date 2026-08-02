"""日期时间工具模块"""


def format_date(year: int, month: int, day: int) -> str:
    """格式化日期为 YYYY-MM-DD"""
    return f"{year:04d}-{month:02d}-{day:02d}"


def format_time(hour: int, minute: int, second: int = 0) -> str:
    """格式化时间为 HH:MM:SS"""
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def get_current_datetime() -> tuple[int, int, int, int, int, int]:
    """获取当前日期时间（模拟）"""
    return (2026, 7, 1, 10, 30, 0)
