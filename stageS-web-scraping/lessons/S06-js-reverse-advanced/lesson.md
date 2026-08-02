# S06: JavaScript 逆向实战

> **课程编号**: S06
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 12 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: S05 JavaScript 逆向基础

---

## 📚 课程概述

本课程通过多个真实网站的逆向案例，系统性提升 JavaScript 逆向能力。涵盖主流电商、社交、资讯平台的加密逻辑分析，培养独立解决复杂逆向问题的能力。

---

## 🎯 学习目标

1. 掌握复杂混淆代码的静态分析技巧
2. 熟练运用动态调试追踪加密调用链
3. 实现 WebAssembly 模块的逆向分析
4. 掌握常见反调试技术的绕过方法
5. 完成多个真实网站的完整逆向流程
6. 构建可复用的逆向工具库

---

## 📋 课程大纲

- [Part 1: 混淆代码深度分析](#part-1-混淆代码深度分析)
- [Part 2: WebAssembly 逆向](#part-2-webassembly-逆向)
- [Part 3: 反调试技术绕过](#part-3-反调试技术绕过)
- [Part 4: 实战案例 - 电商平台](#part-4-实战案例---电商平台)
- [Part 5: 实战案例 - 社交平台](#part-5-实战案例---社交平台)
- [Part 6: 逆向工程最佳实践](#part-6-逆向工程最佳实践)

---

## 🔧 环境准备

```bash
# 安装依赖
cd stageS-web-scraping/lessons/S06-js-reverse-advanced
uv venv && source .venv/bin/activate

# 核心工具
uv add selenium playwright pyexecjs py-mini-racer
uv add requests httpx aiohttp

# Wasm 分析工具
uv add wasmtime  # Wasm 运行时

# 反编译工具
# pip install ghidra (可选，用于复杂 Wasm 分析)
```

---

## 📖 详细内容

### Part 1: 混淆代码深度分析

#### 1.1 控制流平坦化分析

```javascript
// 控制流平坦化特征
// 原始代码：
function original(x) {
    if (x > 0) return x * 2;
    else return -x;
}

// 混淆后（典型结构）：
function obfuscated(x) {
    let state = 0;
    let result;

    while (true) {
        switch (state) {
            case 0:
                if (x > 0) {
                    state = 1;  // true 分支
                } else {
                    state = 2;  // false 分支
                }
                break;
            case 1:
                result = x * 2;
                state = 3;
                break;
            case 2:
                result = -x;
                state = 3;
                break;
            case 3:
                return result;
        }
    }
}

// 还原技巧：
// 1. 追踪状态变量初始值和所有跳转
// 2. 还原真实控制流图
// 3. 使用 AST 分析器自动化还原
```

#### 1.2 字符串数组解密

```javascript
// 常见字符串数组混淆模式
const _0x4e21 = [
    'MTIz',           // base64
    '\\x65\\x6e\\x63', // hex escape
    '\x41\x42\x43',  // direct hex
    'a' + 'b' + 'c',  // 拼接
    String.fromCharCode(97, 98, 99),  // charCode
];

// 动态解密函数
function _0x1a2b(_0x3c4d) {
    return _0x4e21[_0x3c4d];
}

// 分析技巧：
// 1. 在 Console 中打印完整数组
// 2. 识别解密函数逻辑
// 3. 批量还原所有字符串
```

#### 1.3 自动化反混淆脚本

```python
import re
import subprocess

def beautify_js(js_code: str) -> str:
    """使用 prettier 格式化 JS"""
    result = subprocess.run(
        ['npx', 'prettier', '--stdin-filepath', 'input.js'],
        input=js_code,
        capture_output=True,
        text=True
    )
    return result.stdout

def unpack_jjdecode(js_code: str) -> str:
    """解包 jjdecode 混淆"""
    unpacker = """
    function jjdecode(encoded) {
        // jjdecode 解包逻辑
        var pattern = /<script[^>]*>(.*?)<\\/script>/gi;
        // ... 具体实现
        return decoded;
    }
    """
    # 实际使用已知的解包器实现
    return js_code

def extract_strings(js_code: str) -> list:
    """提取所有字符串常量"""
    # 匹配单引号、双引号、模板字符串
    patterns = [
        r'"([^"\\\\]|\\\\.)*"',
        r"'([^'\\\\]|\\\\.)*'",
        r'`([^`\\\\]|\\\\.)*`',
    ]

    strings = set()
    for pattern in patterns:
        matches = re.findall(pattern, js_code)
        strings.update(matches)

    return sorted(strings)
```

---

### Part 2: WebAssembly 逆向

#### 2.1 Wasm 基础概念

```javascript
// Wasm 模块识别
// 在 Network 面板中搜索 .wasm 文件
// 或在代码中搜索类似模式
const wasmCode = new Uint8Array([...]);
const wasmModule = new WebAssembly.Module(wasmCode);
const wasmInstance = new WebAssembly.Instance(wasmModule);

// 常见网站会加载 .wasm 文件来执行加密
// 例如：某些电商的价格计算、签名生成
```

#### 2.2 Wasm 逆向分析流程

```python
import wasmtime

def analyze_wasm(wasm_path: str):
    """分析 Wasm 模块"""
    # 使用 wasmtime 加载
    engine = wasmtime.Engine()
    module = wasmtime.Module.from_file(engine, wasm_path)

    # 导出函数
    print("导出函数：")
    for export in module.exports:
        if export.kind == wasmtime.ExternKind.FUNC:
            print(f"  - {export.name}")

    return module

def call_wasm_function(wasm_path: str, func_name: str, *args):
    """调用 Wasm 函数"""
    engine = wasmtime.Engine()
    module = wasmtime.Module.from_file(engine, wasm_path)

    # 创建实例
    linker = wasmtime.Linker(engine)
    linker.define_wasi()
    wasi = wasmtime.WasiConfig()
    module.set_wasi(wasi)

    instance = linker.instantiate(module)

    # 调用函数
    func = instance.exports()[func_name]
    return func(*args)
```

#### 2.3 内存分析与数据提取

```python
# 从 Wasm 实例中提取数据
def extract_wasm_strings(wasm_path: str) -> list:
    """从 Wasm 二进制中提取字符串"""
    with open(wasm_path, 'rb') as f:
        data = f.read()

    # Wasm 字符串通常以 '\0' 结尾
    # 在 .rodata 和 .data 段中查找
    import re

    # 查找可打印 ASCII 字符串
    strings = re.findall(rb'[ -~]{4,}\x00', data)
    return [s.decode('ascii', errors='ignore').strip('\x00')
            for s in strings]

# Hook Wasm 内存读写
def hook_wasm_memory():
    """在浏览器中 Hook Wasm 内存操作"""
    hook_script = """
    (function() {
        // 拦截 WebAssembly.instantiate
        const originalInstantiate = WebAssembly.instantiate;

        WebAssembly.instantiate = function(buffer, importObject) {
            console.log('Wasm 模块加载中...');

            return originalInstantiate.call(this, buffer, importObject)
                .then(result => {
                    console.log('Wasm 实例化完成');
                    console.log('导出函数:', Object.keys(result.instance.exports));

                    // Hook 导出函数
                    const exports = result.instance.exports;
                    for (const [name, value] of Object.entries(exports)) {
                        if (value instanceof WebAssembly.Function) {
                            const originalFunc = value;
                            // 替换为包装函数
                            exports[name] = function(...args) {
                                console.log(`调用 ${name}(${args.join(', ')})`);
                                const result = originalFunc.call(this, ...args);
                                console.log(`结果: ${result}`);
                                return result;
                            };
                        }
                    }

                    return result;
                });
        };
    })();
    """
    return hook_script
```

---

### Part 3: 反调试技术绕过

#### 3.1 常见反调试技术

| 技术 | 检测方法 | 绕过方式 |
|------|----------|----------|
| `debugger` 语句 | 定时执行 debugger | 使用代理替换或禁用 |
| 函数重定义 | 检查 toString() | 使用 Proxy 拦截 |
| 时间检测 | 记录代码执行时间 | 缓存时间函数结果 |
| 断点检测 | 检测代码修改 | 使用 Proxy 重写 |
| 控制台检测 | 检查 console 对象 | 替换 console 对象 |

#### 3.2 debugger 绕过

```javascript
// 方法1：重写 debugger（仅在 eval 中生效）
const originalDebugger = debugger;
debugger = function() { /* 空实现 */ };

// 方法2：使用 Proxy 拦截
const handler = {
    apply: function(target, thisArg, args) {
        // 不执行 debugger
        return target.apply(thisArg, args);
    }
};
debugger = new Proxy(debugger, handler);

// 方法3：Chrome DevTools 设置
// 1. Settings → Ignore List → 添加目标域名
// 2. 右键 debugger 行 → Never pause here
// 3. 使用 --js-flags="--inspect" 启动
```

#### 3.3 函数 toString 检测绕过

```javascript
// 检测代码
const isDebugged = someFunction.toString().length !== originalLength;

// 绕过方法：缓存原始 toString 结果
const originalFunctions = {};
const functionsToProtect = [encrypt, decrypt, sign];

functionsToProtect.forEach(fn => {
    originalFunctions[fn.name] = fn.toString();
});

// 或使用 Proxy 拦截所有函数的 toString
const FunctionProxy = new Proxy(Function.prototype.toString, {
    apply(target, thisArg, args) {
        // 如果是受保护的函数，返回缓存的 toString 结果
        if (thisArg && thisArg._originalToString) {
            return thisArg._originalToString;
        }
        return target.apply(thisArg, args);
    }
});
```

#### 3.4 定时器反调试绕过

```javascript
// 检测代码：使用 setInterval 检测调试器
setInterval(() => {
    debugger;  // 如果 debugger 被执行会触发断点
}, 1000);

// 绕过方法
// 1. 禁用定时器
const originalSetInterval = setInterval;
setInterval = () => 0;

// 2. 使用 Proxy 包装定时器
setInterval = new Proxy(setInterval, {
    apply(target, thisArg, args) {
        if (args[0].toString().includes('debugger')) {
            return 0;  // 不创建定时器
        }
        return target.apply(thisArg, args);
    }
});

// 3. Chrome DevTools: 右键 → Never pause here
```

#### 3.5 完整反反调试脚本

```javascript
// ==UserScript==
// @name         Anti-Debug Bypass
// @match        *://*/*
// ==/UserScript==

(function() {
    'use strict';

    // 1. 禁用 debugger
    const noop = () => {};
    Object.defineProperty(window, 'debugger', {
        get: noop,
        set: noop
    });

    // 2. 保护关键函数 toString
    const protectedFns = [];

    // 3. 禁用时间检测
    const originalDate = Date;
    const cachedNow = Date.now();
    Date.now = () => cachedNow;

    // 4. 禁用控制台检测
    Object.defineProperty(window, 'console', {
        value: console,  // 使用原生 console
        writable: false
    });

    // 5. 禁用 Error 检测
    const originalError = Error;
    Error = new Proxy(Error, {
        construct(target, args) {
            const error = Reflect.construct(target, args);
            // 过滤可能的检测错误
            return error;
        }
    });

    console.log('[Anti-Debug] 已激活');
})();
```

---

### Part 4: 实战案例 - 电商平台

#### 4.1 目标分析

```javascript
// 目标网站：某电商平台
// 目标接口：商品详情 API
// 关键参数：
// - token: 动态生成的认证令牌
// - sign: 请求签名，防止篡改
// - data: 加密的请求参数

// 分析步骤：
// 1. 找到 token 和 sign 生成逻辑
// 2. 分析加密算法和密钥来源
// 3. 复现 Python 实现
```

#### 4.2 逆向流程

```python
# 完整逆向案例

# Step 1: 抓包分析
# GET /api/product/detail?id=12345
# Headers:
#   token: eyJhbGciOiJIUzI1NiJ9...
#   sign: 8f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c
#   timestamp: 1699999999999

# Step 2: 定位代码
# 搜索关键字：token, sign, timestamp, encrypt

# Step 3: 分析加密逻辑（简化版）
# 伪代码：
# function generateToken(params) {
#     const timestamp = Date.now();
#     const data = JSON.stringify(params);
#     const encrypted = AES.encrypt(data, appKey);
#     const sign = MD5(encrypted + timestamp + appSecret).toUpperCase();
#     return {
#         token: base64(encrypted),
#         sign: sign,
#         timestamp: timestamp
#     };
# }

# Step 4: Python 复现
import hashlib
import base64
import json
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_token_ecommerce(params: dict, app_key: str, app_secret: str) -> dict:
    """生成电商平台 token"""
    # 序列化参数
    data = json.dumps(params, separators=(',', ':'))

    # AES 加密
    key = app_key.encode('utf-8')[:16].ljust(16, b'\0')
    iv = app_key.encode('utf-8')[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(data.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded)

    # Base64 编码
    token = base64.b64encode(encrypted).decode('utf-8')

    # 生成签名
    timestamp = str(int(time.time() * 1000))
    sign_str = token + timestamp + app_secret
    sign = hashlib.md5(sign_str.encode()).hexdigest().upper()

    return {
        'token': token,
        'sign': sign,
        'timestamp': timestamp
    }
```

#### 4.3 完整请求示例

```python
import httpx

async def crawl_ecommerce_product(product_id: int):
    """爬取电商商品详情"""
    app_key = "your_app_key"
    app_secret = "your_app_secret"

    # 构造请求参数
    params = {
        "id": product_id,
        "platform": "web",
        "version": "2.0"
    }

    # 生成认证信息
    auth = generate_token_ecommerce(params, app_key, app_secret)

    # 发送请求
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/product/detail",
            params={"id": product_id},
            headers={
                "token": auth['token'],
                "sign": auth['sign'],
                "timestamp": auth['timestamp']
            }
        )

        return response.json()
```

---

### Part 5: 实战案例 - 社交平台

#### 5.1 目标分析

```javascript
// 目标平台：某社交平台
// 目标接口：动态列表 API
// 关键特征：
// - 使用 RSA + AES 混合加密
// - 请求体完全加密
// - 有复杂的签名校验

// 加密流程分析：
// 1. 客户端生成随机 AES 密钥 (key)
// 2. 使用 RSA 公钥加密 AES 密钥
// 3. 使用 AES 加密请求体
// 4. 生成请求签名
```

#### 5.2 RSA + AES 混合加密实现

```python
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import base64
import hashlib
import json

def generate_social_headers(params: dict, rsa_public_key: str) -> dict:
    """生成社交平台请求头"""
    # 1. 生成随机 AES 密钥
    aes_key = get_random_bytes(32)  # 256 位

    # 2. RSA 加密 AES 密钥
    key = RSA.import_key(rsa_public_key)
    cipher_rsa = PKCS1_v1_5.new(key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

    # 3. AES 加密请求体
    iv = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)

    data = json.dumps(params, separators=(',', ':')).encode()
    padded_data = data + b'\x00' * (16 - len(data) % 16)
    encrypted_data = cipher_aes.encrypt(padded_data)

    # 4. 生成签名
    sign_data = encrypted_key_b64 + base64.b64encode(iv).decode()
    sign = hashlib.sha256(sign_data.encode()).hexdigest()

    return {
        'key': encrypted_key_b64,
        'iv': base64.b64encode(iv).decode(),
        'data': base64.b64encode(encrypted_data).decode(),
        'sign': sign
    }
```

---

### Part 6: 逆向工程最佳实践

#### 6.1 代码组织结构

```python
# 逆向工程项目结构
"""
reverse_project/
├── spiders/
│   ├── __init__.py
│   ├── base.py          # 基础爬虫类
│   ├── ecom_spider.py   # 电商平台爬虫
│   └── social_spider.py # 社交平台爬虫
├── crypto/
│   ├── __init__.py
│   ├── aes_utils.py     # AES 工具
│   ├── rsa_utils.py     # RSA 工具
│   ├── hash_utils.py    # 哈希工具
│   └── wasm_utils.py    # Wasm 分析工具
├── decrypt/
│   ├── __init__.py
│   ├── js_executor.py   # JS 执行器
│   └── browser_driver.py # 浏览器驱动
├── config/
│   └── targets.yaml     # 目标站点配置
└── main.py
"""
```

#### 6.2 可复用工具类

```python
class JSExecutor:
    """JavaScript 执行器封装"""

    def __init__(self, js_file: str = None):
        self.ctx = execjs.compile(open(js_file).read()) if js_file else execjs.get().eval

    def call(self, func_name: str, *args):
        """调用 JS 函数"""
        return self.ctx.call(func_name, *args)

    def exec_code(self, code: str) -> str:
        """执行 JS 代码"""
        return self.ctx.eval(code)

class CryptoHelper:
    """加密助手类"""

    @staticmethod
    def aes_encrypt(data: str, key: str, mode='CBC') -> str:
        """AES 加密"""
        key_bytes = key.encode()[:32].ljust(32, b'\0')
        iv = get_random_bytes(16)

        if mode == 'CBC':
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # ... 其他模式

        padded = pad(data.encode(), 16)
        encrypted = cipher.encrypt(padded)

        return base64.b64encode(iv + encrypted).decode()

    @staticmethod
    def md5(data: str) -> str:
        """MD5 哈希"""
        return hashlib.md5(data.encode()).hexdigest()

    @staticmethod
    def sha256(data: str) -> str:
        """SHA256 哈希"""
        return hashlib.sha256(data.encode()).hexdigest()
```

#### 6.3 逆向流程检查清单

```markdown
## 逆向工程检查清单

### 分析阶段
- [ ] 抓包分析请求结构
- [ ] 识别加密参数名称
- [ ] 确定目标加密函数位置
- [ ] 分析参数来源

### 逆向阶段
- [ ] 定位加密函数
- [ ] 分析加密算法类型
- [ ] 提取密钥/盐值
- [ ] 理解加密流程
- [ ] 复现加密逻辑

### 验证阶段
- [ ] Python 实现对比测试
- [ ] 多组数据验证
- [ ] 边界条件测试
- [ ] 性能优化

### 维护阶段
- [ ] 添加异常处理
- [ ] 实现重试机制
- [ ] 添加日志记录
- [ ] 监控加密逻辑变化
```

---

## 📝 练习题

### 练习 6.1：控制流平坦化还原

```markdown
目标：分析并还原一个控制流平坦化的函数
难度：⭐⭐⭐⭐
提示：
- 绘制状态转换图
- 识别真实控制流
- 还原为可读代码
```

### 练习 6.2：电商签名逆向

```markdown
目标：完成一个电商平台的完整逆向
难度：⭐⭐⭐⭐⭐
要求：
- 定位所有加密逻辑
- Python 复现 100% 一致
- 成功爬取 100+ 商品
```

### 练习 6.3：反调试绕过

```markdown
目标：绕过某网站的全部反调试机制
难度：⭐⭐⭐⭐
提示：
- 逐步分析各种检测
- 编写自动化绕过脚本
- 验证绕过有效性
```

---

## 📚 扩展阅读

- [Wasm 逆向工程入门](https://github.com/danlimi/wasm-reverse)
- [控制流平坦化原理](https://blog.checkpoint.com/2019/07/08/unpacking-control-flow-flattening/)
- [逆向工程工具集](https://github.com/好奇心日报/awesome-reverse-engineering)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 深度分析复杂混淆代码
- [ ] 使用 Wasmtime 分析 WebAssembly 模块
- [ ] 绕过常见反调试技术
- [ ] 完成多个真实网站的完整逆向流程
- [ ] 构建可复用的逆向工具库
- [ ] 独立解决未知网站的逆向问题

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S07: App 逆向入门](../S07-app-reverse-basics/) — Android 应用分析与逆向

---
