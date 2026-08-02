# 项目联动使用指南

## 🎯 完整链路 Demo

现在四个项目已经打通，你可以完成从数据采集到AI问答的完整流程：

```
项目1 (Web Scraper) 采集数据 → 项目3 (Data Pipeline) 分析 → 项目2 (AI Fullstack) 构建问答助手 → 项目4 (E2E Testing) 测试
```

---

## 🚀 快速开始

### 1. 采集数据（项目1）

```bash
cd projects/01-web-scraper
pip install -r requirements.txt

# 采集Python官方文档，导出JSON
python main.py \
  --url https://docs.python.org/zh-cn/3/tutorial/ \
  --max-pages 10 \
  --output python_docs.json

# 你会得到:
# - python_docs.json: 采集到的页面数据
# - python_docs.schema.json: 数据格式说明
```

### 2. 数据分析（项目3）

```bash
cd ../03-data-intelligence-pipeline
pip install -r requirements.txt

# 直接处理项目1的输出，生成分析报告
python -m pipeline.web_scraper_adapter ../01-web-scraper/python_docs.json ./reports/

# 你会得到:
# reports/python_docs_report.md: 完整的数据分析报告
```

### 3. 构建AI问答助手（项目2）

```bash
cd ../02-ai-fullstack-capstone
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload
```

现在访问 http://localhost:8000 就可以使用AI助手了：

1. 导入刚才采集的Python文档内容
2. 提问关于Python教程的问题
3. 体验SSE流式回答效果

### 4. E2E测试（项目4）

```bash
cd ../04-browser-automation-e2e
pip install -r requirements.txt

# 运行静态页面测试
pytest tests/ -v

# 安装Playwright运行真实浏览器测试
pip install playwright
playwright install chromium
pytest tests/ -v --browser chromium
```

---

## 📊 各项目增强说明

### ✅ 项目1增强

- 新增`main.py`入口，支持命令行参数
- 支持JSON/CSV双格式导出
- 自动导出JSON Schema，便于下游系统对接
- 增加采集统计信息输出

### ✅ 项目3增强

- 新增`web_scraper_adapter.py`适配器，原生支持项目1格式
- 一行命令即可处理项目1的输出并生成报告
- 自动字段映射和衍生字段增强

### ✅ 项目2增强

- 集成**LangGraph StateGraph**工作流，实现真实Agent逻辑
- 工作流包含：检索→生成回答→质量检查→条件路由
- 不确定时自动要求用户澄清
- 全新HTMX前端，美观易用
- 支持知识库状态实时显示
- 导入文档后自动刷新统计

### ✅ 项目4增强

- 基础静态页面测试已经完善
- 支持真实Playwright浏览器测试

---

## 🔧 技术亮点

### 1. 无第三方依赖的RAG检索

- 不需要OpenAI API Key即可运行
- 内置词频重叠检索算法
- 轻量高效，适合教学场景

### 2. LangGraph状态机工作流

- 清晰的节点职责分离
- 条件路由实现智能分支
- 易于扩展更多功能（工具调用、多Agent等）

### 3. 现代化HTMX前端

- 零JavaScript手写代码
- 流畅的流式回答体验
- 实时状态更新
- 响应式设计，移动端友好

---

## 🎓 教学延伸建议

### 基础练习

1. 用项目1采集你感兴趣的网站
2. 用项目3分析采集到的数据
3. 将数据导入项目2，构建专属知识助手
4. 用项目4测试你的应用

### 进阶挑战

1. 给项目1增加异步采集能力（参考Stage 2 L24异步编程）
2. 给项目2增加向量数据库支持（参考Stage 4 L51 RAG）
3. 给项目2增加多Agent编排（参考Stage 5 L57多智能体）
4. 部署整个系统到云服务（参考Stage 5 L59部署）
