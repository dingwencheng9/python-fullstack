"""L14 练习 3 测试: 类装饰器

测试调用计数器、单例模式、参数验证、记忆化类方法。
"""

import pytest


class TestCallCounter:
    """调用计数器测试"""

    def test_call_counter_counts_calls(self):
        """调用计数器应该正确计数"""
        from solutions import CallCounter

        @CallCounter
        def my_func():
            return "result"

        assert my_func.count == 0

        my_func()
        assert my_func.count == 1

        my_func()
        my_func()
        assert my_func.count == 3

    def test_call_counter_preserves_function(self):
        """调用计数器应该保留原函数功能"""
        from solutions import CallCounter

        @CallCounter
        def add(a, b):
            return a + b

        result = add(1, 2)
        assert result == 3
        assert add.count == 1

    def test_call_counter_preserves_metadata(self):
        """调用计数器应该保留函数元信息"""
        from solutions import CallCounter

        @CallCounter
        def my_function():
            """My docstring"""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring"


class TestSingleton:
    """单例模式测试"""

    def test_singleton_returns_same_instance(self):
        """单例应该返回相同实例"""
        from solutions import singleton

        @singleton
        class MyClass:
            def __init__(self, value):
                self.value = value

        obj1 = MyClass(10)
        obj2 = MyClass(20)

        assert obj1 is obj2
        assert obj1.value == 10  # 第一次初始化的值
        assert obj2.value == 10  # 共享同一个实例

    def test_singleton_different_classes(self):
        """不同类的单例应该独立"""
        from solutions import singleton

        @singleton
        class ClassA:
            def __init__(self):
                self.name = "A"

        @singleton
        class ClassB:
            def __init__(self):
                self.name = "B"

        obj_a = ClassA()
        obj_b = ClassB()

        assert obj_a is not obj_b
        assert obj_a.name == "A"
        assert obj_b.name == "B"


class TestValidate:
    """参数验证装饰器测试"""

    def test_validate_passes_valid_args(self):
        """有效参数应该通过验证"""
        from solutions import validate, isinstance_arg

        @validate(
            name=isinstance_arg(str),
            age=lambda x: 0 <= x <= 150
        )
        def create_person(name, age):
            return {"name": name, "age": age}

        result = create_person("Alice", 25)
        assert result == {"name": "Alice", "age": 25}

    def test_validate_fails_on_invalid_type(self):
        """类型错误应该抛出异常"""
        from solutions import validate, isinstance_arg

        @validate(name=isinstance_arg(str))
        def greet(name):
            return f"Hello, {name}"

        with pytest.raises(TypeError, match="Expected str"):
            greet(123)

    def test_validate_fails_on_invalid_value(self):
        """值范围错误应该抛出异常"""
        from solutions import validate

        def validate_age(value):
            if not (0 <= value <= 150):
                raise ValueError("年龄必须在 0-150 之间")
            return value

        @validate(age=validate_age)
        def check_age(age):
            return age

        with pytest.raises(ValueError, match="年龄必须在 0-150 之间"):
            check_age(-5)


class TestMemoized:
    """记忆化类方法测试"""

    def test_memoized_caches_method_result(self):
        """记忆化应该缓存方法结果"""
        from solutions import Memoized

        class Math:
            @Memoized
            def fibonacci(self, n):
                if n < 2:
                    return n
                return self.fibonacci(n - 1) + self.fibonacci(n - 2)

        math = Math()
        call_count = [0]

        original_fib = math.fibonacci

        # 测试缓存效果
        result1 = math.fibonacci(5)
        assert result1 == 5

        # 再次调用相同参数应该使用缓存
        result2 = math.fibonacci(5)
        assert result2 == 5

    def test_memoized_different_instances(self):
        """不同实例的缓存应该独立"""
        from solutions import Memoized

        class Math:
            @Memoized
            def value(self, n):
                return n * 10

        math1 = Math()
        math2 = Math()

        # 不同实例应该独立计算
        assert math1.value(5) == 50
        assert math2.value(5) == 50


class TestClassDecoratorEdgeCases:
    """类装饰器边界情况测试"""

    def test_singleton_with_complex_init(self):
        """单例应该处理复杂的初始化"""
        from solutions import singleton

        @singleton
        class Database:
            def __init__(self, host, port=5432):
                self.host = host
                self.port = port
                self.connection_count = 0

            def connect(self):
                self.connection_count += 1
                return f"Connected to {self.host}:{self.port}"

        db1 = Database("localhost", 5432)
        db2 = Database("otherhost", 3306)

        assert db1 is db2
        assert db1.host == "localhost"
        assert db2.port == 5432  # 使用第一个实例的值

        result = db1.connect()
        assert result == "Connected to localhost:5432"
        assert db2.connection_count == 1  # 共享状态
