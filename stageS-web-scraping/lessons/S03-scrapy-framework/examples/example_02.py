"""示例代码：Scrapy Pipeline 数据清洗与存储"""
from dataclasses import dataclass


@dataclass
class MovieItem:
    title: str
    rating: float
    quote: str
    rank: int


class MoviePipeline:
    """电影数据清洗与存储 Pipeline。"""
    
    def __init__(self) -> None:
        self.items: list[MovieItem] = []
    
    def process_item(self, item: MovieItem, spider) -> MovieItem:
        """清洗和存储数据。"""
        # 清洗标题
        item.title = item.title.strip()
        # 清洗引言
        item.quote = item.quote.strip().rstrip(".")
        # 去重
        if not any(m.title == item.title for m in self.items):
            self.items.append(item)
        return item
    
    def close_spider(self, spider) -> None:
        """爬虫关闭时保存数据。"""
        print(f"共抓取 {len(self.items)} 部电影")
        # TODO: 存储到数据库或文件


if __name__ == "__main__":
    print("Pipeline 示例")
