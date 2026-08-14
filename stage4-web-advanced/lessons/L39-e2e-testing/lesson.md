# L39: E2E 测试工程化

> **课程编号**: L39
> **所属阶段**: Stage 4 - Web 开发进阶
> **预计时长**: 5-6 小时
> **难度**: ⭐⭐⭐⭐☆（高级）
> **前置课程**: L17, L27, L35
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ **E2E 测试基础**：理解测试金字塔和 E2E 测试策略
2. ✅ **Playwright 熟练使用**：掌握定位器、断言、页面交互
3. ✅ **测试数据管理**：使用 Fixture 管理测试数据
4. ✅ **认证流程测试**：测试登录、注册、JWT Token
5. ✅ **CI 集成**：将 E2E 测试集成到 GitHub Actions
6. ✅ **最佳实践**：编写可靠、可维护的 E2E 测试

---

```mermaid
flowchart TB
    subgraph Pyramid["测试金字塔"]
        A[E2E 测试<br/>5-10%] --> B[集成测试<br/>20-30%]
        B --> C[单元测试<br/>60-70%]
    end

    subgraph E2E["E2E 测试流程"]
        D[启动测试环境] --> E[登录认证]
        E --> F[执行测试用例]
        F --> G{断言检查}
        G -->|通过| H[截图/报告]
        G -->|失败| I[重试机制]
        I --> J[失败截图]
    end

    subgraph Tools["测试工具"]
        K[Playwright<br/>跨浏览器] --> L[Chromium/Firefox/Safari]
        M[Pytest<br/>测试框架] --> N[pytest-playwright]
        O[CI/CD] --> P[GitHub Actions]
    end

    subgraph BestPractices["最佳实践"]
        Q[Page Object<br/>页面对象模式] --> R[测试隔离]
        S[Fixture<br/>测试数据] --> R
        T[失败重试<br/>flaky 保护] --> R
    end

    style Pyramid fill:#e3f2fd
    style E2E fill:#c8e6c9
    style Tools fill:#fff3e0
```

---

## Part 1: E2E 测试策略

### 1.1 测试金字塔

```
         /\
        /  \
       / E2E \        ← 少量：5-10%，最慢，最贵
      /--------\
     / 集成测试  \    ← 中量：20-30%
    /------------\
   /   单元测试   \  ← 大量：60-70%，最快，最便宜
  /________________\
```

| 测试类型 | 数量 | 速度 | 稳定性 | 成本 |
|----------|------|------|--------|------|
| 单元测试 | 100+ | 秒级 | 高 | 低 |
| 集成测试 | 20-50 | 10秒级 | 中 | 中 |
| E2E 测试 | 5-20 | 分钟级 | 低 | 高 |

### 1.2 何时需要 E2E 测试

**适合 E2E 测试的场景**：
- 用户注册登录流程
- 支付下单完整链路
- 多页面交互状态
- 第三方集成
- 关键业务路径

**不适合 E2E 测试的场景**：
- 单元级别的逻辑验证
- 边界条件测试
- 性能压力测试
- 频繁变动的 UI

### 1.3 Playwright vs Selenium

| 特性 | Playwright | Selenium |
|------|------------|----------|
| 速度 | 快 | 慢 |
| 稳定性 | 高 | 中 |
| 等待机制 | 自动等待 | 手动等待 |
| 跨浏览器 | 原生支持 | WebDriver |
| API 设计 | 现代 | 传统 |
| 社区 | 快速增长 | 成熟 |

---

## Part 2: Playwright 基础

### 2.1 安装与配置

```bash
# 安装 Playwright
uv add pytest-playwright
playwright install chromium  # 安装浏览器

# 或使用 uvx
uvx playwright install chromium
```

### 2.2 核心概念

```python
from playwright.sync_api import sync_playwright

# 同步模式
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("https://example.com")
    page.click("#login-button")
    page.fill("#username", "testuser")
    page.fill("#password", "password123")
    page.click("#submit")

    assert "Welcome" in page.title()
    browser.close()
```

```python
import asyncio
from playwright.async_api import async_playwright

# 异步模式（推荐用于 pytest）
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://example.com")
        await page.click("#login-button")
        await page.fill("#username", "testuser")
        await page.fill("#password", "password123")
        await page.click("#submit")

        assert "Welcome" in await page.title()
        await browser.close()

asyncio.run(main())
```

### 2.3 定位器（Locators）

Playwright 提供了多种定位器，按优先级使用：

```python
# 1. 按角色定位（推荐，最可靠）
await page.get_by_role("button", name="Submit").click()
await page.get_by_role("link", name="Home").click()
await page.get_by_role("textbox", name="Username").fill("test")

# 2. 按标签定位
await page.get_by_label("Email").fill("test@example.com")
await page.get_by_placeholder("Search...").fill("query")

# 3. 按文本定位
await page.get_by_text("Submit").click()
await page.get_by_text("Welcome, John", exact=True).click()

# 4. 按测试 ID 定位（最佳实践）
await page.get_by_test_id("submit-button").click()

# 5. 按 CSS 选择器
await page.locator(".btn-primary").click()
await page.locator("#login-form").fill({"username": "test"})

# 6. 按 XPath（最后选择）
await page.locator("//button[contains(text(), 'Submit')]").click()
```

### 2.4 断言（Assertions）

```python
from playwright.sync_api import expect

# 可见性断言
expect(page.locator("#success-message")).to_be_visible()
expect(page.locator("#loading")).to_be_hidden()
expect(page.locator("#modal")).to_be_attached()

# 文本断言
expect(page.locator("h1")).to_have_text("Welcome")
expect(page.locator("h1")).to_contain_text("Welcome")
expect(page.locator("h1")).to_have_text("Welcome, John", ignore_case=True)

# 值断言
expect(page.locator("#username")).to_have_value("testuser")
expect(page.locator("#email")).to_have_value("test@example.com")

# 属性断言
expect(page.locator("#submit")).to_be_enabled()
expect(page.locator("#submit")).to_be_disabled()
expect(page.locator("a")).to_have_attribute("href", "/home")

# URL 断言
expect(page).to_have_url("**/dashboard")
expect(page).to_have_title("Dashboard")

# 计数断言
expect(page.locator(".todo-item")).to_have_count(5)

# 自定义断言
assert await page.evaluate("() => document.readyState") == "complete"
```

### 2.5 页面交互

```python
# 点击
await page.click("#button")
await page.click("#button", button="right")  # 右键
await page.dblclick("#button")  # 双击

# 输入
await page.fill("#input", "text")
await page.type("#input", "text", delay=100)  # 逐字输入

# 悬停和拖拽
await page.hover("#menu")
await page.drag_and_drop("#source", "#target")

# 键盘操作
await page.keyboard.press("Enter")
await page.keyboard.press("Control+a")
await page.keyboard.type("Hello World")

# 选择下拉框
await page.select_option("#country", "US")
await page.select_option("#country", label="United States")

# 上传文件
await page.set_input_files("#file-upload", "path/to/file.pdf")

# 截图
await page.screenshot(path="screenshot.png")
await page.screenshot(path="full-page.png", full_page=True)
```

---

## Part 3: 认证流程测试

### 3.1 API 辅助方法

```python
import httpx
from typing import Optional

class AuthHelper:
    """认证辅助类"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token: Optional[str] = None

    async def register(self, username: str, email: str, password: str):
        """用户注册"""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.post(
                "/api/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                }
            )
            response.raise_for_status()
            return response.json()

    async def login(self, username: str, password: str) -> str:
        """用户登录，返回 token"""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.post(
                "/api/auth/login",
                params={"username": username, "password": password}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            return self.token

    async def logout(self):
        """用户登出"""
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            await client.post(
                "/api/auth/logout",
                headers={"Authorization": f"Bearer {self.token}"}
            )

    def get_headers(self) -> dict:
        """获取认证头"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
```

### 3.2 登录测试

```python
import pytest
from playwright.sync_api import Page, expect
from app.testing import create_test_user, delete_test_user

class TestLogin:
    """登录功能测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        # 创建测试用户
        self.test_user = create_test_user()
        yield
        # 清理测试用户
        delete_test_user(self.test_user["username"])

    def test_login_success(self):
        """测试成功登录"""
        self.page.goto("/login")

        self.page.get_by_label("用户名").fill(self.test_user["username"])
        self.page.get_by_label("密码").fill(self.test_user["password"])
        self.page.get_by_role("button", name="登录").click()

        # 验证跳转到首页
        expect(self.page).to_have_url("**/dashboard")
        expect(self.page.get_by_text(f"欢迎, {self.test_user['username']}")).to_be_visible()

    def test_login_invalid_password(self):
        """测试密码错误"""
        self.page.goto("/login")

        self.page.get_by_label("用户名").fill(self.test_user["username"])
        self.page.get_by_label("密码").fill("wrong_password")
        self.page.get_by_role("button", name="登录").click()

        # 验证错误提示
        expect(self.page.get_by_role("alert")).to_contain_text("用户名或密码错误")

    def test_login_empty_fields(self):
        """测试空字段验证"""
        self.page.goto("/login")

        self.page.get_by_role("button", name="登录").click()

        # 验证 HTML5 验证
        expect(self.page.get_by_label("用户名")).to_have_attribute("required", "")

    def test_login_redirect(self):
        """测试未登录重定向"""
        self.page.goto("/dashboard")

        # 应该重定向到登录页
        expect(self.page).to_have_url("**/login?redirect=/dashboard")
```

### 3.3 注册测试

```python
class TestRegister:
    """注册功能测试"""

    def test_register_success(self, page: Page):
        """测试成功注册"""
        page.goto("/register")

        username = f"testuser_{uuid.uuid4().hex[:8]}"
        page.get_by_label("用户名").fill(username)
        page.get_by_label("邮箱").fill(f"{username}@example.com")
        page.get_by_label("密码").fill("TestPass123!")
        page.get_by_label("确认密码").fill("TestPass123!")
        page.get_by_role("button", name="注册").click()

        # 验证注册成功
        expect(page).to_have_url("**/login")
        expect(page.get_by_text("注册成功，请登录")).to_be_visible()

    def test_register_duplicate_username(self, page: Page, existing_user):
        """测试用户名重复"""
        page.goto("/register")

        page.get_by_label("用户名").fill(existing_user["username"])
        page.get_by_label("邮箱").fill("new@example.com")
        page.get_by_label("密码").fill("TestPass123!")
        page.get_by_role("button", name="注册").click()

        expect(page.get_by_role("alert")).to_contain_text("用户名已存在")

    def test_register_password_mismatch(self, page: Page):
        """测试密码不匹配"""
        page.goto("/register")

        page.get_by_label("用户名").fill("newuser")
        page.get_by_label("邮箱").fill("new@example.com")
        page.get_by_label("密码").fill("TestPass123!")
        page.get_by_label("确认密码").fill("DifferentPass123!")
        page.get_by_role("button", name="注册").click()

        expect(page.get_by_text("两次密码输入不一致")).to_be_visible()
```

---

## Part 4: 任务管理测试

### 4.1 CRUD 测试

```python
class TestTaskCRUD:
    """任务 CRUD 测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, authenticated_user):
        self.page = page
        self.user = authenticated_user
        self.page.goto("/dashboard")

    def test_create_task(self):
        """测试创建任务"""
        # 点击新建按钮
        self.page.get_by_role("button", name="新建任务").click()

        # 填写表单
        self.page.get_by_label("任务标题").fill("测试任务")
        self.page.get_by_label("任务描述").fill("这是一个测试任务的描述")
        self.page.get_by_role("button", name="保存").click()

        # 验证创建成功
        expect(self.page.get_by_text("测试任务")).to_be_visible()
        expect(self.page.get_by_text("任务创建成功")).to_be_visible()

    def test_update_task(self):
        """测试更新任务"""
        # 先创建一个任务
        self.page.get_by_role("button", name="新建任务").click()
        self.page.get_by_label("任务标题").fill("原始标题")
        self.page.get_by_role("button", name="保存").click()

        # 点击编辑
        self.page.get_by_text("原始标题").hover()
        self.page.get_by_role("button", name="编辑").click()

        # 修改标题
        self.page.get_by_label("任务标题").fill("更新后的标题")
        self.page.get_by_role("button", name="保存").click()

        # 验证更新
        expect(self.page.get_by_text("更新后的标题")).to_be_visible()
        expect(self.page.get_by_text("原始标题")).not_to_be_visible()

    def test_delete_task(self):
        """测试删除任务"""
        # 创建任务
        self.page.get_by_role("button", name="新建任务").click()
        self.page.get_by_label("任务标题").fill("待删除任务")
        self.page.get_by_role("button", name="保存").click()

        # 删除任务
        self.page.get_by_text("待删除任务").hover()
        self.page.get_by_role("button", name="删除").click()
        self.page.get_by_role("button", name="确认删除").click()

        # 验证删除
        expect(self.page.get_by_text("待删除任务")).not_to_be_visible()
        expect(self.page.get_by_text("任务已删除")).to_be_visible()

    def test_complete_task(self):
        """测试完成任务"""
        # 创建任务
        self.page.get_by_role("button", name="新建任务").click()
        self.page.get_by_label("任务标题").fill("待完成任务")
        self.page.get_by_role("button", name="保存").click()

        # 点击完成
        self.page.get_by_text("待完成任务").locator("..").get_by_role("checkbox").check()

        # 验证完成状态
        expect(self.page.get_by_text("待完成任务").locator("..")).to_have_class(".*completed.*")
```

### 4.2 过滤和搜索

```python
class TestTaskFilter:
    """任务过滤和搜索测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, authenticated_user):
        self.page = page
        # 创建多个任务
        for i in range(5):
            self._create_task(f"任务 {i}", completed=(i % 2 == 0))
        self.page.goto("/tasks")

    def _create_task(self, title: str, completed: bool = False):
        """创建任务的辅助方法"""
        self.page.get_by_role("button", name="新建任务").click()
        self.page.get_by_label("任务标题").fill(title)
        if completed:
            self.page.get_by_label("已完成").check()
        self.page.get_by_role("button", name="保存").click()

    def test_filter_completed(self):
        """测试筛选已完成任务"""
        self.page.get_by_role("button", name="已完成").click()

        # 验证只有已完成的任务显示
        items = self.page.locator(".task-item")
        count = await items.count()
        for i in range(count):
            expect(items.nth(i)).to_have_class(".*completed.*")

    def test_search_tasks(self):
        """测试搜索任务"""
        self.page.get_by_placeholder("搜索任务...").fill("任务 0")

        # 验证搜索结果
        expect(self.page.get_by_text("任务 0")).to_be_visible()
        expect(self.page.get_by_text("任务 1")).not_to_be_visible()
```

---

## Part 5: pytest-playwright 集成

### 5.1 配置

```python
# conftest.py
import pytest
from playwright.sync_api import Page, Browser, BrowserContext

@pytest.fixture(scope="session")
def browser_launch_args(browser_type_launch_args):
    """浏览器启动参数"""
    return [
        *browser_type_launch_args,
        "--disable-web-security",
    ]

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """浏览器上下文参数"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
    }

@pytest.fixture
def authenticated_context(
    browser: Browser,
    browser_context_args: dict,
    base_url: str
) -> BrowserContext:
    """创建已认证的浏览器上下文"""
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    # 执行登录
    page.goto(f"{base_url}/login")
    page.get_by_label("用户名").fill("testuser")
    page.get_by_label("密码").fill("testpass123")
    page.get_by_role("button", name="登录").click()

    page.wait_for_url(f"{base_url}/dashboard")

    # 返回干净的上下文
    yield context
    context.close()

@pytest.fixture
def authenticated_user(authenticated_context) -> dict:
    """获取已认证用户信息"""
    return {"username": "testuser", "id": 1}
```

### 5.2 Page Object 模式

```python
# pages/login_page.py
from playwright.sync_api import Page, expect

class LoginPage:
    """登录页面对象"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("/login")
        return self

    def fill_username(self, username: str):
        self.page.get_by_label("用户名").fill(username)
        return self

    def fill_password(self, password: str):
        self.page.get_by_label("密码").fill(password)
        return self

    def submit(self):
        self.page.get_by_role("button", name="登录").click()
        return self

    def login(self, username: str, password: str):
        self.goto()
        self.fill_username(username)
        self.fill_password(password)
        self.submit()

    def expect_error(self, message: str):
        expect(self.page.get_by_role("alert")).to_contain_text(message)
        return self

# pages/dashboard_page.py
from playwright.sync_api import Page, expect

class DashboardPage:
    """仪表盘页面对象"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("/dashboard")
        return self

    def create_task(self, title: str, description: str = ""):
        self.page.get_by_role("button", name="新建任务").click()
        self.page.get_by_label("任务标题").fill(title)
        if description:
            self.page.get_by_label("任务描述").fill(description)
        self.page.get_by_role("button", name="保存").click()
        return self

    def get_task_by_title(self, title: str):
        return self.page.get_by_text(title).locator("..")

# 测试中使用
def test_login_with_page_object(page: Page):
    login_page = LoginPage(page)
    login_page.login("testuser", "password")

    dashboard = DashboardPage(page)
    expect(page).to_have_url("**/dashboard")
```

### 5.3 完整测试文件

```python
# tests/e2e/test_auth.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestAuthentication:
    """认证流程测试"""

    @pytest.fixture
    def login_page(self, page: Page) -> LoginPage:
        return LoginPage(page)

    @pytest.fixture
    def dashboard_page(self, page: Page) -> DashboardPage:
        return DashboardPage(page)

    def test_successful_login(self, login_page: LoginPage, dashboard_page: DashboardPage):
        """成功登录流程"""
        login_page.login("testuser", "password123")
        expect(login_page.page).to_have_url("**/dashboard")

    def test_failed_login_invalid_password(self, login_page: LoginPage):
        """密码错误登录失败"""
        login_page.goto()
        login_page.fill_username("testuser")
        login_page.fill_password("wrongpassword")
        login_page.submit()
        login_page.expect_error("用户名或密码错误")

    def test_logout(self, login_page: LoginPage, dashboard_page: DashboardPage):
        """登出功能"""
        # 登录
        login_page.login("testuser", "password123")
        expect(dashboard_page.page).to_have_url("**/dashboard")

        # 登出
        dashboard_page.page.get_by_role("button", name="登出").click()
        expect(dashboard_page.page).to_have_url("**/login")
```

---

## Part 6: CI 集成

### 6.1 GitHub Actions 配置

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    services:
      api:
        image: ghcr.io/myorg/myapp:latest
        ports:
          - 8000:8000
        env:
          DATABASE_URL: postgresql://test:test@localhost/test
          REDIS_URL: redis://localhost:6379
        options: >-
          --health-cmd "curl -f http://localhost:8000/health || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync

      - name: Install Playwright
        run: |
          uv add playwright
          playwright install --with-deps chromium

      - name: Run E2E tests
        run: |
          pytest tests/e2e/ \
            --base-url http://localhost:8000 \
            --html=reports/e2e-report.html \
            --self-contained-html \
            -v

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-test-results
          path: |
            reports/
            test-results/
          retention-days: 7

      - name: Upload screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-screenshots
          path: test-results/**/snapshots/**/*.{png,webp}
          retention-days: 7
```

### 6.2 测试报告

```python
# pytest.ini
[tool.pytest.ini_options]
addopts = """
    --html=reports/e2e-report.html
    --self-contained-html
    --junitxml=reports/junit.xml
    -v
"""
```

---

## Part 7: 最佳实践

### 7.1 测试隔离

```python
# 每个测试使用独立数据
@pytest.fixture
def unique_user(page: Page):
    user_data = {
        "username": f"user_{uuid.uuid4().hex[:8]}",
        "email": f"user_{uuid.uuid4().hex[:8]}@test.com",
        "password": "TestPass123!"
    }
    # 创建用户
    response = httpx.post(f"{BASE_URL}/api/auth/register", json=user_data)
    yield user_data
    # 清理用户
    httpx.delete(f"{BASE_URL}/api/users/{user_data['username']}")
```

### 7.2 可靠等待

```python
# ❌ 不推荐：固定等待
time.sleep(5)

# ✅ 推荐：自动等待
expect(page.locator("#success")).to_be_visible()

# ✅ 推荐：智能等待
page.wait_for_load_state("networkidle")

# ✅ 推荐：显式等待
page.wait_for_selector("#element", state="visible", timeout=10000)
```

### 7.3 调试技巧

```python
# 失败时自动截图
@pytest.fixture
def page_with_screenshot(page: Page, request):
    yield page
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshots/{request.node.name}.png")

# 录制视频
@pytest.fixture
def video_page(browser: Browser):
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()
    yield page
    context.close()
```

---

## 📝 课程总结

### 核心知识点

1. **测试策略**：测试金字塔、E2E 测试适用场景
2. **Playwright**：定位器、断言、页面交互
3. **认证测试**：登录、注册、JWT Token
4. **CRUD 测试**：创建、读取、更新、删除
5. **Page Object**：页面对象模式
6. **CI 集成**：GitHub Actions 配置

### 关键要点

- ✅ 优先使用 role、label 等语义化定位器
- ✅ 使用 expect 断言而非手动断言
- ✅ 使用 Page Object 模式封装页面逻辑
- ✅ 每个测试独立，使用 Fixture 管理数据
- ✅ 使用自动等待，避免硬编码 sleep

---

## ✅ 完成标准

完成本课程后，你应该能够：

- [ ] 理解测试金字塔和 E2E 测试策略
- [ ] 使用 Playwright 编写端到端测试
- [ ] 测试用户认证流程
- [ ] 测试完整的 CRUD 操作
- [ ] 使用 Page Object 模式组织测试代码
- [ ] 将 E2E 测试集成到 CI/CD
- [ ] 编写可靠、可维护的 E2E 测试

---

**下一步**: 继续学习 [L40: 消息队列](../L40-message-queue/README.md)
