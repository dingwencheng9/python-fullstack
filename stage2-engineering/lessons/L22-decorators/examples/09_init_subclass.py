"""

使用 __init_subclass__ 实现子类自动注册。

本文件演示：
- __init_subclass__ 的基本机制
- 自动插件注册系统
- 枚举约束与验证
- 配置继承与默认值注入

作者: Python 3.13 全栈课程
日期: 2026-07-13
Python版本: 3.6+
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar


def demo_basic_init_subclass() -> None:
    """演示 __init_subclass__ 基本机制"""
    print("=" * 50)
    print("1. __init_subclass__ 基本机制")
    print("=" * 50)

    class Plugin:
        """插件基类"""

        _registry: ClassVar[dict[str, type] | list[type]] = {}

        def __init_subclass__(cls, name: str = "", **kwargs):
            super().__init_subclass__(**kwargs)
            if name:
                cls._registry[name] = cls
                print(f"  [注册] '{name}' → {cls.__name__}")
            else:
                # 无名子类也加入列表
                cls._registry.setdefault("_unregistered", []).append(cls)

    print("定义 AuthPlugin:")

    class AuthPlugin(Plugin, name="auth"):
        pass

    print("定义 CachePlugin:")

    class CachePlugin(Plugin, name="cache"):
        pass

    print("定义 LoggerPlugin:")

    class LoggerPlugin(Plugin, name="logger"):
        pass

    print(f"\n注册表: {Plugin._registry}")
    print()


def demo_plugin_system() -> None:
    """演示插件注册系统的实际应用"""
    print("=" * 50)
    print("2. 插件注册系统")
    print("=" * 50)

    class PluginBase(ABC):
        """插件基类"""

        _plugins: ClassVar[dict[str, type["PluginBase"]]] = {}

        def __init_subclass__(cls, plugin_id: str = "", **kwargs):
            super().__init_subclass__(**kwargs)
            if plugin_id:
                cls._plugins[plugin_id] = cls
                print(f"  [注册] plugin_id='{plugin_id}'")

        @abstractmethod
        def execute(self, data: str) -> str:
            """执行插件逻辑"""
            ...

    # 定义插件
    class ReversePlugin(PluginBase, plugin_id="reverse"):
        def execute(self, data: str) -> str:
            return data[::-1]

    class UpperPlugin(PluginBase, plugin_id="upper"):
        def execute(self, data: str) -> str:
            return data.upper()

    class LengthPlugin(PluginBase, plugin_id="length"):
        def execute(self, data: str) -> str:
            return str(len(data))

    # 使用插件
    test_input = "Hello"
    print(f"\n输入: '{test_input}'")
    print("通过注册表调用插件:")

    for pid, plugin_cls in PluginBase._plugins.items():
        plugin = plugin_cls()
        result = plugin.execute(test_input)
        print(f"  {pid}: '{result}'")
    print()


def demo_enum_like_validation() -> None:
    """演示枚举约束与验证"""
    print("=" * 50)
    print("3. 枚举约束与验证")
    print("=" * 50)

    class Unit(ABC):
        """物理单位基类"""

        _units: ClassVar[dict[str, "Unit"]] = {}
        _valid_symbols: ClassVar[set[str]] = set()

        def __init_subclass__(cls, symbol: str = "", **kwargs):
            super().__init_subclass__(**kwargs)
            if symbol:
                if symbol in cls._valid_symbols:
                    raise ValueError(f"符号 '{symbol}' 已被注册")
                cls._valid_symbols.add(symbol)
                cls._units[symbol] = cls
                cls.symbol = symbol  # 类属性

        @abstractmethod
        def to_base(self, value: float) -> float:
            """转换为基准单位"""
            ...

        @abstractmethod
        def from_base(self, value: float) -> float:
            """从基准单位转换"""
            ...

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.symbol})"

    class Meter(Unit, symbol="m"):
        def to_base(self, value: float) -> float:
            return value

        def from_base(self, value: float) -> float:
            return value

    class Centimeter(Unit, symbol="cm"):
        def to_base(self, value: float) -> float:
            return value / 100

        def from_base(self, value: float) -> float:
            return value * 100

    class Kilometer(Unit, symbol="km"):
        def to_base(self, value: float) -> float:
            return value * 1000

        def from_base(self, value: float) -> float:
            return value / 1000

    # 使用
    print(f"有效符号: {Unit._valid_symbols}")

    km = Kilometer()
    cm = Centimeter()
    print(f"1 km = {km.to_base(1)} m")
    print(f"100 cm = {cm.to_base(100)} m")

    # 通过符号查找
    print(f"通过 'km' 查找: {Unit._units['km']}")
    print()


def demo_config_inheritance() -> None:
    """演示配置继承与默认值注入"""
    print("=" * 50)
    print("4. 配置继承与默认值注入")
    print("=" * 50)

    class ConfigBase:
        """配置基类"""

        _config_registry: ClassVar[dict[str, "ConfigBase"]] = {}
        _default_timeout: ClassVar[int] = 30
        _default_retries: ClassVar[int] = 3

        def __init_subclass__(
            cls,
            scope: str = "default",
            timeout: int | None = None,
            retries: int | None = None,
            **kwargs,
        ):
            super().__init_subclass__(**kwargs)
            # 注入默认值
            cls.timeout = timeout if timeout is not None else cls._default_timeout
            cls.retries = retries if retries is not None else cls._default_retries
            cls.scope = scope
            cls._config_registry[scope] = cls
            print(
                f"  [配置注册] scope='{scope}', timeout={cls.timeout}, retries={cls.retries}"
            )

    print("定义 DevelopmentConfig:")

    class DevelopmentConfig(ConfigBase, scope="dev", timeout=5, retries=1):
        pass

    print("定义 ProductionConfig:")

    class ProductionConfig(ConfigBase, scope="prod", timeout=60, retries=5):
        pass

    print("定义 StagingConfig:")

    class StagingConfig(ConfigBase, scope="staging"):
        # 不指定 timeout/retries，使用默认值
        pass

    print(f"\n配置注册表: {list(ConfigBase._config_registry.keys())}")

    for scope, config_cls in ConfigBase._config_registry.items():
        config = config_cls()
        print(f"  {scope}: timeout={config.timeout}s, retries={config.retries}")
    print()


def demo_order_preservation() -> None:
    """演示注册顺序保持（Python 3.7+ dict 有序）"""
    print("=" * 50)
    print("5. 注册顺序保持")
    print("=" * 50)

    class Handler:
        _handlers: ClassVar[dict[str, "Handler"]] = {}

        def __init_subclass__(cls, handler_id: str = "", order: int = 0, **kwargs):
            super().__init_subclass__(**kwargs)
            if handler_id:
                cls._handlers[handler_id] = cls
                cls._order = order  # 保存注册顺序

        @classmethod
        def get_ordered_handlers(cls) -> list[tuple[str, type]]:
            """按注册顺序返回所有处理器"""
            return sorted(cls._handlers.items(), key=lambda x: x[1]._order)

    class FirstHandler(Handler, handler_id="first", order=1):
        pass

    class SecondHandler(Handler, handler_id="second", order=2):
        pass

    class ThirdHandler(Handler, handler_id="third", order=3):
        pass

    print("按注册顺序执行处理器:")
    for handler_id, handler_cls in Handler.get_ordered_handlers():
        print(f"  → {handler_id} (order={handler_cls._order})")
    print()


def main() -> None:
    """主函数"""
    print(">>> __init_subclass__ 演示\n")

    demo_basic_init_subclass()
    demo_plugin_system()
    demo_enum_like_validation()
    demo_config_inheritance()
    demo_order_preservation()

    print(">>> 演示完成！")
    print()
    print("要点总结:")
    print("  1. __init_subclass__ 在子类创建时自动调用")
    print("  2. 可用于实现自动插件/组件注册")
    print("  3. 支持枚举约束、配置继承等场景")
    print("  4. 是实现类级别隐式装饰器的重要手段")


if __name__ == "__main__":
    main()
