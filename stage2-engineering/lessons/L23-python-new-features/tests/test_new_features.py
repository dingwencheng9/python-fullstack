"""

from __future__ import annotations

测试 L21 新增的 PEP 695 泛型和 match/case 示例

验证 Python 3.13 新特性的正确性
"""

import importlib
import importlib.util
from pathlib import Path

import pytest

LESSON_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = LESSON_ROOT / "examples"


def _load_module(name: str, file_path: Path) -> object:
    """按物理路径加载模块并赋予唯一名，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pep695_module():
    """加载 PEP 695 泛型示例模块"""
    return _load_module("example_03_pep695", EXAMPLES_DIR / "example_03_pep695_generics.py")


@pytest.fixture(scope="module")
def match_case_module():
    """加载 match/case 示例模块"""
    return _load_module("example_04_match_case", EXAMPLES_DIR / "example_04_match_case.py")


# ==================== PEP 695 泛型测试 ====================


class TestGenericFunctions:
    """测试泛型函数"""

    def test_find_first_found(self, pep695_module):
        """测试 find_first - 找到元素"""
        numbers = [1, 2, 3, 4, 5]
        result = pep695_module.find_first(numbers, lambda x: x > 3)
        assert result == 4

    def test_find_first_not_found(self, pep695_module):
        """测试 find_first - 未找到元素"""
        numbers = [1, 2, 3]
        result = pep695_module.find_first(numbers, lambda x: x > 10)
        assert result is None

    def test_filter_items_even(self, pep695_module):
        """测试 filter_items - 过滤偶数"""
        numbers = [1, 2, 3, 4, 5, 6]
        result = pep695_module.filter_items(numbers, lambda x: x % 2 == 0)
        assert result == [2, 4, 6]

    def test_filter_items_no_match(self, pep695_module):
        """测试 filter_items - 无匹配"""
        numbers = [1, 3, 5, 7]
        result = pep695_module.filter_items(numbers, lambda x: x % 2 == 0)
        assert result == []

    def test_transform_strings(self, pep695_module):
        """测试 transform - 字符串转换"""
        words = ["hello", "world"]
        result = pep695_module.transform(words, str.upper)
        assert result == ["HELLO", "WORLD"]

    def test_transform_integers(self, pep695_module):
        """测试 transform - 整数转换"""
        numbers = [1, 2, 3]
        result = pep695_module.transform(numbers, lambda x: x * 2)
        assert result == [2, 4, 6]


class TestGenericClasses:
    """测试泛型类"""

    def test_container_creation(self, pep695_module):
        """测试 Container 创建"""
        container = pep695_module.Container("hello")
        assert container.get() == "hello"

    def test_container_thread_safe(self, pep695_module):
        """测试 Container 线程安全"""
        container = pep695_module.Container(42)
        assert container.get() == 42

    def test_pair_creation(self, pep695_module):
        """测试 Pair 创建"""
        pair = pep695_module.Pair(1, "one")
        assert pair.first == 1
        assert pair.second == "one"

    def test_pair_swap(self, pep695_module):
        """测试 Pair swap 方法"""
        pair = pep695_module.Pair("a", 1)
        swapped = pair.swap()
        assert swapped.first == 1
        assert swapped.second == "a"

    def test_stack_operations(self, pep695_module):
        """测试 Stack 操作"""
        stack = pep695_module.Stack[int]()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_stack_empty(self, pep695_module):
        """测试空 Stack"""
        stack = pep695_module.Stack[str]()
        assert stack.pop() is None
        assert stack.peek() is None


class TestGroupBy:
    """测试 group_by 函数"""

    def test_group_by_length(self, pep695_module):
        """测试按长度分组"""
        words = ["a", "ab", "abc", "b", "bc"]
        result = pep695_module.group_by(words, len)
        assert result == {1: ["a", "b"], 2: ["ab", "bc"], 3: ["abc"]}

    def test_group_by_first_letter(self, pep695_module):
        """测试按首字母分组"""
        words = ["apple", "banana", "cherry", "blueberry"]
        result = pep695_module.group_by(words, lambda x: x[0])
        assert result == {"a": ["apple"], "b": ["banana", "blueberry"], "c": ["cherry"]}

    def test_group_by_empty(self, pep695_module):
        """测试空列表分组"""
        result = pep695_module.group_by([], lambda x: x)
        assert result == {}


class TestSafeExecute:
    """测试 safe_execute 函数"""

    def test_safe_execute_success(self, pep695_module):
        """测试安全执行 - 成功"""
        result = pep695_module.safe_execute(lambda: 1 + 1)
        assert result == 2

    def test_safe_execute_exception(self, pep695_module):
        """测试安全执行 - 异常时返回异常对象"""
        result = pep695_module.safe_execute(lambda: 1 / 0)
        assert isinstance(result, ZeroDivisionError)


# ==================== match/case 测试 ====================


class TestBasicMatch:
    """测试基本 match/case"""

    def test_classify_value_zero(self, match_case_module):
        """测试 classify_value - 零"""
        result = match_case_module.classify_value(0)
        assert "零" in result

    def test_classify_value_positive(self, match_case_module):
        """测试 classify_value - 正整数"""
        result = match_case_module.classify_value(5)
        assert "正" in result

    def test_classify_value_negative(self, match_case_module):
        """测试 classify_value - 负整数"""
        result = match_case_module.classify_value(-3)
        assert "负" in result

    def test_classify_value_strings(self, match_case_module):
        """测试 classify_value - 字符串"""
        result = match_case_module.classify_value("hello")
        assert "非空字符串" in result or "string" in result.lower()

    def test_classify_value_empty_string(self, match_case_module):
        """测试 classify_value - 空字符串"""
        result = match_case_module.classify_value("")
        assert "空字符串" in result

    def test_classify_value_list(self, match_case_module):
        """测试 classify_value - 列表"""
        result = match_case_module.classify_value([1, 2])
        assert "列表" in result or "list" in result.lower()

    def test_classify_value_dict(self, match_case_module):
        """测试 classify_value - 字典"""
        result = match_case_module.classify_value({"a": 1})
        assert "字典" in result or "dict" in result.lower()


class TestShapeMatching:
    """测试形状匹配"""

    def test_circle_describe(self, match_case_module):
        """测试圆形描述"""
        center = match_case_module.Point(x=0, y=0)
        shape = match_case_module.Circle(center=center, radius=5)
        area = match_case_module.describe_shape(shape)
        assert "圆心" in area
        assert "半径" in area

    def test_rectangle_describe(self, match_case_module):
        """测试矩形描述"""
        top_left = match_case_module.Point(x=0, y=0)
        bottom_right = match_case_module.Point(x=4, y=6)
        shape = match_case_module.Rectangle(top_left=top_left, bottom_right=bottom_right)
        area = match_case_module.describe_shape(shape)
        assert "Rectangle" in area or "矩形" in area

    def test_point_describe(self, match_case_module):
        """测试点描述"""
        shape = match_case_module.Point(x=3, y=4)
        area = match_case_module.describe_shape(shape)
        assert "3" in area
        assert "4" in area


class TestHTTPStatus:
    """测试 HTTP 状态码匹配"""

    def test_http_status_success(self, match_case_module):
        """测试成功状态码"""
        assert match_case_module.handle_http_status(200) == "成功"
        assert match_case_module.handle_http_status(201) == "已创建"

    def test_http_status_client_error(self, match_case_module):
        """测试客户端错误状态码"""
        assert match_case_module.handle_http_status(400) == "请求错误"
        assert match_case_module.handle_http_status(404) == "未找到"

    def test_http_status_server_error(self, match_case_module):
        """测试服务器错误状态码"""
        assert match_case_module.handle_http_status(500) == "服务器错误"

    def test_http_status_unknown(self, match_case_module):
        """测试未知状态码"""
        result = match_case_module.handle_http_status(999)
        assert "未知" in result


class TestErrorHandling:
    """测试错误处理模式"""

    def test_handle_error_type_error(self, match_case_module):
        """测试错误处理 - TypeError"""
        result = match_case_module.handle_error_with_match(TypeError("test"))
        assert "类型错误" in result

    def test_handle_error_value_error(self, match_case_module):
        """测试错误处理 - ValueError"""
        result = match_case_module.handle_error_with_match(ValueError("test"))
        assert "值错误" in result

    def test_handle_error_key_error(self, match_case_module):
        """测试错误处理 - KeyError"""
        result = match_case_module.handle_error_with_match(KeyError("test_key"))
        assert "键错误" in result


class TestAPIResponse:
    """测试 API 响应模式"""

    def test_api_response_success(self, match_case_module):
        """测试 API 响应 - 成功"""
        response = {"status": "success", "data": {"users": [{"id": 1, "name": "Alice"}]}}
        result = match_case_module.process_api_response(response)
        assert "success" in result.lower() or "成功" in result

    def test_api_response_error(self, match_case_module):
        """测试 API 响应 - 错误"""
        response = {"status": "error", "error": {"code": "NOT_FOUND", "message": "User not found"}}
        result = match_case_module.process_api_response(response)
        assert "error" in result.lower() or "错误" in result

    def test_api_response_pending(self, match_case_module):
        """测试 API 响应 - 待处理"""
        response = {"status": "pending"}
        result = match_case_module.process_api_response(response)
        assert "pending" in result.lower() or "待处理" in result

    def test_api_response_unknown(self, match_case_module):
        """测试 API 响应 - 未知状态"""
        response = {"status": "unknown"}
        result = match_case_module.process_api_response(response)
        assert "unknown" in result.lower() or "未知" in result
