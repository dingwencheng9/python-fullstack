# Freelance Demo · 一键演示作品集

> **接单时给客户看的"1 个 URL 看完全部能力"。**
>
> 把项目 1（爬虫）+ 项目 3（数据分析）+ 项目 2（AI 问答）串成一条端到端流程：
> **网址 → 自动采集 → 清洗分析 → AI 问答**

---

## 30 秒看懂

```
┌────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  你提供URL │ ──→ │ 1. 合规爬虫  │ ──→ │ 2. 数据分析   │ ──→ │ 3. AI 问答    │
│            │     │   去重清洗   │     │   生成报告    │     │   RAG 检索    │
└────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                        ↓                       ↓                       ↓
                   scraped.json           report.md               http://:8000
```

**输出 3 件交付物**：

1. 📄 **scraped.json** — 结构化的爬取数据
2. 📊 **report.md** — Markdown 分析报告（可一键转 HTML）
3. 🤖 **localhost:8000** — 可对话的 AI 知识库

---

## 一键启动

### 前置条件

```bash
# 1. uv 工具（Python 包管理）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装本仓库 web + ai 可选依赖（首次执行需要）
cd <仓库根目录>
uv sync --extra web --extra ai
```

### 完整流程（默认演示）

```bash
bash projects/freelance-demo/run.sh
```

会用 `https://example.com` 当起始 URL 跑完整流程。

### 自定义 URL

```bash
bash projects/freelance-demo/run.sh --url https://docs.python.org/3.13/ --max-pages 10
```

### 分阶段运行

```bash
# 只跑爬虫
bash projects/freelance-demo/run.sh --skip-report --skip-ai

# 只跑分析（用已有 scraped.json）
bash projects/freelance-demo/run.sh --skip-crawl --skip-ai

# 只启动 AI 问答（用已有 scraped.json）
bash projects/freelance-demo/run.sh --skip-crawl --skip-report
```

### 不安装 web/ai 依赖时如何最小演示

```bash
# 只跑「爬虫 + 分析」(不需要 fastapi/openai)
bash projects/freelance-demo/run.sh --skip-ai
```

---

## 离线快速演示（用样例数据）

仓库已带一份样例数据 `sample_data/scraped.json`，**无需联网**就能跑分析+问答两步：

```bash
# 用样例数据生成报告
PYTHONPATH=projects/03-data-intelligence-pipeline \
  uv run python projects/freelance-demo/run_pipeline.py \
    --input projects/freelance-demo/sample_data/scraped.json \
    --output projects/freelance-demo/sample_data/report.md

# 启动 AI 问答（需要 fastapi）
PYTHONPATH=projects/02-ai-fullstack-capstone \
  uv run python projects/freelance-demo/run_ai.py \
    --documents projects/freelance-demo/sample_data/scraped.json
```

---

## 输出目录结构

```
output/
├── scraped.json    # 项目 1 输出：原始爬取数据
└── report.md       # 项目 3 输出：Markdown 分析报告
```

`report.md` 示例：

```markdown
# 数据智能流水线报告

总页面数: 3
总词数: 118

## 来源统计

| source      | pages | avg_words | python_pages |
| ----------- | ----- | --------- | ------------ |
| example.com | 3     | 39.3      | 2.0          |

## Top 页面

...
```

---

## 接单视频脚本（60 秒）

录这段当 demo 视频：

```
[0-5 秒]
"我用 Python 给您做一个端到端的数据 + AI 工作流，60 秒看完。"
[屏幕：终端 + 浏览器分屏]

[5-15 秒]
"输入一个网址 ..."
$ bash run.sh --url https://docs.python.org/3.13/ --max-pages 5
[屏幕：实时显示爬取进度]

[15-30 秒]
"系统自动合规爬取（尊重 robots.txt + 限速 + 跳过敏感路径）"
[屏幕：日志高亮显示 robots check / rate limit]

[30-40 秒]
"清洗去重，生成 Markdown 报告 ..."
[屏幕：cat output/report.md，看到表格]

[40-55 秒]
"启动 AI 问答，可以直接对刚爬的内容提问 ..."
[屏幕：浏览器打开 http://localhost:8000，输入"Python 3.13 有哪些新特性？"]
"流式回答，含引用回链 ..."

[55-60 秒]
"全程 < 5 分钟。微信加我 [xxx]，给您做定制版。"
[屏幕：你的联系方式 + GitHub URL]
```

---

## 部署到 Railway / Fly.io（让客户能直接访问）

### 推荐方案：Railway 免费层

```bash
# 1. 安装 Railway CLI
npm i -g @railway/cli

# 2. 登录
railway login

# 3. 在仓库根目录初始化
railway init

# 4. 部署
railway up

# 5. 拿到公网 URL，挂到你的 GitHub README / Fiverr 套餐
```

### Fly.io（带免费域名）

```bash
flyctl launch --no-deploy
flyctl secrets set OPENAI_API_KEY=sk-xxx  # 可选
flyctl deploy
```

⚠️ **注意**：免费层会休眠，首次访问需 30 秒预热。在你的演示链接旁标注："首次访问需 30 秒，请耐心等待"。

---

## 如何用这个 Demo 接单

### 场景 1：客户问"你能做爬虫吗"

> "可以，看下这个 demo：[URL]
> 我把爬虫 + 数据分析 + AI 问答打通了，您可以直接试。
> 您具体需要爬什么网站？我报个价。"

### 场景 2：客户问"你能做数据分析吗"

> "可以，看下这个 demo：[URL]
> 您的数据如果是 JSON / CSV / 数据库，我可以适配进来。
> 输出可以是 Markdown 报告 / HTML 看板 / Streamlit 界面。"

### 场景 3：客户问"你能做 AI 知识库吗"

> "可以，看下这个 demo：[URL]
> 这是一个能爬网站 + 自动建知识库的雏形。
> 您的数据如果是 PDF / Word / Excel，我可以加个文档解析层。
> 私有化部署也支持，含 Mock LLM 离线兜底。"

### 场景 4：你主动找客户（cold outreach）

> "[姓名] 您好，我做了一个 [行业垂直] 的数据 + AI 系统：
>
> - 自动采集竞品公开信息
> - 自动生成周报
> - 内部员工可对话查询
>
> Demo：[URL]
>
> 您方便的话我送您一份免费的 [行业] 案例分析？"

---

## 这套 Demo 已打通的技术点

来自 60 节课程 + 4 个综合项目：

| 阶段     | 关键技术                              | 来源课程    |
| -------- | ------------------------------------- | ----------- |
| 爬虫     | requests / BeautifulSoup / robots.txt | L18, 项目 1 |
| 限速     | 滑动窗口 + 退避策略                   | 项目 1, L24 |
| 去重     | 集合 + URL 规范化                     | L05         |
| 数据清洗 | 正则 + Pandas                         | L18, L43    |
| 特征     | 词数 / 域名提取                       | L46         |
| 报告     | Markdown 表格 + 文件输出              | L08, L47    |
| RAG      | 文本分块 + 向量化 + 余弦相似度        | L51         |
| 检索     | 内存向量库                            | L51, 项目 2 |
| Agent    | LangGraph 状态机                      | L54, L57    |
| Web      | FastAPI + Pydantic v2                 | L29         |
| 实时     | SSE 流式输出                          | L37         |
| UI       | HTMX + Jinja2                         | L39         |
| 测试     | pytest + 覆盖率                       | L19, 全程   |
| 部署     | Docker Compose                        | L36         |

---

## 故障排查

### "uv: command not found"

没装 uv：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "ModuleNotFoundError: No module named 'fastapi'"

没装 web extra：

```bash
uv sync --extra web --extra ai
```

### "采集失败：连接超时"

- 检查网络
- 加 `--max-pages 3` 限制页数试试
- 该网站可能反爬，用 `--url https://example.com` 先验证流程

### "AI 问答没响应"

- 检查端口 8000 是否被占用：`lsof -i :8000`
- 默认用 Mock LLM，不需要 OpenAI Key
- 如果想用真实 LLM，设环境变量 `OPENAI_API_KEY=sk-xxx`

---

## 配套阅读

- 兼职计划：[`extensions/freelance-toolkit/`](../../extensions/freelance-toolkit/) 自由职业工具包
- 工具包：[`extensions/freelance-toolkit/`](../../extensions/freelance-toolkit/)
- 各项目原型：[项目 1](../01-web-scraper/) [项目 2](../02-ai-fullstack-capstone/) [项目 3](../03-data-intelligence-pipeline/)
