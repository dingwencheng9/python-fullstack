"""L06 练习2: 继承与方法重写

难度: ⭐⭐☆ (中等)
预计时间: 30 分钟
知识点: 继承、方法重写、super()

任务描述:
完成以下继承层次结构的练习：

练习内容:
1. 定义一个 Vehicle 基类（品牌、速度）
2. 创建 Car 子类（轮数、车门数）+ 加速方法
3. 创建 Truck 子类（载重量）+ 载货方法
4. 实现多态：创建 drive_all() 函数处理不同车型

参考示例:
    class Vehicle:
        def __init__(self, brand: str, speed: int) -> None:
            self.brand = brand
            self.speed = speed

        def drive(self) -> str:
            return f"{self.brand} 以 {self.speed} km/h 行驶"

    class Car(Vehicle):
        def __init__(self, brand: str, speed: int, wheels: int, doors: int) -> None:
            super().__init__(brand, speed)
            self.wheels = wheels
            self.doors = doors

        def drive(self) -> str:
            return f"Car: {super().drive()}, {self.doors} 门"
"""


# ============ 练习开始 ============


# TODO: 1. 定义 Vehicle 基类
class Vehicle:
    """交通工具基类"""

    def __init__(self, brand: str, speed: int) -> None:
        self.brand = brand
        self.speed = speed

    def drive(self) -> str:
        """行驶描述"""
        return f"{self.brand} 以 {self.speed} km/h 行驶"

    def stop(self) -> str:
        """停车描述"""
        return f"{self.brand} 已停车"


# TODO: 2. 定义 Car 子类（继承 Vehicle）
class Car(Vehicle):
    """汽车类"""

    def __init__(self, brand: str, speed: int, wheels: int, doors: int) -> None:
        # 调用父类构造方法
        super().__init__(brand, speed)
        self.wheels = wheels
        self.doors = doors

    def drive(self) -> str:
        """重写行驶描述"""
        base = super().drive()
        return f"Car: {base}, {self.doors} 门 {self.wheels} 轮"


# TODO: 3. 定义 Truck 子类（继承 Vehicle）
class Truck(Vehicle):
    """卡车类"""

    def __init__(self, brand: str, speed: int, max_load: float) -> None:
        super().__init__(brand, speed)
        self.max_load = max_load
        self.current_load = 0.0

    def drive(self) -> str:
        """重写行驶描述"""
        base = super().drive()
        return f"Truck: {base}, 载重 {self.current_load:.1f}/{self.max_load:.1f} 吨"

    def load_cargo(self, weight: float) -> bool:
        """装载货物"""
        if weight < 0:
            return False
        if self.current_load + weight > self.max_load:
            return False
        self.current_load += weight
        return True

    def unload_cargo(self, weight: float) -> bool:
        """卸载货物"""
        if weight < 0 or weight > self.current_load:
            return False
        self.current_load -= weight
        return True


# TODO: 4. 实现多态函数 drive_all()
def drive_all(vehicles: list[Vehicle]) -> list[str]:
    """让所有交通工具行驶（多态演示）

    Args:
        vehicles: 交通工具列表（包含 Car、Truck 等）

    Returns:
        每个交通工具的行驶描述列表
    """
    results: list[str] = []
    for vehicle in vehicles:
        results.append(vehicle.drive())
    return results


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== 继承与方法重写练习测试 ===\n")

    # 创建不同类型的交通工具
    car = Car("Toyota", 120, 4, 4)
    truck = Truck("Volvo", 90, 20.0)

    # 测试基础功能
    print("1. 基础行驶测试:")
    print(f"   {car.drive()}")
    print(f"   {truck.drive()}")

    # 测试卡车载货
    print("\n2. 卡车载货测试:")
    print(f"   初始状态: {truck.drive()}")
    truck.load_cargo(5.0)
    print(f"   载货 5 吨: {truck.drive()}")
    truck.load_cargo(10.0)
    print(f"   载货 10 吨: {truck.drive()}")
    truck.unload_cargo(3.0)
    print(f"   卸货 3 吨: {truck.drive()}")

    # 测试多态
    print("\n3. 多态测试（drive_all）:")
    vehicles: list[Vehicle] = [car, truck, Car("Honda", 100, 4, 2)]
    for desc in drive_all(vehicles):
        print(f"   {desc}")
