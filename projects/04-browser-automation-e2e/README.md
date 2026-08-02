# 项目 4: Browser Automation E2E — 用户视角端到端测试

> **难度**: ⭐⭐⭐⭐ | **预计时间**: 8h | **技术**: Playwright + pytest

## 项目目标

用真实浏览器行为验证 HTMX 页面、Capstone 页面和 SSE/流式交互，补齐测试金字塔的最上层。

```
用户点击 → 页面交互 → 网络请求/DOM更新 → 截图/Trace → 断言
```

## 为什么用 Playwright？

| 能力      | Selenium   | Playwright |
| --------- | ---------- | ---------- |
| 自动等待  | 弱         | 强         |
| Trace     | 需额外配置 | 原生       |
| 截图/视频 | 可做       | 原生       |
| CI 体验   | 一般       | 好         |
| 教学成本  | 高         | 低         |

本项目主推 Playwright。Selenium 作为历史对比，不作为主实现。

## 文件结构

```
projects/04-browser-automation-e2e/
├── pages/
│   ├── htmx_demo.html
│   └── capstone_demo.html
├── tests/
│   ├── test_static_pages.py
│   ├── test_interactions.py
│   └── test_artifacts.py
├── artifacts/
└── README.md
```

## 快速开始

```bash
pip install pytest beautifulsoup4
python -m pytest tests/ -v
```

> 若安装 Playwright：`pip install playwright && playwright install chromium`，可扩展为真实浏览器测试。

## 测试目标

- HTMX 属性是否正确
- 表单、搜索、结果区域是否完整
- Capstone 页面是否具备文档导入与问答入口
- 截图/报告目录是否存在
- 页面无空链接、无重复 id

## 完成标准

- [ ] 10+ 测试通过
- [ ] 所有页面可离线解析
- [ ] artifacts/ 可保存截图或测试报告
- [ ] 不依赖外部服务

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

### 运行测试

```bash
# 运行全部 E2E 测试
pytest tests/ -v

# 运行单个测试（项目实际只有 static_pages / interactions / artifacts 三组）
pytest tests/test_static_pages.py -v
pytest tests/test_interactions.py -v
pytest tests/test_artifacts.py -v
```

### 查看报告

```bash
# 生成 HTML 报告（需先 pip install pytest-html）
pytest --html=report.html
```
