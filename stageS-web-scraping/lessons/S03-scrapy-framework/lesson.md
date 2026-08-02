# S03: 工业级爬虫 — Scrapy 框架

> **课程编号**: S03
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 10 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: S02 XPath 与 BeautifulSoup

---

## 📚 课程概述

Scrapy 是 Python 最成熟的工业级爬虫框架，提供完整的请求/响应管道、数据提取、存储一体化解决方案。本课程从零构建 Scrapy 项目，掌握生产级爬虫开发的核心技能。

---

## 🎯 学习目标

1. 理解 Scrapy 架构与异步爬取原理
2. 掌握 Scrapy 项目创建与配置
3. 熟练使用 Selectors 提取数据
4. 实现翻页抓取与增量爬取
5. 掌握 Item Pipeline 数据清洗与存储
6. 配置反爬应对策略

---

## 📋 课程大纲

- [Part 1: Scrapy 架构与异步原理](#part-1-scrapy-架构与异步原理)
- [Part 2: 项目创建与核心组件](#part-2-项目创建与核心组件)
- [Part 3: 数据提取与 Selectors](#part-3-数据提取与-selectors)
- [Part 4: Item 与 Pipeline](#part-4-item-与-pipeline)
- [Part 5: 反爬应对与中间件](#part-5-反爬应对与中间件)

---

## 🔧 环境准备

```bash
# 创建虚拟环境
cd stageS-web-scraping/lessons/S03-scrapy-framework
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 安装 Scrapy
uv add scrapy

# 创建 Scrapy 项目
scrapy startproject tutorial
cd tutorial

# 运行第一个爬虫
scrapy genspider quotes quotes.toscrape.com
scrapy crawl quotes
```

---

## 📖 详细内容

### Part 1: Scrapy 架构与异步原理

#### 1.1 为什么需要 Scrapy？

**对比 Requests + BS4 的局限**：

| 维度 | Requests + BS4 | Scrapy |
|------|----------------|--------|
| 请求管理 | 手动串行/并发 | 内置异步并发 |
| 去重 | 需手动实现 | 自动 Request 去重 |
| 断点续爬 | 需手动实现 | 内置支持 |
| 中间件 | 无 | 请求/响应中间件 |
| 数据管道 | 无 | Item Pipeline |
| 配置管理 | 硬编码 | settings.py |

#### 1.2 Twisted 异步引擎

Scrapy 基于 Twisted 事件驱动框架：

```python
# 同步思维（阻塞）
def fetch_all(urls):
    results = []
    for url in urls:
        response = requests.get(url)  # 等待完成才继续
        results.append(parse(response))
    return results

# 异步思维（非阻塞）
async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

Scrapy 使用 Twisted 的 Deferred 机制，实现高并发爬取：

```python
# Scrapy 的并发模型
# settings.py
CONCURRENT_REQUESTS = 16          # 并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # 单域名并发
DOWNLOAD_DELAY = 0.5              # 请求间隔
```

#### 1.3 Scrapy 架构图

```
                    ┌─────────────────────────────────────┐
                    │           Scrapy Engine             │
                    │  (核心调度器，控制数据流)            │
                    └──────────┬──────────────┬───────────┘
                               │              │
              ┌────────────────┴───┐    ┌─────┴────────────┐
              │    Scheduler       │    │  Item Pipeline   │
              │  (Request 队列)    │    │  (数据处理链)    │
              └────────────────────┘    └──────────────────┘
                               │
              ┌────────────────┴───┐
              │   Downloader       │
              │   Middleware       │
              └─────────┬──────────┘
                        │
              ┌─────────┴──────────┐
              │    Downloader      │
              │  (Twisted 异步)    │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │   Spider           │
              │  (解析逻辑)        │
              └────────────────────┘
```

---

### Part 2: 项目创建与核心组件

#### 2.1 创建项目

```bash
# 创建项目
scrapy startproject myspider myproject
cd myproject

# 目录结构
myspider/
├── myspider/              # Python 包
│   ├── __init__.py
│   ├── items.py          # 定义数据结构
│   ├── middlewares.py    # 中间件
│   ├── pipelines.py      # 数据管道
│   ├── settings.py       # 配置
│   └── spiders/          # 爬虫目录
│       └── __init__.py
├── scrapy.cfg            # 项目配置
└── main.py               # 启动脚本
```

#### 2.2 定义 Item（数据结构）

```python
# items.py
import scrapy

class ProductItem(scrapy.Item):
    """商品数据结构"""
    product_id = scrapy.Field()           # 商品ID
    title = scrapy.Field()                 # 商品标题
    price = scrapy.Field()                 # 价格
    shop = scrapy.Field()                  # 店铺名
    category = scrapy.Field()              # 分类
    sales = scrapy.Field()                 # 销量
    url = scrapy.Field()                   # 商品链接
    images = scrapy.Field()                # 图片列表
    crawled_at = scrapy.Field()            # 爬取时间
```

#### 2.3 编写 Spider

```python
# spiders/product_spider.py
import scrapy
from myspider.items import ProductItem

class ProductSpider(scrapy.Spider):
    """商品爬虫"""
    name = 'products'
    allowed_domains = ['jd.com']

    # 初始 URL
    start_urls = ['https://search.jd.com/Search?keyword=手机']

    def parse(self, response):
        """解析商品列表页"""
        # 提取商品链接
        selectors = response.css('div.gl-warp > div.gl-item')

        for sel in selectors:
            item = ProductItem()
            item['product_id'] = sel.css('::attr(data-sku)').get()
            item['title'] = sel.css('div.p-name em::text').get()
            item['price'] = sel.css('div.p-price i::text').get()
            item['shop'] = sel.css('div.p-shop a::text').get()
            item['url'] = response.urljoin(
                sel.css('div.p-name a::attr(href)').get()
            )
            yield item

        # 翻页处理
        next_page = response.css('a.pn-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

#### 2.4 Settings 配置

```python
# settings.py

# 爬虫名称与robot协议
BOT_NAME = 'myspider'
ROBOTSTXT_OBEY = True

# 并发与延迟
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 请求头
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 开启 Pipeline
ITEM_PIPELINES = {
    'myspider.pipelines.ProductPipeline': 300,
    'myspider.pipelines.ImagePipeline': 400,
}

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Cookie 处理
COOKIES_ENABLED = False  # 大多数情况禁用

# Telnet 终端（调试用）
TELNETCONSOLE_ENABLED = False
```

---

### Part 3: 数据提取与 Selectors

#### 3.1 CSS 选择器 vs XPath

Scrapy 提供两种选择器：

```python
# CSS 选择器（更直观）
response.css('div.product-title::text').get()
response.css('ul.items li::text').getall()

# XPath（更强大）
response.xpath('//div[@class="product-title"]/text()').get()
response.xpath('//ul[@class="items"]/li/text()').getall()

# 混用场景
# 使用 XPath 获取父元素，再用 CSS 提取子元素
sel = response.xpath('//div[contains(@class, "product")]')
title = sel.css('.title::text').get()
```

#### 3.2 常用提取方法

```python
# 基本提取
response.css('title::text').get()           # 单个（返回字符串）
response.css('li::text').getall()           # 多个（返回列表）
response.css('li::text').getall(default='') # 带默认值

# 属性提取
response.css('img::attr(src)').get()        # 获取 src 属性
response.css('a::attr(href)').get()         # 获取 href 属性
response.css('div::attr(data-id)').get()    # 获取 data-id

# 正则结合
response.css('title::text').re(r'(\d+)')    # 正则匹配
response.css('title::text').re_first(r'(\d+)')  # 首个匹配

# 链式选择
response.css('.container').css('.product').css('.title::text').get()
```

#### 3.3 复杂数据提取示例

```python
def parse_product(self, response):
    """解析商品详情页"""
    item = ProductItem()

    # 多级嵌套提取
    item['title'] = response.css(
        'div.product-main h1::text'
    ).get(default='').strip()

    # 价格可能有多层（原价、促销价）
    item['price'] = (
        response.css('span.price-now::text').get() or
        response.css('span.price-original::text').get() or
        '未知'
    ).strip()

    # 批量提取规格
    specs = {}
    for row in response.css('table.specs tr'):
        key = row.css('th::text').get()
        value = row.css('td::text').get()
        if key and value:
            specs[key.strip()] = value.strip()
    item['specs'] = specs

    # 图片列表
    item['images'] = response.css(
        'div.thumbnails img::attr(data-src)'
    ).getall()

    yield item
```

#### 3.4 LinkExtractor 链接提取

```python
from scrapy.linkextractors import LinkExtractor

class PaginationSpider(scrapy.Spider):
    name = 'pagination'

    def __init__(self):
        # 定义列表页链接规则
        self.list_extractor = LinkExtractor(
            restrict_css='div.pagination a.page',
            restrict_xpaths='//div[@class="list"]'
        )
        # 定义详情页链接规则
        self.detail_extractor = LinkExtractor(
            restrict_css='a.product-link',
            allow=r'/product/\d+\.html'
        )

    def parse(self, response):
        # 提取详情页链接
        for link in self.detail_extractor.extract_links(response):
            yield response.follow(link, self.parse_detail)

        # 提取分页链接
        for link in self.list_extractor.extract_links(response):
            yield response.follow(link, self.parse)
```

---

### Part 4: Item 与 Pipeline

#### 4.1 Pipeline 处理链

Pipeline 特点：
- 按顺序执行，可中断
- 返回 Item 继续传递，返回 DropItem 丢弃
- 支持初始化和清理逻辑

```python
# pipelines.py
import itemadapter
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class PriceCleanPipeline:
    """价格清洗管道"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 清洗价格字段
        price = adapter.get('price')
        if price:
            # 提取数字部分
            import re
            cleaned = re.search(r'[\d.]+', str(price))
            if cleaned:
                adapter['price'] = float(cleaned.group())
            else:
                raise DropItem(f"无效价格: {price}")

        return item


class DuplicatesPipeline:
    """去重管道"""

    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        product_id = adapter.get('product_id')

        if product_id in self.seen:
            raise DropItem(f"重复商品: {product_id}")

        self.seen.add(product_id)
        return item


class MongoPipeline:
    """MongoDB 存储管道"""

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        import pymongo
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.db[adapter['product_id']] = dict(adapter)
        return item
```

#### 4.2 图片管道

```python
# pipelines.py
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline
from itemadapter import ItemAdapter

class ProductImagesPipeline(ImagesPipeline):
    """商品图片下载管道"""

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        image_urls = adapter.get('images', [])

        for url in image_urls:
            # 构建请求，自动下载
            yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)

        # 处理下载结果
        downloaded_images = []
        for ok, value in results:
            if ok:
                downloaded_images.append(value['path'])

        adapter['downloaded_images'] = downloaded_images
        return item

    # 自定义图片命名
    def file_path(self, request, response=None, info=None):
        item = info.context.get('item', {})
        product_id = item.get('product_id', 'unknown')

        # 从 URL 提取文件名
        from urllib.parse import urlparse, unquote
        parsed = urlparse(request.url)
        filename = unquote(parsed.path.split('/')[-1])

        return f'full/{product_id}/{filename}'
```

#### 4.3 Settings 中启用 Pipeline

```python
# settings.py

# 图片存储配置
IMAGES_STORE = 'images'  # 相对于项目根目录
IMAGES_THUMBS = {
    'small': (100, 100),
    'medium': (300, 300),
}
IMAGES_EXPIRES = 90  # 过期天数

# Pipeline 执行顺序（数字越小越先执行）
ITEM_PIPELINES = {
    'myspider.pipelines.PriceCleanPipeline': 100,
    'myspider.pipelines.DuplicatesPipeline': 200,
    'myspider.pipelines.ProductImagesPipeline': 300,
    'myspider.pipelines.MongoPipeline': 400,
}
```

---

### Part 5: 反爬应对与中间件

#### 5.1 UA 轮换中间件

```python
# middlewares.py
import random

class RandomUserAgentMiddleware:
    """随机 User-Agent 中间件"""

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            # 添加更多 UA...
        ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


class RotateProxyMiddleware:
    """代理轮换中间件"""

    def __init__(self, proxy_list):
        self.proxies = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_list=crawler.settings.getlist('PROXY_LIST')
        )

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = f'http://{proxy}'
```

#### 5.2 代理池配置

```python
# settings.py

# 代理列表
PROXY_LIST = [
    'user:pass@proxy1.example.com:8080',
    'proxy2.example.com:8080',
]

DOWNLOADER_MIDDLEWARES = {
    'myspider.middlewares.RandomUserAgentMiddleware': 400,
    'myspider.middlewares.RotateProxyMiddleware': 410,
}
```

#### 5.3 Cookie 与 Session

```python
# settings.py
# 大多数网站不需要 Cookie（可能反而被追踪）
COOKIES_ENABLED = False

# 需要登录的网站
COOKIES_ENABLED = True
COOKIES_DEBUG = True  # 调试日志

# 自定义 Cookie 中间件
class CookiesMiddleware:
    """固定 Cookie 中间件"""

    def process_request(self, request, spider):
        request.cookies = {
            'session_id': 'xxx',
            'user_token': 'yyy',
        }
```

#### 5.4 限速与爬取模式

```python
# settings.py

# 自动限速（根据响应时间自动调整）
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# 禁用 DNS 缓存（每次重新解析）
DNS_TIMEOUT = 60

# 连接池大小
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
```

#### 5.5 登录与 Session 维护

```python
class LoginSpider(scrapy.Spider):
    name = 'login_spider'

    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def start_requests(self):
        """先登录再爬取"""
        # 方式1：FormRequest
        yield scrapy.FormRequest(
            url='https://example.com/login',
            formdata={'username': self.username, 'password': self.password},
            callback=self.after_login
        )

    def after_login(self, response):
        """登录后回调"""
        if '登录成功' in response.text:
            # 登录成功，开始爬取
            yield scrapy.Request('https://example.com/data', self.parse_data)
        else:
            self.logger.error('登录失败')

    def parse_data(self, response):
        # 解析数据...
        pass
```

---

### Part 6: 高级特性

#### 6.1 分布式爬取（Crawlab/Splash）

```python
# settings.py
# 对接 Crawlab
CRAWLAB_API_URL = 'http://localhost:8080/api/job'

# Splash 渲染
SPLASH_URL = 'http://localhost:8050'

# Splash 中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
}
```

#### 6.2 增量爬取

```python
class IncrementalSpider(scrapy.Spider):
    name = 'incremental'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 加载已爬取记录
        self.crawled_ids = self.load_crawled()

    def load_crawled(self):
        try:
            with open('crawled.json') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    def parse(self, response):
        for item in self.extract_items(response):
            if item['id'] not in self.crawled_ids:
                self.crawled_ids.add(item['id'])
                yield item

        # 保存已爬取记录
        with open('crawled.json', 'w') as f:
            json.dump(list(self.crawled_ids), f)
```

---

## 📝 练习题

### 练习 3.1：Scrapy 基础爬虫

```markdown
目标：使用 Scrapy 爬取豆瓣电影 Top250
难度：⭐⭐⭐
提示：
- 翻页处理（URL 参数变化）
- 列表提取与详情页解析
- Item 定义与 Pipeline
```

### 练习 3.2：完整数据管道

```markdown
目标：爬取电商商品数据，存储到 MongoDB
难度：⭐⭐⭐⭐
提示：
- Item 数据清洗
- 图片下载
- MongoDB 存储
```

### 练习 3.3：反爬应对

```markdown
目标：爬取有反爬机制的网站
难度：⭐⭐⭐⭐
要求：
- UA 轮换
- 代理池
- 限速控制
```

---

## 📚 扩展阅读

- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Scrapy 最佳实践](https://docs.scrapy.org/en/latest/topics/practices.html)
- [Crawlab 分布式爬虫管理](https://crawlab.cn/)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 理解 Scrapy 异步架构与 Twisted 原理
- [ ] 创建完整的 Scrapy 项目
- [ ] 编写 Spider 解析网页
- [ ] 使用 Item Pipeline 处理数据
- [ ] 配置中间件应对反爬
- [ ] 实现增量爬取

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S04: 自动化抓包 — Selenium 与 Playwright](../S04-selenium-playwright/) — 浏览器自动化测试

---
