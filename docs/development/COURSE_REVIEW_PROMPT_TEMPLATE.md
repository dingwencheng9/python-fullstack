# Stage 0-2 课程审查提示词模板

> **用途**: 用于审查 Stage 0 (L01-L10)、Stage 1 (L10-L16)、Stage 2 (L17-L25) 的课程质量
> **适用场景**: 深度审计、代码审查、教学质量评估
> **前置条件**: 已启用相关 skill（如 `python-review`、`systematic-debugging` 等）

---

## 阶段一：环境准备与知识边界验证

```
请按照以下步骤准备审查环境：

1. 读取课程目录结构
   - Stage 0: stage0-python-basics/lessons/L01-L10
   - Stage 1: stage1-python-advanced/lessons/L10-L16  
   - Stage 2: stage2-modern-engineering/lessons/L17-L25

2. 构建知识边界 DAG
   根据 docs/knowledge/KNOWLEDGE_DAG.md 定义每节课的知识点集合 A(n)：

   L01 绝对纯净法则:
   - 禁止出现: if/for/while/def/class/list/dict/tuple
   - 允许出现: print/input/变量/类型注解/f-string/运算符

   L02 允许增加:
   - if/elif/else/while/for/range/match-case/enumerate/zip/tuple

   L03 允许增加:
   - list/dict/set/tuple/类型注解中的复合类型

3. 验证前置要求
   - 检查每节课的 lesson.md 是否使用前置课程知识点
   - 检查 examples/ 代码是否符合知识点白名单
```

---

## 阶段二：目录结构完整性审查

```
请审查每个课程的目录结构是否完整：

标准目录结构:
L{XX}-课程名/
├── README.md           # 课程入口导航（< 50 行）
├── lesson.md           # 详细教学内容
├── examples/           # 示例代码（可直接运行）
├── exercises/          # 练习题模板（有则必须有测试）
├── solutions/          # 参考解答
└── tests/              # pytest 测试（有 exercises 时必须）

审查要点:
1. README.md 是否存在且 < 50 行
2. lesson.md 是否包含完整知识点（无答案泄露）
3. examples/ 是否有 __init__.py
4. exercises/ 是否有对应测试
5. solutions/ 代码是否工程级（无 sys.path 污染）
```

---

## 阶段三：代码质量深度审查

### 3.1 Python 代码规范

```
请使用 python-review agent 审查所有 .py 文件：

审查维度:
□ PEP 8 规范（ruff check）
□ 类型注解完整性（mypy strict）
□ 无 sys.path.insert/append（CI 熔断规则）
□ 无 eval()/exec()（安全规则）
□ 无硬编码密钥
□ 错误处理完整性
□ 文档字符串质量

工具命令:
make lint-strict   # ruff 检查
make typecheck     # mypy 检查
```

### 3.2 测试覆盖审查

```
请审查测试覆盖质量：

分层要求:
| 课程类型        | 必须有 tests | 说明                    |
|----------------|-------------|------------------------|
| 有 exercises/  | ✅ 必须      | 验证学生答案，防止退化  |
| 项目课         | ✅ 必须      | 功能测试 + 集成测试     |
| 只有 examples/ | ❌ 可选      | 教学演示，建议但不强制  |

审查要点:
1. exercises 是否有对应测试验证
2. 测试命名是否符合规范（test_xxx.py）
3. 测试是否使用 pytest 框架
4. 测试是否有有意义的断言（非 pass）
5. Mock 对象使用是否正确
```

### 3.3 依赖管理审查

```
请审查 pyproject.toml 配置：

四大铁律:
1. Stage 级 pyproject.toml — 虚拟容器，不可构建
   - ✅ 保留 [project]（name, version, requires-python）
   - ❌ 禁止 [build-system]

2. Lesson 级 pyproject.toml — 仅工具配置
   - ❌ 禁止 [project]、[dependencies]
   - ✅ 允许 [tool.pytest.ini_options]、[tool.ruff]、[tool.mypy]

3. 隔离 venv — 统一环境，禁止碎片化
   - ❌ 禁止在 stage*/ 或 stage*/lessons/L*/ 创建 .venv
   - ✅ 所有环境统一使用根 .venv

4. 跨 Lesson 导入 — 自包含，禁止跨目录引用
   - ❌ 禁止跨 Lesson 目录的直接导入
   - ✅ 跨 Lesson 的代码复用通过复制自包含实现
```

---

## 阶段四：知识边界越界检测

```
请检测课程内容是否越界：

L01 严格禁止的知识点:
| 越界知识点         | 所属课程 |
|------------------|---------|
| if/elif/else     | L02     |
| while/for        | L02     |
| def              | L10     |
| class            | L05     |
| list/dict/tuple  | L03     |

检测方法:
1. grep -rE "def |class |if |for |while " examples/*.py
2. 检查 lesson.md 是否使用后续课程术语
3. 检查类型注解是否使用未引入的类型
```

---

## 阶段五：文档质量审查

```
请审查文档完整性：

lesson.md 格式标准检查:
□ 包含学习目标（3-5 个）
□ 包含核心概念解释
□ 包含代码示例（可运行）
□ 包含练习题说明
□ 无答案泄露
□ 无前置课程术语

README.md 检查:
□ < 50 行
□ 包含课程目标
□ 包含前置要求
□ 包含学习路径指引
□ 包含快速开始命令
```

---

## 阶段六：执行验证

```
请执行以下验证命令：

1. 语法检查
   uv run python -m py_compile examples/*.py
   uv run python -m py_compile solutions/*.py

2. 测试收集
   uv run pytest --collect-only stage0-python-basics/lessons/
   uv run pytest --collect-only stage1-python-advanced/lessons/
   uv run pytest --collect-only stage2-modern-engineering/lessons/

3. Lint 检查
   make lint-strict

4. 类型检查
   make typecheck

5. 全量测试
   make test
```

---

## 阶段七：问题汇总与修复建议

```
请汇总发现的问题并提供修复建议：

问题分类:
1. 🔴 CRITICAL（阻塞）: 必须修复
   - sys.path 污染
   - 依赖缺失
   - 目录结构不完整

2. 🟡 HIGH: 应该修复
   - 类型注解缺失
   - 测试覆盖不足
   - 知识边界越界

3. 🟢 MEDIUM: 建议修复
   - 文档格式不规范
   - 代码风格问题
   - 注释缺失

输出格式:
# {Stage} 审查报告

## 执行摘要

## 问题清单（按严重程度排序）

## 修复方案对比

## 最佳实践建议
```

---

## 使用示例

### 完整审查流程

```bash
# 1. 准备阶段
读取 CLAUDE.md 了解项目规范
读取 COURSE_MAPPING.md 了解课程结构
读取 docs/knowledge/KNOWLEDGE_DAG.md 了解知识边界

# 2. 执行审查
使用 systematic-debugging skill 进行系统化审查
使用 python-review agent 审查代码质量
使用 TDD-guide agent 验证测试覆盖

# 3. 修复问题
修复 CRITICAL 问题
修复 HIGH 问题
验证修复结果

# 4. 提交审查报告
```

### 按课程审查

```bash
# 审查单个课程
uv run pytest stage0-python-basics/lessons/L01/tests/ -v

# 审查单个 Stage
uv run pytest stage0-python-basics/lessons/*/tests/ -v

# 审查 Stage 0-2
uv run pytest stage{0,1,2}*/lessons/*/tests/ -v
```

---

## 快速检查清单

```
审查前:
□ [ ] 读取 CLAUDE.md
□ [ ] 读取 COURSE_MAPPING.md
□ [ ] 确认知识边界 DAG

审查中:
□ [ ] 检查目录结构完整性
□ [ ] 检查代码规范（ruff + mypy）
□ [ ] 检查测试覆盖
□ [ ] 检查依赖管理
□ [ ] 检查知识边界

审查后:
□ [ ] 修复 CRITICAL 问题
□ [ ] 修复 HIGH 问题
□ [ ] 运行 make ci-local 验证
□ [ ] 提交审查报告
```

---

## 关键文件索引

| 文件 | 用途 |
|------|------|
| `CLAUDE.md` | 项目配置与规范 |
| `COURSE_MAPPING.md` | 课程体系总览 |
| `docs/knowledge/KNOWLEDGE_DAG.md` | 知识边界 DAG |
| `docs/development/TESTING_CONVENTIONS.md` | 测试约定 |
| `docs/development/LESSON_FORMAT_STANDARD.md` | lesson.md 格式标准 |
| `QUICKSTART.md` | 快速开始命令 |
