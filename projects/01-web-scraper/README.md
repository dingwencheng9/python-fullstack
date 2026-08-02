# 项目 1: Web Scraper — 数据采集与分析管道

> **难度**: ⭐⭐⭐ | **预计时间**: 12h | **前置课程**: L08 文件, L09 异常, L40 Pandas, L48 DuckDB

## 🎯 项目目标

构建一个生产级的 Web 爬虫系统，从目标网站采集数据、清洗、存储、分析，最终生成报告。

```
用户输入URL → 爬虫采集 → 数据清洗 → 存储分析 → 导出报告
```

## 📋 功能要求

### P0 — 核心功能（6h）

```
1. 单页面采集
   - requests + BeautifulSoup 提取标题、正文、元数据
   - 处理编码、超时、重试
   - 输出 JSON / CSV

2. 多页面爬取
   - 支持分页 / 链接遍历
   - 请求间隔控制（防止被封）
   - 去重已爬页面

3. 数据清洗
   - 清洗 HTML 标签
   - 规范化文本（空白/大小写/特殊字符）
   - 字段提取（日期/作者/标签）
```

### P1 — 进阶功能（4h）

```
4. 动态页面支持
   - Playwright 渲染 JavaScript 页面
   - 等待元素加载完成
   - 截屏调试

5. 数据存储与分析
   - DuckDB 存储采集数据
   - SQL 聚合分析（每日采集量/Top 来源）
   - Pandas 导出统计报表
```

### P2 — 生产化与合规（2h）

```
6. 错误处理与日志
   - retry 机制（指数退避）
   - 结构化日志
   - 断点续爬

7. 合规采集策略
   - robots.txt 尊重
   - 透明 User-Agent
   - 请求限速
   - 识别 403/429/验证码后停止或退避
   - 跳过 login/admin/checkout/payment 等敏感路径

8. 配置化
   - YAML 配置文件（目标/规则/间隔）
   - CLI 参数解析
```

## 📁 项目结构

```
projects/01-web-scraper/
├── scraper/
│   ├── __init__.py
│   ├── collector.py     # 请求 + 解析
│   ├── policy.py        # 合规策略：限速/封禁识别/敏感路径
│   ├── robots.py        # robots.txt 检查
│   ├── pipeline.py      # 清洗 + 存储
│   └── config.py        # 配置管理
├── tests/
│   ├── __init__.py
│   └── test_scraper.py  # 单元测试
├── data/                # 输出目录
├── requirements.txt     # 依赖
└── README.md
```

## 📦 依赖

```txt
requests>=2.32
beautifulsoup4>=4.12
lxml>=5.0
playwright>=1.40
pandas>=2.2
duckdb>=1.0
pyyaml>=6.0
pydantic>=2.0
httpx>=0.27
```

## 🧪 测试要求

- 单元测试覆盖率 ≥ 80%
- Mock HTTP 请求（不依赖真实网络）
- 测试清洗逻辑的边界情况

## 📊 评分标准

| 维度       | 权重 | 评分标准            |
| ---------- | ---- | ------------------- |
| 功能完整性 | 30%  | 完成 P0 所有功能    |
| 代码质量   | 25%  | 类型注解 + 错误处理 |
| 测试覆盖   | 25%  | ≥80% 覆盖率         |
| 数据质量   | 20%  | 清洗正确、输出可用  |

## 🎓 进阶扩展（可选）

完成基础项目后，可探索以下方向深化：

### 1. Scrapy框架

```python
# 使用Scrapy重构爬虫
import scrapy

class MySpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]

    def parse(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "content": response.css("p::text").getall()
        }
```

### 2. 反爬虫对抗

- User-Agent 轮换
- 代理IP池
- Cookie管理
- 频率限制与指数退避

### 3. 动态渲染页面

```python
# 使用Playwright处理JavaScript渲染
from playwright.async_api import async_playwright

async def scrape_dynamic():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        content = await page.content()
```

### 4. 分布式爬虫

- Scrapy-Redis 分布式队列
- 多机并发爬取
- 数据去重（布隆过滤器）

### 5. 数据质量增强

- 参考 [Stage 5 数据工程](../../stage5-data-engineering/README.md)
- 数据验证与schema校验
- 异常检测与清洗

### 6. 法律合规

⚠️ **重要提醒**：

- 遵守 robots.txt 协议
- 控制爬取频率，避免影响目标站点
- 商业使用需评估版权风险
- 个人信息保护法合规

## 🔗 参考课程

- [L08: 文件操作](../../stage0-python-basics/lessons/L06-file-operations/)
- [L09: 异常处理](../../stage0-python-basics/lessons/L09-exceptions/)
- [L50: Pandas 完整实战](../../stage5-data-engineering/lessons/L50-pandas-complete/)
- [L49: DuckDB 分析引擎](../../stage5-data-engineering/lessons/L49-duckdb/)

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

```bash
# 运行爬虫
python main.py

# 运行测试
pytest tests/ -v
```
