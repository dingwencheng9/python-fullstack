"""P06: 应用配置"""

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """应用配置"""

    # 数据处理配置
    chunk_size: int = 10000
    max_workers: int = 4

    # DuckDB 配置
    duckdb_path: str = ":memory:"

    # RAG 配置
    embedding_dim: int = 384
    vector_store_path: str = "data/vectors"

    # 可视化配置
    figure_dpi: int = 100
    figure_size: tuple[int, int] = (10, 6)

    class Config:
        env_prefix = "P06_"


def get_config() -> Config:
    """获取配置单例"""
    return Config()
