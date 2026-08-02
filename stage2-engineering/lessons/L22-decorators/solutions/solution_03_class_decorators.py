"""

from __future__ import annotations

L20 练习 3 参考答案 - 类装饰器

解题思路：
本练习的完整实现展示了以下核心概念和技术要点：

1. **问题分析**：
   - 理解练习要求和核心目标
   - 识别关键技术点和实现难点
   - 确定合适的数据结构和算法

2. **实现策略**：
   - 采用模块化设计，每个函数/类职责单一
   - 使用 Python 3.13 类型提示增强代码可读性
   - 遵循 PEP 8 编码规范和最佳实践

3. **关键技术点**：
   - 正确使用语言特性（类型系统/异步/装饰器等）
   - 处理边界条件和异常情况
   - 编写清晰的文档字符串和注释

4. **测试验证**：
   - 覆盖正常流程和异常情况
   - 使用 pytest 进行单元测试
   - 确保代码质量和可维护性

学习建议：
- 先理解问题需求，再查看实现代码
- 对比自己的实现，找出差距和改进点
- 运行代码并修改参数，观察行为变化
- 尝试扩展功能，加深理解
"""

from functools import update_wrapper, wraps
import time


class CallCounter:
    """计数装饰器 - 使用类实现"""

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"{self.func.__name__} has been called {self.calls} times")
        return self.func(*args, **kwargs)

    def reset(self):
        """重置计数"""
        self.calls = 0


class Memoize:
    """缓存装饰器 - 使用类实现"""

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def __call__(self, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result

    def cache_info(self):
        """获取缓存统计信息"""
        return {"hits": self.hits, "misses": self.misses}

    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0


class RateLimiter:
    """限流装饰器 - 使用类实现"""

    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.call_times = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # 移除过期的调用记录
            self.call_times = [t for t in self.call_times if now - t < self.period]

            # 检查是否超过限制
            if len(self.call_times) >= self.max_calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {self.max_calls} calls per {self.period}s"
                )

            # 记录本次调用
            self.call_times.append(now)
            return func(*args, **kwargs)

        return wrapper


def log_method_calls(cls):
    """日志装饰器 - 记录类的所有方法调用"""
    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith("_"):
            setattr(cls, name, _log_method(method, cls.__name__))
    return cls


def _log_method(method, class_name):
    """辅助函数 - 为方法添加日志"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        print(f"Calling {class_name}.{method.__name__}({args[1:]}, {kwargs})")
        result = method(*args, **kwargs)
        print(f"{class_name}.{method.__name__} returned {result!r}")
        return result

    return wrapper


def add_methods(**methods):
    """动态添加方法到类"""

    def decorator(cls):
        for name, method in methods.items():
            setattr(cls, name, method)
        return cls

    return decorator
