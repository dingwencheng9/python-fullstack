"""P06: 数据分析与 RAG 智能报告平台 - 应用入口"""

from app.config import Config
from app.data.loader import DataLoader
from app.data.cleaner import DataCleaner
from app.pipeline.etl import ETLPipeline
from app.analytics.olap import OLAPQuery
from app.rag.vector_store import VectorStore
from app.visualization.chart_generator import ChartGenerator

__version__ = "1.0.0"


class DataRagPlatform:
    """数据分析与 RAG 智能报告平台"""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.loader = DataLoader(self.config)
        self.cleaner = DataCleaner()
        self.pipeline = ETLPipeline(self.config)
        self.olap = OLAPQuery(self.config)
        self.vector_store = VectorStore(self.config)
        self.chart_gen = ChartGenerator()

    async def load_and_process(self, file_path: str) -> dict:
        """加载并处理数据"""
        # 1. 加载数据
        df = await self.loader.load(file_path)

        # 2. 清洗数据
        df_clean = self.cleaner.clean(df)

        # 3. ETL 管道
        df_processed = await self.pipeline.process(df_clean)

        return {"data": df_processed}

    async def rag_query(self, query: str, top_k: int = 5) -> list[dict]:
        """RAG 智能查询"""
        return await self.vector_store.search(query, top_k)

    def generate_report(self, data: dict) -> bytes:
        """生成报告"""
        charts = self.chart_gen.create_dashboard(data)
        return charts


__all__ = ["DataRagPlatform", "Config"]
