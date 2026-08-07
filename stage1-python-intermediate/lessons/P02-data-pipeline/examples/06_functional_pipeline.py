"""P02 示例 6: 函数式数据管道

演示 L17 函数式编程的核心概念：
- map/filter/reduce
- functools.reduce 函数组合
- 管道操作符
- 纯函数设计
- 偏函数 partial

运行方式:
    python examples/06_functional_pipeline.py
"""

from functools import reduce, partial
from typing import Callable, Iterator, TypeVar, Generic
import re

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


# ============================================================
# 1. 基础函数式操作
# ============================================================

def increment(x: int) -> int:
    """加一"""
    return x + 1


def double(x: int) -> int:
    """翻倍"""
    return x * 2


def is_even(x: int) -> bool:
    """判断偶数"""
    return x % 2 == 0


def square(x: int) -> int:
    """平方"""
    return x ** 2


def basic_functional():
    """基础函数式操作"""
    print("\n=== 基础函数式操作 ===")

    numbers = [1, 2, 3, 4, 5]

    # map: 转换
    doubled = list(map(double, numbers))
    print(f"原始: {numbers}")
    print(f"map(double): {doubled}")

    # filter: 过滤
    evens = list(filter(is_even, numbers))
    print(f"filter(is_even): {evens}")

    # reduce: 聚合
    total = reduce(lambda a, b: a + b, numbers, 0)
    print(f"reduce(sum): {total}")

    # 组合操作
    result = reduce(
        lambda a, b: a + b,
        map(square,
        filter(is_even, numbers)),
        0
    )
    print(f"偶数平方和: {result}")


# ============================================================
# 2. 管道组合器
# ============================================================

class Pipeline(Generic[T]):
    """函数式管道

    使用方法链式调用组合多个函数。
    """

    def __init__(self, initial: Callable[[], T] | T | None = None) -> None:
        if initial is None:
            self._funcs: list[Callable] = []
            self._source: Callable[[], Iterator] | None = None
        elif callable(initial) and not isinstance(initial, type):
            self._source = initial
            self._funcs = []
        else:
            self._funcs = []
            self._source = lambda: iter([initial])  # type: ignore

    def pipe(self, func: Callable) -> "Pipeline":
        """添加管道阶段"""
        new_pipeline = Pipeline()
        new_pipeline._funcs = self._funcs + [func]
        new_pipeline._source = self._source
        return new_pipeline

    def map(self, func: Callable[[T], U]) -> "Pipeline[U]":
        """添加映射阶段"""
        return self.pipe(lambda items: map(func, items))  # type: ignore

    def filter(self, predicate: Callable[[T], bool]) -> "Pipeline[T]":
        """添加过滤阶段"""
        return self.pipe(lambda items: filter(predicate, items))  # type: ignore

    def reduce(self, func: Callable[[U, T], U], initial: U) -> U:
        """执行管道并聚合结果"""
        if self._source:
            items = self._source()
            for func_ in self._funcs:
                items = func_(items)
            return reduce(func, items, initial)
        raise ValueError("Pipeline has no source")

    def collect(self) -> list[T]:
        """收集所有结果"""
        if self._source:
            items = self._source()
            for func_ in self._funcs:
                items = func_(items)
            return list(items)
        raise ValueError("Pipeline has no source")

    def first(self) -> T | None:
        """获取第一个结果"""
        results = self.collect()
        return results[0] if results else None


def functional_pipeline():
    """函数式管道演示"""
    print("\n=== 函数式管道 ===")

    # 创建管道
    result = (
        Pipeline(lambda: range(1, 11))
        .map(double)
        .filter(is_even)
        .map(square)
        .reduce(lambda a, b: a + b, 0)
    )
    print(f"1-10 的偶数翻倍后平方和: {result}")

    # 链式收集
    result = (
        Pipeline(lambda: ["apple", "banana", "cherry", "date"])
        .map(str.upper)
        .filter(lambda s: len(s) > 5)
        .collect()
    )
    print(f"长水果名大写: {result}")


# ============================================================
# 3. 函数组合器
# ============================================================

def compose(*functions: Callable) -> Callable:
    """函数组合：f ∘ g ∘ h = f(g(h(x)))

    使用方法：
        composed = compose(f, g, h)
        result = composed(x)  # 等价于 f(g(h(x)))
    """
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


def pipe(*functions: Callable) -> Callable:
    """管道组合：h | g | f = f(g(h(x)))

    使用方法：
        piped = pipe(h, g, f)
        result = piped(x)  # 等价于 f(g(h(x)))
    """
    def piped(x):
        result = x
        for func in functions:
            result = func(result)
        return result
    return piped


def function_composition():
    """函数组合演示"""
    print("\n=== 函数组合 ===")

    # compose: 从右到左组合
    f = lambda x: x + 1
    g = lambda x: x * 2
    h = lambda x: x ** 2

    composed = compose(f, g, h)
    print(f"compose(f, g, h)(3) = f(g(h(3))) = f(g(9)) = f(18) = {composed(3)}")

    # pipe: 从左到右组合
    piped = pipe(h, g, f)
    print(f"pipe(h, g, f)(3) = f(g(h(3))) = f(g(9)) = f(18) = {piped(3)}")

    # 实际例子：文本处理管道
    strip = str.strip
    lower = str.lower
    remove_digits = lambda s: "".join(c for c in s if not c.isdigit())

    clean_text = compose(strip, lower, remove_digits)
    text = "  123ABC456 "
    print(f"清理文本: '{text}' → '{clean_text(text)}'")


# ============================================================
# 4. 偏函数
# ============================================================

def partial_examples():
    """偏函数演示"""
    print("\n=== 偏函数 ===")

    # partial: 预设部分参数
    def power(base: float, exponent: float) -> float:
        return base ** exponent

    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    sqrt = partial(power, exponent=0.5)

    print(f"square(5): {square(5)}")
    print(f"cube(5): {cube(5)}")
    print(f"sqrt(16): {sqrt(16)}")

    # 用于 map/filter
    numbers = [1, 2, 3, 4, 5]
    powered = list(map(partial(power, exponent=3), numbers))
    print(f"立方: {powered}")


# ============================================================
# 5. 数据转换管道
# ============================================================

def data_transformation():
    """数据转换管道"""
    print("\n=== 数据转换管道 ===")

    # 原始数据
    users = [
        {"id": "001", "name": "Alice", "age": 28, "score": 92.5, "active": True},
        {"id": "002", "name": "Bob", "age": 35, "score": 78.0, "active": False},
        {"id": "003", "name": "Carol", "age": 22, "score": 88.5, "active": True},
        {"id": "004", "name": "David", "age": 45, "score": 65.0, "active": True},
        {"id": "005", "name": "Eve", "age": 31, "score": 95.0, "active": False},
    ]

    # 管道：过滤活跃用户 → 计算平均分
    active_users = filter(lambda u: u["active"], users)
    scores = map(lambda u: u["score"], active_users)
    avg_score = reduce(lambda a, b: a + b, scores, 0) / len(users)

    print(f"活跃用户平均分: {avg_score:.1f}")

    # 更复杂的管道
    pipeline = (
        Pipeline(lambda: users)
        .filter(lambda u: u["active"])
        .map(lambda u: {**u, "grade": "A" if u["score"] >= 90 else "B" if u["score"] >= 80 else "C"})
        .filter(lambda u: u["grade"] in ["A", "B"])
        .collect()
    )

    print("活跃用户中等级 A/B:")
    for u in pipeline:
        print(f"  {u['name']}: {u['score']} → {u['grade']}")


# ============================================================
# 6. 分组与聚合
# ============================================================

def group_and_aggregate():
    """分组与聚合"""
    print("\n=== 分组与聚合 ===")

    records = [
        {"category": "fruit", "name": "apple", "price": 3.5},
        {"category": "fruit", "name": "banana", "price": 2.0},
        {"category": "vegetable", "name": "carrot", "price": 1.5},
        {"category": "vegetable", "name": "broccoli", "price": 4.0},
        {"category": "fruit", "name": "orange", "price": 4.5},
    ]

    # 按类别分组
    def group_by(items: Iterator[dict], key: str) -> dict[str, list[dict]]:
        groups: dict[str, list[dict]] = {}
        for item in items:
            group_key = item[key]
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)
        return groups

    # 计算每个类别的总价值
    def total_value(group: list[dict]) -> float:
        return reduce(lambda a, b: a + b["price"], group, 0.0)

    groups = group_by(iter(records), "category")

    print("按类别分组:")
    for category, items in groups.items():
        total = total_value(items)
        print(f"  {category}: {len(items)} 项, 总价值 ${total:.2f}")


# ============================================================
# 7. 纯函数工具
# ============================================================

def pure_functions():
    """纯函数工具"""
    print("\n=== 纯函数工具 ===")

    # juxt: 同时应用多个函数
    def juxt(*funcs: Callable) -> Callable:
        """返回一个函数，同时应用多个函数并返回结果列表"""
        def juxted(x):
            return [f(x) for f in funcs]
        return juxted

    stats = juxt(min, max, sum, len)
    numbers = [1, 2, 3, 4, 5]
    print(f"juxt(min, max, sum, len)({numbers}): {stats(numbers)}")

    # complement: 取反
    def complement(pred: Callable) -> Callable:
        """返回谓词的反函数"""
        def complemented(x):
            return not pred(x)
        return complemented

    is_odd = complement(is_even)
    print(f"is_even(4): {is_even(4)}, is_odd(4): {is_odd(4)}")

    # iterate: 重复应用函数
    def iterate(func: Callable, n: int) -> Callable:
        """返回重复应用 n 次的函数"""
        def applied(x):
            result = x
            for _ in range(n):
                result = func(result)
            return result
        return applied

    double_thrice = iterate(double, 3)
    print(f"iterate(double, 3)(2): {double_thrice(2)}")


# ============================================================
# 8. 字符串处理管道
# ============================================================

def string_pipeline():
    """字符串处理管道"""
    print("\n=== 字符串处理管道 ===")

    text = "  The Quick Brown FOX  "

    # 清理管道
    clean = (
        Pipeline(lambda: [text])
        .map(str.strip)
        .map(str.lower)
        .map(lambda s: re.sub(r"\s+", " ", s))
        .collect()[0]
    )
    print(f"原始: '{text}'")
    print(f"清理后: '{clean}'")

    # 词频统计
    words = "apple banana apple cherry banana apple"
    word_list = words.split()

    frequency = reduce(
        lambda acc, word: {**acc, word: acc.get(word, 0) + 1},
        word_list,
        {}
    )
    print(f"词频: {frequency}")


# ============================================================
# 主函数
# ============================================================

def main() -> None:
    """主函数"""
    print("=" * 60)
    print("P02 示例 6: 函数式数据管道")
    print("=" * 60)

    basic_functional()
    functional_pipeline()
    function_composition()
    partial_examples()
    data_transformation()
    group_and_aggregate()
    pure_functions()
    string_pipeline()

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
