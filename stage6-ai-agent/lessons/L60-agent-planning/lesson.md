L60: Agent 规划与推理 - 详细教程

> **所属阶段**: Stage 6 - AI Agent 开发
> **课程编号**: L60
> **所属阶段**: Stage 6 - AI Agent 开发
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐⭐（AI Agent 专家级）
> **前置课程**: L59 Agent 记忆
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13

---

---

## 📚 目录

- [第一章：规划模式](#第一章规划模式)
- [第二章：推理技术](#第二章推理技术)
- [第三章：任务分解](#第三章任务分解)
- [第四章：自我修正](#第四章自我修正)

---

## 第一章：规划模式

### 1.1 Plan-and-Execute (经典模式)

**核心思想**: 先规划，再执行，最后总结

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from operator import add

class PlanState(TypedDict):
    input: str
    plan: list[str]
    past_steps: Annotated[list, add]
    response: str

def planner_node(state: PlanState):
    """生成执行计划"""
    prompt = f"""
任务: {state['input']}

请将任务分解为具体步骤:
1. ...
2. ...
3. ...
"""
    response = llm.invoke(prompt)
    steps = parse_steps(response.content)

    return {"plan": steps}

def executor_node(state: PlanState):
    """执行单个步骤"""
    current_step = state["plan"][0]

    # 执行工具调用
    result = execute_step(current_step)

    return {
        "past_steps": [f"{current_step} -> {result}"],
        "plan": state["plan"][1:]  # 移除已执行步骤
    }

def should_continue(state: PlanState):
    if len(state["plan"]) == 0:
        return "summarize"
    return "execute"

# 构建图
graph = StateGraph(PlanState)
graph.add_node("planner", planner_node)
graph.add_node("execute", executor_node)
graph.add_node("summarize", summarize_node)

graph.set_entry_point("planner")
graph.add_conditional_edges("execute", should_continue)
graph.add_edge("planner", "execute")
graph.add_edge("summarize", END)

app = graph.compile()
```python
---

### 1.2 ReWOO (推理无观察)

**核心思想**: 一次性生成完整计划，避免串行依赖

```python
class ReWOOState(TypedDict):
    task: str
    plan_string: str
    steps: list
    results: dict
    result: str

def planner(state: ReWOOState):
    """生成完整计划（带变量占位符）"""
    prompt = f"""
任务: {state['task']}

生成计划（使用 #E[id] 表示中间结果）:

Plan:
#E1 = search(query="...")
#E2 = calculate(expression="#E1")
#E3 = summarize(text="#E2")
"""
    response = llm.invoke(prompt)
    steps = parse_plan(response.content)

    return {"plan_string": response.content, "steps": steps}

def solver(state: ReWOOState):
    """并行执行所有步骤"""
    results = {}

    for step in state["steps"]:
        # 替换变量
        resolved_step = resolve_variables(step, results)

        # 执行工具
        result = execute_tool(resolved_step)
        results[step.id] = result

    return {"results": results}

def reporter(state: ReWOOState):
    """生成最终答案"""
    prompt = f"""
任务: {state['task']}
计划: {state['plan_string']}
结果: {state['results']}

请生成最终答案:
"""
    response = llm.invoke(prompt)
    return {"result": response.content}
```python
---

### 1.3 LLMCompiler (并行优化)

**核心思想**: 自动识别可并行步骤

```python
import asyncio
from typing import Literal

class CompilerState(TypedDict):
    task: str
    dag: dict  # 依赖图
    results: dict

def plan_with_dependencies(state: CompilerState):
    """生成带依赖关系的计划"""
    prompt = f"""
任务: {state['task']}

生成 DAG (有向无环图):
{{
    "step1": {{"depends": [], "action": "..."}},
    "step2": {{"depends": ["step1"], "action": "..."}},
    "step3": {{"depends": ["step1"], "action": "..."}}
}}
"""
    response = llm.invoke(prompt)
    dag = parse_dag(response.content)

    return {"dag": dag}

async def execute_dag(state: CompilerState):
    """并行执行 DAG"""
    dag = state["dag"]
    results = {}

    async def execute_node(node_id: str):
        node = dag[node_id]

        # 等待依赖完成
        for dep in node["depends"]:
            while dep not in results:
                await asyncio.sleep(0.1)

        # 执行
        result = await execute_async(node["action"], results)
        results[node_id] = result

    # 并行执行所有节点
    tasks = [execute_node(node_id) for node_id in dag]
    await asyncio.gather(*tasks)

    return {"results": results}
```python
---

## 第二章：推理技术

### 2.1 Chain-of-Thought (思维链)

**核心技巧**: 添加 "让我们一步一步思考" 提示

```python
def chain_of_thought(question: str) -> str:
    prompt = f"""
问题: {question}

让我们一步一步思考:

步骤1: 理解问题
[分析问题的关键要素]

步骤2: 制定方案
[列出解决思路]

步骤3: 执行计算
[进行具体推导]

步骤4: 验证答案
[检查结果合理性]

最终答案: [给出结论]
"""

    response = llm.invoke(prompt)
    return extract_final_answer(response.content)

# 示例
question = "小明有3个苹果，小红比小明多2个，他们一共有几个？"
answer = chain_of_thought(question)
# 输出: 8个
```python
---

### 2.2 Tree-of-Thoughts (思维树)

**核心思想**: 探索多条推理路径，选择最优解

```python
from typing import List

class ThoughtNode:
    def __init__(self, content: str, score: float):
        self.content = content
        self.score = score
        self.children: List[ThoughtNode] = []

def tree_of_thoughts(question: str, depth: int = 3) -> str:
    """思维树搜索"""

    def generate_thoughts(parent: ThoughtNode, current_depth: int):
        if current_depth >= depth:
            return

        # 生成多个候选思路
        prompt = f"""
问题: {question}
当前思路: {parent.content}

生成3个不同的下一步思路:
1. ...
2. ...
3. ...
"""
        response = llm.invoke(prompt)
        candidates = parse_thoughts(response.content)

        # 评估每个思路
        for thought in candidates:
            score = evaluate_thought(thought, question)
            node = ThoughtNode(thought, score)
            parent.children.append(node)

            # 递归探索
            generate_thoughts(node, current_depth + 1)

    # 初始节点
    root = ThoughtNode("开始分析问题", 1.0)
    generate_thoughts(root, 0)

    # 找到最优路径
    best_path = find_best_path(root)
    return "\n".join([node.content for node in best_path])
```python
---

### 2.3 Self-Consistency (自我一致性)

**核心思想**: 多次采样，投票选最优

```python
def self_consistency(question: str, n_samples: int = 5) -> str:
    """多次推理取一致答案"""
    answers = []

    for i in range(n_samples):
        # 多次独立推理
        answer = chain_of_thought(question)
        answers.append(answer)

    # 投票
    from collections import Counter
    vote = Counter(answers)
    best_answer, count = vote.most_common(1)[0]

    confidence = count / n_samples

    return {
        "answer": best_answer,
        "confidence": confidence,
        "all_answers": answers
    }
```python
---

## 第三章：任务分解

### 3.1 递归分解

```python
class Task:
    def __init__(self, description: str, complexity: int):
        self.description = description
        self.complexity = complexity
        self.subtasks: List[Task] = []

def decompose_task(task: Task, max_complexity: int = 3) -> Task:
    """递归分解任务"""
    if task.complexity <= max_complexity:
        return task

    # 询问 LLM 分解
    prompt = f"""
任务: {task.description}
复杂度: {task.complexity}

请将任务分解为3-5个子任务:
1. [子任务1] (复杂度: X)
2. [子任务2] (复杂度: Y)
...
"""

    response = llm.invoke(prompt)
    subtasks = parse_subtasks(response.content)

    # 递归分解子任务
    for subtask in subtasks:
        task.subtasks.append(decompose_task(subtask, max_complexity))

    return task
```python
---

### 3.2 依赖图生成

```python
from collections import defaultdict, deque

class TaskGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)

    def add_dependency(self, task: str, depends_on: str):
        """添加依赖: task 依赖 depends_on"""
        self.graph[depends_on].append(task)
        self.in_degree[task] += 1

    def topological_sort(self) -> list[str]:
        """拓扑排序 (执行顺序)"""
        queue = deque([node for node in self.graph if self.in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    def parallel_groups(self) -> list[list[str]]:
        """返回可并行执行的任务组"""
        groups = []
        remaining = set(self.graph.keys())

        while remaining:
            # 找到所有无依赖的任务
            ready = [t for t in remaining if self.in_degree[t] == 0]
            groups.append(ready)

            # 移除已执行任务
            for task in ready:
                remaining.remove(task)
                for dep in self.graph[task]:
                    self.in_degree[dep] -= 1

        return groups
```python
---

## 第四章：自我修正

### 4.1 Reflexion (反思模式)

```python
class ReflexionState(TypedDict):
    task: str
    trajectory: list[str]
    reflection: str
    answer: str

def actor_node(state: ReflexionState):
    """执行任务"""
    prompt = f"""
任务: {state['task']}
历史反思: {state['reflection']}

请执行任务:
"""
    response = llm.invoke(prompt)

    return {
        "trajectory": state["trajectory"] + [response.content],
        "answer": response.content
    }

def evaluator_node(state: ReflexionState):
    """评估结果"""
    prompt = f"""
任务: {state['task']}
答案: {state['answer']}

评估 (0-10分):
理由:
"""
    response = llm.invoke(prompt)
    score = extract_score(response.content)

    return {"score": score}

def reflector_node(state: ReflexionState):
    """生成反思"""
    prompt = f"""
任务: {state['task']}
执行轨迹: {state['trajectory']}
评分: {state['score']}

反思: 哪里做得不好？如何改进？
"""
    response = llm.invoke(prompt)

    return {"reflection": response.content}

def should_retry(state: ReflexionState):
    return "actor" if state["score"] < 8 and len(state["trajectory"]) < 3 else "end"

# 构建图
graph = StateGraph(ReflexionState)
graph.add_node("actor", actor_node)
graph.add_node("evaluator", evaluator_node)
graph.add_node("reflector", reflector_node)

graph.set_entry_point("actor")
graph.add_edge("actor", "evaluator")
graph.add_edge("evaluator", "reflector")
graph.add_conditional_edges("reflector", should_retry)
```python
---

### 4.2 验证反馈循环

```python
def validate_and_correct(task: str, max_iterations: int = 3):
    """验证-修正循环"""
    current_answer = None

    for i in range(max_iterations):
        # 生成答案
        if current_answer is None:
            current_answer = generate_answer(task)
        else:
            current_answer = refine_answer(task, current_answer, feedback)

        # 验证
        is_valid, feedback = validate_answer(current_answer, task)

        if is_valid:
            return current_answer

    return current_answer  # 返回最后一次尝试

def validate_answer(answer: str, task: str) -> tuple[bool, str]:
    """验证答案并返回反馈"""
    prompt = f"""
任务: {task}
答案: {answer}

验证清单:
1. 是否回答了问题？
2. 逻辑是否自洽？
3. 是否有明显错误？

判断: 通过/不通过
反馈: [具体问题]
"""
    response = llm.invoke(prompt)

    is_valid = "通过" in response.content
    feedback = extract_feedback(response.content)

    return is_valid, feedback
```

---

## 🎯 最佳实践总结

### ✅ 规划设计清单

- [ ] 任务分解粒度适中 (不超过3层)
- [ ] 依赖关系显式标注
- [ ] 并行步骤自动识别
- [ ] 失败重试机制
- [ ] 超时保护
- [ ] 中间结果缓存
- [ ] 进度可视化

### 规划模式选择

| 任务类型 | 推荐模式         | 原因         |
| -------- | ---------------- | ------------ |
| 简单串行 | Plan-and-Execute | 经典稳定     |
| 复杂推理 | Tree-of-Thoughts | 探索多条路径 |
| 需要并行 | LLMCompiler      | 自动优化     |
| 需要反思 | Reflexion        | 自我改进     |

---

## 🔗 延伸阅读

### 相关课程

- **L54 Agent 基础** - ReAct Agent
- **L55 LangGraph** - 状态机编排
- **L61 多智能体编排** - Supervisor 模式

### 推荐资源

- [Chain-of-Thought 论文](https://arxiv.org/abs/2201.11903)
- [Tree-of-Thoughts 论文](https://arxiv.org/abs/2305.10601)
- [Reflexion 论文](https://arxiv.org/abs/2303.11366)

---

## 📝 练习题

### 练习 1: Plan-and-Execute

实现任务规划器:

- 分解任务
- 顺序执行
- 结果总结

### 练习 2: Tree-of-Thoughts

实现思维树搜索:

- 多路径探索
- 思路评分
- 最优路径选择

### 练习 3: Reflexion

实现自我反思循环:

- 执行任务
- 评估结果
- 生成反思
- 重新尝试

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L55 MCP 协议](../L55-mcp-protocol/lesson.md)

## 🔗 下一步

完成本课后继续学习：

- [L61: 多智能体系统](../L61-multi-agent/README.md)

> 📖 **学习路径提示**：L61 将学习多智能体协作与编排。
