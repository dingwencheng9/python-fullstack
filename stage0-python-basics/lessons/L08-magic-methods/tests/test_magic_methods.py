"""L07 Magic Methods 测试用例"""

import pytest


@pytest.fixture(autouse=True)
def _inject_solutions(request: pytest.FixtureRequest) -> None:
    """注入 solutions 中的模块到全局命名空间。

    ``vector``、``money``、``collection`` 以及练习对应的
    ``fraction``、``set_class``、``callable_solution`` 通过 fixture 注入，
    ruff 静态分析时无法识别，因此使用 noqa: F821。
    """
    from solutions import vector, money, collection, fraction, set_class
    from solutions import callable as callable_module

    request.module.__dict__["vector"] = vector
    request.module.__dict__["money"] = money
    request.module.__dict__["collection"] = collection
    request.module.__dict__["fraction"] = fraction
    request.module.__dict__["set_class"] = set_class
    request.module.__dict__["callable_solution"] = callable_module


class TestVectorMagicMethods:
    """测试 Vector 类的魔法方法"""

    def test_vector_creation(self):
        """测试向量创建"""
        v = vector.Vector(3.0, 4.0)  # noqa: F821
        assert v.x == 3.0
        assert v.y == 4.0

    def test_vector_add(self):
        """测试向量加法"""
        v1 = vector.Vector(1.0, 2.0)  # noqa: F821
        v2 = vector.Vector(3.0, 4.0)  # noqa: F821
        result = v1 + v2
        assert result.x == 4.0
        assert result.y == 6.0

    def test_vector_sub(self):
        """测试向量减法"""
        v1 = vector.Vector(5.0, 7.0)  # noqa: F821
        v2 = vector.Vector(2.0, 3.0)  # noqa: F821
        result = v1 - v2
        assert result.x == 3.0
        assert result.y == 4.0

    def test_vector_scalar_mul(self):
        """测试标量乘法"""
        v = vector.Vector(2.0, 3.0)  # noqa: F821
        result = v * 2
        assert result.x == 4.0
        assert result.y == 6.0

    def test_vector_rmul(self):
        """测试右乘"""
        v = vector.Vector(2.0, 3.0)  # noqa: F821
        result = 3 * v
        assert result.x == 6.0
        assert result.y == 9.0

    def test_vector_eq(self):
        """测试相等比较"""
        v1 = vector.Vector(1.0, 2.0)  # noqa: F821
        v2 = vector.Vector(1.0, 2.0)  # noqa: F821
        v3 = vector.Vector(1.0, 3.0)  # noqa: F821
        assert v1 == v2
        assert v1 != v3

    def test_vector_repr(self):
        """测试 repr"""
        v = vector.Vector(1.0, 2.0)  # noqa: F821
        assert repr(v) == "Vector(1.0, 2.0)"

    def test_vector_str(self):
        """测试 str"""
        v = vector.Vector(1.0, 2.0)  # noqa: F821
        assert str(v) == "(1.0, 2.0)"

    def test_vector_hash(self):
        """测试哈希（可放入 set/dict）"""
        v1 = vector.Vector(1.0, 2.0)  # noqa: F821
        v2 = vector.Vector(1.0, 2.0)  # noqa: F821
        s = {v1, v2}
        assert len(s) == 1

    def test_vector_magnitude(self):
        """测试向量长度"""
        v = vector.Vector(3.0, 4.0)  # noqa: F821
        assert v.magnitude() == 5.0


class TestMoneyMagicMethods:
    """测试 Money 类的魔法方法"""

    def test_money_creation(self):
        """测试货币创建"""
        m = money.Money(10, 50)  # noqa: F821
        assert m.dollars == 10
        assert m.cents == 50

    def test_money_normalization(self):
        """测试进位归一化"""
        m = money.Money(1, 150)  # noqa: F821
        assert m.dollars == 2
        assert m.cents == 50

    def test_money_repr(self):
        """测试 repr"""
        m = money.Money(5, 25)  # noqa: F821
        assert repr(m) == "Money(5, 25)"

    def test_money_str(self):
        """测试 str"""
        m = money.Money(5, 5)  # noqa: F821
        assert str(m) == "$5.05"

    def test_money_eq(self):
        """测试相等比较"""
        m1 = money.Money(10, 50)  # noqa: F821
        m2 = money.Money(10, 50)  # noqa: F821
        m3 = money.Money(10, 51)  # noqa: F821
        assert m1 == m2
        assert m1 != m3

    def test_money_add(self):
        """测试加法"""
        m1 = money.Money(1, 50)  # noqa: F821
        m2 = money.Money(2, 75)  # noqa: F821
        result = m1 + m2
        assert result.dollars == 4
        assert result.cents == 25

    def test_money_sub(self):
        """测试减法"""
        m1 = money.Money(5, 0)  # noqa: F821
        m2 = money.Money(2, 50)  # noqa: F821
        result = m1 - m2
        assert result.dollars == 2
        assert result.cents == 50

    def test_money_sub_negative_raises(self):
        """测试负数结果抛出异常"""
        m1 = money.Money(1, 0)  # noqa: F821
        m2 = money.Money(2, 0)  # noqa: F821
        with pytest.raises(ValueError, match="余额不能为负"):
            m1 - m2

    def test_money_mul(self):
        """测试标量乘法"""
        m = money.Money(2, 0)  # noqa: F821
        result = m * 3
        assert result.dollars == 6
        assert result.cents == 0


class TestBagMagicMethods:
    """测试 Bag 类的魔法方法"""

    def test_bag_creation(self):
        """测试 Bag 创建"""
        bag = collection.Bag()  # noqa: F821
        assert len(bag) == 0

    def test_bag_add(self):
        """测试添加物品"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        bag.add("banana")
        assert len(bag) == 2

    def test_bag_remove(self):
        """测试移除物品"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        bag.remove("apple")
        assert len(bag) == 0

    def test_bag_remove_nonexistent(self):
        """测试移除不存在的物品"""
        bag = collection.Bag()  # noqa: F821
        result = bag.remove("apple")
        assert result is False

    def test_bag_contains(self):
        """测试包含检查"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        assert "apple" in bag
        assert "banana" not in bag

    def test_bag_len(self):
        """测试长度"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        bag.add("banana")
        bag.add("apple")
        assert len(bag) == 3

    def test_bag_iter(self):
        """测试迭代"""
        bag = collection.Bag()  # noqa: F821
        bag.add("a")
        bag.add("b")
        bag.add("c")
        items = list(bag)
        assert len(items) == 3
        assert set(items) == {"a", "b", "c"}

    def test_bag_count(self):
        """测试物品计数"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        bag.add("apple")
        bag.add("banana")
        assert bag.count("apple") == 2
        assert bag.count("banana") == 1
        assert bag.count("orange") == 0

    def test_bag_repr(self):
        """测试 repr"""
        bag = collection.Bag()  # noqa: F821
        bag.add("apple")
        bag.add("banana")
        assert "apple" in repr(bag)
        assert "banana" in repr(bag)


class TestFractionExerciseSolution:
    """测试 Fraction 练习对应答案"""

    def test_fraction_reduces_to_lowest_terms(self):
        f = fraction.Fraction(2, 4)  # noqa: F821
        assert f.numerator == 1
        assert f.denominator == 2

    def test_fraction_denominator_zero_raises(self):
        with pytest.raises(ValueError, match="分母不能为零"):
            fraction.Fraction(1, 0)  # noqa: F821

    def test_fraction_str_and_repr(self):
        f = fraction.Fraction(-2, 4)  # noqa: F821
        assert str(f) == "-1/2"
        assert repr(f) == "Fraction(-1, 2)"

    def test_fraction_equality_and_hash(self):
        f1 = fraction.Fraction(1, 2)  # noqa: F821
        f2 = fraction.Fraction(2, 4)  # noqa: F821
        assert f1 == f2
        assert len({f1, f2}) == 1

    def test_fraction_add(self):
        f1 = fraction.Fraction(1, 3)  # noqa: F821
        f2 = fraction.Fraction(1, 6)  # noqa: F821
        assert f1 + f2 == fraction.Fraction(1, 2)  # noqa: F821


class TestSetExerciseSolution:
    """测试 Set 练习对应答案"""

    def test_set_add_deduplicates(self):
        s = set_class.Set()  # noqa: F821
        s.add("apple")
        s.add("apple")
        assert len(s) == 1

    def test_set_contains_remove_iter(self):
        s = set_class.Set()  # noqa: F821
        s.add("apple")
        s.add("banana")
        assert "apple" in s
        assert s.remove("apple") is True
        assert s.remove("orange") is False
        assert list(s) == ["banana"]


class TestMultiplierExerciseSolution:
    """测试 Multiplier 练习对应答案"""

    def test_multiplier_call(self):
        doubler = callable_solution.Multiplier(2)  # noqa: F821
        assert doubler(5) == 10
        assert doubler(3.5) == 7

    def test_multiplier_repr(self):
        tripler = callable_solution.Multiplier(3)  # noqa: F821
        assert repr(tripler) == "Multiplier(3)"
