"""P06: 数据加载模块"""

from pathlib import Path
import pandas as pd


class DataLoader:
    """数据加载器"""

    def __init__(self, config=None):
        self.config = config

    async def load(self, file_path: str) -> pd.DataFrame:
        """加载数据文件"""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".csv":
            return pd.read_csv(file_path)
        elif suffix == ".parquet":
            return pd.read_parquet(file_path)
        elif suffix == ".json":
            return pd.read_json(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")

    def load_chunks(self, file_path: str, chunk_size: int = 10000):
        """分块加载大文件"""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".csv":
            return pd.read_csv(file_path, chunksize=chunk_size)
        else:
            raise ValueError(f"分块加载不支持: {suffix}")
