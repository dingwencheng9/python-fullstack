"""L07 练习2: 创建一个 Set 类（简化版集合）

难度: ⭐⭐☆ (中等)
预计时间: 30 分钟
知识点: __len__、__contains__、__iter__（选学，见 L11） 魔术方法、迭代器协议

任务要求:
1. __init__ - 初始化空集合
2. add(item) - 添加元素
3. remove(item) - 移除元素
4. __len__ - 返回集合大小
5. __contains__(item) - 判断元素是否在集合中
6. __iter__ - 返回迭代器（选学，详见 L11）

提示:
1. 内部使用 list 存储元素
2. __contains__ 可以遍历列表检查
3. __iter__ 返回 iter(self._items)（选学）
"""

from collections.abc import Iterator


class Set:
    """简化版集合类"""

    def __init__(self) -> None:
        """初始化空集合"""
        self._items: list[str] = []

    def add(self, item: str) -> None:
        """添加元素"""
        if item not in self._items:
            self._items.append(item)

    def remove(self, item: str) -> bool:
        """移除元素"""
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def __len__(self) -> int:
        """返回集合大小"""
        return len(self._items)

    def __contains__(self, item: str) -> bool:
        """判断元素是否在集合中"""
        return item in self._items

    def __iter__(self) -> Iterator[str]:
        """返回迭代器"""
        return iter(self._items)


# 测试代码
if __name__ == "__main__":
    s = Set()
    s.add("apple")
    s.add("banana")
    s.add("apple")  # 重复添加

    print(f"集合大小: {len(s)}")  # 预期: 2
    print(f"'apple' in s: {'apple' in s}")  # 预期: True
    print(f"'orange' in s: {'orange' in s}")  # 预期: False

    s.remove("banana")
    print(f"移除后大小: {len(s)}")  # 预期: 1
