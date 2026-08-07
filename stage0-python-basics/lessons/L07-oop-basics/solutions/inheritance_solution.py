"""L07 练习2参考答案: 继承与方法重写"""


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


class Car(Vehicle):
    """汽车类"""

    def __init__(self, brand: str, speed: int, wheels: int, doors: int) -> None:
        super().__init__(brand, speed)
        self.wheels = wheels
        self.doors = doors

    def drive(self) -> str:
        """重写行驶描述"""
        base = super().drive()
        return f"Car: {base}, {self.doors} 门 {self.wheels} 轮"


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


def drive_all(vehicles: list[Vehicle]) -> list[str]:
    """让所有交通工具行驶（多态演示）"""
    results: list[str] = []
    for vehicle in vehicles:
        results.append(vehicle.drive())
    return results
