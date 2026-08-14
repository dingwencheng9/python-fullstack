# L35: HTMX + FastAPI 全栈开发

> 🔧 **Stage 3 Web 基础核心课** | ⏱️ 4 小时 | ⭐⭐⭐⭐☆（高级）  
> 前置课程：L27 FastAPI、L32 SSE、Jinja2 模板基础  
> 关键词：HTMX、无刷新交互、OOB 更新、客户端渲染、服务器渲染、渐进增强、交互式表单

## 📋 课程定位

HTMX 让你用"服务器端思维"构建交互式 Web 应用。不需要复杂的 JavaScript 框架，本课程教你用纯 Python 构建现代交互体验。

## 🎯 学习目标

完成本课后，你将能够：

- [ ] 理解 HTMX 的核心理念与适用场景
- [ ] 使用 HTMX 属性实现无刷新交互
- [ ] 使用 OOB 更新处理多区域更新
- [ ] 实现服务端渲染与客户端渲染的权衡
- [ ] 设计 HTMX 友好的 REST API
- [ ] 实现复杂交互场景（搜索建议、无限滚动、表单验证）
- [ ] 结合 SSE 实现实时更新

## 📂 课程结构

```text
L35-htmx/
├── README.md              # 课程说明与学习路径
├── lesson.md             # 详细课程讲义
├── examples/
│   ├── 01_basic_htmx.py       # HTMX 基础
│   └── 02_crud_operations.py  # CRUD 操作
├── exercises/             # 练习题
├── solutions/            # 参考答案
└── tests/               # 单元测试
```

## 🚀 快速开始

```bash
cd stage3-web-basics/lessons/L35-htmx
uv sync
uv run pytest tests -v
uv run uvicorn examples.htmx_app:app --reload
```

## 🔗 下一步

完成本课后继续学习：

- [P04: Web 基础综合项目](../../stage3-web-basics/README.md)
- [L36: 异步背压机制](../L36-async-backpressure/README.md)

> 📖 **里程碑**：P04 是 Stage 3 的综合项目，将整合 HTTP、FastAPI、SQL、Docker 和实时通信知识。
