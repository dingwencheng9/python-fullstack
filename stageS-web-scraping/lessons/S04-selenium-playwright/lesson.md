# S04: 自动化抓包 — Selenium 与 Playwright

> **课程编号**: S04
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 8 小时
> **难度**: ⭐⭐⭐☆☆
> **前置课程**: S01 前端基础

---

## 📚 课程概述

当传统爬虫无法应对 JavaScript 动态渲染、验证码或需要登录态的复杂场景时，浏览器自动化工具成为最佳选择。本课程深入讲解 Selenium 与 Playwright 两大框架，掌握无头浏览器自动化抓包技术。

---

## 🎯 学习目标

1. 理解 Selenium 与 Playwright 的适用场景
2. 掌握浏览器自动化操作（点击、输入、滚动）
3. 熟练使用等待策略处理动态内容
4. 实现登录态维持与 Cookie 管理
5. 掌握网络请求拦截与响应捕获
6. 实现反检测与隐蔽爬取

---

## 📋 课程大纲

- [Part 1: Selenium 核心原理](#part-1-selenium-核心原理)
- [Part 2: Playwright 进阶特性](#part-2-playwright-进阶特性)
- [Part 3: 网络拦截与请求分析](#part-3-网络拦截与请求分析)
- [Part 4: 动态内容与等待策略](#part-4-动态内容与等待策略)
- [Part 5: 反检测与隐蔽爬取](#part-5-反检测与隐蔽爬取)

---

## 🔧 环境准备

```bash
# 安装依赖
cd stageS-web-scraping/lessons/S04-selenium-playwright
uv venv && source .venv/bin/activate
uv add selenium playwright
uv run playwright install chromium

# 验证安装
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

---

## 📖 详细内容

### Part 1: Selenium 核心原理

#### 1.1 Selenium vs Playwright 对比

| 维度 | Selenium | Playwright |
|------|----------|------------|
| 启动速度 | 较慢 | 快 |
| API 设计 | 较旧 | 现代 Promise/async |
| 等待机制 | 隐式/显式等待 | 自动等待 + 显式等待 |
| 浏览器支持 | 全系列 | Chromium/Firefox/WebKit |
| 移动端模拟 | 有限 | 完整支持 |
| 社区生态 | 成熟庞大 | 快速增长 |

#### 1.2 Selenium 基础操作

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置 Chrome 选项
options = Options()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-blink-features=AutomationControlled')

# 创建驱动
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# 基本操作
driver.get('https://example.com')
print(driver.title)

# 元素定位
element = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
element.send_keys('搜索内容')
element.submit()

# 等待元素
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, 'result'))
)

driver.quit()
```

#### 1.3 元素交互

```python
from selenium.webdriver.common.action_chains import ActionChains

# 点击
button = driver.find_element(By.ID, 'submit')
button.click()

# 悬停
menu = driver.find_element(By.CSS_SELECTOR, '.dropdown')
ActionChains(driver).move_to_element(menu).perform()

# 拖拽
source = driver.find_element(By.ID, 'draggable')
target = driver.find_element(By.ID, 'droppable')
ActionChains(driver).drag_and_drop(source, target).perform()

# 键盘操作
from selenium.webdriver.common.keys import Keys
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'a')
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.DELETE)

# 执行 JavaScript
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
```

---

### Part 2: Playwright 进阶特性

#### 2.1 Playwright 基础架构

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )

    # 创建上下文（隔离环境）
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        locale='zh-CN',
    )

    # 创建页面
    page = context.new_page()

    # 访问页面
    page.goto('https://example.com')

    # 自动等待点击
    page.click('button#submit')

    # 等待导航完成
    page.wait_for_load_state('networkidle')

    # 获取内容
    content = page.content()

    browser.close()
```

#### 2.2 异步版本（推荐生产使用）

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto('https://example.com')
        await page.fill('input[name="q"]', 'search query')
        await page.click('button[type="submit"]')

        # 等待搜索结果
        await page.wait_for_selector('.search-result')

        # 提取数据
        results = await page.query_selector_all('.result-item')
        for result in results:
            title = await result.query_selector('h3').inner_text()
            print(title)

        await browser.close()

asyncio.run(main())
```

#### 2.3 框架检测与规避

```python
# 检测并规避 WebDriver
async def stealth_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )

        context = await browser.new_context(
            # 随机化视口
            viewport={
                'width': random.randint(1200, 1920),
                'height': random.randint(800, 1080),
            },
            # 使用真实 UA
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )

        # 注入 JavaScript 规避检测
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
        """)

        return browser
```

---

### Part 3: 网络拦截与请求分析

#### 3.1 请求/响应拦截

```python
# Selenium 网关捕获
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_capabilities = DesiredCapabilities.CHROME.copy()
desired_capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
driver.get('https://example.com')

# 读取性能日志
for log in driver.get_log('performance'):
    import json
    msg = json.loads(log['message'])
    if msg['message']['method'] == 'Network.responseReceived':
        print(msg['message']['params']['response']['url'])
```

#### 3.2 Playwright 网络拦截

```python
# 拦截特定请求
async def intercept_requests():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 拦截图片请求
        await page.route('**/*.{png,jpg,jpeg,gif,svg}',
            lambda route: route.abort())

        # 修改请求头
        await page.route('**/api/**', lambda route: route.continue_(
            headers={**route.request.headers, 'X-Custom-Header': 'value'}
        ))

        # 模拟响应
        await page.route('**/api/user', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"name": "test", "id": 123}'
        ))

        await page.goto('https://example.com')
        await browser.close()
```

#### 3.3 提取 API 数据

```python
# 直接获取 API 响应数据
async def extract_api_data():
    api_responses = {}

    async def handle_response(response):
        if '/api/' in response.url:
            try:
                data = await response.json()
                api_responses[response.url] = data
            except:
                pass

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        page.on('response', handle_response)
        await page.goto('https://example.com/dashboard')

        # 等待数据加载
        await page.wait_for_load_state('networkidle')

        print(f"捕获到 {len(api_responses)} 个 API 响应")
        for url, data in api_responses.items():
            print(f"{url}: {data}")

        await browser.close()
```

---

### Part 4: 动态内容与等待策略

#### 4.1 等待机制对比

```python
# Selenium 等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 显式等待（推荐）
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.element_to_be_clickable((By.ID, 'dynamic-button'))
)

# 条件等待
wait.until(EC.title_contains('目标标题'))
wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'iframe')))
wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'loading')))

# Playwright 自动等待（更智能）
page.click('button#submit')  # 自动等待元素可点击
page.fill('input', 'text')   # 自动等待元素可见
page.select_option('select', 'value')  # 自动等待选项可用
```

#### 4.2 复杂等待场景

```python
# Playwright 高级等待
async def advanced_waiting():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 等待函数返回 true
        await page.wait_for_function("""
            () => document.querySelectorAll('.item').length >= 10
        """, timeout=30000)

        # 等待导航
        async with page.expect_navigation():
            await page.click('button.next-page')

        # 等待下载
        async with page.expect_download() as download_info:
            await page.click('button.download')
        download = await download_info.value

        # 等待弹出窗口
        async with page.expect_popup() as popup_info:
            await page.click('a[target="_blank"]')
        popup = await popup_info.value
        await popup.wait_for_load_state()

        await browser.close()
```

#### 4.3 分页与无限滚动

```python
# 处理分页
async def paginate():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        all_items = []
        page_num = 1

        while True:
            await page.goto(f'https://example.com/page/{page_num}')
            await page.wait_for_selector('.item-list')

            # 提取当前页数据
            items = await page.query_selector_all('.item')
            if not items:
                break

            for item in items:
                text = await item.inner_text()
                all_items.append(text)

            # 检查是否有下一页
            next_btn = page.locator('button.next-page')
            if not await next_btn.is_enabled():
                break

            page_num += 1

        print(f"共获取 {len(all_items)} 条数据")
        await browser.close()

# 处理无限滚动
async def infinite_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto('https://example.com/feed')

        last_height = await page.evaluate('document.body.scrollHeight')

        while True:
            # 滚动到底部
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

            # 等待新内容加载
            await page.wait_for_timeout(1000)

            new_height = await page.evaluate('document.body.scrollHeight')
            if new_height == last_height:
                break

            last_height = new_height

        await browser.close()
```

---

### Part 5: 反检测与隐蔽爬取

#### 5.1 常见检测手段

| 检测类型 | 检测方法 | 规避策略 |
|----------|----------|----------|
| WebDriver | navigator.webdriver | 修改属性值 |
| Chrome runtime | window.chrome | 注入 JS |
| 自动化属性 | $cdc_/__webdriver_evaluate | 使用真实浏览器 |
| 指纹检测 | Canvas/WebGL | 随机化或禁用 |
| 行为检测 | 鼠标轨迹 | 添加随机延迟 |

#### 5.2 完整反检测配置

```python
from playwright.sync_api import sync_playwright
import random

def create_stealth_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--disable-notifications',
                '--disable-extensions',
                '--disable-background-networking',
                '--safebrowsing-disable-auto-update',
                '--disable-sync',
                '--metrics-recording-only',
                '--mute-audio',
            ]
        )

        context = browser.new_context(
            viewport={
                'width': random.choice([1280, 1366, 1440, 1920]),
                'height': random.choice([720, 768, 900, 1080]),
            },
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            permissions=['geolocation'],
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            },
        )

        # 注入反检测脚本
        context.add_init_script("""
            // 修改 WebDriver 属性
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });

            // 修改 Chrome 属性
            window.chrome = {
                runtime: {},
                loadTimes: () => {},
                csi: () => {},
            };

            // 修改 Permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );

            // 修改 Plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            // 修改 Languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en'],
            });

            // 隐藏 Automation 相关函数
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """)

        return browser, context
```

#### 5.3 随机行为模拟

```python
import asyncio
import random
from playwright.async_api import async_playwright

async def human_behavior_demo():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # 模拟人类滚动行为
        async def human_scroll():
            for _ in range(5):
                scroll_amount = random.randint(200, 800)
                await page.evaluate(f'window.scrollBy(0, {scroll_amount})')
                await asyncio.sleep(random.uniform(0.3, 1.0))

        # 模拟鼠标移动
        async def human_mouse_move():
            for _ in range(10):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.1, 0.3))

        await page.goto('https://example.com')

        # 在关键操作间添加随机延迟
        await asyncio.sleep(random.uniform(1, 3))
        await human_scroll()
        await human_mouse_move()
        await page.click('button.read-more')
        await asyncio.sleep(random.uniform(2, 4))

        await browser.close()
```

---

## 📝 练习题

### 练习 4.1：Selenium 基础爬虫

```markdown
目标：使用 Selenium 爬取微博热搜榜
难度：⭐⭐⭐
要求：
- 处理登录态
- 提取热搜标题和热度
- 处理动态加载
```

### 练习 4.2：Playwright API 拦截

```markdown
目标：使用 Playwright 拦截并提取 B 站视频数据
难度：⭐⭐⭐⭐
提示：
- 拦截 /api/* 请求
- 提取视频元数据
- 保存到本地 JSON
```

### 练习 4.3：反检测爬虫

```markdown
目标：绕过某网站的 WebDriver 检测
难度：⭐⭐⭐⭐
要求：
- 实现完整反检测配置
- 验证检测规避效果
- 提取目标数据
```

---

## 📚 扩展阅读

- [Playwright 官方文档](https://playwright.dev/python/)
- [Selenium 文档](https://www.selenium.dev/documentation/)
- [undetected-playwright](https://github.com/ultrafunkamsterdam/undetected-playwright)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 理解 Selenium 与 Playwright 的适用场景
- [ ] 使用两种框架进行浏览器自动化操作
- [ ] 实现网络请求拦截与数据提取
- [ ] 处理动态内容的等待策略
- [ ] 配置反检测规避 WebDriver 检测
- [ ] 模拟人类行为进行隐蔽爬取

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S05: JavaScript 逆向基础](../S05-js-reverse-basics/) — JavaScript 代码分析与逆向

---
