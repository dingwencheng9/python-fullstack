# Stage R: 前沿探索实验室

> **阶段编号**: Stage R
> **课程数量**: 10 课 (R01-R10)
> **预计学时**: ~45 小时
> **前置要求**: Stage M (企业级 AI 应用)
> **状态**: 🔶 骨架（内容已部分扩充，练习和实战项目待完善）

---

## 📚 课程列表

| 编号 | 课程名称 | 主题 | 学时 | 难度 | 状态 |
|------|----------|------|------|------|------|
| R01 | Python 3.14t 完全体 | 新语法、内省增强、调试改进 | 4h | ⭐⭐⭐⭐ | ✅ |
| R02 | GIL Free Fallback 策略 | 多线程优化、free-threaded 构建 | 5h | ⭐⭐⭐⭐⭐ | ✅ |
| R03 | PEP 649/810 延迟注解 | 运行时注解、t-string 模板 | 5h | ⭐⭐⭐⭐ | ✅ |
| R04 | t-string 模板与格式化 | 模板字符串、安全转义、表达式 | 4h | ⭐⭐⭐ | ✅ |
| R05 | Python 路线图与未来展望 | 语言演进、PEP 流程、社区动态 | 3h | ⭐⭐⭐ | ✅ |
| R06 | WASI 边缘部署 | WebAssembly、边缘计算、轻量运行 | 5h | ⭐⭐⭐⭐ | ✅ |
| R07 | Wasm 性能基准 | 性能测试、内存模型、互操作性 | 5h | ⭐⭐⭐⭐ | ✅ |
| R08 | Python 3.15 预览 | 下一代特性抢先看 | 4h | ⭐⭐⭐ | ✅ |
| R09 | AI 辅助编程未来 | Copilot、Code Agent、智能化开发 | 4h | ⭐⭐⭐⭐ | ✅ |
| R10 | 课程毕业与展望 | 技术回顾、项目展示、职业规划 | 3h | ⭐⭐⭐ | ✅ |

---

## 🎯 学习路径

```
R01 Python 3.14 → R02 GIL 规避 → R03 延迟注解
      ↓              ↓              ↓
R04 t-string ← R09 AI 编程 → R07 Wasm 性能
                    ↓              ↓
R05 路线图 → R06 WASI 部署 → R08 3.15 预览
                                        ↓
                                   R10 毕业总结
```

---

## 📖 学习目标

完成 Stage R 后，你将掌握：

1. **Python 前沿特性** — 3.14/3.15 新语法、内省增强、调试改进
2. **GIL 优化** — free-threaded 构建、多线程性能、规避策略
3. **延迟注解** — PEP 649/810 运行时注解、类型检查优化
4. **模板字符串** — t-string 语法、安全转义、实际应用
5. **WebAssembly** — WASI 标准、边缘部署、轻量运行时
6. **性能优化** — Wasm 性能基准、编译优化、性能评估
7. **AI 编程** — Copilot、Code Agent、智能化开发工具
8. **技术预研** — 语言路线图、PEP 流程、社区参与

---

## 🛠️ 环境要求

- **Python 版本**: 3.13.x (基线) / 3.14t 或 3.15a (前沿特性)
- **包管理**: uv
- **核心依赖**: cython, wasmer, wasmtime
- **可选依赖**: python3.14t, python3.15a

```bash
# 安装依赖
uv sync

# 运行测试（全阶段）
uv run pytest stageR-frontier/lessons/ -v

# 代码检查
uv run ruff check stageR-frontier/
uv run mypy stageR-frontier/lessons/ --ignore-missing-imports

# 性能基准测试
python -m benchmark stageR-frontier/
```

---

## 📁 课程结构

每个课程包含：

```
R{XX}-课程名/
├── README.md           # 课程概览与快速开始
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板
├── solutions/          # 参考解答
└── tests/              # 单元测试
```

---

## 🔗 衔接课程

- **前置**: [Stage M: 企业级 AI 应用](../stageM-enterprise/)
- **后续**: 课程完结 🎉

---

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 课程数量 | 10 |
| 示例代码 | ~50 个 |
| 练习题 | ~25 个 |
| 测试用例 | 300+ |
| 预计学时 | ~45 小时 |

---

## 🏆 完成标准

- [ ] 完成所有 10 个课程的学习
- [ ] 通过所有课程测试
- [ ] 完成所有练习题
- [ ] 掌握 Python 前沿技术
- [ ] 具备技术预研能力
- [ ] 完成课程毕业项目

---

## ⚡ 快速参考

### Python 3.14 新特性

```python
# PEP 749: inline def (Python 3.14+)
inline def add(a: int, b: int) -> int:
    return a + b

# PEP 742: 类型推断增强
@overload
def process(data: str) -> str: ...
@overload
def process(data: int) -> int: ...
```

### t-string 模板 (PEP 750)

```python
# t-string: 模板字符串
template = t"Hello, {name}! Today is {date:%Y-%m-%d}."
result = template.format(name="Alice", date=datetime.now())
```

### Wasm 边缘部署

```python
import wasmtime

# WASI 运行时
engine = wasmtime.Engine()
store = wasmtime.Store(engine)
module = wasmtime.Module.from_file(store, "app.wasm")
```

---

> **版本**: v5.0
> **最后更新**: 2026-07-22
