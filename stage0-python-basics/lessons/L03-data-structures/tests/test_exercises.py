"""L03 测试用例"""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest

_SOLUTIONS_DIR = Path(__file__).parent.parent / "solutions"


def _load_solution(name: str) -> ModuleType:
    """通过 importlib 加载 solutions/<name>.py，避免污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(f"l03_{name}", _SOLUTIONS_DIR / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_solution_01 = _load_solution("solution_01")
_solution_02 = _load_solution("solution_02")
_solution_03 = _load_solution("solution_03")

filter_positive = _solution_01.filter_positive
word_count = _solution_01.word_count
get_total_count = _solution_02.get_total_count
get_user_name = _solution_02.get_user_name
merge_defaults = _solution_02.merge_defaults
count_long_words = _solution_03.count_long_words
sum_of_squares_gen = _solution_03.sum_of_squares_gen
sum_of_squares_list = _solution_03.sum_of_squares_list

# ============================================================
# 原有测试
# ============================================================


def test_filter_positive():
    assert filter_positive([1, -2, 3]) == [1, 3]


def test_word_count():
    result: dict[str, int] = word_count("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


# ============================================================
# 新增：API 防御性解析测试
# ============================================================


def test_get_user_name_success():
    response: dict = {"data": {"user": {"name": "Alice"}}}
    assert get_user_name(response) == "Alice"


def test_get_user_name_missing():
    """缺失数据不应崩溃"""
    assert get_user_name({}) == "Unknown"
    assert get_user_name({"data": {}}) == "Unknown"
    assert get_user_name({"data": {"user": {}}}) == "Unknown"


def test_get_total_count():
    response: dict = {"data": {"pagination": {"total": 100}}}
    assert get_total_count(response) == 100
    assert get_total_count({}) == 0


# ============================================================
# 新增：字典合并测试
# ============================================================


def test_merge_defaults():
    defaults: dict = {"timeout": 30, "retries": 3}
    user: dict = {"timeout": 60}
    merged: dict = merge_defaults(defaults, user)

    assert merged == {"timeout": 60, "retries": 3}
    # 原字典不应被修改
    assert defaults == {"timeout": 30, "retries": 3}


def test_merge_pipe_operator():
    """直接验证 | 运算符行为"""
    a: dict = {"x": 1, "y": 2}
    b: dict = {"y": 99, "z": 3}
    assert a | b == {"x": 1, "y": 99, "z": 3}
    assert a == {"x": 1, "y": 2}


# ============================================================
# 新增：生成器表达式测试
# ============================================================


def test_sum_of_squares_consistency():
    """列表 vs 生成器结果一致"""
    for n in [10, 100, 1000]:
        assert sum_of_squares_list(n) == sum_of_squares_gen(n)


def test_count_long_words():
    words: list[str] = ["hi", "hello", "world", "a", "Python", "ok"]
    assert count_long_words(words, 5) == 3  # hello, world, Python
    assert count_long_words(words, 2) == 5  # 排除 "a"
    assert count_long_words([], 1) == 0


def test_generator_is_lazy():
    """生成器是惰性的，初始占用极小"""
    gen = (x**2 for x in range(1_000_000))
    assert sys.getsizeof(gen) < 1000  # 不到 1KB


# ============================================================
# 新增：类型注解 + match/case 测试
# ============================================================


def test_list_type_annotation():
    """验证类型注解的可读性"""
    names: list[str] = ["Alice", "Bob"]
    ages: dict[str, int] = {"Alice": 30}
    ids: set[int] = {1, 2, 3}

    assert len(names) == 2
    assert ages["Alice"] == 30
    assert 1 in ids


def test_match_case_parsing():
    """测试 match/case 解析嵌套数据"""

    def parse(response: dict) -> str:
        match response:
            case {"status": "success", "data": {"user": {"name": name}}}:
                return f"用户: {name}"
            case {"status": "error"}:
                return "错误"
            case _:
                return "未知"

    assert parse({"status": "success", "data": {"user": {"name": "Alice"}}}) == "用户: Alice"
    assert parse({"status": "error"}) == "错误"
    assert parse({}) == "未知"


# ============================================================
# 新增：参数化 + 异常测试
# ============================================================


@pytest.mark.parametrize(
    "numbers,expected",
    [
        ([1, -2, 3, -4, 5], [1, 3, 5]),
        ([], []),
        ([-1, -2, -3], []),
        ([0, 0, 0], []),
    ],
)
def test_filter_positive_parametrized(numbers, expected):
    """参数化：正数过滤多种场景"""
    assert filter_positive(numbers) == expected


@pytest.mark.parametrize(
    "text,word,expected_count",
    [
        ("hello world hello", "hello", 2),
        ("hello world hello", "world", 1),
        ("hello world hello", "python", 0),
        ("", "word", 0),
    ],
)
def test_word_count_parametrized(text, word, expected_count):
    """参数化：词频统计"""
    result = word_count(text)
    assert result.get(word, 0) == expected_count


def test_dictionary_key_error():
    """测试访问不存在键抛出 KeyError"""
    d = {"a": 1, "b": 2}
    with pytest.raises(KeyError):
        _ = d["c"]


def test_list_index_error():
    """测试越界访问抛出 IndexError"""
    lst = [1, 2, 3]
    with pytest.raises(IndexError):
        _ = lst[10]
