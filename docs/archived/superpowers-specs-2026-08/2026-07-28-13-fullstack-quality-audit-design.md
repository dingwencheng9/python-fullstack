# 13-Fullstack 全量质量门禁审计设计

> **文档版本**: v1.0
> **日期**: 2026-07-28
> **目标**: 对 13-fullstack 课程（11 Stage、117 课）进行系统性深度审计与打磨
> **策略**: 审计即重构——审到哪修到哪

---

## 1. 背景与目标

13-fullstack 是一个包含 **11 个 Stage、117 节核心课程**的 Python 3.13 全栈课程体系，涵盖 Python 基础 → AI Agent → 企业级应用 → 前沿探索的完整学习路径。

课程已有大量历史审计积累（CLAUDE.md v4.5、COURSE_MAPPING.md v2.2），存在已知的 P0 阻断问题（如 L61 fixture bug）和大量待完善的骨架课程。本次审计目标：

1. **P0 阻断层**: 修复所有 CI 熔断规则违反和已知 bug
2. **P1 质量层**: 逐课审计 L01-L65 核心课程（65 课）
3. **P2 完善层**: 填实 Stage A/P/K/M/R 专精课程骨架（52 课）
4. **全量验证**: make ci-local 通过 + 输出完成度报告

---

## 2. 审计分层与优先级

### P0 - 阻断层（立即修复）

**范围**: CLAUDE.md 配置错误、已知 bug、CI 熔断规则违反

| 问题 | 位置 | 修复策略 |
|------|------|----------|
| L61 使用不存在的 `examples` fixture | L61/tests/ | 替换为 `solutions` fixture |
| CI 熔断规则违反（sys.path.insert in tests） | 跨课扫描 | 移除并使用 conftest.py |
| 硬编码依赖未锁定上限 | pyproject.toml | 添加版本上限 |
| Ruff/Mypy 配置不一致 | 跨 stage | 统一为 target=py313, strict |

### P1 - 质量层（逐课扫描）

**范围**: Stage 0-6 核心课程（L01-L65），共 65 课

**审计维度**:

| 维度 | 检查项 |
|------|--------|
| 代码质量 | PEP 8 / PEP 695 合规、严格类型提示、无 sys.path 污染、无 eval/exec、examples/ vs solutions/ 边界 |
| 知识点 DAG | L01 纯净法则合规、无前向引用（if/for/def/class 不越界） |
| 测试覆盖 | 有 exercises 必有测试、fixture 注入模式正确 |
| 文档完整性 | lesson.md 格式标准、README 导航一致性、无空占位符 |

### P2 - 完善层（按需填实）

**范围**: Stage A（20 课）、Stage P（9 课）、Stage K（5 课）、Stage M（8 课）、Stage R（10 课），共 52 课

**策略**: 骨架课程逐步填实，专精课程补全 exercises/solutions/tests

---

## 3. 执行流程

### Phase 0: P0 阻断层扫描与修复

```
1. CI 门禁快速扫描（ruff + mypy --strict）
2. 识别所有 sys.path.insert / eval / exec 使用
3. 识别 fixture 配置错误（L61 等）
4. 修复所有 P0 问题
5. make ci-local 验证通过
```

### Phase 1: P1 核心课程审计（L01-L65）

每课执行以下流程：

```
1. 读取 lesson.md → 提取本课知识点集合 A(n)
2. 扫描 examples/ 代码 → 对照知识点白名单
3. 扫描 solutions/ 代码 → 检查 PEP 8 + 类型提示
4. 运行 pytest tests/ → 验证测试通过
5. 检查 tests/ fixture 使用是否正确
6. 发现问题 → 立即修复
7. 下一课...
```

**并发策略**: 按 Stage 分批，每批 Stage 内课并行扫描，发现问题串行修复。

### Phase 2: P2 专精课程完善

```
1. Stage K（完整）→ 代码质量 + 知识点审计
2. Stage A（A01-A05 完善中）→ 补全剩余 A06-A20
3. Stage M（骨架）→ 按需填实
4. Stage R（骨架）→ 按需填实
5. Stage P（骨架）→ 按需填实
```

### Phase 3: 全量验证与报告

```
1. make ci-local 全量通过
2. 生成完成度报告（含所有修复项统计）
3. 更新 CLAUDE.md 版本号
```

---

## 4. 质量标准

| 标准 | 要求 |
|------|------|
| Ruff | 0 errors (target=py313) |
| Mypy | strict mode, 0 errors |
| Pytest | All collected, 0 errors |
| 测试覆盖 | 有 exercises 的课程必须有测试 |
| 知识点 | 无前向引用，符合 DAG 依赖 |
| 文档 | lesson.md 格式标准，README 一致 |

---

## 5. 禁止模式

- 审计过程中**不输出报告但不修复**（审计即重构原则）
- P0 问题发现即修，不跳过
- 不引入新的 sys.path 污染
- 不降低现有代码质量（必须全量通过 ci-local）

---

## 6. 成功标准

- P0 阻断问题: 0 个
- L01-L65 课程: 100% 通过审计
- make ci-local: 100% 通过
- 117 课完成度报告输出
