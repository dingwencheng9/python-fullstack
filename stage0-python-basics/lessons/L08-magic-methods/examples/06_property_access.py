"""示例6: 属性访问 __getattr__ __setattr__"""


class LazyObject:
    """演示属性访问控制"""

    def __init__(self) -> None:
        # 使用 object.__setattr__ 避免触发我们的 __setattr__
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_loaded", False)

    def __getattr__(self, name: str) -> str:
        """访问不存在的属性时调用"""
        if name.startswith("_"):
            return f"[私有属性: {name}]"  # 私有属性用替代值
        if name not in self._data:
            return f"[未加载: {name}]"
        return self._data[name]

    def __setattr__(self, name: str, value: str) -> None:
        """设置属性时调用"""
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def load(self, key: str, value: str) -> None:
        self._data[key] = value


# 演示
obj = LazyObject()
obj.load("name", "Alice")
obj.load("age", "30")

print(f"name: {obj.name}")  # Alice
print(f"city: {obj.city}")  # [未加载: city]
print(f"age: {obj.age}")  # 30
