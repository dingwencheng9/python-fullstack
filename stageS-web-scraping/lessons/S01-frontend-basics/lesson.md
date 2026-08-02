# S01: 前端基础 — HTML/CSS/DOM

> **课程编号**: S01
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 6 小时
> **难度**: ⭐☆☆☆☆
> **前置课程**: L01 Python 核心语法

---

## 📚 课程概述

本课程为零基础爬虫学习者提供前端基础知识，帮助理解网页结构，为后续的网页解析打下坚实基础。

---

## 🎯 学习目标

1. 理解 HTML 文档结构
2. 掌握 CSS 选择器语法
3. 熟练使用 Chrome 开发者工具
4. 理解 DOM 树模型

---

## 📋 课程大纲

### Part 1: HTML 基础结构

### Part 2: CSS 选择器

### Part 3: 开发者工具

### Part 4: DOM 树结构

---

## 🔧 环境准备

```bash
# 本课程为纯前端知识，无需 Python 环境
# 推荐使用 Chrome DevTools 进行实践
```

---

## 📖 详细内容

### Part 1: HTML 基础结构

#### 1.1 什么是 HTML？

HTML（HyperText Markup Language）是用于描述网页结构的标记语言。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>网页标题</title>
</head>
<body>
    <h1>这是标题</h1>
    <p>这是段落</p>
    <a href="https://example.com">链接</a>
</body>
</html>
```

#### 1.2 常用 HTML 标签

| 标签 | 含义 | 示例 |
|------|------|------|
| `<div>` | 块级容器 | `<div class="container">` |
| `<span>` | 行内容器 | `<span class="highlight">` |
| `<a>` | 链接 | `<a href="url">` |
| `<img>` | 图片 | `<img src="url" alt="描述">` |
| `<ul>/<ol>` | 列表 | `<ul><li>项</li></ul>` |
| `<table>` | 表格 | `<table><tr><td>` |
| `<input>` | 输入框 | `<input type="text">` |
| `<button>` | 按钮 | `<button>点击</button>` |

#### 1.3 元素属性

```html
<!-- id 属性：唯一标识 -->
<div id="main-content">

<!-- class 属性：可重复，用于分组 -->
<div class="article card">

<!-- data-* 属性：自定义数据 -->
<div data-id="123" data-type="post">

<!-- href/src 属性：资源链接 -->
<a href="/about">关于</a>
<img src="/logo.png">
```

---

### Part 2: CSS 选择器

#### 2.1 基本选择器

```css
/* 标签选择器 */
p { color: blue; }

/* 类选择器 */
.highlight { background: yellow; }

/* ID 选择器 */
#header { height: 60px; }

/* 通配符选择器 */
* { margin: 0; }
```

#### 2.2 组合选择器

```css
/* 后代选择器（空格） */
.article p { line-height: 1.8; }

/* 子选择器（>） */
.menu > li { display: inline; }

/* 相邻兄弟（+） */
h1 + p { font-size: 18px; }

/* 通用兄弟（~） */
h2 ~ p { color: gray; }
```

#### 2.3 属性选择器

```css
/* 存在属性 */
[disabled] { opacity: 0.5; }

/* 属性值匹配 */
[type="text"] { border: 1px solid; }
[class^="btn-"] { /* btn- 开头 */ }
[href$=".pdf"] { /* .pdf 结尾 */ }
[class*="icon"] { /* 包含 icon */ }
```

---

### Part 3: 开发者工具

#### 3.1 Elements 面板

Chrome DevTools 的 Elements 面板用于查看和编辑 HTML/CSS。

**常用操作**：
1. 右键 → 检查（Inspect）查看元素
2. 双击元素可编辑 HTML
3. 右侧 Styles 面板可修改 CSS
4. Event Listeners 查看绑定事件

#### 3.2 Network 面板

用于分析网络请求，对爬虫至关重要。

**关键信息**：
- Request URL：请求地址
- Request Method：GET/POST
- Status Code：响应状态码
- Payload：POST 请求参数
- Preview/Response：响应内容

#### 3.3 复制 XPath/CSS 选择器

```javascript
// 在 Console 中获取元素
document.querySelector('.title')           // CSS 选择器
document.querySelector('//div[@class="title"]')  // XPath

// 右键菜单可直接复制
// Copy → Copy selector / Copy XPath
```

---

### Part 4: DOM 树结构

#### 4.1 DOM 是什么？

DOM（Document Object Model）将 HTML 解析为树形结构。

```
document
└── html
    └── head
    │   ├── title
    │   └── meta
    └── body
        ├── div.container
        │   ├── h1.title
        │   └── p.content
        └── ul.list
            ├── li.item (1)
            ├── li.item (2)
            └── li.item (3)
```

#### 4.2 节点关系

```javascript
// 父节点
element.parentNode

// 子节点
element.childNodes      // 包括文本节点
element.children        // 仅元素节点

// 兄弟节点
element.previousSibling
element.nextSibling

// 首尾子节点
element.firstChild
element.lastChild
```

#### 4.3 XPath 基础

XPath 是在 DOM 树中定位节点的语言。

```xpath
# 绝对路径
/html/body/div[1]/h1

# 相对路径
//div[@class='title']/h1

# 属性选择
//a[@href='/about']

# 文本匹配
//span[contains(text(), '价格')]

# 位置索引
//li[1]           # 第一个
//li[last()]      # 最后一个
//li[position() < 3]  # 前两个
```

---

## 📝 练习题

### 练习 1.1：分析电商商品页面结构

```markdown
目标：分析京东商品页面，提取商品名称、价格、店铺名
难度：⭐
提示：使用 Chrome 检查商品卡片元素结构
```

### 练习 1.2：编写 CSS 选择器

```markdown
目标：为指定元素编写 CSS 选择器
难度：⭐⭐
提示：掌握类、ID、属性选择器组合
```

### 练习 1.3：使用 XPath 定位元素

```markdown
目标：从网页中定位特定元素
难度：⭐⭐
提示：注意位置索引和文本匹配
```

---

## 📚 扩展阅读

- [MDN HTML 教程](https://developer.mozilla.org/zh-CN/docs/Learn/HTML)
- [MDN CSS 教程](https://developer.mozilla.org/zh-CN/docs/Learn/CSS)
- [XPath 教程 - W3Schools](https://www.w3schools.com/xml/xpath_intro.asp)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 理解 HTML 标签、属性、元素的关系
- [ ] 编写 CSS 选择器定位元素
- [ ] 使用 Chrome DevTools 分析网页结构
- [ ] 编写基本 XPath 表达式

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S02: 网页数据解析 — XPath 与 Beautiful Soup](../S02-xpath-beautifulsoup/) — 学习网页数据抓取基础

---
