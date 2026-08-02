"""示例代码：Scrapy 基础爬虫"""
import scrapy
from dataclasses import dataclass


@dataclass
class MovieItem:
    """电影数据模型。"""
    title: str = ""
    rating: float = 0.0
    quote: str = ""
    rank: int = 0


class DoubanSpider(scrapy.Spider):
    """豆瓣电影 Top250 爬虫。"""
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    
    def parse(self, response):
        """解析电影列表页。"""
        for item in response.css("div.item"):
            movie = MovieItem()
            movie.rank = int(item.css("em::text").get() or "0")
            movie.title = item.css("span.title::text").get() or ""
            movie.rating = float(item.css("span.rating_num::text").get() or "0")
            movie.quote = item.css("span.inq::text").get() or ""
            yield movie
        
        # 翻页
        next_page = response.css("span.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


if __name__ == "__main__":
    print("Scrapy 爬虫示例")
