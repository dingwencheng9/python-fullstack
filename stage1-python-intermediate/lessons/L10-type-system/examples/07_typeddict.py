"""
L10 示例 7: TypedDict 与类型安全的 **kwargs

展示如何使用 TypedDict 定义字典结构类型，
以及 PEP 692 Unpack 实现类型安全的 **kwargs。
"""

from __future__ import annotations

from typing import TypedDict, Unpack

# ============================================================================
# 基础 TypedDict
# ============================================================================


class UserDict(TypedDict):
    """用户字典类型"""

    name: str
    age: int
    email: str


def create_user(**kwargs: Unpack[UserDict]) -> UserDict:
    """✨ 使用 TypedDict 的 **kwargs"""
    return kwargs


# ============================================================================
# 可选字段
# ============================================================================


class UserOptional(TypedDict, total=False):
    """所有字段可选"""

    name: str
    age: int
    email: str


class UserPartial(TypedDict):
    """部分字段必需"""

    name: str  # 必需
    age: int  # 必需


class UserPartialOptional(UserPartial, total=False):
    """添加可选字段"""

    email: str  # 可选
    phone: str  # 可选


def update_user(**kwargs: Unpack[UserPartialOptional]) -> UserPartialOptional:
    """更新用户信息"""
    return kwargs


# ============================================================================
# 实际应用：配置管理
# ============================================================================


class DatabaseConfig(TypedDict):
    """数据库配置"""

    host: str
    port: int
    database: str


class CacheConfig(TypedDict, total=False):
    """缓存配置（可选）"""

    enabled: bool
    ttl: int


class AppConfig(TypedDict):
    """应用配置"""

    debug: bool
    database: DatabaseConfig


class FullConfig(AppConfig, total=False):
    """完整配置（带可选字段）"""

    cache: CacheConfig


def configure_app(**config: Unpack[FullConfig]) -> None:
    """配置应用"""
    print(f"Debug mode: {config.get('debug', False)}")

    if "database" in config:
        db = config["database"]
        print(f"Database: {db['host']}:{db['port']}/{db['database']}")

    if "cache" in config and config["cache"].get("enabled"):
        print(f"Cache TTL: {config['cache'].get('ttl', 300)}s")


# ============================================================================
# 实际应用：API 响应
# ============================================================================


class APIResponse(TypedDict):
    """API 响应基础"""

    success: bool
    message: str


class APIDataResponse(APIResponse):
    """带数据的响应"""

    data: dict[str, str | int]


class APIErrorResponse(APIResponse):
    """错误响应"""

    error_code: int


def make_success_response(**kwargs: Unpack[APIDataResponse]) -> APIDataResponse:
    """创建成功响应"""
    return kwargs


def make_error_response(**kwargs: Unpack[APIErrorResponse]) -> APIErrorResponse:
    """创建错误响应"""
    return kwargs


# ============================================================================
# 演示函数
# ============================================================================


def demonstrate_basic_typeddict() -> None:
    """演示基础 TypedDict"""

    print("📝 基础 TypedDict 演示")
    print("=" * 70)

    # 正确用法
    user1 = create_user(name="Alice", age=25, email="alice@example.com")
    print(f"\n用户 1: {user1}")


def demonstrate_optional_fields() -> None:
    """演示可选字段"""

    print("\n\n🔧 可选字段演示")
    print("=" * 70)

    # 只提供必需字段
    user1 = update_user(name="Alice", age=25)
    print(f"\n最小信息: {user1}")

    # 提供完整信息
    user2 = update_user(name="Bob", age=30, email="bob@example.com", phone="123-456-7890")
    print(f"完整信息: {user2}")


def demonstrate_nested_typeddict() -> None:
    """演示嵌套 TypedDict"""

    print("\n\n🏗️  嵌套 TypedDict 演示")
    print("=" * 70)

    # 配置应用
    print("\n配置 1: 最小配置")
    configure_app(debug=True, database={"host": "localhost", "port": 5432, "database": "myapp"})

    print("\n配置 2: 完整配置")
    configure_app(
        debug=False,
        database={"host": "prod.example.com", "port": 5432, "database": "prod_db"},
        cache={"enabled": True, "ttl": 600},
    )


def demonstrate_api_responses() -> None:
    """演示 API 响应"""

    print("\n\n🌐 API 响应演示")
    print("=" * 70)

    success = make_success_response(
        success=True,
        message="User created successfully",
        data={"user_id": 123, "username": "alice"},
    )
    print(f"\n成功响应: {success}")

    error = make_error_response(success=False, message="User not found", error_code=404)
    print(f"错误响应: {error}")


def show_best_practices() -> None:
    """展示最佳实践"""

    print("\n\n💡 TypedDict 最佳实践")
    print("=" * 70)

    practices = [
        "1. 使用 TypedDict 为字典提供结构化类型",
        "2. 使用 Unpack 为 **kwargs 提供类型安全",
        "3. total=False 使所有字段可选",
        "4. 通过继承组合必需和可选字段",
        "5. 用于配置、API 响应、函数选项等场景",
        "6. 比普通 dict 提供更好的 IDE 支持",
        "7. mypy 可以检测缺失或错误的键",
    ]

    for practice in practices:
        print(f"  {practice}")


def show_comparison() -> None:
    """对比普通字典和 TypedDict"""

    print("\n\n🆚 普通字典 vs TypedDict")
    print("=" * 70)

    comparison = """
普通字典:
  def create_user(**kwargs) -> dict:
      return kwargs

  user = create_user(name="Alice", age=25)
  # ❌ 无类型检查
  # ❌ 拼写错误不会被检测
  # ❌ 缺失字段不会警告

TypedDict:
  class UserDict(TypedDict):
      name: str
      age: int

  def create_user(**kwargs: Unpack[UserDict]) -> UserDict:
      return kwargs

  user = create_user(name="Alice", age=25)
  # ✅ mypy 检查类型
  # ✅ IDE 自动补全
  # ✅ 拼写错误被检测
  # ✅ 缺失字段会警告
"""

    print(comparison)


def main() -> None:
    """主函数"""

    print("✨ TypedDict for **kwargs 完整演示")
    print("=" * 70)

    demonstrate_basic_typeddict()
    demonstrate_optional_fields()
    demonstrate_nested_typeddict()
    demonstrate_api_responses()
    show_best_practices()
    show_comparison()

    print("\n\n🎯 关键要点：")
    print("  • TypedDict: 字典的结构化类型")
    print("  • Unpack: 为 **kwargs 提供类型")
    print("  • total=False: 所有字段可选")
    print("  • 继承: 组合必需和可选字段")
    print("  • 用途: 配置、API、选项等")


if __name__ == "__main__":
    main()
