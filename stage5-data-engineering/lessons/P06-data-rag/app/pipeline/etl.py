"""P06: ETL 管道模块"""

import asyncio
from pandas import DataFrame


class ETLPipeline:
    """ETL 数据管道"""

    def __init__(self, config=None):
        self.config = config

    async def process(self, df: DataFrame) -> DataFrame:
        """处理数据"""
        df = df.copy()

        # 转换数据类型
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            df[col] = df[col].astype("float32")

        return df

    async def batch_process(self, df: DataFrame, batch_size: int = 1000) -> list[DataFrame]:
        """批量处理数据"""
        batches = []
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i : i + batch_size]
            processed = await self.process(batch)
            batches.append(processed)
        return batches
