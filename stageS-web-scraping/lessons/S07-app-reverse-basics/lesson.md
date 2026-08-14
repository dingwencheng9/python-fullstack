# S07: App 逆向入门

> **课程编号**: S07
> **所属阶段**: Stage P - Python 爬虫专精
> **课程时长**: 10 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: S01 前端基础

---

## 📚 课程概述

移动端 App 已成为主流数据源，但 App 的数据获取比网页更加困难。本课程从零讲解 App 逆向基础，涵盖 Android 环境搭建、APK 结构分析、网络抓包和 Java/Smali 代码阅读。

---

## 🎯 学习目标

1. 搭建 Android 逆向分析环境
2. 理解 APK 结构与 dex 文件格式
3. 掌握网络抓包技术（Charles/Mitmproxy）
4. 阅读和理解 Smali 汇编代码
5. 分析 App 加密逻辑与签名机制
6. 实现 App 数据抓取

---

## 📋 课程大纲

- [Part 1: Android 逆向环境搭建](#part-1-android-逆向环境搭建)
- [Part 2: APK 结构与静态分析](#part-2-apk-结构与静态分析)
- [Part 3: 网络抓包技术](#part-3-网络抓包技术)
- [Part 4: Smali 代码基础](#part-4-smali-代码基础)
- [Part 5: App 加密与签名](#part-5-app-加密与签名)

---

## 🔧 环境准备

### macOS 环境配置

```bash
# Android Studio + 模拟器（推荐方式1）
# 下载地址：https://developer.android.com/studio
# 创建模拟器：Pixel 5 API 30+

# ADB 工具
brew install android-platform-tools
adb version

# APK 反编译工具
uv venv && source .venv/bin/activate
uv add apktool jadx frida-tools

# 安装 Objection（动态分析）
uv add objection

# 模拟器连接
adb connect localhost:5555
```

---

## 📖 详细内容

### Part 1: Android 逆向环境搭建

#### 1.1 模拟器选择

| 模拟器 | 优点 | 缺点 |
|--------|------|------|
| Android Studio 模拟器 | 官方、稳定性高 | 性能开销大 |
| Genymotion | 性能好、Root 方便 | 免费版功能有限 |
|雷电模拟器 | 游戏性能优化 | 定制化程度低 |
| MuMu 模拟器 | 国内应用兼容好 | 性能一般 |

#### 1.2 模拟器配置

```bash
# 使用 adb 连接模拟器
# Android Studio 模拟器
adb connect 127.0.0.1:5555

# Genymotion
adb connect 192.168.56.101:5555

# 验证连接
adb devices
# 输出应包含：localhost:5555 device

# 安装应用
adb install app.apk

# 卸载应用
adb uninstall com.example.app

# 查看已安装应用包名
adb shell pm list packages
```

#### 1.3 Root 与 SSL 证书配置

```bash
# Android 7+ 的 SSL Pinning 问题
# 方法1：使用 JustTrustMe/Xposed 模块

# 1. 下载 JustTrustMe APK
# https://github.com/Fuzion24/JustTrustMe/releases

# 2. 安装到模拟器
adb install JustTrustMe.apk

# 3. 下载 Xposed 框架
# https://github.com/acp0/XposedInstaller

# 4. 安装 Xposed
adb install Xposed.apk

# 方法2：安装用户证书到系统目录
# 需要 Root 权限

# 将证书转为系统证书格式
openssl x509 -inform DER -in mitmproxy-cert.cer -out cert.pem
openssl x509 -inform PEM -subject_hash_old -in cert.pem | head -1
mv cert.pem 9a5ba575.0  # 使用上一步的 hash 值
adb push 9a5ba575.0 /sdcard/
adb shell
su
mount -o rw,remount /system
mv /sdcard/9a5ba575.0 /system/etc/security/cacerts/
chmod 644 /system/etc/security/cacerts/9a5ba575.0
```

---

### Part 2: APK 结构与静态分析

#### 2.1 APK 内部结构

```bash
# 解包 APK
apktool d target.apk -o output_dir

# 查看解包后的结构
output_dir/
├── AndroidManifest.xml    # 应用清单（编译后的 XML）
├── apktool.yml           # apktool 配置
├── assets/               # 资源文件
│   └── *.js              # 可能包含 JS 代码
├── lib/                  # 原生库 (.so 文件)
│   ├── arm64-v8a/
│   ├── armeabi-v7a/
│   └── x86/
├── res/                  # 资源目录
├── smali/                # 反编译的 Smali 代码
│   └── com/example/
│       └── MainActivity.smali
└── unknown/              # 未知文件
```

#### 2.2 使用 Jadx 分析 APK

```bash
# 启动 Jadx GUI
jadx-gui target.apk

# 命令行导出 Java 源码
jadx -d output_dir target.apk

# 搜索关键字
jadx-gui target.apk
# 使用搜索功能（Ctrl+Shift+F）
# 搜索：encrypt, decrypt, sign, token, API_KEY, BASE_URL
```

#### 2.3 关键文件分析

```xml
<!-- AndroidManifest.xml 示例 -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.app"
    android:versionCode="1"
    android:versionName="1.0.0">

    <!-- 应用权限 -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <!-- 应用组件 -->
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <!-- 网络安全配置 -->
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                </trust-anchors>
            </base-config>
        </network-security-config>

    </application>
</manifest>
```

#### 2.4 资源文件分析

```bash
# 查看 strings.xml（可能包含 API 地址）
cat res/values/strings.xml

# 查看 network_security_config.xml（SSL 配置）
cat res/xml/network_security_config.xml

# 查看 lib 目录的 .so 文件
ls -la lib/
file lib/arm64-v8a/libnative-lib.so

# 使用 strings 提取 .so 文件中的字符串
strings lib/arm64-v8a/libnative-lib.so | grep -E "api|encrypt|key|http"
```

---

### Part 3: 网络抓包技术

#### 3.1 Charles 配置

```bash
# Charles 基本配置
# 1. Proxy → Proxy Settings
#    Port: 8888
#    Enable HTTP/2
# 2. Proxy → SSL Proxying Settings
#    Enable SSL Proxying
#    Add: * (捕获所有 HTTPS)
# 3. Help → SSL Proxying → Save Charles Root Certificate

# 模拟器配置
# 设置代理
adb shell settings put global http_proxy localhost:8888

# 清除代理
adb shell settings delete global http_proxy
```

#### 3.2 Mitmproxy 配置

```bash
# 启动 mitmproxy
mitmproxy --listen-port 8888

# 或使用 mitmweb（Web 界面）
mitmweb --listen-port 8888

# 导出证书
# mitmproxy 会自动在 ~/.mitmproxy/ 生成证书
ls ~/.mitmproxy/

# Python 脚本处理抓包数据
# save_flows.py
from mitmproxy import http, ctx

def request(flow: http.HTTPFlow):
    # 过滤特定域名
    if 'api.example.com' in flow.request.pretty_host:
        ctx.log.info(f"Request: {flow.request.pretty_url}")
        ctx.log.info(f"Headers: {flow.request.headers}")
        ctx.log.info(f"Body: {flow.request.content}")

def response(flow: http.HTTPFlow):
    if 'api.example.com' in flow.request.pretty_host:
        ctx.log.info(f"Response: {flow.response.content}")

# 启动 mitmproxy 加脚本
mitmproxy -s save_flows.py
```

#### 3.3 App 抓包实战

```python
# Python + mitmdump 抓包示例
from mitmproxy import http, ctx
import json
import hashlib

class AppInterceptor:
    def __init__(self):
        self.requests = []
        self.responses = []

    def request(self, flow: http.HTTPFlow):
        # 记录请求
        request_data = {
            'url': flow.request.pretty_url,
            'method': flow.request.method,
            'headers': dict(flow.request.headers),
            'body': flow.request.content.decode('utf-8', errors='ignore'),
        }
        self.requests.append(request_data)

        # 打印关键信息
        if '/api/' in flow.request.pretty_path:
            ctx.log.info(f"API Request: {flow.request.pretty_path}")

    def response(self, flow: http.HTTPFlow):
        # 记录响应
        try:
            body = flow.response.content.decode('utf-8')
            response_data = {
                'url': flow.request.pretty_url,
                'status': flow.response.status_code,
                'body': json.loads(body) if body else None,
            }
            self.responses.append(response_data)
        except:
            pass

addons = [AppInterceptor()]
```

#### 3.4 SSL Pinning 绕过

```python
# 使用 Frida 绕过 SSL Pinning
# ssl_pinning_bypass.js
Java.perform(function() {
    var TrustManagerImpl = Java.use('javax.net.ssl.X509TrustManager');

    var TrustManager = Java.use('android.app.Application$TrustManager');
    TrustManager.checkServerTrusted.implementation = function(chain, authType) {
        console.log('[Bypass] SSL check bypassed');
        return;
    };

    // 通用绕过方法
    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    var context = SSLContext.getInstance('TLS');
    context.init(null, TrustManagerImpl.$new(), null);

    // Hook OkHttp
    try {
        var OkHttpClient = Java.use('okhttp3.OkHttpClient');
        OkHttpClient.$init.overload('okhttp3.OkHttpClient$Builder').implementation = function(builder) {
            builder.hostnameVerifier(function(hostname, session) { return true; });
            return this.$init(builder);
        };
    } catch(e) {
        console.log('OkHttp hook not available');
    }
});
```

---

### Part 4: Smali 代码基础

#### 4.1 Smali 语法入门

```smali
# 类声明
.class public Lcom/example/app/MainActivity;
.super Landroid/app/Activity;

# 字段
.field private secretKey:Ljava/lang/String;
.field private apiUrl:Ljava/lang/String;

# 方法
.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .registers 3
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    const-string v0, "Hello"
    const-string v1, "World"
    invoke-static {v0, v1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    return-void
.end method
```

#### 4.2 寄存器与数据类型

```smali
# 寄存器说明
# p0 = this (实例方法) 或 第一个参数 (静态方法)
# p1, p2, ... = 方法参数
# v0, v1, ... = 本地变量

# 数据类型
# V      - void
# Z      - boolean
# B      - byte
# C      - char
# S      - short
# I      - int
# J      - long
# F      - float
# D      - double
# Lxxx;  - 对象类型 (Ljava/lang/String;)
# [xxx   - 数组类型 ([I = int[], [[B = byte[][])

# 寄存器操作示例
.method example()V
    .registers 4

    const/4 v0, 0x1        # v0 = 1
    const/4 v1, 0x0        # v1 = 0
    const-string v2, "test"  # v2 = "test"

    # 加法
    add-int v3, v0, v1     # v3 = v0 + v1

    # 调用方法
    invoke-virtual {v2}, Ljava/lang/String;->length()I

    move-result v3          # 获取返回值
.end method
```

#### 4.3 常见指令

```smali
# 赋值指令
const/4 v0, 0x1           # 整数常量
const-string v0, "str"    # 字符串常量
const-class v0, Ljava/lang/String;  # Class 对象

# 对象操作
new-instance v0, Ljava/lang/StringBuilder;  # 创建对象
invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V  # 调用构造函数

# 方法调用
invoke-virtual {p0, v0}, Lcom/example/App;->encrypt(Ljava/lang/String;)Ljava/lang/String;
# p0 = this, v0 = 参数

# 返回值处理
invoke-virtual {v0}, Ljava/lang/String;->getBytes()[B
move-result-object v1     # 获取返回的对象

# 条件跳转
if-eq v0, v1, :cond_1     # v0 == v1 时跳转
if-ne v0, v1, :cond_2     # v0 != v1 时跳转
if-gt v0, v1, :cond_3     # v0 > v1 时跳转
if-le v0, v1, :cond_4     # v0 <= v1 时跳转

# 循环示例
:loop_start
add-int/lit8 v0, v0, 0x1  # v0++
if-lt v0, v1, :loop_start  # v0 < v1 时继续循环
```

#### 4.4 从 Smali 还原 Java

```smali
# Smali 代码
.method public static encrypt(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    .registers 6
    .param p0, "data"    # Ljava/lang/String;
    .param p1, "key"     # Ljava/lang/String;

    .local v0, "md":Ljava/security/MessageDigest;
    .local v1, "result":Ljava/lang/StringBuilder;
    .local v2, "i":I

    invoke-static {p1}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;
    move-result-object v0

    invoke-virtual {v0, p0}, Ljava/security/MessageDigest;->update([B)V

    invoke-virtual {v0}, Ljava/security/MessageDigest;->digest()[B
    move-result-object v3

    new-instance v1, Ljava/lang/StringBuilder;
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const/4 v2, 0x0
    :goto_0
    array-length v4, v3
    if-ge v2, v4, :goto_1

    aget-byte v4, v3, v2
    invoke-virtual {v1, v4}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;
    add-int/lit8 v2, v2, 0x1
    goto :goto_0

    :goto_1
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v3

    return-object v3
.end method
```

**还原为 Java**：

```java
public static String encrypt(String data, String key) throws Exception {
    MessageDigest md = MessageDigest.getInstance(key);
    md.update(data.getBytes());
    byte[] result = md.digest();

    StringBuilder sb = new StringBuilder();
    for (byte b : result) {
        sb.append((char) b);
    }

    return sb.toString();
}
```

---

### Part 5: App 加密与签名

#### 5.1 App 签名机制

```bash
# 查看 APK 签名信息
apksigner verify -v target.apk

# 提取签名
keytool -printcert -jarfile target.apk

# 查看签名使用的算法
apksigner verify --print-certs target.apk
```

#### 5.2 签名算法分析

```java
// 常见 App 签名校验代码（简化）
public class SignUtil {
    public static String getSignature(Context context) {
        try {
            PackageInfo pkgInfo = context.getPackageManager()
                .getPackageInfo(context.getPackageName(),
                    PackageManager.GET_SIGNATURES);

            Signature[] signatures = pkgInfo.signatures;
            if (signatures != null && signatures.length > 0) {
                Signature signature = signatures[0];
                MessageDigest md = MessageDigest.getInstance("MD5");
                md.update(signature.toByteArray());
                return bytesToHex(md.digest());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

#### 5.3 常见加密特征识别

```java
// AES 加密
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class AESUtil {
    public static String encrypt(String data, String key) throws Exception {
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.encodeToString(encrypted, Base64.DEFAULT);
    }
}

// RSA 加密
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.X509EncodedKeySpec;
import javax.crypto.Cipher;

public class RSAUtil {
    public static String encrypt(String data, String publicKeyStr) throws Exception {
        byte[] keyBytes = Base64.decode(publicKeyStr, Base64.DEFAULT);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(keyBytes);
        KeyFactory factory = KeyFactory.getInstance("RSA");
        PublicKey publicKey = factory.generatePublic(spec);

        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.encodeToString(encrypted, Base64.DEFAULT);
    }
}
```

#### 5.4 App 数据抓取方案

```python
import subprocess
import frida
import json
import httpx

class AppScraper:
    """App 数据抓取器"""

    def __init__(self, package_name: str):
        self.package_name = package_name
        self.session = None

    def start_frida(self, script_path: str):
        """启动 Frida 并注入脚本"""
        device = frida.get_usb_device()
        pid = device.spawn([self.package_name])
        self.session = device.attach(pid)

        with open(script_path, 'r') as f:
            script_code = f.read()

        script = self.session.create_script(script_code)
        script.on('message', self.on_message)
        script.load()

        device.resume(pid)

        return self.session

    def on_message(self, message, data):
        """处理 Frida 消息"""
        if message['type'] == 'send':
            payload = message['payload']
            print(f"[Frida] {payload}")

            # 保存数据
            if 'api_data' in payload:
                self.save_api_data(payload['api_data'])

    def save_api_data(self, data: dict):
        """保存 API 数据"""
        with open(f"api_data_{data.get('url', 'unknown')}.json", 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def stop(self):
        """停止 Frida 会话"""
        if self.session:
            self.session.detach()
```

---

## 📝 练习题

### 练习 7.1：APK 静态分析

```markdown
目标：分析某新闻 App 的 API 接口
难度：⭐⭐⭐
要求：
- 解包并分析 APK 结构
- 找到所有网络请求相关的代码
- 提取 API 域名和路径
```

### 练习 7.2：SSL Pinning 绕过

```markdown
目标：绕过某 App 的 SSL Pinning
难度：⭐⭐⭐⭐
提示：
- 使用 Frida 注入脚本
- 验证抓包是否成功
- 提取加密请求内容
```

### 练习 7.3：Smali 逆向

```markdown
目标：将 Smali 代码还原为可读 Java
难度：⭐⭐⭐⭐
要求：
- 阅读 Smali 汇编代码
- 理解寄存器与数据类型
- 还原加密函数逻辑
```

---

## 📚 扩展阅读

- [Android 逆向工程入门](https://www.ringieraxelspringer.pl/2019/08/08/android-reverse-engineering-for-beginners/)
- [Frida 官方文档](https://frida.re/docs/)
- [Smali 语法参考](https://github.com/JesusFreke/smali/wiki)

---

## ✅ 课后检查

完成本课程后，你应该能够：

- [ ] 搭建完整的 Android 逆向环境
- [ ] 解包和分析 APK 文件结构
- [ ] 使用 Charles/Mitmproxy 进行网络抓包
- [ ] 绕过 SSL Pinning 限制
- [ ] 阅读和理解 Smali 汇编代码
- [ ] 分析 App 的加密和签名机制
- [ ] 实现 App 数据的抓取

---

**课程版本**: v1.0
**最后更新**: 2026-07-22

---

## 🔗 下一步

- [S08: Frida 动态分析](../S08-frida-dynamic/) — 使用 Frida 进行动态 Hook

---
