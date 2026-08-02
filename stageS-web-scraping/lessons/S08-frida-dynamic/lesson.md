# S08: Frida 动态分析

> **课程编号**: S08
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 10 小时
> **难度**: ⭐⭐⭐⭐⭐
> **前置课程**: S07 App 逆向入门

---

## 📚 课程概述

Frida 是移动端逆向工程的瑞士军刀，提供强大的动态插桩能力。本课程深入讲解 Frida 的使用技巧，包括 Java 层 Hook、Native 层追踪、脚本编写和自动化分析，掌握高级 App 逆向技能。

---

## 🎯 学习目标

1. 掌握 Frida 环境配置与基础使用
2. 熟练使用 Frida 进行 Java 层 Hook
3. 实现 Native 层 (ARM) 函数追踪
4. 编写自动化 Frida 脚本
5. 绕过常见 App 保护机制
6. 实现加密算法的动态提取

---

## 📋 课程大纲

- [Part 1: Frida 基础与环境](#part-1-frida-基础与环境)
- [Part 2: Java 层 Hook](#part-2-java-层-hook)
- [Part 3: Native 层追踪](#part-3-native-层追踪)
- [Part 4: 高级 Hook 技术](#part-4-高级-hook-技术)
- [Part 5: 自动化与脚本编写](#part-5-自动化与脚本编写)

---

## 🔧 环境准备

```bash
# Frida 安装
pip install frida frida-tools

# 验证安装
frida --version

# 启动 Frida Server (Android)
# 1. 下载对应版本的 frida-server
# https://github.com/frida/frida/releases
# 例如: frida-server-16.x.x-android-arm64.xz

# 2. 推送到设备
adb push frida-server /data/local/tmp/
adb shell "chmod 777 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# 3. 端口转发
adb reverse tcp:27042 tcp:27042

# 4. 测试连接
frida-ps -U
```

---

## 📖 详细内容

### Part 1: Frida 基础与环境

#### 1.1 Frida 工作原理

```
┌─────────────────────────────────────────────────────────┐
│                    Host (PC)                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ frida CLI   │    │ frida-py    │    │ frida-gui   │ │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘ │
│         │                  │                  │         │
│         └────────────────┬┴─────────────────┘         │
│                          │                            │
│                   ┌──────▼──────┐                     │
│                   │ frida-helper │                     │
│                   │   (进程)     │                     │
│                   └──────┬──────┘                     │
└──────────────────────────┼────────────────────────────┘
                           │ TCP:27042
┌──────────────────────────┼────────────────────────────┐
│                    Device (手机)                       │
│                   ┌──────▼──────┐                     │
│                   │ frida-server │                     │
│                   │   (Daemon)   │                     │
│                   └──────┬──────┘                     │
│                          │                            │
│         ┌────────────────┼────────────────┐           │
│         │                │                │           │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐  │
│  │   App A     │  │   App B     │  │   App C     │  │
│  │ (注入代码)   │  │             │  │             │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└───────────────────────────────────────────────────────┘
```

#### 1.2 基础使用

```bash
# 列出设备上的进程
frida-ps -U              # USB 连接
frida-ps -R              # 远程连接
frida-ps -Uai            # 显示应用名称

# 附加到进程
frida -U -f com.example.app          # 启动并附加
frida -U com.example.app              # 附加到已运行进程
frida -U -l script.js com.example.app  # 加载脚本

# 常用选项
-U    # USB 设备
-f    # 指定启动的应用
-l    # 加载 JS 脚本
-o    # 输出到文件
--no-pause  # 不暂停应用
```

#### 1.3 Python API 基础

```python
import frida
import sys

# 连接到设备
device = frida.get_usb_device()
print(f"设备: {device.name}")
print(f"系统: {device.type}")

# 附加到进程
pid = device.spawn(["com.example.app"])
session = device.attach(pid)

# 加载脚本
script_code = """
RPC.exports = {
    hello: function() {
        return "Hello from Frida!";
    }
};
"""

script = session.create_script(script_code)
script.on('message', lambda msg, data: print(f"[+] {msg}"))
script.load()

# 调用导出的函数
rpc_exports = session.exports
print(rpc_exports.hello())

# 保持脚本运行
sys.stdin.read()
```

---

### Part 2: Java 层 Hook

#### 2.1 基础 Hook

```javascript
// hook基础.js
// Hook Java 类的方法

Java.perform(function() {
    // 找到目标类
    var MainActivity = Java.use("com.example.app.MainActivity");

    // Hook 实例方法
    MainActivity.onCreate.implementation = function(bundle) {
        console.log("[*] onCreate called!");
        console.log("[*] Bundle: " + bundle);

        // 调用原始方法
        this.onCreate(bundle);
    };

    // Hook 静态方法
    var StringUtils = Java.use("com.example.app.utils.StringUtils");
    StringUtils.isEmpty.overload("java.lang.String").implementation = function(str) {
        console.log("[*] isEmpty called with: " + str);
        return this.isEmpty(str);
    };
});
```

#### 2.2 方法重载处理

```javascript
Java.perform(function() {
    var CryptoUtils = Java.use("com.example.app.crypto.CryptoUtils");

    // 方式1：匹配特定重载
    CryptoUtils.encrypt.overload("java.lang.String").implementation = function(str) {
        console.log("[*] encrypt(String) called");
        return this.encrypt(str);
    };

    CryptoUtils.encrypt.overload("byte[]", "java.lang.String").implementation = function(data, key) {
        console.log("[*] encrypt(byte[], String) called");
        console.log("[*] Data length: " + data.length);
        console.log("[*] Key: " + key);
        return this.encrypt(data, key);
    };

    // 方式2：列出所有重载
    var overloads = CryptoUtils.encrypt.overloads;
    console.log("[*] encrypt overloads: " + overloads.length);

    // 方式3：通用处理（所有重载）
    CryptoUtils.decrypt.implementation = function() {
        var args = Array.prototype.slice.call(arguments);
        console.log("[*] decrypt called with " + args.length + " args");
        console.log("[*] Args: " + JSON.stringify(args.map(String)));
        return this.decrypt.apply(this, arguments);
    };
});
```

#### 2.3 修改返回值与参数

```javascript
Java.perform(function() {
    var UserManager = Java.use("com.example.app.UserManager");

    // 修改返回值
    UserManager.isVipUser.implementation = function() {
        console.log("[*] isVipUser called, returning true");
        return true;  // 强制返回 true
    };

    // 修改参数
    UserManager.getUserLevel.implementation = function(userId) {
        console.log("[*] getUserLevel called with: " + userId);
        var fakeUserId = "vip_user_123";  // 替换 userId
        return this.getUserLevel(fakeUserId);
    };

    // 使用 $new 创建实例
    var StringBuilder = Java.use("java.lang.StringBuilder");
    var sb = StringBuilder.$new();
    sb.append("Hello");
    sb.append(" ");
    sb.append("Frida");
    console.log("[*] StringBuilder result: " + sb.toString());
});
```

#### 2.4 追踪加密调用

```javascript
// 完整加密追踪示例
Java.perform(function() {

    // Hook AES 加密
    var Cipher = Java.use("javax.crypto.Cipher");

    Cipher.doFinal.overload("[B").implementation = function(data) {
        var result = this.doFinal(data);

        // 打印调用栈
        console.log("[=== AES doFinal ===]");
        console.log("[*] Input: " + bytesToHex(data));
        console.log("[*] Output: " + bytesToHex(result));
        console.log("[*] Mode: " + this.getAlgorithm());

        // 打印 key 和 IV
        try {
            var key = this.getKey();
            var iv = this.getIV();
            console.log("[*] Key: " + (key ? bytesToHex(key) : "null"));
            console.log("[*] IV: " + (iv ? bytesToHex(iv) : "null"));
        } catch (e) {
            console.log("[!] Error getting key/iv: " + e);
        }

        // 打印调用栈
        console.log("[*] Stack trace:");
        var stack = Java.use("android.util.Log").getStackTraceString(
            Java.use("java.lang.Exception").$new()
        );
        console.log(stack);

        return result;
    };

    // 辅助函数
    function bytesToHex(bytes) {
        if (!bytes) return "null";
        var hex = "";
        for (var i = 0; i < Math.min(bytes.length, 64); i++) {
            hex += bytes[i].toString(16).padStart(2, "0");
        }
        if (bytes.length > 64) hex += "...";
        return hex;
    }
});
```

---

### Part 3: Native 层追踪

#### 3.1 Native 函数基础

```javascript
// Hook Native 函数
// 适用于 .so 库中的 C/C++ 函数

Interceptor.attach(Module.findBaseAddress("libnative-lib.so"), {
    onEnter: function(args) {
        console.log("[*] native_encrypt called");
        console.log("[*] Arg0 (JNIEnv*): " + args[0]);
        console.log("[*] Arg1 (jclass/jobject): " + args[1]);
        console.log("[*] Arg2 (jstring): " + args[2]);

        // 读取 jstring 内容
        if (args[2]) {
            var str = Memory.readCString(ptr(args[2]));
            console.log("[*] String arg: " + str);
        }
    },
    onLeave: function(retval) {
        console.log("[*] Return value: " + retval);

        // 读取返回值内容
        if (retval && !retval.isNull()) {
            console.log("[*] Return string: " + retval.readCString());
        }
    }
});
```

#### 3.2 ARM 汇编追踪

```javascript
// 追踪 ARM 汇编级别的函数调用

var moduleName = "libnative-lib.so";
var targetAddr = Module.findExportByName(moduleName, "Java_com_example_app_MainActivity_encrypt");

console.log("[*] Target address: " + targetAddr);

Interceptor.attach(targetAddr, {
    onEnter: function(args) {
        this.context = this.context || null;

        console.log("[=== Enter Function ===]");

        // 读取寄存器 (ARM)
        console.log("[*] R0: " + this.context.r0);
        console.log("[*] R1: " + this.context.r1);
        console.log("[*] R2: " + this.context.r2);
        console.log("[*] R3: " + this.context.r3);

        // 读取栈参数
        console.log("[*] SP[0]: " + this.context.sp.readPointer());
        console.log("[*] SP[4]: " + this.context.sp.add(4).readPointer());
    },
    onLeave: function(retval) {
        console.log("[=== Leave Function ===]");
        console.log("[*] Return value: 0x" + retval.toString(16));
    }
});
```

#### 3.3 Stalker 指令追踪

```javascript
// 使用 Stalker 追踪每一条指令
// 适合分析复杂的 Native 函数

var moduleName = "libnative-lib.so";
var targetFunc = Module.findExportByName(moduleName, "calculate_signature");

console.log("[*] Tracing: " + targetFunc);

Stalker.follow({
    events: {
        // 记录执行的基本块
        call: true,
        // 记录代码访问
        exec: false,
    },
    onReceive: function(events) {
        // 解析事件
        var parser = Stalker.parse(events);
        console.log(parser);
    },
    transform: function(it) {
        // 自定义指令转换
        it = it.toJSON();

        // 在特定地址添加日志
        if (it.address.equals(targetFunc.add(0x20))) {
            console.log("[!] Reached specific offset");
        }

        it.pause();  // 暂停执行

        // 继续执行
        it.resume();
    }
});
```

#### 3.4 Native 内存操作

```javascript
// 读取和修改内存

var baseAddr = Module.findBaseAddress("libnative-lib.so");
console.log("[*] Base address: " + baseAddr);

// 读取字符串
var strPtr = baseAddr.add(0x1234);
console.log("[*] String at offset: " + strPtr.readCString());

// 读取整数
console.log("[*] Int32 at offset: " + baseAddr.add(0x2000).readInt());

// 读取字节数组
console.log("[*] Bytes at offset: " + baseAddr.add(0x3000).readByteArray(16));

// 修改内存
baseAddr.add(0x4000).writeInt(0x12345678);

// 枚举内存区域
Process.enumerateRanges('r-x').forEach(function(range) {
    console.log("[*] Range: " + range.base + " - " + range.size + " " + range.protection);
});
```

---

### Part 4: 高级 Hook 技术

#### 4.1 主动调用

```javascript
// 主动调用 Java 方法

Java.perform(function() {

    // 获取类
    var StringUtils = Java.use("com.example.app.utils.StringUtils");
    var CryptoUtils = Java.use("com.example.app.crypto.CryptoUtils");

    // 主动调用静态方法
    var result = StringUtils.md5("hello world");
    console.log("[*] MD5('hello world'): " + result);

    // 主动调用构造函数
    var DateFormat = Java.use("java.text.SimpleDateFormat");
    var df = DateFormat.$new("yyyy-MM-dd", Java.use("java.util.Locale").US);

    // 主动调用实例方法
    var dateStr = df.format(Java.use("java.util.Date").$new());
    console.log("[*] Formatted date: " + dateStr);

    // 调用带 Native 实现的方法
    var encrypted = CryptoUtils.nativeEncrypt("test data", "secret_key");
    console.log("[*] Encrypted: " + encrypted);
});
```

#### 4.2 动态类加载追踪

```javascript
// 追踪动态加载的类

Java.perform(function() {
    var System = Java.use("java.lang.System");
    var loadedClasses = [];

    System.loadLibrary.implementation = function(libName) {
        console.log("[*] Loading native library: " + libName);
        this.loadLibrary(libName);

        // 库加载后，扫描新导出的符号
        try {
            var exports = Module.enumerateExportsSync(libName);
            console.log("[*] Exports (" + exports.length + "):");
            exports.forEach(function(exp) {
                console.log("    - " + exp.name + " @ " + exp.address);
            });
        } catch (e) {
            console.log("[!] Error: " + e);
        }
    };

    // 追踪 ClassLoader
    Java.use("java.lang.ClassLoader")
        .loadClass.implementation = function(className) {
            console.log("[*] Loading class: " + className);
            var result = this.loadClass(className);
            console.log("[*] Loaded: " + result + " -> " + result.$className);
            return result;
        };
});
```

#### 4.3 Frida RPC 服务

```javascript
// 创建 RPC 服务，从 Python 调用

rpc.exports = {
    // 获取签名
    getSign: function(data, key) {
        var result = null;
        Java.perform(function() {
            var SignUtil = Java.use("com.example.app.SignUtil");
            result = SignUtil.getSign(data, key);
        });
        return result;
    },

    // 获取设备信息
    getDeviceInfo: function() {
        var info = {};
        Java.perform(function() {
            var Build = Java.use("android.os.Build");
            var Secure = Java.use("android.provider.Settings$Secure");

            var context = Java.use("android.app.ActivityThread")
                .currentApplication()
                .getApplicationContext();

            info = {
                manufacturer: Build.MANUFACTURER,
                model: Build.MODEL,
                androidId: Secure.getString(
                    context.getContentResolver(),
                    "android_id"
                ),
                deviceId: Build.getSerial()
            };
        });
        return info;
    },

    // 解密数据
    decrypt: function(encryptedData) {
        var result = null;
        Java.perform(function() {
            var Crypto = Java.use("com.example.app.Crypto");
            result = Crypto.decrypt(encryptedData);
        });
        return result;
    }
};
```

#### 4.4 Python RPC 客户端

```python
import frida
import json

def on_message(message, data):
    if message['type'] == 'send':
        print(f"[*] {message['payload']}")
    elif message['type'] == 'error':
        print(f"[!] Error: {message['stack']}")

# 连接到设备并加载脚本
device = frida.get_usb_device()
session = device.attach("com.example.app")

with open('rpc_script.js', 'r') as f:
    script_code = f.read()

script = session.create_script(script_code)
script.on('message', on_message)
script.load()

# 调用 RPC 方法
rpc_exports = session.exports

# 获取签名
sign = rpc_exports.get_sign("data_to_sign", "app_secret")
print(f"[+] Sign: {sign}")

# 获取设备信息
device_info = rpc_exports.get_device_info()
print(f"[+] Device info: {json.dumps(device_info, indent=2)}")

# 解密数据
decrypted = rpc_exports.decrypt("encrypted_base64_string")
print(f"[+] Decrypted: {decrypted}")

# 保持连接
print("[*] Press Ctrl+C to exit")
import time
time.sleep(1000)
```

---

### Part 5: 自动化与脚本编写

#### 5.1 Hook Framework 封装

```javascript
// hook_framework.js - 通用 Hook 框架

var HookFramework = {
    // 配置
    config: {
        verbose: true,
        stackTrace: true,
        hookNative: true
    },

    // 日志
    log: function(tag, msg) {
        if (this.config.verbose) {
            console.log("[" + tag + "] " + msg);
        }
    },

    // Hook Java 方法
    hookJava: function(className, methodName, callback) {
        Java.perform(function() {
            try {
                var cls = Java.use(className);
                var overloads = cls[methodName].overloads;

                console.log("[*] Hooking " + className + "." + methodName +
                           " (" + overloads.length + " overloads)");

                overloads.forEach(function(overload, i) {
                    overload.implementation = function() {
                        console.log("\n=== " + className + "." + methodName + " #" + i + " ===");
                        console.log("[>] Arguments:");
                        for (var j = 0; j < arguments.length; j++) {
                            console.log("    [" + j + "] " + arguments[j]);
                        }

                        var start = Date.now();
                        var result = callback.apply(this, arguments);
                        var elapsed = Date.now() - start;

                        console.log("[<] Result: " + result);
                        console.log("[*] Elapsed: " + elapsed + "ms");

                        if (HookFramework.config.stackTrace) {
                            console.log("[*] Stack trace:");
                            var trace = Java.use("android.util.Log")
                                .getStackTraceString(
                                    Java.use("java.lang.Exception").$new()
                                );
                            console.log(trace);
                        }

                        return result;
                    };
                });
            } catch (e) {
                console.log("[!] Hook failed: " + e);
            }
        });
    },

    // Hook Native 函数
    hookNative: function(moduleName, funcName, callback) {
        try {
            var addr = Module.findExportByName(moduleName, funcName);
            if (!addr) {
                console.log("[!] Function not found: " + moduleName + "!" + funcName);
                return;
            }

            console.log("[*] Hooking native: " + moduleName + "!" + funcName + " @ " + addr);

            Interceptor.attach(addr, {
                onEnter: function(args) {
                    callback.onEnter(args);
                },
                onLeave: function(retval) {
                    callback.onLeave(retval);
                }
            });
        } catch (e) {
            console.log("[!] Hook failed: " + e);
        }
    }
};

// 使用示例
Java.perform(function() {
    // Hook 所有 AES 相关方法
    HookFramework.hookJava(
        "javax.crypto.Cipher",
        "doFinal",
        {
            onEnter: function(args) {
                this.input = args[0];
            },
            onLeave: function(result) {
                console.log("[*] AES Input: " + bytesToHex(this.input));
                console.log("[*] AES Output: " + bytesToHex(result));
            }
        }
    );
});
```

#### 5.2 自动化分析脚本

```python
# auto_analyzer.py - 自动化 App 分析

import frida
import json
import time
import hashlib

class AppAnalyzer:
    def __init__(self, package_name: str):
        self.package_name = package_name
        self.device = frida.get_usb_device()
        self.session = None
        self.script = None
        self.findings = []

    def start(self):
        """启动分析"""
        print(f"[*] Starting analysis for {self.package_name}")

        # 启动应用
        pid = self.device.spawn([self.package_name])
        self.session = self.device.attach(pid)

        # 加载分析脚本
        with open('analyzer_script.js', 'r') as f:
            script_code = f.read()

        self.script = self.session.create_script(script_code)
        self.script.on('message', self.on_message)
        self.script.load()

        # 恢复应用
        self.device.resume(pid)

        print("[*] Analysis started, press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def on_message(self, message, data):
        """处理 Frida 消息"""
        if message['type'] == 'send':
            payload = message['payload']
            self.findings.append(payload)
            print(f"[+] {json.dumps(payload, ensure_ascii=False)}")

    def stop(self):
        """停止分析并保存结果"""
        print("[*] Saving findings...")

        # 统计发现
        crypto_calls = [f for f in self.findings if f.get('type') == 'crypto']
        network_calls = [f for f in self.findings if f.get('type') == 'network']

        print(f"\n[*] Summary:")
        print(f"    - Crypto calls: {len(crypto_calls)}")
        print(f"    - Network calls: {len(network_calls)}")

        # 保存详细结果
        with open('analysis_result.json', 'w') as f:
            json.dump({
                'package': self.package_name,
                'findings': self.findings,
                'summary': {
                    'crypto_count': len(crypto_calls),
                    'network_count': len(network_calls)
                }
            }, f, indent=2, ensure_ascii=False)

        print("[*] Results saved to analysis_result.json")

        if self.session:
            self.session.detach()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python auto_analyzer.py <package_name>")
        sys.exit(1)

    analyzer = AppAnalyzer(sys.argv[1])
    analyzer.start()
```

#### 5.3 批量 Hook 脚本

```javascript
// batch_hooks.js - 批量 Hook 常用库

Java.perform(function() {

    // ==================== Crypto Hooks ====================

    // javax.crypto.Cipher
    var Cipher = Java.use("javax.crypto.Cipher");
    Cipher.doFinal.overload("[B").implementation = function(data) {
        var result = this.doFinal(data);
        send({
            type: "crypto",
            method: "Cipher.doFinal",
            input: arrayToHex(data),
            output: arrayToHex(result),
            algorithm: this.getAlgorithm()
        });
        return result;
    };

    // java.security.MessageDigest
    var MessageDigest = Java.use("java.security.MessageDigest");
    MessageDigest.digest.overload("[B").implementation = function(data) {
        var result = this.digest(data);
        send({
            type: "crypto",
            method: "MessageDigest.digest",
            input: arrayToHex(data),
            output: arrayToHex(result),
            algorithm: this.getAlgorithm()
        });
        return result;
    };

    // ==================== Network Hooks ====================

    // okhttp3.OkHttpClient
    try {
        var OkHttpClient = Java.use("okhttp3.OkHttpClient");
        OkHttpClient.newCall.implementation = function(request) {
            send({
                type: "network",
                method: "OkHttpClient.newCall",
                url: request.url().toString(),
                method: request.method()
            });
            return this.newCall(request);
        };
    } catch (e) {
        console.log("[*] OkHttp3 not found");
    }

    // java.net.HttpURLConnection
    var HttpURLConnection = Java.use("java.net.HttpURLConnection");
    HttpURLConnection.connect.implementation = function() {
        send({
            type: "network",
            method: "HttpURLConnection.connect",
            url: this.getURL().toString()
        });
        return this.connect();
    };

    // ==================== Utils Hooks ====================

    // Base64
    try {
        var Base64 = Java.use("android.util.Base64");
        Base64.encodeToString.overload("[B", "int").implementation = function(data, flags) {
            var result = this.encodeToString(data, flags);
            send({
                type: "util",
                method: "Base64.encode",
                input: arrayToHex(data),
                output: result
            });
            return result;
        };
    } catch (e) {}

    // ==================== Helpers ====================

    function arrayToHex(array) {
        if (!array) return "null";
        var hex = "";
        for (var i = 0; i < Math.min(array.length, 64); i++) {
            var b = array[i];
            if (b < 0) b += 256;
            hex += b.toString(16).padStart(2, "0");
        }
        if (array.length > 64) hex += "...";
        return hex;
    }

    console.log("[*] Batch hooks installed");
});
```

---

## 📝 练习题

### 练习 8.1：Java 层 Hook 基础

```markdown
目标：Hook 某 App 的登录接口，提取用户名和密码
难度：⭐⭐⭐
提示：
- 找到登录相关的 Activity
- Hook 网络请求方法
- 提取加密参数
```

### 练习 8.2：Native 层追踪

```markdown
目标：追踪 Native 库中的签名计算函数
难度：⭐⭐⭐⭐
要求：
- 找到 Native 库和目标函数
- 追踪函数参数和返回值
- 提取密钥材料
```

### 练习 8.3：自动化分析

```markdown
目标：编写自动化分析脚本，批量提取加密信息
难度：⭐⭐⭐⭐
要求：
- 实现 RPC 服务
- 编写 Python 客户端
- 批量处理多个样本
```

---

## 📚 扩展阅读

- [Frida 官方文档](https://frida.re/docs/)
- [Frida 代码示例](https://github.com/oleavr/frida-agent-example)
- [Frida Gum API](https://frida.re/docs/gum/)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 配置 Frida 环境和 Frida Server
- [ ] 使用 Frida 进行 Java 层 Hook
- [ ] 追踪 Native 层函数调用
- [ ] 编写自动化 Hook 脚本
- [ ] 实现 Frida RPC 服务
- [ ] 绕过常见 App 保护机制
- [ ] 自动化提取加密信息

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S09: 爬虫综合项目](../S09-scraping-project/) — 综合实战项目

---
