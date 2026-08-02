"""示例3: 比较运算符魔法方法"""

from __future__ import annotations


class Version:
    """演示版本号比较"""

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __lt__(self, other: Version) -> bool:
        """小于比较"""
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other: Version) -> bool:
        """小于等于"""
        return self == other or self < other

    def __gt__(self, other: Version) -> bool:
        """大于"""
        return other < self

    def __ge__(self, other: Version) -> bool:
        """大于等于"""
        return self == other or other < self

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))

    def __repr__(self) -> str:
        return f"Version({self.major}.{self.minor}.{self.patch})"


# 演示
v1 = Version(1, 2, 3)
v2 = Version(1, 2, 4)
v3 = Version(2, 0, 0)

print(f"{v1} == {v2}: {v1 == v2}")  # False
print(f"{v1} < {v2}: {v1 < v2}")  # True
print(f"{v2} < {v3}: {v2 < v3}")  # True
print(f"{v1} <= {v2}: {v1 <= v2}")  # False

# 用于排序
versions = [v3, v1, v2]
print(f"排序后: {sorted(versions)}")
