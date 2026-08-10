"""P06: 数据清洗模块"""

import pandas as pd


class DataCleaner:
    """数据清洗器"""

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗数据"""
        df = df.copy()

        # 移除重复行
        df = df.drop_duplicates()

        # 处理缺失值
        for col in df.columns:
            if df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna("")

        return df

    def validate(self, df: pd.DataFrame) -> bool:
        """验证数据质量"""
        if df.empty:
            return False
        if df.isnull().any().any():
            return False
        return True
