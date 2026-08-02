"""元组不可变性示例。

演示元组的创建、解包、作为字典键的用法，以及不可变特性。
"""

# 创建元组
print("=== 元组创建 ===")
point: tuple[int, int] = (10, 20)
single_element: tuple[int] = (42,)  # 单元素元组需要逗号
rgb: tuple[int, int, int] = (255, 128, 0)

print(f"坐标点: {point}")
print(f"单元素元组: {single_element}")
print(f"RGB 颜色: {rgb}")

# 索引访问
print("\n=== 索引访问 ===")
x: int = point[0]
y: int = point[1]
print(f"x 坐标: {x}")
print(f"y 坐标: {y}")

# 元组解包（Unpacking）
print("\n=== 元组解包 ===")
x, y = point
print(f"解包后 x={x}, y={y}")

r, g, b = rgb
print(f"解包后 r={r}, g={g}, b={b}")

# 元组作为字典键
print("\n=== 元组作为字典键 ===")
coordinate_map: dict[tuple[int, int], str] = {
    (0, 0): "原点",
    (1, 0): "X轴单位点",
    (0, 1): "Y轴单位点",
}

location: str = coordinate_map[(0, 0)]
print(f"坐标 (0, 0) 对应: {location}")

# 演示不可变性
print("\n=== 不可变性验证 ===")
print("尝试修改元组会报错:")
print("point[0] = 30  # TypeError: 'tuple' object does not support item assignment")

# 元组可以包含可变对象（但元组本身不可变）
nested: tuple[int, list[int]] = (1, [2, 3])
print(f"\n嵌套元组: {nested}")
nested[1].append(4)  # 可以修改内部的列表
print(f"修改内部列表后: {nested}")
print("注意：元组本身不可变，但内部的可变对象可以修改")
