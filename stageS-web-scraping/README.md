# Stage S: Python 爬虫专精

> **阶段定位**: 垂直领域专精课程
> **课程编号**: S01-S09
> **建议学时**: 80 小时
> **前置要求**: Stage 0 (Python 基础) 完成
> **状态**: 🔶 骨架（课程结构已建立，内容待扩充）

---

## 📚 课程列表

| 编号 | 课程名称 | 时长 | 难度 | 状态 |
|------|----------|------|------|------|
| S01 | 前端基础 | 6h | ⭐☆☆☆☆ | ✅ |
| S02 | 网页数据解析 | 8h | ⭐⭐☆☆☆ | ✅ |
| S03 | 工业级爬虫 | 10h | ⭐⭐⭐☆☆ | ✅ |
| S04 | 自动化抓包 | 8h | ⭐⭐⭐☆☆ | ✅ |
| S05 | JavaScript 逆向基础 | 10h | ⭐⭐⭐⭐☆ | ✅ |
| S06 | JavaScript 逆向实战 | 12h | ⭐⭐⭐⭐⭐ | ✅ |
| S07 | App 逆向入门 | 10h | ⭐⭐⭐⭐☆ | ✅ |
| S08 | Frida 动态分析 | 10h | ⭐⭐⭐⭐⭐ | ✅ |
| S09 | 爬虫综合项目 | 8h | ⭐⭐⭐⭐⭐ | ✅ |

---

## 🎯 学习路径

```
L01-L10 (Stage 0)
    ↓
S01 → S02 → S03 ─┬→ S05 → S06
    ↓            │
S04              ↓
    ↓            │
S07 → S08 ──────┘
    ↓
S09 (综合项目)
```

---

## 📖 课程大纲

### S01: 前端基础

掌握 HTML 文档结构、CSS 选择器和 Chrome 开发者工具。

### S02: 网页数据解析

掌握 Requests 发送请求、Beautiful Soup 解析 HTML、XPath 定位元素。

### S03: 工业级爬虫

掌握 Scrapy 架构、Spider 开发、Item Pipeline、分布式爬虫。

### S04: 自动化抓包

掌握浏览器自动化，反检测技术，抓包工具。

### S05: JavaScript 逆向基础

掌握 JS 核心语法、加密算法基础、代码扣取技巧。

### S06: JavaScript 逆向实战

掌握 Token 生成、验证码破解、Hook 技术、AST 解混淆。

### S07: App 逆向入门

掌握 Android 架构，反编译技术，网络抓包、Python 调用 Java。

### S08: Frida 动态分析

掌握 Frida Hook、RPC 远程调用、SO 逆向、自动化脚本。

### S09: 爬虫综合项目

全站爬虫、分布式采集，反反爬策略、数据清洗与部署监控。

---

## 🔧 环境要求

```bash
# Python 版本
python >= 3.13

# 核心依赖（按需安装）
uv add requests beautifulsoup4 lxml
uv add scrapy scrapy-redis
uv add selenium playwright
uv add pyexecjs frida
uv add jpype1
```

---

## 📁 目录结构

```
stageS-web-scraping/
├── README.md              # 本文件
├── pyproject.toml        # 项目配置
└── lessons/
    ├── S01-frontend-basics/
    ├── S02-xpath-beautifulsoup/
    ├── S03-scrapy-framework/
    ├── S04-selenium-playwright/
    ├── S05-js-reverse-basics/
    ├── S06-js-reverse-advanced/
    ├── S07-app-reverse-basics/
    ├── S08-frida-dynamic/
    └── S09-scraping-project/
```

---

## 🔗 相关课程

| 课程 | 关联内容 |
|------|----------|
| L01-L10 | Python 基础语法 |
| L18 | 正则表达式 |
| L27, L34 | Web 框架（FastAPI） |

---

**最后更新**: 2026-08-02
