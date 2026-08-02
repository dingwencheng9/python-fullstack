# S09: 爬虫综合项目

> **课程编号**: S09
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 8 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: S01-S08 全部课程

---

## 📚 课程概述

本课程是 Stage P 的收官之作，通过一个完整的商业级爬虫系统项目，整合前端抓取、JavaScript 逆向、App 逆向和分布式爬取等全部技术栈。项目涵盖需求分析、架构设计、工程实现和数据治理的完整流程。

---

## 🎯 学习目标

1. 设计可扩展的分布式爬虫架构
2. 实现多数据源的综合抓取方案
3. 构建完整的数据清洗与存储管道
4. 实现爬虫监控与告警系统
5. 完成项目文档与部署上线
6. 掌握生产环境爬虫最佳实践

---

## 📋 课程大纲

- [Part 1: 项目需求与架构设计](#part-1-项目需求与架构设计)
- [Part 2: 网页爬虫实现](#part-2-网页爬虫实现)
- [Part 3: App 爬虫实现](#part-3-app-爬虫实现)
- [Part 4: 数据管道与存储](#part-4-数据管道与存储)
- [Part 5: 监控与运维](#part-5-监控与运维)
- [Part 6: 项目部署](#part-6-项目部署)

---

## 🔧 环境准备

```bash
# 创建项目
cd stageS-web-scraping/lessons/S09-scraping-project
uv venv && source .venv/bin/activate

# 核心依赖
uv add scrapy selenium playwright
uv add pyexecjs py-mini-racer
uv add frida-tools objection
uv add redis celery flower
uv add sqlalchemy pymongo redis
uv add httpx aiohttp playwright
uv add prometheus-client
uv add schedule APScheduler

# 辅助工具
uv add python-dotenv
uv add loguru
uv add pydantic

# Android 工具（可选）
# adb, apktool, jadx
```

---

## 📖 详细内容

### Part 1: 项目需求与架构设计

#### 1.1 需求分析

```markdown
# 项目背景
某电商数据分析平台需要整合多个数据源：
1. 竞品商品信息（网页爬取）
2. 用户评论数据（App 数据）
3. 价格历史趋势（API 逆向）

# 功能需求
- 实时监控竞品价格变动
- 自动采集用户评论和评分
- 存储历史数据进行趋势分析
- 提供数据查询 API

# 非功能需求
- 日均抓取量：100万+ 页面
- 数据延迟：< 5分钟
- 可用性：99.9%
- 支持横向扩展
```

#### 1.2 系统架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                        数据采集层                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Web Spider │  │ App Spider  │  │ API Crawler │              │
│  │   (Scrapy) │  │  (Frida)    │  │  (逆向)     │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────┐            │
│  │              消息队列 (Redis/RedisQueue)          │            │
│  └─────────────────────────────────────────────────┘            │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                        数据处理层                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  数据清洗   │  │  数据去重   │  │  数据转换   │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────┐            │
│  │              处理管道 (Celery/Pipeline)            │            │
│  └─────────────────────────────────────────────────┘            │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                        数据存储层                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ PostgreSQL  │  │   MongoDB   │  │    Redis    │              │
│  │ (结构化)    │  │ (非结构化)  │  │ (缓存/队列) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────────┐
│                        监控层                                      │
├──────────────────────────┼────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Prometheus  │  │   Grafana   │  │   Flower    │              │
│  │  (指标)     │  │  (可视化)   │  │  (任务监控) │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

#### 1.3 项目目录结构

```
ecommerce_scraper/
├── config/
│   ├── __init__.py
│   ├── settings.py          # 基础配置
│   ├── spiders.py           # 爬虫配置
│   └── database.py          # 数据库配置
├── spiders/
│   ├── __init__.py
│   ├── base.py              # 爬虫基类
│   ├── web/                 # 网页爬虫
│   │   ├── __init__.py
│   │   ├── product_spider.py
│   │   └── comment_spider.py
│   ├── app/                 # App 爬虫
│   │   ├── __init__.py
│   │   ├── frida_scripts/
│   │   └── app_spider.py
│   └── api/                # API 爬虫
│       ├── __init__.py
│       ├── crypto_utils.py
│       └── api_spider.py
├── pipelines/
│   ├── __init__.py
│   ├── cleaners.py          # 数据清洗
│   ├── deduplicator.py      # 去重
│   └── validators.py        # 验证
├── storage/
│   ├── __init__.py
│   ├── postgres_repo.py     # PG 存储
│   └── mongo_repo.py       # Mongo 存储
├── workers/
│   ├── __init__.py
│   ├── celery_app.py       # Celery 配置
│   └── tasks.py            # 异步任务
├── monitoring/
│   ├── __init__.py
│   ├── metrics.py          # 指标收集
│   └── alerts.py           # 告警
├── scripts/
│   ├── run_spider.py
│   ├── init_db.py
│   └── benchmark.py
├── tests/
│   ├── __init__.py
│   ├── test_spiders.py
│   ├── test_pipelines.py
│   └── test_integration.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

### Part 2: 网页爬虫实现

#### 2.1 Scrapy 爬虫基类

```python
# spiders/base.py
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from loguru import logger
import hashlib
from datetime import datetime

class BaseProductSpider(scrapy.Spider):
    """商品爬虫基类"""

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'DOWNLOAD_TIMEOUT': 30,
        'RETRY_TIMES': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_count = 0
        self.error_count = 0
        self.start_time = datetime.now()

    @property
    def spider_id(self) -> str:
        """生成爬虫唯一标识"""
        return hashlib.md5(
            f"{self.name}:{self.start_time.isoformat()}".encode()
        ).hexdigest()[:8]

    def generate_item_id(self, *parts) -> str:
        """生成 Item ID"""
        raw = ":".join(str(p) for p in parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def get_source(self) -> dict:
        """获取数据源信息"""
        return {
            "spider": self.name,
            "spider_id": self.spider_id,
            "crawled_at": datetime.now().isoformat(),
        }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """创建爬虫实例"""
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        logger.info(f"[{self.name}] 爬虫启动, ID: {self.spider_id}")

    def spider_closed(self, spider, reason):
        duration = (datetime.now() - self.start_time).total_seconds()
        logger.info(
            f"[{self.name}] 爬虫关闭, 原因: {reason}, "
            f"处理: {self.processed_count}, 错误: {self.error_count}, "
            f"耗时: {duration:.1f}s"
        )
```

#### 2.2 商品详情爬虫

```python
# spiders/web/product_spider.py
import scrapy
from scrapy.http import Response
from typing import Iterator
from ..base import BaseProductSpider
from pipelines.items import ProductItem, CommentItem

class JDProductSpider(BaseProductSpider):
    """京东商品爬虫"""

    name = "jd_product"
    allowed_domains = ["jd.com", "3.cn"]

    def __init__(self, keywords: list[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keywords = keywords or ["手机", "电脑"]

    def start_requests(self) -> Iterator[scrapy.Request]:
        """生成初始请求"""
        for keyword in self.keywords:
            url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8"
            yield scrapy.Request(
                url,
                callback=self.parse_list,
                meta={"keyword": keyword, "page": 1}
            )

    def parse_list(self, response: Response) -> Iterator:
        """解析商品列表页"""
        keyword = response.meta["keyword"]
        page = response.meta["page"]

        # 提取商品链接
        selectors = response.css("div.gl-warp > div.gl-item")
        self.logger.info(f"解析 {keyword} 第 {page} 页，找到 {len(selectors)} 个商品")

        for sel in selectors:
            item = ProductItem()
            item.update(self.get_source())

            item["product_id"] = sel.css("::attr(data-sku)").get()
            item["keyword"] = keyword
            item["page"] = page

            # 提取基本信息
            item["title"] = " ".join(
                sel.css("div.p-name em::text").getall()
            ).strip()

            # 价格（可能有多个）
            priceSelectors = sel.css("div.p-price i::text").getall()
            item["prices"] = [p.strip() for p in priceSelectors]
            item["current_price"] = priceSelectors[0] if priceSelectors else None

            # 店铺信息
            shop_elem = sel.css("div.p-shop a::attr(title)").get()
            item["shop_name"] = shop_elem.strip() if shop_elem else None
            item["shop_id"] = sel.css("div.p-shop a::attr(data-vid)").get()

            # 商品链接
            detail_url = sel.css("div.p-name a::attr(href)").get()
            item["detail_url"] = response.urljoin(detail_url)

            self.processed_count += 1
            yield item

            # 跟进详情页
            yield response.follow(
                detail_url,
                self.parse_detail,
                meta={"item": item}
            )

        # 翻页（最多10页）
        if page < 10:
            next_page = page + 1
            next_url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8&page={next_page}"
            yield response.follow(
                next_url,
                self.parse_list,
                meta={"keyword": keyword, "page": next_page}
            )

    def parse_detail(self, response: Response) -> Iterator:
        """解析商品详情页"""
        item = response.meta["item"]

        # 商品 ID
        item["jd_id"] = response.css("::attr(data-id)").get()

        # 类别
        breadcrumb = response.css("div.breadcrumb li a::text").getall()
        item["category"] = [c.strip() for c in breadcrumb]

        # 评分
        item["score"] = response.css("div.comment-con::text").get()

        # 销量（如果有）
        sale_elem = response.css("strong#J_TiGoodsSaleCount::text").get()
        if sale_elem:
            item["sales"] = self._parse_number(sale_elem)

        yield item

    @staticmethod
    def _parse_number(text: str) -> int:
        """解析数字"""
        import re
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0
```

#### 2.3 评论爬虫

```python
# spiders/web/comment_spider.py
import scrapy
from typing import Iterator
from ..base import BaseProductSpider
from pipelines.items import CommentItem

class CommentSpider(BaseProductSpider):
    """商品评论爬虫"""

    name = "product_comment"
    allowed_domains = ["jd.com"]

    def __init__(self, product_ids: list[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_ids = product_ids or []

    def start_requests(self) -> Iterator[scrapy.Request]:
        """生成初始请求"""
        for product_id in self.product_ids:
            # 京东评论 API
            url = f"https://sclub.jd.com/comment/productPageComments.action"
            params = {
                "productId": product_id,
                "score": 0,
                "sortType": 5,  # 推荐排序
                "page": 0,
                "pageSize": 10,
            }
            yield scrapy.FormRequest(
                url,
                formdata=params,
                callback=self.parse_comments,
                meta={"product_id": product_id, "page": 0}
            )

    def parse_comments(self, response) -> Iterator:
        """解析评论"""
        import json

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error(f"JSON 解析失败: {response.url}")
            self.error_count += 1
            return

        product_id = response.meta["product_id"]
        page = response.meta["page"]

        comments = data.get("comments", [])
        self.logger.info(f"商品 {product_id} 第 {page} 页，找到 {len(comments)} 条评论")

        for comment_data in comments:
            item = CommentItem()
            item.update(self.get_source())

            item["comment_id"] = comment_data.get("id")
            item["product_id"] = product_id
            item["user_id"] = comment_data.get("id")
            item["user_name"] = comment_data.get("nickname")
            item["content"] = comment_data.get("content")
            item["score"] = comment_data.get("score")
            item["create_time"] = comment_data.get("creationTime")
            item["like_count"] = comment_data.get("usefulVoteCount", 0)
            item["reply_count"] = comment_data.get("replyCount", 0)

            # 追评
            if comment_data.get("afterContent"):
                item["after_comment"] = comment_data["afterContent"]

            self.processed_count += 1
            yield item

        # 翻页
        max_page = data.get("maxPage", 0)
        if page < min(max_page, 100):  # 最多抓取 100 页
            next_params = {
                "productId": product_id,
                "score": 0,
                "sortType": 5,
                "page": page + 1,
                "pageSize": 10,
            }
            yield scrapy.FormRequest(
                "https://sclub.jd.com/comment/productPageComments.action",
                formdata=next_params,
                callback=self.parse_comments,
                meta={"product_id": product_id, "page": page + 1}
            )
```

---

### Part 3: App 爬虫实现

#### 3.1 Frida Hook 管理器

```python
# spiders/app/frida_manager.py
import frida
import time
import json
from typing import Callable, Optional
from dataclasses import dataclass, field
from loguru import logger

@dataclass
class HookConfig:
    """Hook 配置"""
    package_name: str
    script_path: str
    on_message: Optional[Callable] = None
    rpc_exports: dict = field(default_factory=dict)

class FridaHookManager:
    """Frida Hook 管理器"""

    def __init__(self):
        self.device = frida.get_usb_device(timeout=10000)
        self.sessions = {}
        self.scripts = {}
        self.results = {}

    def start_hook(self, config: HookConfig) -> str:
        """启动 Hook"""
        logger.info(f"启动 Hook: {config.package_name}")

        try:
            # 启动应用
            pid = self.device.spawn([config.package_name])

            # 附加到进程
            session = self.device.attach(pid)
            self.sessions[config.package_name] = session

            # 加载脚本
            with open(config.script_path, 'r') as f:
                script_code = f.read()

            script = session.create_script(script_code)

            # 消息回调
            def on_message(msg, data):
                if config.on_message:
                    config.on_message(msg, data)
                elif msg['type'] == 'send':
                    logger.debug(f"[Frida] {msg['payload']}")

            script.on('message', on_message)
            script.load()

            self.scripts[config.package_name] = script

            # 恢复应用
            self.device.resume(pid)

            logger.info(f"Hook 启动成功: {config.package_name}, PID: {pid}")
            return pid

        except Exception as e:
            logger.error(f"Hook 启动失败: {e}")
            raise

    def call_rpc(self, package_name: str, method: str, *args) -> any:
        """调用 RPC 方法"""
        if package_name not in self.scripts:
            raise ValueError(f"Hook 未启动: {package_name}")

        script = self.scripts[package_name]

        # 检查导出方法
        if not hasattr(script.exports, method):
            raise AttributeError(f"RPC 方法不存在: {method}")

        rpc_method = getattr(script.exports, method)
        return rpc_method(*args)

    def stop_hook(self, package_name: str):
        """停止 Hook"""
        if package_name in self.sessions:
            session = self.sessions[package_name]
            session.detach()
            del self.sessions[package_name]
            del self.scripts[package_name]
            logger.info(f"Hook 已停止: {package_name}")

    def stop_all(self):
        """停止所有 Hook"""
        for package_name in list(self.sessions.keys()):
            self.stop_hook(package_name)
```

#### 3.2 App 数据爬虫

```python
# spiders/app/app_spider.py
import json
import time
from typing import Iterator, Dict, Any
from ..base import BaseProductSpider
from .frida_manager import FridaHookManager, HookConfig
from pipelines.items import AppProductItem, AppCommentItem

class AppProductSpider(BaseProductSpider):
    """App 商品数据爬虫"""

    name = "app_product"

    def __init__(self, package_name: str, keywords: list[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package_name = package_name
        self.keywords = keywords or []
        self.frida_manager = FridaHookManager()
        self.pending_products = []

    def start_requests(self) -> Iterator:
        """启动 Hook 并初始化"""
        # 定义消息回调
        def on_message(msg, data):
            if msg['type'] == 'send':
                payload = msg['payload']
                if isinstance(payload, dict):
                    self._handle_frida_message(payload)

        # 启动 Frida Hook
        config = HookConfig(
            package_name=self.package_name,
            script_path="spiders/app/frida_scripts/product_hook.js",
            on_message=on_message,
            rpc_exports={
                "getSearchResult": self._get_search_result,
                "getProductDetail": self._get_product_detail,
            }
        )

        try:
            self.frida_manager.start_hook(config)
            self.logger.info("Frida Hook 启动成功")

            # 等待应用加载
            time.sleep(3)

            # 触发搜索
            for keyword in self.keywords:
                self._trigger_search(keyword)
                time.sleep(2)  # 等待数据加载

        except Exception as e:
            self.logger.error(f"启动失败: {e}")
            raise

    def _trigger_search(self, keyword: str):
        """触发搜索"""
        try:
            # 通过 RPC 调用搜索
            result = self.frida_manager.call_rpc(
                self.package_name,
                "triggerSearch",
                keyword
            )
            self.logger.info(f"触发搜索: {keyword}")
        except Exception as e:
            self.logger.error(f"触发搜索失败: {e}")

    def _handle_frida_message(self, payload: Dict[str, Any]):
        """处理 Frida 消息"""
        msg_type = payload.get("type")

        if msg_type == "product":
            item = AppProductItem()
            item.update(self.get_source())
            item.update(payload.get("data", {}))
            self.processed_count += 1
            self.pending_products.append(item)

        elif msg_type == "comment":
            item = AppCommentItem()
            item.update(self.get_source())
            item.update(payload.get("data", {}))
            self.processed_count += 1
            yield item

        elif msg_type == "network":
            self.logger.debug(f"Network: {payload.get('url')}")

    def parse(self, response) -> Iterator:
        """解析（由 Frida 消息触发）"""
        # App 爬虫通过 Frida 获取数据
        # 这里处理从 pending_products 中提取的数据
        while self.pending_products:
            item = self.pending_products.pop(0)
            yield item

    def closed(self, reason):
        """清理资源"""
        self.frida_manager.stop_all()
        super().closed(reason)
```

#### 3.3 通用 Hook 脚本

```javascript
// spiders/app/frida_scripts/product_hook.js

// 全局数据存储
var productCache = [];
var commentCache = [];
var networkLogs = [];

// ==================== Hook 配置 ====================

Java.perform(function() {

    // ==================== 网络拦截 ====================

    // OkHttp3 拦截
    try {
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        OkHttpClient.newCall.implementation = function(request) {
            var url = request.url().toString();

            // 记录网络请求
            send({
                type: "network",
                url: url,
                method: request.method(),
                timestamp: Date.now()
            });

            // 如果是数据接口，拦截响应
            if (url.includes("/api/") || url.includes("/v2/")) {
                // 拦截逻辑
                networkLogs.push({url: url, request: request});
            }

            return this.newCall(request);
        };
    } catch (e) {
        console.log("OkHttp3 hook failed: " + e);
    }

    // ==================== 数据解析 ====================

    // 搜索结果解析
    var SearchResultParser = Java.use("com.example.app.data.SearchResultParser");
    SearchResultParser.parse.implementation = function(json) {
        console.log("[*] SearchResultParser.parse called");
        console.log("[*] JSON length: " + json.length);

        // 解析并提取数据
        try {
            var result = JSON.parse(json);
            if (result.data && result.data.products) {
                result.data.products.forEach(function(product) {
                    send({
                        type: "product",
                        data: {
                            product_id: product.id,
                            title: product.title,
                            price: product.price,
                            sales: product.sales,
                            shop_name: product.shopName
                        }
                    });
                    productCache.push(product);
                });
            }
        } catch (e) {
            console.log("[!] Parse error: " + e);
        }

        return this.parse(json);
    };

    // ==================== 加密函数追踪 ====================

    // 签名生成追踪
    var SignUtil = Java.use("com.example.app.utils.SignUtil");
    SignUtil.getSign.overload("java.util.Map").implementation = function(map) {
        console.log("[*] SignUtil.getSign called");

        // 记录参数
        var entries = map.entrySet().toArray();
        var params = {};
        entries.forEach(function(entry) {
            params[entry.getKey()] = entry.getValue();
        });

        console.log("[*] Sign params: " + JSON.stringify(params));

        // 调用原始方法
        var result = this.getSign(map);
        console.log("[*] Sign result: " + result);

        send({
            type: "sign",
            params: params,
            result: result
        });

        return result;
    };

    // ==================== RPC 导出 ====================

    rpc.exports = {
        triggerSearch: function(keyword) {
            // 触发搜索
            Java.perform(function() {
                var SearchActivity = Java.use("com.example.app.SearchActivity");
                var instance = SearchActivity.$new();
                instance.search(keyword);
            });
        },

        getSearchResult: function() {
            return JSON.stringify(productCache);
        },

        getProductDetail: function(productId) {
            // 获取商品详情
            var product = null;
            productCache.forEach(function(p) {
                if (p.id == productId) {
                    product = p;
                }
            });
            return product ? JSON.stringify(product) : null;
        },

        getNetworkLogs: function() {
            return JSON.stringify(networkLogs);
        }
    };

    console.log("[*] Frida script loaded");
});
```

---

### Part 4: 数据管道与存储

#### 4.1 数据清洗管道

```python
# pipelines/cleaners.py
import re
from typing import Any, Optional
from dataclasses import dataclass
from loguru import logger

@dataclass
class CleaningResult:
    """清洗结果"""
    success: bool
    cleaned_value: Any
    original_value: Any
    error: Optional[str] = None

def clean_price(text: Optional[str]) -> CleaningResult:
    """清洗价格"""
    if not text:
        return CleaningResult(False, None, text, "空值")

    try:
        # 提取数字部分
        cleaned = re.search(r"[\d.]+", str(text).replace(",", ""))
        if cleaned:
            price = float(cleaned.group())
            return CleaningResult(True, price, text)
        return CleaningResult(False, None, text, "无法解析价格")
    except Exception as e:
        return CleaningResult(False, None, text, str(e))

def clean_text(text: Optional[str]) -> CleaningResult:
    """清洗文本"""
    if not text:
        return CleaningResult(False, "", text, "空值")

    try:
        # 移除多余空白
        cleaned = " ".join(str(text).split())
        # 移除特殊字符（可选）
        # cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)
        return CleaningResult(True, cleaned, text)
    except Exception as e:
        return CleaningResult(False, text, text, str(e))

def clean_url(url: Optional[str]) -> CleaningResult:
    """清洗 URL"""
    if not url:
        return CleaningResult(False, None, url, "空值")

    try:
        # 基本验证
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return CleaningResult(True, url, url)
    except Exception as e:
        return CleaningResult(False, None, url, str(e))

def clean_phone(phone: Optional[str]) -> Optional[str]:
    """清洗手机号"""
    if not phone:
        return None

    # 提取纯数字
    digits = re.sub(r"\D", "", str(phone))

    # 验证长度（中国手机号 11 位）
    if len(digits) == 11:
        return digits
    return None

class DataCleaner:
    """数据清洗器"""

    def __init__(self):
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
        }

    def clean_product(self, product: dict) -> dict:
        """清洗商品数据"""
        self.stats["total"] += 1

        cleaned = product.copy()

        # 清洗价格
        if "price" in cleaned:
            result = clean_price(cleaned["price"])
            if result.success:
                cleaned["price"] = result.cleaned_value
                self.stats["success"] += 1
            else:
                logger.warning(f"价格清洗失败: {result.error}")
                self.stats["failed"] += 1

        # 清洗标题
        if "title" in cleaned:
            result = clean_text(cleaned["title"])
            cleaned["title"] = result.cleaned_value

        # 清洗 URL
        if "url" in cleaned:
            result = clean_url(cleaned["url"])
            cleaned["url"] = result.cleaned_value

        # 清洗店铺名
        if "shop_name" in cleaned:
            result = clean_text(cleaned["shop_name"])
            cleaned["shop_name"] = result.cleaned_value

        return cleaned
```

#### 4.2 去重管道

```python
# pipelines/deduplicator.py
import hashlib
import json
from typing import Any, Dict, Optional
from collections import defaultdict

class DataDeduplicator:
    """数据去重器"""

    def __init__(self, key_fields: list[str] = None):
        """
        初始化去重器

        Args:
            key_fields: 用于生成唯一 key 的字段列表
        """
        self.key_fields = key_fields or ["id", "product_id", "comment_id"]
        self.seen_keys: set = set()
        self.duplicate_count = 0

    def generate_key(self, item: Dict[str, Any]) -> Optional[str]:
        """生成唯一 key"""
        parts = []

        for field in self.key_fields:
            value = item.get(field)
            if value:
                parts.append(str(value))

        if not parts:
            return None

        # 生成 hash
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()

    def is_duplicate(self, item: Dict[str, Any]) -> bool:
        """检查是否重复"""
        key = self.generate_key(item)

        if not key:
            return False

        if key in self.seen_keys:
            self.duplicate_count += 1
            return True

        self.seen_keys.add(key)
        return False

    def reset(self):
        """重置去重状态"""
        self.seen_keys.clear()
        self.duplicate_count = 0

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "unique_count": len(self.seen_keys),
            "duplicate_count": self.duplicate_count,
        }


class BloomFilterDeduplicator:
    """布隆过滤器去重（内存优化版）"""

    def __init__(self, expected_items: int = 1000000, false_positive_rate: float = 0.01):
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate
        self.seen: set = set()  # 简化为 set，生产环境用 bloom-filter

        # 计算合适的 set 大小
        # 实际使用 bloom-filter 库更优
        self.max_size = int(expected_items * 1.2)
        self.duplicate_count = 0

    def is_duplicate(self, item: Dict[str, Any]) -> bool:
        """检查是否重复（可能误判）"""
        # 使用多字段组合 hash
        key = self._make_key(item)

        if key in self.seen:
            self.duplicate_count += 1
            return True

        # 限制 set 大小（淘汰旧数据）
        if len(self.seen) >= self.max_size:
            # 清除一半旧数据
            self.seen = set(list(self.seen)[self.max_size // 2:])

        self.seen.add(key)
        return False

    def _make_key(self, item: Dict[str, Any]) -> str:
        """生成 key"""
        parts = []
        for key in sorted(item.keys()):
            value = item.get(key)
            if value is not None:
                parts.append(f"{key}={value}")
        return hashlib.md5("|".join(parts).encode()).hexdigest()
```

#### 4.3 数据存储

```python
# storage/mongo_repo.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from loguru import logger
import json

class MongoRepository:
    """MongoDB 仓储"""

    def __init__(self, connection_string: str, database: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[database]

        # 初始化索引
        self._ensure_indexes()

    def _ensure_indexes(self):
        """确保索引存在"""
        # 商品集合
        products = self.db["products"]
        products.create_index([("product_id", ASCENDING)], unique=True)
        products.create_index([("source", ASCENDING), ("crawled_at", DESCENDING)])
        products.create_index([("category", ASCENDING)])

        # 评论集合
        comments = self.db["comments"]
        comments.create_index([("comment_id", ASCENDING)], unique=True)
        comments.create_index([("product_id", ASCENDING), ("crawled_at", DESCENDING)])

        # 价格历史集合
        price_history = self.db["price_history"]
        price_history.create_index([
            ("product_id", ASCENDING),
            ("crawled_at", DESCENDING)
        ], unique=True)

    def insert_product(self, product: Dict[str, Any]) -> bool:
        """插入商品"""
        try:
            product["updated_at"] = datetime.now()
            self.db["products"].update_one(
                {"product_id": product["product_id"]},
                {"$set": product, "$setOnInsert": {"created_at": datetime.now()}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"插入商品失败: {e}")
            return False

    def insert_comment(self, comment: Dict[str, Any]) -> bool:
        """插入评论"""
        try:
            comment["updated_at"] = datetime.now()
            self.db["comments"].update_one(
                {"comment_id": comment["comment_id"]},
                {"$set": comment, "$setOnInsert": {"created_at": datetime.now()}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"插入评论失败: {e}")
            return False

    def batch_insert(self, collection: str, items: List[Dict[str, Any]]) -> int:
        """批量插入"""
        if not items:
            return 0

        try:
            result = self.db[collection].insert_many(items, ordered=False)
            return len(result.inserted_ids)
        except Exception as e:
            logger.error(f"批量插入失败: {e}")
            return 0

    def get_products_by_keyword(self, keyword: str, limit: int = 100) -> List[Dict]:
        """按关键词搜索商品"""
        cursor = self.db["products"].find(
            {"title": {"$regex": keyword}}
        ).sort("crawled_at", DESCENDING).limit(limit)

        return list(cursor)

    def get_price_trend(self, product_id: str, days: int = 30) -> List[Dict]:
        """获取价格趋势"""
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=days)

        cursor = self.db["price_history"].find({
            "product_id": product_id,
            "crawled_at": {"$gte": start_date}
        }).sort("crawled_at", ASCENDING)

        return list(cursor)

    def close(self):
        """关闭连接"""
        self.client.close()
```

---

### Part 5: 监控与运维

#### 5.1 指标收集

```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from typing import Optional
from datetime import datetime

# 创建注册表
REGISTRY = CollectorRegistry()

# 爬虫指标
spider_requests_total = Counter(
    "spider_requests_total",
    "Total number of requests",
    ["spider_name", "status"],
    registry=REGISTRY
)

spider_items_total = Counter(
    "spider_items_total",
    "Total number of items scraped",
    ["spider_name", "item_type"],
    registry=REGISTRY
)

spider_duration_seconds = Histogram(
    "spider_duration_seconds",
    "Spider execution duration",
    ["spider_name"],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600],
    registry=REGISTRY
)

# 活跃爬虫数
active_spiders = Gauge(
    "active_spiders",
    "Number of active spiders",
    registry=REGISTRY
)

# 数据质量指标
data_quality_errors = Counter(
    "data_quality_errors_total",
    "Data quality errors",
    ["spider_name", "error_type"],
    registry=REGISTRY
)

# 去重统计
duplicates_detected = Counter(
    "duplicates_detected_total",
    "Number of duplicates detected",
    ["spider_name"],
    registry=REGISTRY
)


class MetricsCollector:
    """指标收集器"""

    def __init__(self, spider_name: str):
        self.spider_name = spider_name
        self.start_time: Optional[datetime] = None

    def start(self):
        """开始计时"""
        self.start_time = datetime.now()
        active_spiders.inc()

    def end(self):
        """结束计时"""
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            spider_duration_seconds.labels(spider_name=self.spider_name).observe(duration)
            active_spiders.dec()

    def record_request(self, status: str = "success"):
        """记录请求"""
        spider_requests_total.labels(
            spider_name=self.spider_name,
            status=status
        ).inc()

    def record_item(self, item_type: str):
        """记录抓取项"""
        spider_items_total.labels(
            spider_name=self.spider_name,
            item_type=item_type
        ).inc()

    def record_error(self, error_type: str):
        """记录错误"""
        data_quality_errors.labels(
            spider_name=self.spider_name,
            error_type=error_type
        ).inc()

    def record_duplicate(self):
        """记录重复"""
        duplicates_detected.labels(spider_name=self.spider_name).inc()

    @staticmethod
    def get_metrics() -> bytes:
        """获取所有指标"""
        return generate_latest(REGISTRY)
```

#### 5.2 告警系统

```python
# monitoring/alerts.py
import httpx
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

@dataclass
class Alert:
    """告警"""
    level: str  # critical, warning, info
    title: str
    message: str
    metadata: Dict[str, Any]
    timestamp: datetime

class AlertManager:
    """告警管理器"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.alerts: list[Alert] = []
        self.level_thresholds = {
            "error_rate": 0.1,      # 错误率超过 10%
            "response_time": 30,    # 响应时间超过 30 秒
            "items_per_minute": 10, # 每分钟抓取少于 10 条
        }

    async def send_alert(self, alert: Alert):
        """发送告警"""
        self.alerts.append(alert)

        if self.webhook_url:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        self.webhook_url,
                        json={
                            "level": alert.level,
                            "title": alert.title,
                            "message": alert.message,
                            "metadata": alert.metadata,
                            "timestamp": alert.timestamp.isoformat(),
                        }
                    )
            except Exception as e:
                logger.error(f"发送告警失败: {e}")

        # 记录日志
        logger.warning(f"[{alert.level.upper()}] {alert.title}: {alert.message}")

    async def check_error_rate(self, spider_name: str, error_count: int, total_count: int):
        """检查错误率"""
        if total_count == 0:
            return

        error_rate = error_count / total_count
        threshold = self.level_thresholds["error_rate"]

        if error_rate > threshold:
            await self.send_alert(Alert(
                level="warning",
                title=f"{spider_name} 错误率过高",
                message=f"错误率 {error_rate:.2%} 超过阈值 {threshold:.2%}",
                metadata={
                    "spider": spider_name,
                    "error_rate": error_rate,
                    "threshold": threshold,
                    "error_count": error_count,
                    "total_count": total_count,
                },
                timestamp=datetime.now()
            ))

    async def check_slow_spider(self, spider_name: str, duration: float):
        """检查慢爬虫"""
        threshold = self.level_thresholds["response_time"]

        if duration > threshold:
            await self.send_alert(Alert(
                level="info",
                title=f"{spider_name} 执行缓慢",
                message=f"执行时间 {duration:.1f}s 超过阈值 {threshold}s",
                metadata={
                    "spider": spider_name,
                    "duration": duration,
                    "threshold": threshold,
                },
                timestamp=datetime.now()
            ))
```

---

### Part 6: 项目部署

#### 6.1 Docker 配置

```dockerfile
# docker/Dockerfile
FROM python:3.13-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Chrome (用于 Selenium)
RUN curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    -o /tmp/chrome.deb \
    && dpkg -i /tmp/chrome.deb \
    || apt-get install -f -y \
    && rm /tmp/chrome.deb

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 crawler && chown -R crawler:crawler /app
USER crawler

# 环境变量
ENV PYTHONUNBUFFERED=1
ENV SCRAPY_SETTINGS_MODULE=config.settings

# 默认命令
CMD ["python", "-m", "scrapy", "crawl", "jd_product"]
```

#### 6.2 Docker Compose

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  # Scrapy 爬虫
  scrapy-worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    volumes:
      - ../data:/app/data
      - ../logs:/app/logs
    environment:
      - REDIS_URL=redis://redis:6379
      - MONGODB_URI=mongodb://mongo:27017
      - PROMETHEUS_PORT=9090
    depends_on:
      - redis
      - mongo
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

  # MongoDB
  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

  # Celery Worker
  celery-worker:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A workers.celery_app worker --loglevel=info --concurrency=4
    volumes:
      - ../data:/app/data
    environment:
      - REDIS_URL=redis://redis:6379
      - MONGODB_URI=mongodb://admin:password@mongo:27017
    depends_on:
      - redis
      - mongo

  # Flower (Celery 监控)
  flower:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    command: celery -A workers.celery_app flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - celery-worker

  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus

volumes:
  redis-data:
  mongo-data:
  prometheus-data:
  grafana-data:
```

#### 6.3 部署验证脚本

```bash
# docker/deploy.sh
#!/bin/bash
set -e

echo "=== 开始部署爬虫系统 ==="

# 1. 构建镜像
echo "[1/5] 构建 Docker 镜像..."
docker-compose build

# 2. 启动基础服务
echo "[2/5] 启动 Redis 和 MongoDB..."
docker-compose up -d redis mongo

# 3. 等待服务就绪
echo "[3/5] 等待服务就绪..."
sleep 10

# 4. 启动爬虫
echo "[4/5] 启动爬虫服务..."
docker-compose up -d scrapy-worker celery-worker

# 5. 验证
echo "[5/5] 验证部署..."
curl -s http://localhost:5555/api/workers | jq . || echo "Flower 未就绪"
curl -s http://localhost:9090/-/healthy | grep "Prometheus" || echo "Prometheus 未就绪"

echo ""
echo "=== 部署完成 ==="
echo "Flower 监控: http://localhost:5555"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000 (admin/admin)"
```

---

## 📝 练习题

### 练习 9.1：架构设计

```markdown
目标：设计一个电商数据采集系统架构
难度：⭐⭐⭐⭐
要求：
- 包含网页、App、API 三个数据源
- 实现分布式爬取
- 设计数据管道和存储
- 包含监控告警
```

### 练习 9.2：完整实现

```markdown
目标：实现一个完整的网页爬虫系统
难度：⭐⭐⭐⭐⭐
要求：
- 使用 Scrapy 抓取商品数据
- 实现数据清洗和去重
- 存储到 MongoDB
- 配置监控指标
```

### 练习 9.3：部署上线

```markdown
目标：将爬虫系统部署到生产环境
难度：⭐⭐⭐⭐⭐
要求：
- Docker 容器化
- Docker Compose 编排
- 配置监控告警
- 验证系统可用性
```

---

## 📚 扩展阅读

- [Scrapy 官方文档](https://docs.scrapy.org/)
- [Frida 官方文档](https://frida.re/docs/)
- [分布式爬虫架构指南](https://github.com/Administrator-Python/awesome-scrapy)
- [Prometheus 监控实战](https://prometheus.io/docs/introduction/overview/)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 设计可扩展的分布式爬虫架构
- [ ] 实现网页爬虫（Scrapy）
- [ ] 实现 App 爬虫（Frida）
- [ ] 实现 API 逆向爬虫
- [ ] 构建数据清洗与存储管道
- [ ] 配置 Prometheus 监控
- [ ] 实现 Docker 容器化部署
- [ ] 掌握生产环境爬虫最佳实践

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [Stage K: DevOps 与平台工程](../../../stageK-devops/) — 学习容器化和自动化部署
- [Stage R: 前沿探索实验室](../../../stageR-frontier/) — 探索前沿技术

---
