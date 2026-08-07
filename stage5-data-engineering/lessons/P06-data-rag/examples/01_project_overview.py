"""P06 示例: 项目概述"""

from __future__ import annotations

# ============ 数据分析平台架构 ============

class DataRagPlatform:
    """数据分析与 RAG 智能报告平台"""

    def __init__(self):
        self.name = "DataRag"
        self.version = "1.0"
        self.components = {
            "data_loader": "Pandas + PyArrow",
            "etl_pipeline": "asyncio + aiohttp",
            "analytics": "DuckDB OLAP",
            "rag": "NumPy 向量检索",
            "visualization": "Matplotlib + Seaborn",
        }

    def summary(self) -> str:
        return f"""
{'='*60}
DataRag - 数据分析与 RAG 智能报告平台
{'='*60}

版本: {self.version}
组件数: {len(self.components)}

组件详情:
"""
        for name, tech in self.components.items():
            summary += f"  • {name}: {tech}\n"
        return summary

    def tech_stack(self) -> dict:
        """返回技术栈映射"""
        return {
            "数据处理": ["Pandas", "NumPy", "PyArrow"],
            "数据库": ["DuckDB"],
            "异步": ["asyncio", "aiohttp"],
            "向量检索": ["NumPy"],
            "可视化": ["Matplotlib", "Seaborn"],
            "测试": ["pytest"],
        }


def demonstrate():
    """演示项目"""
    platform = DataRagPlatform()

    print(platform.summary())

    print("\n技术栈:")
    for category, tools in platform.tech_stack().items():
        print(f"  {category}: {', '.join(tools)}")

    print("\n整合的 Stage 5 课程:")
    lessons = [
        ("L47", "Pandas 完整实战"),
        ("L48", "数据可视化"),
        ("L49", "DuckDB"),
        ("L50", "Pandas 进阶"),
        ("L51", "异步数据管道"),
        ("L52", "NumPy RAG"),
        ("L53", "DuckDB OLAP"),
    ]
    for code, title in lessons:
        print(f"  {code}: {title}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate()
