# R07: Wasm 性能基准

> **课程编号**: R07
> **所属阶段**: Stage R - 前沿探索实验室
> **预计时长**: 2-3 小时
> **难度**: ⭐⭐⭐⭐
> **前置课程**: R06
> **版本**: v5.0
> **最后更新**: 2026-07-22

---

## 📌 学习目标

1. **基准测试方法论**：Wasm 性能测试的正确方法
2. **性能对比分析**：CPython vs Wasm vs PyPy
3. **瓶颈识别**：定位 Wasm 性能瓶颈
4. **优化策略**：提升 Wasm 执行效率

---

## Part 1: 基准测试方法论

### 1.1 测试环境

```python
# 基准测试配置

import time
import statistics
from dataclasses import dataclass

@dataclass
class BenchmarkConfig:
    """基准测试配置"""
    warmup_iterations: int = 10
    measured_iterations: int = 100
    gc_before: bool = True

config = BenchmarkConfig(
    warmup_iterations=10,
    measured_iterations=100,
    gc_before=True,
)

def run_benchmark(func, config: BenchmarkConfig) -> dict:
    """运行基准测试"""
    import gc

    # 预热
    for _ in range(config.warmup_iterations):
        func()

    # 清理
    if config.gc_before:
        gc.collect()

    # 测量
    times = []
    for _ in range(config.measured_iterations):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return {
        "min": min(times),
        "max": max(times),
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
    }
```

### 1.2 测试场景

```python
# 测试场景定义

TEST_CASES = {
    "cpu_intensive": {
        "描述": "CPU 密集型计算",
        "函数": lambda: sum(i * i for i in range(100000)),
    },
    "memory_bound": {
        "描述": "内存密集型操作",
        "函数": lambda: [i for i in range(10000)],
    },
    "io_bound": {
        "描述": "I/O 密集型操作",
        "函数": lambda: "\n".join(str(i) for i in range(1000)),
    },
    "numeric": {
        "描述": "数值计算",
        "函数": lambda: sum(math.sqrt(i) for i in range(1, 10001)),
    },
}
```

---

## Part 2: 性能对比

### 2.1 Python vs Wasm

```python
# 性能对比分析

COMPARISON_RESULTS = {
    "启动时间": {
        "CPython": "50-200ms",
        "Wasmtime": "10-50ms",
        "Pyodide": "2-5s (首次)",
        "结论": "Wasmtime 启动更快",
    },
    "执行速度": {
        "CPython": "基准",
        "Wasmtime": "0.8-1.2x",
        "Pyodide": "0.3-0.8x",
        "结论": "浏览器 Wasm 较慢",
    },
    "内存占用": {
        "CPython": "10-50MB",
        "Wasmtime": "5-20MB",
        "Pyodide": "20-50MB",
        "结论": "Wasmtime 内存更小",
    },
}

def generate_report(results: dict) -> str:
    """生成对比报告"""
    lines = ["# 性能对比报告", ""]
    for category, data in results.items():
        lines.append(f"## {category}")
        for key, value in data.items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    return "\n".join(lines)
```

### 2.2 场景分析

```python
# 适用场景分析

SCENARIOS = {
    "适合 Wasm": [
        "边缘计算（启动时间重要）",
        "浏览器端执行",
        "沙箱隔离需求",
        "跨平台分发",
    ],
    "适合 CPython": [
        "服务器端长期运行",
        "复杂数值计算",
        "需要完整标准库",
        "性能要求极高",
    ],
    "适合 PyPy": [
        "长期运行的脚本",
        "数值计算为主",
        "内存充足",
    ],
}
```

---

## Part 3: 瓶颈分析

### 3.1 热点识别

```python
# 性能分析工具

def profile_wasm():
    """Wasm 模块性能分析"""

    # 1. 启动时间分解
    startup_phases = {
        "下载": "wasm_binary_size / bandwidth",
        "解析": "wasm_parse_time",
        "编译": "jit_compile_time",
        "实例化": "instantiation_time",
    }

    # 2. 执行时间分解
    execution_phases = {
        "解释执行": "interpreter_overhead",
        "JIT 编译": "jit_overhead",
        "实际计算": "computation_time",
        "系统调用": "wasi_call_overhead",
    }

    return {"startup": startup_phases, "execution": execution_phases}

# 使用 wasmtime 剖析
"""
$ wasmtime --profile=perf my_module.wasm
$ cat profile.data | warp-ct-top
"""
```

### 3.2 优化策略

```python
# 优化策略清单

OPTIMIZATIONS = {
    "启动优化": [
        "AOT 编译预生成",
        "模块懒加载",
        "增量编译",
    ],
    "执行优化": [
        "减少 WASI 调用",
        "批量 I/O 操作",
        "使用 Wasm SIMD",
    ],
    "内存优化": [
        "使用线性内存池",
        "减少 GC 压力",
        "紧凑数据结构",
    ],
}
```

---

## 📚 延伸阅读

- [WebAssembly 基准测试套件](https://github.com/WasmBench/wasmbench)
- [Pyodide 性能分析](https://pyodide.org/en/stable/performance)
- [Wasmtime profiling](https://docs.wasmtime.dev/examples/profiling.html)

---

## ✅ 自检清单

- [ ] 设计 Wasm 基准测试
- [ ] 对比不同运行时的性能
- [ ] 识别性能瓶颈
- [ ] 应用优化策略

---

**课程制作**: Python 3.13 全栈课程组
**最后更新**: 2026-07-22
**版本**: v5.0

---

## 🔗 下一步

- [R08: Python 3.15 预览](../R08-python-315-preview/) — 新特性抢先看

---
