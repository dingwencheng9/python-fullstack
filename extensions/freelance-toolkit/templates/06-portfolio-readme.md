# GitHub 个人主页 README 模板

> 这是接单时**第一张名片**。客户搜你 → 看到你的 GitHub → 1 分钟内决定要不要联系你。
> **没有这个，你的所有项目都是孤立的零散文件。**

---

## 创建方法

1. 在 GitHub 上创建一个**与你用户名同名**的仓库（例如 `username/username`）
2. 在仓库根目录创建 `README.md`
3. 内容会自动显示在你的个人主页 https://github.com/username

---

## 模板（直接复制修改）

```markdown
# 你好，我是 [你的名字] 👋

🐍 **Python 全栈开发者** | 🤖 **AI 应用工程师** | 📊 **数据分析师**

📍 [城市] | 💼 接单中 | 📧 [邮箱]

---

## 🛠️ 技术栈

**后端**：Python 3.13、FastAPI、SQLAlchemy 2.0、Pydantic V2、Async/Await
**数据**：Pandas、NumPy、DuckDB、PostgreSQL、Redis
**AI**：LangGraph、LangChain、RAG、向量数据库、OpenAI API
**前端**：HTMX、SSE、WebSocket、基础 React
**工程化**：Docker、CI/CD、pytest、Playwright E2E

---

## 🚀 作品集

### 🤖 [企业知识库 AI 助手](https://github.com/username/ai-knowledge-base)

基于 LangGraph + FastAPI + HTMX 的 RAG 问答系统，含 SSE 流式输出、引用回链、Mock LLM 离线兜底。

**亮点**：

- LangGraph 状态机驱动的多步推理流程
- 内存向量库 + Qdrant 持久化双方案
- Docker Compose 一键部署
- 测试覆盖率 85%+

[🎬 演示视频](#) | [💻 在线 Demo](#) | [📖 文档](#)

---

### 🕷️ [合规网络爬虫框架](https://github.com/username/web-scraper)

生产级 Python 爬虫，支持 robots.txt 尊重、限速、敏感路径跳过、429 退避。

**亮点**：

- 单进程 10+ 页/分钟，数据准确率 98%+
- DuckDB 嵌入式存储，零运维
- 异步采集扩展，10+ QPS
- 32 个测试用例全覆盖

[🎬 演示视频](#) | [📖 文档](#)

---

### 📊 [数据智能流水线](https://github.com/username/data-pipeline)

端到端数据流水线：爬虫 JSON → 清洗 → 特征工程 → DuckDB 分析 → Markdown 报告。

**亮点**：

- 日均处理 10 万+ 条数据
- Pandas/Polars 双引擎可切换
- 可视化报告自动生成

[🎬 演示视频](#)

---

### 🧪 [E2E 自动化测试框架](https://github.com/username/e2e-tests)

Playwright + pytest + Page Object 模式，覆盖率 85%。

[💻 仓库](#)

---

## 💼 接单服务

### 🥉 基础（¥500-3000）

- 网页数据采集 + Excel/JSON 报表
- Excel/PDF 办公自动化
- 简单 API CRUD

### 🥈 中等（¥3000-15000）

- FastAPI 后端开发
- 数据分析报告 + 看板
- 网页流程自动化机器人

### 🥇 高级（¥15000+）

- 企业内部 RAG 知识库
- AI Agent 流程自动化
- 私有化部署 + 长期运维

📩 **询价方式**：发送项目需求到 [邮箱]，我会在 24 小时内回复。

---

## 📈 GitHub 数据

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=default)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact)

---

## 📝 最近博客

- [文章 1：合规网络爬虫的 5 个细节](#)
- [文章 2：用 LangGraph 替代 LangChain Chain 的理由](#)
- [文章 3：FastAPI + HTMX 比 React 简单 10 倍](#)

---

## 📬 联系方式

- 📧 Email: [your@email.com]
- 💬 微信: [wx-id]（备注 GitHub 来意）
- 🐦 Twitter/X: [@username]
- 🔗 LinkedIn: [linkedin.com/in/username]
- 🌐 个人主页: [yourname.com]

⏰ **响应时间**：工作日 24 小时内，周末 48 小时内。
```

---

## 加分细节

### 1. 头像

- 真人照片 > 卡通头像 > 默认 GitHub 头像
- 西装/正装是过时的，干净穿着 + 自然笑容更好
- 不要用模糊的、暗色的、太年轻看起来不专业的

### 2. 仓库置顶

GitHub 个人页可以置顶 6 个仓库。**严格挑选**：

- 4 个作品集项目（项目1-4）必须置顶
- 剩下 2 个：你的最佳贡献 / 个人博客 / 教程类

### 3. 写好仓库描述

每个仓库的 description 要包含：

- 解决什么问题（1 句话）
- 用了什么技术（关键词）
- 是否在产品环境运行过

❌ "My Python project"
✅ "🕷️ 生产级合规网络爬虫框架 | Python 3.13 + DuckDB + 异步并发"

### 4. README 顶部的徽章

适度使用：

```markdown
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/user/repo/actions/workflows/test.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/user/repo)
```

不要超过 5 个，避免炫技嫌疑。

### 5. 提交活动

GitHub 个人页底部的"contribution graph"是可见的：

- **绿色越多越好**——客户判断你是否在持续工作
- 如果你的提交都在私有仓库，开启 [Include private contributions](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-contribution-settings-on-your-profile)

### 6. 真实 demo 链接

**如果客户点了"Demo"链接发现挂了/404，整个页面的可信度归零。**

- 部署在 Railway / Render / Fly.io / Vercel（免费层够用）
- 至少保证作品集顶置的 1-2 个项目有可访问 URL
- 在 README 里写："Demo 偶尔休眠（免费托管），首次访问需 30 秒预热"

---

## 反例：不要这样写

❌ **过度自夸**

> "10 年 Python 经验，精通所有框架"
> （客户：那你怎么不去字节腾讯？）

❌ **空话太多**

> "热爱编程，追求卓越，永不止步"
> （客户：所有人都这么说）

❌ **隐藏价格**

> "联系我了解报价"
> （客户：怕你坑我）

❌ **作品集是 todo list / 学习项目**

> 把"FastAPI 学习笔记""跟着教程做的 ToDo App"放置顶
> （客户：你能做的就这？）

✅ **这样写**

> "用 LangGraph + FastAPI 给 X 公司做的内部知识库，节省了员工 30% 查文档时间"
> （即使是练习项目，也用真实业务场景包装）

---

## 检查清单

发布前对照这 10 点：

- [ ] 第一行就有"接单中"和联系方式
- [ ] 顶置 6 个真实可演示的仓库
- [ ] 至少 2 个作品有可点击的演示链接
- [ ] 至少 1 个作品有 30-60 秒视频
- [ ] 价格区间公开（不公开等于没询价）
- [ ] 有真实头像
- [ ] 有"最近 1 个月"的 commit（让客户知道你在活跃）
- [ ] README 没有错别字（用 Grammarly / 飞书校对）
- [ ] 至少 1 个仓库有 ≥ 5 stars（可以发到技术群求 star，不要刷）
- [ ] 用 [GitHub Readme Activity Graph](https://github.com/Ashutosh00710/github-readme-activity-graph) 增加视觉吸引力

---

## 灵感参考（去 GitHub 看真实优秀案例）

搜索：`type:user followers:>100 location:china python freelance`

查看几位活跃中文自由职业者的个人页，看他们的：

- 排版风格
- 项目命名方式
- 联系方式呈现
- 社交链接整合

⚠️ 不要照抄，模仿排版即可，内容必须是你自己的真实项目。
