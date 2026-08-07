"""L07 练习3参考答案: @property 装饰器"""


class Student:
    """学生成绩类"""

    def __init__(self, name: str, score: float) -> None:
        self._name = name
        self.score = score

    @property
    def name(self) -> str:
        return self._name

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, value: float) -> None:
        if not 0 <= value <= 100:
            raise ValueError(f"成绩必须在 0-100 之间，得到 {value}")
        self._score = value

    @property
    def grade(self) -> str:
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
        return "及格" if self._score >= 60 else "不及格"


class Temperature:
    """温度类（摄氏/华氏转换）"""

    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self._celsius = (value - 32) * 5 / 9
