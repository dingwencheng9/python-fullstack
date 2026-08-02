"""Capstone 配置（使用 pydantic-settings 强类型验证）。"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置（从环境变量或 .env 文件加载）。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 应用配置
    app_env: str = Field(default="development", description="应用环境")
    app_host: str = Field(default="0.0.0.0", description="监听地址")
    app_port: int = Field(default=8000, ge=1, le=65535, description="监听端口")

    # 模型配置
    model_name: str = Field(default="mock", description="LLM 模型名称")

    # 存储配置
    qdrant_url: str = Field(default="http://localhost:6333", description="Qdrant 服务地址")
    duckdb_path: str = Field(default="data/app.duckdb", description="DuckDB 数据库路径")

    # 安全配置
    secret_key: str = Field(
        default="dev-only-insecure-key-change-in-production",
        min_length=16,
        description="JWT 密钥（生产环境必须设置）",
    )
    algorithm: str = Field(default="HS256", description="JWT 加密算法")
    access_token_expire_minutes: int = Field(
        default=30, ge=1, le=43200, description="访问令牌过期时间（分钟）"
    )


# 全局配置实例（单例模式）
settings = Settings()
