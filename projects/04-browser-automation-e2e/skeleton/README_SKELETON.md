# 项目 4 Browser Automation E2E 骨架代码使用指南

## 🎯 使用方法

骨架代码是为了帮助你分步实现 E2E 测试，关键位置已经留好`TODO`注释，你只需要按照提示补全代码即可。

### 📋 文件结构

```
skeleton/
├── README_SKELETON.md          # 本文件
├── pages/
│   ├── base_page_skeleton.py  # 基础 Page Object 骨架
│   ├── htmx_page_skeleton.py  # HTMX 页面骨架
│   └── capstone_page_skeleton.py # AI全栈应用页面骨架
└── tests/
    ├── test_static_skeleton.py    # 静态页面测试骨架
    ├── test_interaction_skeleton.py # 交互测试骨架
    └── test_screenshot_skeleton.py # 截图测试骨架
```

### 🚀 练习步骤

建议按顺序完成：

#### 第一步：Page Object 模式

1. `pages/base_page_skeleton.py` - 实现基础页面对象，封装通用操作
2. `pages/htmx_page_skeleton.py` - HTMX 演示页面封装
3. `pages/capstone_page_skeleton.py` - AI全栈应用页面封装

#### 第二步：静态测试

1. `tests/test_static_skeleton.py` - 测试页面基本结构
2. 检查标题、主要元素存在
3. 检查没有重复 id，没有空链接

#### 第三步：交互测试

1. `tests/test_interaction_skeleton.py` - 测试用户交互
2. 测试表单填写、按钮点击
3. 测试 HTMX 异步更新

#### 第四步：截图测试

1. `tests/test_screenshot_skeleton.py` - 截图对比测试
2. 视觉回归测试基础

### ✅ 验证方法

写完后和`pages/`、`tests/`目录下的参考实现对比：

```bash
# 安装 Playwright
pip install playwright
playwright install chromium

# 运行测试
pytest tests/ -v --headed
```

### 💡 知识点提示

**涉及知识点：**

- Playwright API 使用
- Page Object 设计模式
- 元素定位和选择器
- 网络等待和超时处理
- 截图和视觉对比
- CI/CD 中运行 E2E

### 🎯 挑战练习

完成基础功能后，可以尝试扩展：

1. 添加视觉差异对比（像素级）
2. 增加登录流程测试
3. 测试 SSE 流式输出
4. 使用 pytest-xdist 并行运行测试
