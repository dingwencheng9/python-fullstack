"""L06 练习3: @property 装饰器

难度: ⭐⭐⭐☆☆ (较难)
预计时间: 40 分钟
知识点: @property、只读属性、计算属性、属性验证

任务描述:
使用 @property 装饰器实现一个带验证的学生成绩类。

练习内容:
1. Student 类：使用 @property 实现以下功能
   - name: 只读属性
   - score: 带验证的属性（0-100）
   - grade: 计算属性（根据 score 返回等级）
   - pass_status: 计算属性（是否及格）

2. Temperature 类：实现摄氏/华氏温度转换
   - celsius: 主属性
   - fahrenheit: 计算属性（自动转换）

参考示例:
    class Student:
        def __init__(self, name: str, score: float) -> None:
            self._name = name
            self.score = score  # 使用 setter

        @property
        def name(self) -> str:
            return self._name

        @property
        def score(self) -> float:
            return self._score

        @score.setter
        def score(self, value: float) -> None:
            if not 0 <= value <= 100:
                raise ValueError("成绩必须在 0-100 之间")
            self._score = value
"""


# ============ 练习开始 ============


# TODO: 1. 实现 Student 类
class Student:
    """学生成绩类

    属性:
        name: 学生姓名（只读）
        score: 成绩（0-100，带验证）
        grade: 等级（计算属性）
        pass_status: 是否及格（计算属性）
    """

    def __init__(self, name: str, score: float) -> None:
        self._name = name
        # 使用 setter 进行验证
        self.score = score

    @property
    def name(self) -> str:
        """学生姓名（只读）"""
        return self._name

    @property
    def score(self) -> float:
        """成绩（带验证）"""
        return self._score

    @score.setter
    def score(self, value: float) -> None:
        """设置成绩，带范围验证"""
        if not 0 <= value <= 100:
            raise ValueError(f"成绩必须在 0-100 之间，得到 {value}")
        self._score = value

    @property
    def grade(self) -> str:
        """计算等级"""
        score = self._score
        if score >= 90:
            return "A"
        if score >= 80:
            return "B"
        if score >= 70:
            return "C"
        if score >= 60:
            return "D"
        return "F"

    @property
    def pass_status(self) -> str:
        """是否及格"""
        return "及格" if self._score >= 60 else "不及格"


# TODO: 2. 实现 Temperature 类
class Temperature:
    """温度类（摄氏/华氏转换）

    属性:
        celsius: 摄氏温度
        fahrenheit: 华氏温度（计算属性）
    """

    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """摄氏温度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """设置摄氏温度"""
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """华氏温度（计算属性）"""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        """设置华氏温度"""
        self._celsius = (value - 32) * 5 / 9


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== @property 装饰器练习测试 ===\n")

    # 测试 Student 类
    print("1. Student 类测试:")
    student = Student("Alice", 85)
    print(f"   姓名: {student.name}")
    print(f"   成绩: {student.score}")
    print(f"   等级: {student.grade}")
    print(f"   状态: {student.pass_status}")

    # 测试成绩修改
    print("\n2. 成绩修改测试:")
    student.score = 92
    print(f"   修改后: 成绩={student.score}, 等级={student.grade}")

    # 测试异常
    print("\n3. 成绩验证测试:")
    try:
        student.score = 150  # 超出范围
    except ValueError as e:
        print(f"   捕获异常: {e}")

    # 测试 Temperature 类
    print("\n4. Temperature 类测试:")
    temp = Temperature(25)
    print(f"   摄氏温度: {temp.celsius:.1f}°C")
    print(f"   华氏温度: {temp.fahrenheit:.1f}°F")
    temp.fahrenheit = 212
    print(f"   沸点: 摄氏={temp.celsius:.1f}°C, 华氏={temp.fahrenheit:.1f}°F")
