# S05: JavaScript 逆向基础

> **课程编号**: S05
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 10 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: S01 前端基础, L16 正则表达式

---

## 📚 课程概述

当网页数据通过 JavaScript 动态生成、加密或混淆时，传统爬虫束手无策。本课程从零开始掌握 JavaScript 逆向工程核心技能，包括浏览器调试、代码混淆识别、加密算法分析和 Node.js 环境下的 JavaScript 执行。

---

## 🎯 学习目标

1. 掌握 Chrome DevTools 调试 JavaScript
2. 理解常见代码混淆技术与原理
3. 识别并分析加密算法（AES、DES、RSA 等）
4. 熟练使用 Python 执行 JavaScript 代码
5. 实现常见加密参数逆向
6. 掌握补环境技术与 hook 技术

---

## 📋 课程大纲

- [Part 1: JavaScript 调试基础](#part-1-javascript-调试基础)
- [Part 2: 代码混淆与识别](#part-2-代码混淆与识别)
- [Part 3: 加密算法分析](#part-3-加密算法分析)
- [Part 4: Python 执行 JavaScript](#part-4-python-执行-javascript)
- [Part 5: Hook 与补环境](#part-5-hook-与补环境)

---

## 🔧 环境准备

```bash
# 安装依赖
cd stageS-web-scraping/lessons/S05-js-reverse-basics
uv venv && source .venv/bin/activate
uv add selenium playwright
uv add pyexecjs  # JavaScript 执行引擎
uv add js2py    # 备选 JS 执行方案

# 浏览器环境
uv run playwright install chromium
```

---

## 📖 详细内容

### Part 1: JavaScript 调试基础

#### 1.1 Chrome DevTools 调试技巧

```javascript
// 断点类型
// 1. 代码行断点 - 在源代码面板点击行号
// 2. 条件断点 - 右键点击行号，输入条件表达式
// 3. 断点触发时执行
debugger;  // 代码中的断点

// 监听网络请求
// 1. Network 面板 → Filter → XHR/fetch
// 2. 右键请求 → Copy → Copy as cURL
// 3. 分析请求参数来源

// Console API
console.log('调试信息');
console.table({a: 1, b: 2});  // 表格输出
console.trace();  // 打印调用栈
```

#### 1.2 追踪数据来源

```javascript
// 场景：找到某个加密参数是如何生成的
// 步骤1：在 Network 中找到请求，记录请求 URL 和参数
// 步骤2：在 Sources 面板搜索参数名
// 步骤3：使用 "Add script to ignore list" 缩小范围

// 技巧：在 Console 中直接执行代码片段
// Copy → Copy as JavaScript 获取元素的完整属性访问路径

// 监控对象属性变化
const handler = {
    get: function(target, prop) {
        console.log(`Getting ${prop}:`, target[prop]);
        return target[prop];
    }
};
const proxiedObj = new Proxy(yourObject, handler);
```

#### 1.3 快速定位加密代码

```javascript
// 策略1：搜索关键字
// 常见加密关键字：encrypt, decrypt, encode, hash, cipher, crypto, sign, token, params, data

// 策略2：识别加密函数调用链
// 例如：发现请求参数中有一个 token 字段
// 1. 搜索 "token" 或 "sign"
// 2. 找到赋值语句
// 3. 追踪变量来源

// 策略3：搜索加密库引入
// 搜索：CryptoJS, jsencrypt, crypto, forge, bignumber
```

---

### Part 2: 代码混淆与识别

#### 2.1 常见混淆技术

| 混淆类型 | 特征 | 识别方法 |
|----------|------|----------|
| 变量名混淆 | a, b, c, _0x1234 | 函数名短且无意义 |
| 字符串加密 | `%5cx` 转义序列 | Console 输出正常但源码乱码 |
| 控制流平坦化 | switch-case 结构 | 分支跳转变量 |
| 死代码注入 | 无用函数调用 | 代码行数异常多 |
| 数组打乱 | 大型数组常量 | 二维数组拆分拼接 |

#### 2.2 字符串解密

```javascript
// 场景：源码中字符串被编码
// 常见模式：
// 1. 16进制编码: \x41\x42\x43
// 2. Unicode编码: ABC
// 3. Base64编码
// 4. 运行时拼接

// 简单解密函数
function decodeString(str) {
    // 处理 \\x 十六进制
    let decoded = str.replace(/\\x([0-9a-f]{2})/gi,
        (_, hex) => String.fromCharCode(parseInt(hex, 16)));

    // 处理 \\u Unicode
    decoded = decoded.replace(/\\u([0-9a-f]{4})/gi,
        (_, hex) => String.fromCharCode(parseInt(hex, 16)));

    return decoded;
}

// Console 快速解密
// 在 Console 中粘贴：decodeURIComponent('%E4%B8%AD%E6%96%87')
```

#### 2.3 反混淆工具

```javascript
// 推荐工具
// 1. Chrome DevTools 内置格式化
//    右键 → Format / Pretty Print

// 2. JSBeautifier (在线)
//    https://beautifier.io/

// 3. de4js (在线)
//    https://lelinhtinh.github.io/de4js/

// 4. AST Explorer
//    https://astexplorer.net/

// 手动还原控制流平坦化示例
// 观察 switch 变量的变化规律，构造状态映射表
```

---

### Part 3: 加密算法分析

#### 3.1 对称加密（DES/AES）

```javascript
// DES 加密特征
// 1. 使用 des 或者 crypto-js 中的 DES 方法
// 2. 密钥长度 8 字节
// 3. 常见模式：ECB, CBC, CTR

// AES 加密特征
// 1. 使用 aes 或 crypto-js 中的 AES 方法
// 2. 密钥长度：16/24/32 字节
// 3. 常见模式：CBC, CTR, GCM

// 典型加密调用
const encrypted = CryptoJS.AES.encrypt(
    plaintext,    // 待加密字符串
    key,          // 密钥
    {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
        iv: iv      // CBC 模式需要 IV
    }
);
```

#### 3.2 非对称加密（RSA）

```javascript
// RSA 加密特征
// 1. 使用 JSEncrypt、Forge 或 crypto-js
// 2. 密钥通常以 PEM 格式存储
// 3. 加密数据长度受限（密钥位数 / 8 - 11）

// 典型 RSA 加密流程
const publicKey = `-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5...
-----END PUBLIC KEY-----`;

const encryptor = new JSEncrypt();
encryptor.setPublicKey(publicKey);
const encrypted = encryptor.encrypt('plaintext');

// Python 端解密
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# 加载私钥
with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(), password=None, backend=default_backend()
    )

# 解密
decrypted = private_key.decrypt(
    base64.b64decode(encrypted),
    padding.PKCS1v15()
)
```

#### 3.3 MD5/SHA 哈希

```javascript
// 哈希特征
// 1. MD5 输出 32 位十六进制
// 2. SHA1 输出 40 位十六进制
// 3. SHA256 输出 64 位十六进制
// 4. 不可逆，用于签名校验

// 典型使用
const signature = CryptoJS.MD5(
    'appId' + timestamp + 'appSecret'
).toString().toUpperCase();

// 常见组合：时间戳 + 随机数 + 密钥 的哈希
```

#### 3.4 实战：逆向某网站签名算法

```javascript
// 场景：某电商 APP 请求需要 sign 参数
// 步骤1：找到 sign 生成代码
// 步骤2：分析参数构成
// sign = MD5(sorted(params) + appSecret).toUpperCase()

// 步骤3：构造 Python 复现
import hashlib
from typing import Dict

def generate_sign(params: Dict[str, str], app_secret: str) -> str:
    """复现签名算法"""
    # 1. 按字典序排序参数
    sorted_keys = sorted(params.keys())

    # 2. 拼接 key=value 格式
    parts = [f"{k}={params[k]}" for k in sorted_keys]
    sign_str = ''.join(parts) + app_secret

    # 3. MD5 哈希
    return hashlib.md5(sign_str.encode()).hexdigest().upper()
```

---

### Part 4: Python 执行 JavaScript

#### 4.1 PyExecjs

```python
import execjs

# 方法1：直接执行 JS 代码
ctx = execjs.compile("""
    function add(a, b) {
        return a + b;
    }
""")
result = ctx.call("add", 1, 2)
print(result)  # 3

# 方法2：执行外部 JS 文件
with open('crypto_utils.js', 'r') as f:
    ctx = execjs.compile(f.read())

# 调用加密函数
encrypted = ctx.call("encryptAES", "plaintext", "key1234567890")
```

#### 4.2 PyMiniRacer（高性能）

```python
from py_mini_racer import MiniRacer

ctx = MiniRacer()
ctx.eval("""
    function encrypt(data) {
        return CryptoJS.AES.encrypt(data, 'secret').toString();
    }
""")

result = ctx.call("encrypt", "hello")
print(result)
```

#### 4.3 Node.js 子进程

```python
import subprocess
import json

def exec_js(js_code: str, *args) -> str:
    """通过 Node.js 执行 JavaScript"""
    # 构建 Node.js 脚本
    node_script = f"""
    const result = (function() {{
        {js_code}
        return encrypt.apply(null, {json.dumps(args)});
    }})();
    console.log(JSON.stringify(result));
    """

    result = subprocess.run(
        ['node', '-e', node_script],
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

# 使用示例
js_code = """
function encrypt(text, key) {
    return CryptoJS.AES.encrypt(text, key).toString();
}
"""
result = exec_js(js_code, "plaintext", "secret_key")
```

#### 4.4 补环境技术

```python
import execjs
from pathlib import Path

def exec_js_file(js_file: str, func_name: str, *args):
    """执行外部 JS 文件中的函数"""
    ctx = execjs.external(Path(js_file).parent.as_posix())

    # 如果 JS 文件需要 window 等对象，手动注入
    ctx.exec(f"""
        global.window = global;
        global.document = {{ body: {{ clientWidth: 1920 }} }};
        global.navigator = {{ userAgent: 'Mozilla/5.0' }};
        global.location = {{ href: 'http://example.com' }};
    """)

    return ctx.call(func_name, *args)
```

---

### Part 5: Hook 与补环境

#### 5.1 浏览器 Hook

```javascript
// Hook CryptoJS AES 加密
(function() {
    const originalEncrypt = CryptoJS.AES.encrypt;
    CryptoJS.AES.encrypt = function() {
        console.log('AES Encrypt 参数:', arguments);
        console.trace('调用栈');
        return originalEncrypt.apply(this, arguments);
    };
})();

// Hook XHR/Fetch
const originalFetch = window.fetch;
window.fetch = function() {
    console.log('Fetch 请求:', arguments[0], arguments[1]);
    return originalFetch.apply(this, arguments);
};

// Hook console 对象
const originalLog = console.log;
console.log = function() {
    if (arguments[0] && typeof arguments[0] === 'string'
        && arguments[0].includes('encrypt')) {
        debugger;  // 触发断点
    }
    return originalLog.apply(this, arguments);
};
```

#### 5.2 Python Hook

```python
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

# 使用 Selenium 注入 Hook 脚本
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# 注入 Hook 脚本
hook_script = """
(function() {
    // 保存原始加密函数
    const originalEncrypt = window.encryptData;

    // Hook 替换
    window.encryptData = function() {
        console.log('Hook 触发:', arguments);
        debugger;
        return originalEncrypt.apply(this, arguments);
    };

    console.log('Hook 已安装');
})();
"""

driver.execute_script(hook_script)
```

#### 5.3 补环境方案

```python
# 场景：JS 代码依赖浏览器环境（window, document, navigator 等）
# 方案：使用 jsdom 或 happy-dom 模拟浏览器环境

# 方法1：使用 jsdom
import subprocess
import json

def exec_with_dom(js_code: str, *args):
    """使用 jsdom 补环境"""
    script = f"""
    const {{ JSDOM }} = require('jsdom');
    const dom = new JSDOM('', {{ url: 'http://example.com' }});
    const window = dom.window;
    global.window = window;
    global.document = window.document;
    global.navigator = window.navigator;

    // 加载用户代码
    {js_code}

    // 调用函数
    console.log(JSON.stringify(main.apply(null, {json.dumps(args)})));
    """

    result = subprocess.run(
        ['node', '-e', script],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# 方法2：使用 selenum 执行后提取变量
def extract_js_variable(driver, var_name: str):
    """从浏览器执行环境中提取变量"""
    script = f"""
    return JSON.stringify({var_name});
    """
    result = driver.execute_script(script)
    return json.loads(result)
```

#### 5.4 常见补环境常量

```python
# 常见需要补的环境变量
COMMON_SHIMS = """
// Window 对象
global.window = global;
global.self = global;
global.document = { cookie: '', querySelector: () => null };
global.navigator = {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    language: 'zh-CN',
    appVersion: '5.0'
};
global.location = {
    href: 'http://example.com',
    hostname: 'example.com',
    pathname: '/',
    search: ''
};
global.history = { pushState: () => {} };
global.matchMedia = () => ({ matches: false, media: '' });

// Crypto 对象
global.crypto = {
    getRandomValues: (arr) => {
        for (let i = 0; i < arr.length; i++) {
            arr[i] = Math.floor(Math.random() * 256);
        }
        return arr;
    }
};

// setTimeout/setInterval
global.setTimeout = (fn, ms) => 1;
global.setInterval = (fn, ms) => 1;
global.clearTimeout = () => {};
global.clearInterval = () => {};

// Image 对象
global.Image = class {{}};
global.HTMLElement = class {{}};
"""
```

---

## 📝 练习题

### 练习 5.1：基础加密逆向

```markdown
目标：逆向某网站登录接口的密码加密逻辑
难度：⭐⭐⭐
提示：
- 使用 DevTools 追踪加密函数
- 分析 CryptoJS AES 调用参数
- Python 复现加密流程
```

### 练习 5.2：签名算法逆向

```markdown
目标：逆向某 API 的签名生成算法
难度：⭐⭐⭐⭐
提示：
- 搜索 sign、signature、token 等关键字
- 分析参数拼接规则
- 验证签名计算结果
```

### 练习 5.3：补环境执行

```markdown
目标：成功执行依赖浏览器环境的 JS 代码
难度：⭐⭐⭐⭐
要求：
- 识别缺失的环境对象
- 实现完整的补环境方案
- 对比浏览器执行结果
```

---

## 📚 扩展阅读

- [CryptoJS 文档](https://cryptojs.gitbook.io/docs/)
- [JS逆向入门指南](https://book.tidesec.com/docs/reverse/)
- [AST Explorer](https://astexplorer.net/)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 使用 Chrome DevTools 调试 JavaScript
- [ ] 识别常见代码混淆技术
- [ ] 分析 AES/DES/RSA 等加密算法
- [ ] 使用 Python 执行 JavaScript 代码
- [ ] 实现常见加密参数的 Python 复现
- [ ] 使用 Hook 技术追踪加密调用
- [ ] 实现完整的浏览器环境补全

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S06: JavaScript 逆向实战](../S06-js-reverse-advanced/) — 真实网站逆向案例

---
