# R06: WASI 边缘部署

> **课程编号**: R06
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: R01, K02
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

1. **理解 WASI 标准**：WebAssembly System Interface 核心概念
2. **部署 Python 到边缘**：使用 Pyodide 和 Wasmtime
3. **构建 Serverless 函数**：边缘计算的 Python 函数
4. **优化 Wasm 性能**：减少启动时间和内存占用

---

## 📖 课程导读

### 什么是 WASI？

WASI（WebAssembly System Interface）为 WebAssembly 提供系统接口，使 Wasm 模块可以在浏览器之外运行。

| 运行环境 | 特性 |
|----------|------|
| **浏览器** | 受限的网络访问，沙箱安全 |
| **Wasmtime** | 文件系统、网络、完全系统接口 |
| **WASI** | 标准化的系统接口 |

---

## Part 1: WASI 核心概念

### 1.1 Wasm 运行时

```python
# Python Wasm 运行时对比

RUNTIMES = {
    "wasmtime": {
        "描述": "生产级 Wasm 运行时",
        "平台": "所有主流平台",
        "支持": "WASI Preview 1/2",
    },
    "wasmer": {
        "描述": "轻量级运行时",
        "平台": "所有主流平台",
        "支持": "WASI Preview 1",
    },
    "pyodide": {
        "描述": "浏览器中的 Python",
        "平台": "仅浏览器",
        "支持": "Emscripten",
    },
}

def choose_runtime() -> str:
    """选择合适的运行时"""
    import platform
    if platform.system() == "Emscripten":
        return "pyodide"
    return "wasmtime"
```

### 1.2 WASI 权限模型

```python
# WASI 权限概念

"""
WASI 使用基于能力的权限模型：

1. 文件系统访问
   - wasifilesystem: 目录访问
   - 沙箱隔离

2. 网络访问
   - wasinetwork: TCP/UDP
   - 特定端口

3. 时钟访问
   - wasiclocks: 时间查询
   - 沙箱时间
"""

# 示例：WASI capability grants
CAPABILITIES = {
    "dir": ["./", "./data"],  # 允许的目录
    "network": {"tcp": 8080},  # 允许的端口
    "env": ["PATH", "HOME"],  # 允许的环境变量
}
```

---

## Part 2: Pyodide 部署

### 2.1 浏览器中运行 Python

```html
<!-- index.html - Pyodide 示例 -->

<!DOCTYPE html>
<html>
<head>
    <title>Pyodide Demo</title>
</head>
<body>
    <h1>Python in Browser</h1>
    <div id="output"></div>

    <script type="module">
        import { loadPyodide } from
            "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/";

        async function main() {
            // 加载 Python 环境
            const pyodide = await loadPyodide();

            // 运行 Python 代码
            const result = pyodide.runPython(`
                import sys
                import json

                def process(data):
                    return [x * 2 for x in data]

                result = process([1, 2, 3, 4, 5])
                json.dumps(result)
            `);

            document.getElementById("output").textContent = result;
        }

        main();
    </script>
</body>
</html>
```

### 2.2 Pyodide 与 JavaScript 互操作

```python
# Python 端 - pyodide.ffi

import pyodide.ffi

# 从 JavaScript 接收数据
def process_js_data(data_js):
    """处理来自 JavaScript 的数据"""
    # data_js 是一个 JavaScript 对象
    return [item * 2 for item in data_js.to_list()]

# 注册到全局
pyodide.ffi.create_proxy(process_js_data)

# JavaScript 端
"""
const data = [1, 2, 3, 4, 5];
const result = pyodide.runPython(`
    process_js_data(${JSON.stringify(data)})
`);
"""
```

---

## Part 3: Wasmtime 边缘部署

### 3.1 安装与配置

```bash
# 安装 Wasmtime
curl https://wasmtime.org/install.sh -sSf | bash

# 或使用 cargo 安装
cargo install wasmtime

# 验证安装
wasmtime --version
```

### 3.2 Python 编译为 Wasm

```python
# 使用 PyO3 编译 Python 为 Wasm

# pyproject.toml 配置
[project]
name = "my-edge-module"
version = "0.1.0"

[tool.maturin]
features = ["extension-module"]
target = "wasm32-wasi"

# 模块代码
# my_module.py
def process(data: list[int]) -> list[int]:
    """边缘处理函数"""
    return [x * 2 for x in data]

def handler(event: dict) -> dict:
    """WASI 入口点"""
    return {
        "status": "ok",
        "result": process(event.get("data", []))
    }

# 编译
# maturin build --target wasm32-wasi
```

### 3.3 边缘函数示例

```python
# edge_function.py - 边缘计算函数

"""
边缘函数示例：处理传感器数据
在边缘设备上进行预处理，减少云端负载
"""

import json
from typing import NamedTuple

class SensorReading(NamedTuple):
    timestamp: float
    temperature: float
    humidity: float

def process_readings(readings: list[SensorReading]) -> dict:
    """处理传感器读数"""
    if not readings:
        return {"error": "no data"}

    temps = [r.temperature for r in readings]
    humids = [r.humidity for r in readings]

    return {
        "count": len(readings),
        "avg_temp": sum(temps) / len(temps),
        "avg_humidity": sum(humids) / len(humids),
        "min_temp": min(temps),
        "max_temp": max(temps),
    }

def wasi_main():
    """WASI 入口函数"""
    import sys

    # 从 stdin 读取输入
    input_data = sys.stdin.read()

    # 解析 JSON
    data = json.loads(input_data)
    readings = [SensorReading(**r) for r in data["readings"]]

    # 处理
    result = process_readings(readings)

    # 输出 JSON
    print(json.dumps(result))

if __name__ == "__main__":
    wasi_main()
```

---

## Part 4: 性能优化

### 4.1 启动时间优化

```python
# 优化策略

"""
Wasm 启动时间瓶颈：
1. 字节码解析
2. JIT 编译
3. 模块初始化

优化方法：
- AOT 编译
- 模块缓存
- 懒加载
"""

# 预编译模块
def preload_modules():
    """预加载常用模块"""
    import sys

    # 预导入标准库
    modules = ["json", "math", "statistics", "typing"]
    for mod in modules:
        __import__(mod)

# 使用 WASI component model
"""
.component_import {
    import json from "std";
    import math from "std";
}
"""
```

### 4.2 内存优化

```python
# 内存管理

"""
Wasm 内存是线性的，有限的
需要优化数据结构减少内存占用
"""

# 使用紧凑的数据结构
from dataclasses import dataclass
import array

@dataclass
class CompactReading:
    """紧凑的传感器读数"""
    # 使用固定大小类型
    temp: int16  # 温度 * 100
    humid: int16  # 湿度 * 100
    time: uint32  # Unix 时间戳

# 使用 array 模块减少开销
def create_reading_array(readings: list[CompactReading]) -> array:
    """创建紧凑数组"""
    arr = array.array('h')  # signed short
    for r in readings:
        arr.extend([r.temp, r.humid])
    return arr
```

---

## 💡 常见陷阱

### 陷阱 1: 假设完整文件系统

```python
# ❌ 错误：假设完整文件系统访问
import os
with open("/etc/config.json") as f:  # ❌ WASI 不支持
    config = json.load(f)

# ✅ 正确：使用 WASI 目录
with open("./config.json") as f:  # ✅ 相对路径
    config = json.load(f)
```

### 陷阱 2: 忽略沙箱限制

```python
# ❌ 错误：尝试访问网络
import socket
socket.socket()  # ❌ 默认不允许

# ✅ 正确：使用 WASI 网络接口
# 需要显式请求 wasinetwork capability
```

---

## 📚 延伸阅读

- [WASI 官方文档](https://github.com/WebAssembly/WASI)
- [Pyodide 文档](https://pyodide.org/)
- [Wasmtime 文档](https://docs.wasmtime.org/)

---

## ✅ 自检清单

- [ ] 理解 WASI 和 Wasm 运行时
- [ ] 使用 Pyodide 在浏览器中运行 Python
- [ ] 部署 Python 函数到 Wasmtime
- [ ] 优化 Wasm 启动时间和内存

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0

---

## 🔗 下一步

- [R07: Wasm 性能基准](../R07-wasm-benchmark/) — 性能测试与优化

---
