"""示例代码：电商数据采集系统架构"""
from dataclasses import dataclass, field
from enum import Enum


class DataSource(Enum):
    WEB = "web"
    APP = "app"
    API = "api"


@dataclass
class ScraperConfig:
    """爬虫系统配置。"""
    source: DataSource
    max_concurrency: int = 10
    retry_times: int = 3
    timeout: int = 30
    proxy_pool: list[str] = field(default_factory=list)


class ScraperSystem:
    """分布式爬虫系统主类。"""
    
    def __init__(self) -> None:
        self.configs: dict[str, ScraperConfig] = {}
    
    def add_source(self, name: str, config: ScraperConfig) -> None:
        self.configs[name] = config
    
    def run(self) -> None:
        """运行爬虫任务。"""
        for name, config in self.configs.items():
            print(f"启动数据源: {name} ({config.source.value})")
            # TODO: 调度爬虫任务


if __name__ == "__main__":
    system = ScraperSystem()
    system.add_source("jd", ScraperConfig(source=DataSource.WEB))
    system.run()
