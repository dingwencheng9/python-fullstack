"""
示例 2: 环境配置与密钥管理

展示 pydantic-settings 配置管理和密钥管理最佳实践。
"""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """应用配置 - 简化版"""

    # 应用配置
    app_name: str = "ai-agent"
    app_version: str = "1.0.0"
    debug: bool = False

    # LLM 配置
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # 数据库配置
    database_url: str = "postgresql://user:pass@localhost:5432/agent"

    # Redis 配置
    redis_url: str = "redis://localhost:6379/0"

    # 可观测性配置
    otlp_endpoint: str = "http://localhost:4317"
    metrics_enabled: bool = True


class SecretManager:
    """密钥管理器 - 演示版"""

    # 模拟的密钥存储
    _secrets: dict[str, str] = {}

    @classmethod
    def get_api_key(cls, key_name: str) -> str:
        """获取 API Key"""
        # 1. 优先从环境变量获取
        api_key = os.environ.get(key_name)
        if api_key:
            return api_key

        # 2. 从密钥存储获取
        if key_name in cls._secrets:
            return cls._secrets[key_name]

        raise ValueError(f"API Key not found: {key_name}")

    @classmethod
    def set_secret(cls, key: str, value: str) -> None:
        """设置密钥"""
        cls._secrets[key] = value


def validate_api_key(api_key: str) -> bool:
    """验证 API Key 格式"""
    if not api_key:
        return False

    # 验证常见 API Key 格式
    valid_prefixes = ["sk-", "sk-ant-", "ghp_", "AKIA"]

    for prefix in valid_prefixes:
        if api_key.startswith(prefix):
            return True

    return False


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("环境配置与密钥管理示例")
    print("=" * 60)

    # 1. 加载配置
    print("\n--- 配置加载 ---")
    settings = Settings(
        app_name="my-agent",
        openai_api_key="sk-test12345678",
    )
    print(f"应用名称: {settings.app_name}")
    print(f"版本: {settings.app_version}")
    print(f"调试模式: {settings.debug}")

    # 2. 密钥管理
    print("\n--- 密钥管理 ---")

    # 设置密钥
    SecretManager.set_secret("OPENAI_API_KEY", "sk-secret12345678")
    print("✅ 密钥已设置")

    # 获取密钥
    try:
        key = SecretManager.get_api_key("OPENAI_API_KEY")
        print(f"✅ 密钥获取成功: {key[:10]}...")
    except ValueError as e:
        print(f"❌ 密钥获取失败: {e}")

    # 3. API Key 验证
    print("\n--- API Key 验证 ---")
    test_keys = [
        "sk-test12345678",  # OpenAI
        "sk-ant-api03-xxxxx",  # Anthropic
        "ghp_xxxxxxxxxxxx",  # GitHub
        "invalid-key",  # 无效
    ]

    for key in test_keys:
        is_valid = validate_api_key(key)
        prefix = key[:10] if len(key) > 10 else key
        print(f"  {prefix}: {'✅ 有效' if is_valid else '❌ 无效'}")

    # 4. 环境变量覆盖
    print("\n--- 环境变量覆盖 ---")
    os.environ["OPENAI_API_KEY"] = "sk-from-env-12345"

    try:
        key = SecretManager.get_api_key("OPENAI_API_KEY")
        print(f"从环境变量获取: {key[:15]}...")
    except ValueError:
        pass

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert validate_api_key("sk-test12345678"), "OpenAI Key 格式应该有效"
    assert validate_api_key("sk-ant-api03-xxxxx"), "Anthropic Key 格式应该有效"
    assert not validate_api_key("invalid-key"), "无效 Key 格式应该无效"
    print("✅ 密钥管理验证通过!")


if __name__ == "__main__":
    main()
