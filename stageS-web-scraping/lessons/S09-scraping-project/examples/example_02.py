"""示例代码：完整 Scrapy 项目结构示例"""
from pathlib import Path


PROJECT_STRUCTURE = {
    "scrapy_project/": {
        "scrapy.cfg": "[settings]\ndefault = scrapy_project.settings",
        "scrapy_project/": {
            "__init__.py": "",
            "items.py": "from scrapy import Item, Field",
            "pipelines.py": "# 数据清洗与存储 Pipeline",
            "settings.py": "BOT_NAME = 'project'\nROBOTSTXT_OBEY = True",
            "spiders/": {
                "__init__.py": "",
                "product_spider.py": "# 商品数据爬虫",
            },
        },
    }
}


def create_project(root: Path) -> None:
    """创建 Scrapy 项目目录结构。"""
    # TODO: 递归创建目录和文件
    print(f"创建项目: {root}")


if __name__ == "__main__":
    print("Scrapy 项目结构示例")
