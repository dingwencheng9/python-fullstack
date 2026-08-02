"""配置管理"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ScraperConfig(BaseModel):
    """爬虫配置"""

    start_url: str = Field(..., description="起始 URL")
    max_pages: int = Field(default=10, ge=1, le=1000)
    delay: float = Field(default=1.0, ge=0.1, description="请求间隔(秒)")
    timeout: int = Field(default=10, ge=1)
    output_dir: str = Field(default="data", description="输出目录")
    user_agent: str = Field(default="Mozilla/5.0 (compatible; PythonScraper/1.0)")

    @classmethod
    def from_yaml(cls, path: str | Path) -> ScraperConfig:
        """从 YAML 文件加载配置"""
        with Path(path).open() as f:
            data = yaml.safe_load(f)
        return cls(**data)


def load_config(path: str | Path | None = None) -> ScraperConfig:
    """加载配置（支持 YAML 文件）"""
    if path and Path(path).exists():
        return ScraperConfig.from_yaml(path)
    # 交互式输入
    url = input("请输入目标 URL: ").strip()
    return ScraperConfig(start_url=url)
