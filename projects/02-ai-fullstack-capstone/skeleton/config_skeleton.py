"""

from __future__ import annotations

【骨架代码】应用配置 — 环境变量加载

TODO: 按照注释提示，补全代码
"""

from __future__ import annotations

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """应用配置

    TODO: 定义以下配置字段：
    1. debug: bool = False - 是否调试模式
    2. host: str = "0.0.0.0" - 监听地址
    3. port: int = 8000 - 监听端口
    4. openai_api_key: str | None = None - OpenAI API Key
    5. default_llm_model: str = "gpt-3.5-turbo" - 默认模型
    6. enable_mock_llm: bool = True - 是否启用 Mock LLM（离线可用）
    7. embedding_dim: int = 1536 - 嵌入维度
    """

    # ← 你的代码写在这里


# 创建全局配置实例
config: AppConfig = AppConfig()
