# S02: 网页数据解析 — XPath 与 Beautiful Soup

> **课程编号**: S02
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 8 小时
> **难度**: ⭐⭐☆☆☆
> **前置课程**: S01, L16

---

## 📚 课程概述

本课程介绍如何使用 Python 进行网页数据解析，包括 Requests 库、Beautiful Soup 和 XPath。

---

## 🎯 学习目标

1. 掌握 Requests 库发送 HTTP 请求
2. 熟练使用 Beautiful Soup 解析 HTML
3. 编写高效的 XPath 表达式
4. 处理反爬策略

---

## 📋 课程大纲

### Part 1: HTTP 请求基础 (Requests)

### Part 2: Beautiful Soup 解析 (Beautiful Soup 4)

### Part 3: XPath 高级语法

### Part 4: 反爬应对策略

---

## 🔧 环境准备

```bash
uv add requests beautifulsoup4 lxml
```

---

## 📖 详细内容

### Part 1: HTTP 请求基础

#### 1.1 Requests 库基础

```python
import requests

# GET 请求
response = requests.get('https://example.com')
print(response.status_code)
print(response.text)

# 带参数
params = {'page': 1, 'limit': 20}
response = requests.get('https://api.example.com/list', params=params)

# POST 请求
data = {'username': 'user', 'password': 'pass'}
response = requests.post('https://api.example.com/login', json=data)

# 带 Headers
headers = {'User-Agent': 'Mozilla/5.0 ...'}
response = requests.get(url, headers=headers)
```

#### 1.2 会话与 Cookie

```python
session = requests.Session()

# 登录
session.post('https://example.com/login', json={'user': 'xxx', 'pass': 'yyy'})

# 后续请求自动携带 Cookie
response = session.get('https://example.com/profile')
```

---

### Part 2: Beautiful Soup 解析

#### 2.1 基础用法

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <div class="article">
        <h1 class="title">标题</h1>
        <p class="content">内容...</p>
        <a href="/next">下一页</a>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html, 'lxml')

# 按标签查找
soup.find('h1')           # 第一个 h1
soup.find_all('p')        # 所有 p 标签

# 按 class 查找
soup.find(class_='title')  # 注意 class_ 参数
soup.find_all('div', class_='article')

# 按 id 查找
soup.find(id='main')

# 按属性查找
soup.find('a', href='/next')
```

#### 2.2 CSS 选择器

```python
# select 方法支持 CSS 选择器
soup.select('.article .title')    # 后代选择器
soup.select('#main > .item')      # 子选择器
soup.select('a[href^="/"]')       # 属性选择器

# 获取文本和属性
element.get_text()       # 获取文本
element['href']          # 获取属性
element.get('class')     # 安全获取属性
```

#### 2.3 导航树

```python
# 子节点
soup.body.children       # 子节点迭代器
soup.body.descendants    # 所有后代

# 父节点
element.parent
element.parents           # 所有祖先

# 兄弟节点
element.next_sibling
element.previous_sibling
```

---

### Part 3: XPath 高级语法

#### 3.1 轴(Axes)

```xpath
# 父轴 parent::
/html/body/div[1]/parent::*

# 子轴 child::
/html/body/div/child::p

# 属性轴 attribute::
//div[@class='title']/@id

# 位置轴
//ul/li[1]           # 第一个 li
//ul/li[last()]       # 最后一个 li
//ul/li[position() < 3]  # 前两个
```

#### 3.2 函数

```xpath
# contains() 模糊匹配
//div[contains(@class, 'article')]

# starts-with() 开头匹配
//a[starts-with(@href, '/user')]

# text() 文本匹配
//span[contains(text(), '价格')]
//p[text()='确定']

# normalize-space() 去除空格
//span[normalize-space()='确定']
```

#### 3.3 lxml 库使用

```python
from lxml import etree

html = """
<html>
<body>
    <div class="items">
        <div class="item">
            <span class="name">商品A</span>
            <span class="price">99.00</span>
        </div>
        <div class="item">
            <span class="name">商品B</span>
            <span class="price">199.00</span>
        </div>
    </div>
</body>
</html>
"""

tree = etree.HTML(html)

# XPath 提取
names = tree.xpath('//span[@class="name"]/text()')
prices = tree.xpath('//span[@class="price"]/text()')

# 获取元素属性
links = tree.xpath('//a/@href')
```

---

### Part 4: 反爬应对策略

#### 4.1 User-Agent 伪装

```python
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605...',
]

headers = {'User-Agent': random.choice(USER_AGENTS)}
response = requests.get(url, headers=headers)
```

#### 4.2 请求延时

```python
import time
import random

def crawl_with_delay(urls):
    for url in urls:
        response = requests.get(url)
        # 处理数据...
        time.sleep(random.uniform(1, 3))  # 1-3秒随机延时
```

#### 4.3 代理池

```python
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
response = requests.get(url, proxies=proxies)
```

---

## 📝 练习题

### 练习 2.1：爬取豆瓣电影Top250

```markdown
目标：爬取豆瓣电影名称、评分、评价人数
难度：⭐⭐
提示：分析分页规律，使用 requests + bs4
```

### 练习 2.2：XPath 强化

```markdown
目标：使用 XPath 提取复杂表格数据
难度：⭐⭐⭐
提示：掌握位置索引和轴语法
```

### 练习 2.3：登录态爬取

```markdown
目标：模拟登录后爬取用户数据
难度：⭐⭐⭐
提示：使用 Session 维持登录态
```

---

## ✅ 课后检查

- [ ] 掌握 requests 发送 GET/POST 请求
- [ ] 使用 bs4 提取页面数据
- [ ] 编写 XPath 定位元素
- [ ] 处理常见的反爬措施

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S03: 工业级爬虫 — Scrapy 框架](../S03-scrapy-framework/) — 掌握 Scrapy 分布式爬虫

---
