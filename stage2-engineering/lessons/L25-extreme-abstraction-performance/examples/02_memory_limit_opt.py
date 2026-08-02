"""
L23 示例 02: 内存极限优化

展示使用 __slots__ 和其他技术实现内存极限优化。

主题:
1. __slots__ 内存节约分析
2. 大规模对象存储优化
3. 内存分析工具
4. 实战案例：粒子系统
"""

from __future__ import annotations

import gc
import sys
from dataclasses import dataclass
from typing import ClassVar

# ============================================================================
# 第一部分: __slots__ 内存节约分析
# ============================================================================


class NormalPoint:
    """普通类 - 使用 __dict__"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    """优化类 - 使用 __slots__"""

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


@dataclass(slots=True)
class DataPoint:
    """数据类 - 使用 slots"""

    x: float
    y: float


def analyze_memory_usage() -> None:
    """分析不同实现的内存使用"""

    print("\n" + "=" * 80)
    print("内存分析 1: 单个对象内存占用")
    print("=" * 80)

    # 创建实例
    normal = NormalPoint(1.0, 2.0)
    slotted = SlottedPoint(1.0, 2.0)
    data = DataPoint(1.0, 2.0)

    # 计算内存占用
    normal_size = sys.getsizeof(normal) + sys.getsizeof(normal.__dict__)
    slotted_size = sys.getsizeof(slotted)
    data_size = sys.getsizeof(data)

    print(f"\n{'类型':<30} {'内存 (bytes)':<15} {'节省':<15}")
    print("-" * 60)
    print(f"{'普通类 (__dict__)':<30} {normal_size:<15} {'基准':<15}")
    print(f"{'__slots__ 类':<30} {slotted_size:<15} {f'-{(1 - slotted_size / normal_size) * 100:.1f}%':<15}")
    print(f"{'dataclass(slots=True)':<30} {data_size:<15} {f'-{(1 - data_size / normal_size) * 100:.1f}%':<15}")

    print(f"\n✅ __slots__ 节省 {(1 - slotted_size / normal_size) * 100:.1f}% 内存")
    print(f"✅ dataclass(slots=True) 节省 {(1 - data_size / normal_size) * 100:.1f}% 内存")


def analyze_large_scale_memory() -> None:
    """分析大规模对象的内存占用"""

    print("\n" + "=" * 80)
    print("内存分析 2: 大规模对象内存占用")
    print("=" * 80)

    n = 100_000
    print(f"\n创建 {n:,} 个对象...")

    # 创建普通对象
    gc.collect()
    mem_before_normal = _get_memory_usage()
    normal_objects = [NormalPoint(float(i), float(i)) for i in range(n)]
    mem_after_normal = _get_memory_usage()
    normal_mem = mem_after_normal - mem_before_normal

    # 清理
    del normal_objects
    gc.collect()

    # 创建 __slots__ 对象
    mem_before_slotted = _get_memory_usage()
    slotted_objects = [SlottedPoint(float(i), float(i)) for i in range(n)]
    mem_after_slotted = _get_memory_usage()
    slotted_mem = mem_after_slotted - mem_before_slotted

    # 清理
    del slotted_objects
    gc.collect()

    print(f"\n{'类型':<30} {'内存 (MB)':<15} {'节省':<15}")
    print("-" * 60)
    print(f"{'普通类 (__dict__)':<30} {normal_mem / 1024 / 1024:<15.2f} {'基准':<15}")
    print(f"{'__slots__ 类':<30} {slotted_mem / 1024 / 1024:<15.2f} {f'-{(1 - slotted_mem / normal_mem) * 100:.1f}%':<15}")

    print(f"\n✅ 对于 {n:,} 个对象，__slots__ 节省 {(normal_mem - slotted_mem) / 1024 / 1024:.2f} MB")


def _get_memory_usage() -> int:
    """获取当前内存使用量（近似值）"""
    import resource

    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


# ============================================================================
# 第二部分: 复杂对象内存优化
# ============================================================================


class NormalParticle:
    """普通粒子类"""

    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, mass: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

    def update(self, dt: float) -> None:
        """更新位置"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt


class SlottedParticle:
    """优化粒子类 - 使用 __slots__"""

    __slots__ = ("mass", "vx", "vy", "vz", "x", "y", "z")

    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float, mass: float) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass

    def update(self, dt: float) -> None:
        """更新位置"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt


def compare_particle_memory() -> None:
    """对比粒子类的内存使用"""

    print("\n" + "=" * 80)
    print("内存分析 3: 复杂对象内存优化")
    print("=" * 80)

    # 单个对象
    normal_particle = NormalParticle(1.0, 2.0, 3.0, 0.1, 0.2, 0.3, 1.5)
    slotted_particle = SlottedParticle(1.0, 2.0, 3.0, 0.1, 0.2, 0.3, 1.5)

    normal_size = sys.getsizeof(normal_particle) + sys.getsizeof(normal_particle.__dict__)
    slotted_size = sys.getsizeof(slotted_particle)

    print("\n单个粒子对象:")
    print(f"  普通类: {normal_size} bytes")
    print(f"  __slots__: {slotted_size} bytes")
    print(f"  节省: {(1 - slotted_size / normal_size) * 100:.1f}%")

    # 大规模粒子系统
    n = 50_000
    print(f"\n创建 {n:,} 个粒子对象...")

    gc.collect()
    mem_before = _get_memory_usage()
    particles = [SlottedParticle(float(i), float(i), float(i), 0.1, 0.2, 0.3, 1.5) for i in range(n)]
    mem_after = _get_memory_usage()
    mem_used = mem_after - mem_before

    print(f"\n{n:,} 个 __slots__ 粒子:")
    print(f"  总内存: {mem_used / 1024 / 1024:.2f} MB")
    print(f"  平均每个: {mem_used / n:.1f} bytes")

    # 估算如果使用普通类的内存
    estimated_normal_mem = (normal_size / slotted_size) * mem_used
    estimated_saving = estimated_normal_mem - mem_used

    print("\n估算使用普通类:")
    print(f"  总内存: {estimated_normal_mem / 1024 / 1024:.2f} MB")
    print(f"  节省: {estimated_saving / 1024 / 1024:.2f} MB")

    # 清理
    del particles
    gc.collect()


# ============================================================================
# 第三部分: __slots__ 继承优化
# ============================================================================


class BaseEntity:
    """基础实体类"""

    __slots__ = ("id", "name")

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class MovableEntity(BaseEntity):
    """可移动实体 - 继承并添加新属性"""

    __slots__ = ("vx", "vy", "x", "y")

    def __init__(self, id: int, name: str, x: float, y: float) -> None:
        super().__init__(id, name)
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def move(self, dt: float) -> None:
        """移动"""
        self.x += self.vx * dt
        self.y += self.vy * dt


class CollidableEntity(MovableEntity):
    """可碰撞实体 - 多层继承"""

    __slots__ = ("mass", "radius")

    def __init__(self, id: int, name: str, x: float, y: float, radius: float, mass: float) -> None:
        super().__init__(id, name, x, y)
        self.radius = radius
        self.mass = mass


def analyze_inheritance_memory() -> None:
    """分析继承层次的内存使用"""

    print("\n" + "=" * 80)
    print("内存分析 4: __slots__ 继承优化")
    print("=" * 80)

    # 创建不同层次的对象
    base = BaseEntity(1, "Base")
    movable = MovableEntity(2, "Movable", 10.0, 20.0)
    collidable = CollidableEntity(3, "Collidable", 30.0, 40.0, 5.0, 10.0)

    print(f"\n{'类型':<30} {'属性数':<10} {'内存 (bytes)':<15}")
    print("-" * 55)
    print(f"{'BaseEntity':<30} {2:<10} {sys.getsizeof(base):<15}")
    print(f"{'MovableEntity':<30} {6:<10} {sys.getsizeof(movable):<15}")
    print(f"{'CollidableEntity':<30} {8:<10} {sys.getsizeof(collidable):<15}")

    print("\n✅ 继承链中的 __slots__ 保持内存效率")
    print("✅ 每层只需定义新增的属性")


# ============================================================================
# 第四部分: 实战案例 - 粒子模拟系统
# ============================================================================


@dataclass(slots=True)
class Particle3D:
    """3D 粒子 - 使用 dataclass slots"""

    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    mass: float

    # 类常量
    G: ClassVar[float] = 6.674e-11  # 引力常数

    def kinetic_energy(self) -> float:
        """计算动能"""
        v_squared = self.vx**2 + self.vy**2 + self.vz**2
        return 0.5 * self.mass * v_squared

    def update(self, dt: float) -> None:
        """更新位置"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt


class ParticleSystem:
    """粒子系统 - 内存优化版本"""

    def __init__(self, n_particles: int) -> None:
        self.n_particles = n_particles
        self.particles: list[Particle3D] = []
        self._initialize()

    def _initialize(self) -> None:
        """初始化粒子 - 禁用 GC 提升性能"""
        print(f"\n初始化 {self.n_particles:,} 个粒子...")

        gc.disable()

        for i in range(self.n_particles):
            particle = Particle3D(
                x=float(i),
                y=float(i),
                z=float(i),
                vx=0.1,
                vy=0.2,
                vz=0.3,
                mass=1.0,
            )
            self.particles.append(particle)

        gc.collect()
        gc.enable()

        print("✅ 初始化完成")

    def update(self, dt: float) -> None:
        """更新所有粒子"""
        for particle in self.particles:
            particle.update(dt)

    def total_kinetic_energy(self) -> float:
        """计算总动能"""
        return sum(p.kinetic_energy() for p in self.particles)

    def memory_usage(self) -> float:
        """估算内存使用 (MB)"""
        single_particle_size = sys.getsizeof(self.particles[0])
        total_size = single_particle_size * self.n_particles
        return total_size / 1024 / 1024


def demo_particle_system() -> None:
    """演示粒子系统"""

    print("\n" + "=" * 80)
    print("实战案例: 粒子模拟系统")
    print("=" * 80)

    n = 100_000
    system = ParticleSystem(n)

    print("\n系统信息:")
    print(f"  粒子数量: {system.n_particles:,}")
    print(f"  估算内存: {system.memory_usage():.2f} MB")
    print(f"  单粒子大小: {sys.getsizeof(system.particles[0])} bytes")

    # 计算初始动能
    initial_energy = system.total_kinetic_energy()
    print(f"  初始总动能: {initial_energy:.2e} J")

    # 更新模拟
    print("\n更新模拟 100 步...")
    for _ in range(100):
        system.update(0.01)

    final_energy = system.total_kinetic_energy()
    print(f"  最终总动能: {final_energy:.2e} J")

    print("\n✅ 使用 __slots__ 使得模拟 100,000 粒子成为可能")


# ============================================================================
# 第五部分: 内存优化最佳实践
# ============================================================================


def show_best_practices() -> None:
    """展示内存优化最佳实践"""

    print("\n" + "=" * 80)
    print("内存优化最佳实践")
    print("=" * 80)

    print("\n1. 何时使用 __slots__:")
    print("   ✅ 需要创建大量实例（>10,000）")
    print("   ✅ 内存是瓶颈")
    print("   ✅ 属性固定且明确")
    print("   ❌ 需要动态添加属性")
    print("   ❌ 需要使用 weakref")
    print("   ❌ 实例数量很少（<1,000）")

    print("\n2. __slots__ 与继承:")
    print("   ✅ 每个子类只定义新增属性")
    print("   ✅ 基类和子类都使用 __slots__")
    print("   ⚠️  混用 __slots__ 和 __dict__ 会失去优势")

    print("\n3. 性能权衡:")
    print("   ✅ 内存节省: 40-60%")
    print("   ✅ 访问速度: 提升 20-50%")
    print("   ❌ 灵活性: 不能动态添加属性")
    print("   ❌ 序列化: 不能使用 __dict__ 序列化")

    print("\n4. 推荐工具:")
    print("   • sys.getsizeof() - 快速内存估算")
    print("   • memory_profiler - 详细内存分析")
    print("   • pympler - 内存泄漏检测")
    print("   • objgraph - 对象引用图")

    print("\n5. 实战建议:")
    print("   • 先测量，后优化")
    print("   • 优先优化热点路径")
    print("   • 使用 dataclass(slots=True) 兼顾可读性")
    print("   • 大规模对象创建时禁用 GC")


# ============================================================================
# 主程序
# ============================================================================


def main() -> None:
    """运行所有内存优化示例"""

    print("\n" + "=" * 80)
    print("L23 示例 02: 内存极限优化")
    print("=" * 80)
    print("\n本示例展示 __slots__ 和其他内存优化技术")
    print("运行环境:")
    print(f"  Python 版本: {sys.version.split()[0]}")
    print(f"  GC 状态: {'启用' if gc.isenabled() else '禁用'}")

    # 运行所有分析
    analyze_memory_usage()
    analyze_large_scale_memory()
    compare_particle_memory()
    analyze_inheritance_memory()
    demo_particle_system()
    show_best_practices()

    # 总结
    print("\n" + "=" * 80)
    print("内存优化总结")
    print("=" * 80)
    print("\n关键收益:")
    print("  ✅ 单对象内存节省: 40-60%")
    print("  ✅ 大规模对象内存节省: 50-70%")
    print("  ✅ 属性访问速度提升: 20-50%")
    print("  ✅ 对象创建速度提升: 10-30%")

    print("\n适用场景:")
    print("  • 大规模数据处理 (>100,000 对象)")
    print("  • 科学计算和模拟")
    print("  • 游戏引擎")
    print("  • 实时系统")
    print("  • 嵌入式设备")

    print("\n推荐阅读:")
    print("  • Python 数据模型: __slots__")
    print("  • 高性能 Python 编程")
    print("  • Python 内存管理深度解析")
    print()


if __name__ == "__main__":
    main()
