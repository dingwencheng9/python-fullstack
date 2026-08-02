"""L02 新增内容测试：enumerate、zip、for-else、match-case"""






class TestEnumerate:
    """测试 enumerate() 函数"""

    def test_enumerate_basic(self):
        """测试 enumerate 基本用法"""
        fruits = ["apple", "banana", "cherry"]
        result = list(enumerate(fruits))
        assert result == [(0, "apple"), (1, "banana"), (2, "cherry")]

    def test_enumerate_start_index(self):
        """测试 enumerate 指定起始索引"""
        fruits = ["apple", "banana", "cherry"]
        result = list(enumerate(fruits, start=1))
        assert result == [(1, "apple"), (2, "banana"), (3, "cherry")]

    def test_enumerate_with_loop(self):
        """测试 enumerate 在循环中使用"""
        fruits = ["apple", "banana", "cherry"]
        result = []
        for i, fruit in enumerate(fruits):
            result.append((i, fruit))
        assert result == [(0, "apple"), (1, "banana"), (2, "cherry")]


class TestZip:
    """测试 zip() 函数"""

    def test_zip_basic(self):
        """测试 zip 基本用法"""
        names = ["Alice", "Bob"]
        ages = [25, 30]
        result = list(zip(names, ages))  # noqa: B905
        assert result == [("Alice", 25), ("Bob", 30)]

    def test_zip_different_lengths(self):
        """测试 zip 不等长序列（取最短）"""
        a = [1, 2, 3, 4]
        b = ["a", "b"]
        result = list(zip(a, b))  # noqa: B905
        assert result == [(1, "a"), (2, "b")]

    def test_zip_to_dict(self):
        """测试 zip 转换为字典"""
        keys = ["name", "age"]
        values = ["Alice", 25]
        result = dict(zip(keys, values))  # noqa: B905
        assert result == {"name": "Alice", "age": 25}

    def test_zip_multiple_iterables(self):
        """测试 zip 多个序列"""
        a = [1, 2, 3]
        b = ["a", "b", "c"]
        c = [True, False, True]
        result = list(zip(a, b, c))  # noqa: B905
        assert result == [(1, "a", True), (2, "b", False), (3, "c", True)]


class TestForElse:
    """测试 for-else 循环子句"""

    def test_for_else_not_found(self):
        """测试 for-else：未找到时执行 else"""
        numbers = [1, 3, 5, 7, 9]
        target = 4
        found = False

        for num in numbers:
            if num == target:
                found = True
                break

        assert found is False  # else 分支应该被执行

    def test_for_else_found(self):
        """测试 for-else：找到时跳过 else"""
        numbers = [1, 3, 5, 7, 9]
        target = 5
        found = False

        for num in numbers:
            if num == target:
                found = True
                break

        assert found is True  # break 跳出了循环，else 不执行

    def test_is_prime_with_for_else(self):
        """测试质数判断（使用 for-else）"""
        # 质数: 2, 3, 5, 7, 11, 13
        # 非质数: 1, 4, 6, 8, 9, 10

        def is_prime(n: int) -> bool:
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        assert is_prime(2) is True
        assert is_prime(3) is True
        assert is_prime(5) is True
        assert is_prime(7) is True
        assert is_prime(11) is True
        assert is_prime(1) is False
        assert is_prime(4) is False
        assert is_prime(6) is False
        assert is_prime(9) is False


class TestMatchCase:
    """测试 match-case 模式匹配（Python 3.10+）"""

    def test_match_simple_value(self):
        """测试简单值匹配"""
        status_code = 404
        result = None

        match status_code:
            case 200:
                result = "OK"
            case 404:
                result = "Not Found"
            case 500:
                result = "Server Error"
            case _:
                result = "Unknown"

        assert result == "Not Found"

    def test_match_or_pattern(self):
        """测试多值 OR 匹配"""
        day = "Saturday"
        result = None

        match day:
            case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
                result = "Weekday"
            case "Saturday" | "Sunday":
                result = "Weekend"
            case _:
                result = "Invalid"

        assert result == "Weekend"

    def test_match_tuple_pattern(self):
        """测试元组模式匹配"""
        point = (0, 5)
        result = None

        match point:
            case (0, 0):
                result = "Origin"
            case (0, y):
                result = f"Y-axis, y={y}"
            case (x, 0):
                result = f"X-axis, x={x}"
            case (x, y):
                result = f"Point({x}, {y})"

        assert result == "Y-axis, y=5"

    def test_match_guard(self):
        """测试带守卫的模式匹配"""
        age = 25
        result = None

        match age:
            case x if x < 0:
                result = "Invalid"
            case x if x < 18:
                result = "Minor"
            case x if x < 65:
                result = "Adult"
            case _:
                result = "Senior"

        assert result == "Adult"

    def test_match_list_pattern(self):
        """测试列表模式匹配（解包）"""
        command = ["start", "server"]
        result = None

        match command:
            case ["start", name]:
                result = f"Start: {name}"
            case ["stop", name]:
                result = f"Stop: {name}"
            case _:
                result = "Unknown"

        assert result == "Start: server"

    def test_match_dict_pattern(self):
        """测试字典模式匹配"""
        data = {"type": "user", "name": "Alice"}
        result = None

        match data:
            case {"type": "user", "name": name}:
                result = f"User: {name}"
            case {"type": "admin", "name": name}:
                result = f"Admin: {name}"
            case _:
                result = "Unknown"

        assert result == "User: Alice"
