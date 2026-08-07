#!/usr/bin/env python3
"""
Stage 0 知识点边界扫描器 (AST 版本)
使用 AST 分析精确检测语法越界
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
import sys

# ============================================================
# DAG 知识点边界定义（基于 CLAUDE.md L01 纯净法则）
# ============================================================

@dataclass
class LessonBoundary:
    """课程知识点边界定义"""
    lesson_id: str
    name: str
    # 禁止的 AST 节点类型
    forbidden_nodes: set[type] = field(default_factory=set)
    # 描述
    description: str = ""


# L01 Bootstrap: 只允许基础类型和变量，禁止所有控制流、函数、类
L01_BOUNDARY = LessonBoundary(
    lesson_id="L01",
    name="Python 核心语法",
    forbidden_nodes={
        ast.FunctionDef,      # def 函数定义 (L04)
        ast.AsyncFunctionDef, # async def (L14)
        ast.ClassDef,         # class 类定义 (L07)
        ast.If,               # if 语句 (L02)
        ast.For,              # for 循环 (L02)
        ast.While,            # while 循环 (L02)
        ast.Match,            # match-case (L02)
        ast.Try,              # try-except (L06)
        ast.With,             # with 语句 (L09)
        ast.Lambda,           # lambda 表达式 (L04)
        ast.ListComp,         # 列表推导式 (L03)
        ast.DictComp,         # 字典推导式 (L03)
        ast.SetComp,          # 集合推导式 (L03)
        ast.GeneratorExp,     # 生成器表达式 (L03)
    },
    description="L01 纯净法则：只允许变量赋值、基础类型、f-string 格式化"
)

# L02: 允许 def 函数（用于测试框架）、if/for/while/match-case
# 禁止 class/try/with/lambda/comprehension
# 注意: def 函数定义是允许的（因为测试框架需要），但越界的是函数体的完整实现
L02_BOUNDARY = LessonBoundary(
    lesson_id="L02",
    name="运算符与控制流",
    forbidden_nodes={
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Try,
        ast.With,
        ast.Lambda,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
    },
    description="L02: 允许控制流和 def 函数（测试框架），禁止 class/异常"
)

# L03: 允许 def 函数（用于测试框架）、list/dict/tuple/set/for/if
# 禁止 class/try/with/lambda
L03_BOUNDARY = LessonBoundary(
    lesson_id="L03",
    name="数据结构",
    forbidden_nodes={
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Try,
        ast.With,
        ast.Lambda,
    },
    description="L03: 允许数据结构和 def 函数（测试框架），禁止 class/异常"
)

# L04: 允许 def/lambda，禁止 class/try/with/lambda(Lambda在L04才学)
L04_BOUNDARY = LessonBoundary(
    lesson_id="L04",
    name="函数与模块",
    forbidden_nodes={
        ast.ClassDef,
        ast.Try,
        ast.With,
    },
    description="L04: 允许 def/lambda，禁止 class/异常/with"
)

# L05: 允许 def，禁止 async/await/class/try
L05_BOUNDARY = LessonBoundary(
    lesson_id="L05",
    name="调试工具与环境",
    forbidden_nodes={
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Try,
    },
    description="L05: 允许 def，禁止 async/类/异常"
)

# L06: 允许 try/except/raise/def/class/lambda，禁止 with
L06_BOUNDARY = LessonBoundary(
    lesson_id="L06",
    name="异常处理与防御代码",
    forbidden_nodes={
        ast.With,
    },
    description="L06: 允许异常处理，禁止 with(L09才学)"
)

# L07: 允许 class/def/继承/组合，禁止 try/with
L07_BOUNDARY = LessonBoundary(
    lesson_id="L07",
    name="面向对象基础",
    forbidden_nodes={
        ast.Try,
        ast.With,
    },
    description="L07: 允许 OOP，禁止异常处理/with"
)

# L08: 允许 __magic__ 方法，禁止 try/with
L08_BOUNDARY = LessonBoundary(
    lesson_id="L08",
    name="魔术方法与协议",
    forbidden_nodes={
        ast.Try,
        ast.With,
    },
    description="L08: 允许魔术方法，禁止异常/with"
)

# L09: 允许 with 语句
L09_BOUNDARY = LessonBoundary(
    lesson_id="L09",
    name="文件操作与上下文管理",
    forbidden_nodes=set(),
    description="L09: 允许所有已学知识点"
)

# P01: 综合项目
P01_BOUNDARY = LessonBoundary(
    lesson_id="P01",
    name="综合实战：学员管理系统",
    forbidden_nodes=set(),
    description="P01: 可使用所有已学知识点"
)

LESSON_BOUNDARIES = {
    "L01": L01_BOUNDARY,
    "L02": L02_BOUNDARY,
    "L03": L03_BOUNDARY,
    "L04": L04_BOUNDARY,
    "L05": L05_BOUNDARY,
    "L06": L06_BOUNDARY,
    "L07": L07_BOUNDARY,
    "L08": L08_BOUNDARY,
    "L09": L09_BOUNDARY,
    "P01": P01_BOUNDARY,
}

# AST 节点中文名称
NODE_NAMES = {
    ast.FunctionDef: "def 函数定义",
    ast.AsyncFunctionDef: "async def 异步函数",
    ast.ClassDef: "class 类定义",
    ast.If: "if 条件语句",
    ast.For: "for 循环",
    ast.While: "while 循环",
    ast.Match: "match-case 语句",
    ast.Try: "try-except 异常处理",
    ast.With: "with 上下文管理",
    ast.Lambda: "lambda 表达式",
    ast.ListComp: "列表推导式",
    ast.DictComp: "字典推导式",
    ast.SetComp: "集合推导式",
    ast.GeneratorExp: "生成器表达式",
}


@dataclass
class Violation:
    """违规项"""
    lesson_id: str
    file_path: str
    line_number: int
    node_type: str
    code_snippet: str


class ViolationFinder(ast.NodeVisitor):
    """AST 节点访问器，查找违规的语法结构"""

    def __init__(self, forbidden_nodes: set[type]):
        self.forbidden_nodes = forbidden_nodes
        self.violations: list[Violation] = []
        self.current_file = ""
        self.source_lines: list[str] = []
        self.current_scope_is_class = False  # 类内部的方法定义是允许的

    def _get_node_snippet(self, node: ast.AST) -> str:
        """安全获取节点代码片段"""
        try:
            lineno = node.lineno
            if 1 <= lineno <= len(self.source_lines):
                return self.source_lines[lineno - 1].strip()
        except Exception:
            pass
        return f"<{type(node).__name__} at line {node.lineno}>"

    def visit(self, node: ast.AST) -> None:
        """访问节点"""
        # 检查是否是禁止的节点类型
        if type(node) in self.forbidden_nodes:
            # 类内部的方法定义不算是越界（因为类是在后续课程学的）
            if isinstance(node, ast.FunctionDef) and self.current_scope_is_class:
                pass  # 类方法，允许
            else:
                # 获取代码片段（使用更安全的方式）
                snippet = self._get_node_snippet(node)

                self.violations.append(Violation(
                    lesson_id="",
                    file_path=self.current_file,
                    line_number=node.lineno,
                    node_type=NODE_NAMES.get(type(node), type(node).__name__),
                    code_snippet=snippet[:80]
                ))

        # 跟踪当前作用域
        if isinstance(node, ast.ClassDef):
            old_scope = self.current_scope_is_class
            self.current_scope_is_class = True
            self.generic_visit(node)
            self.current_scope_is_class = old_scope
        else:
            self.generic_visit(node)

    def visit_Module(self, node: ast.Module) -> None:
        """访问模块"""
        self.generic_visit(node)


def scan_file(file_path: Path, boundary: LessonBoundary) -> list[Violation]:
    """扫描单个文件的违规项"""
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError as e:
        print(f"  ⚠️ 语法错误 {file_path}: {e}")
        return []
    except Exception as e:
        print(f"  ⚠️ 无法解析 {file_path}: {e}")
        return []

    finder = ViolationFinder(boundary.forbidden_nodes)
    finder.current_file = str(file_path)
    finder.source_lines = content.split("\n")
    finder.visit(tree)

    # 设置 lesson_id
    for v in finder.violations:
        v.lesson_id = boundary.lesson_id

    return finder.violations


def main():
    """主函数"""
    stage0_path = Path("/Users/nexo/python-fullstack/stage0-python-basics/lessons")

    print("=" * 70)
    print("🔍 Stage 0 知识点边界扫描器 (AST 版本)")
    print("=" * 70)

    all_violations = []

    # 按顺序扫描所有课程
    lesson_dirs = sorted(stage0_path.glob("L*")) + sorted(stage0_path.glob("P*"))

    for lesson_path in lesson_dirs:
        if not lesson_path.is_dir():
            continue

        lesson_id = lesson_path.name.split("-")[0]
        boundary = LESSON_BOUNDARIES.get(lesson_id)
        if not boundary:
            continue

        print(f"\n📚 扫描 {lesson_id} ({boundary.name})")
        print(f"   说明: {boundary.description}")

        exercises_dir = lesson_path / "exercises"
        if not exercises_dir.exists():
            print("   ⚠️ 无 exercises/ 目录")
            continue

        lesson_violations = []
        for py_file in sorted(exercises_dir.glob("*.py")):
            if py_file.name == "__init__.py":
                continue

            violations = scan_file(py_file, boundary)
            if violations:
                print(f"   ❌ {py_file.name}: {len(violations)} 个违规")
                for v in violations:
                    print(f"      Line {v.line_number}: {v.node_type}")
                    print(f"        → {v.code_snippet[:60]}...")
                lesson_violations.extend(violations)
            else:
                print(f"   ✅ {py_file.name}")

        all_violations.extend(lesson_violations)

    # 输出汇总报告
    print("\n" + "=" * 70)
    print("📊 扫描结果汇总")
    print("=" * 70)

    if all_violations:
        print(f"\n❌ 发现 {len(all_violations)} 个语法越界:\n")

        # 按课程分组统计
        by_lesson = {}
        for v in all_violations:
            if v.lesson_id not in by_lesson:
                by_lesson[v.lesson_id] = {"count": 0, "files": {}, "nodes": set()}
            by_lesson[v.lesson_id]["count"] += 1
            rel_path = Path(v.file_path).relative_to(stage0_path.parent.parent)
            file_key = str(rel_path)
            if file_key not in by_lesson[v.lesson_id]["files"]:
                by_lesson[v.lesson_id]["files"][file_key] = []
            by_lesson[v.lesson_id]["files"][file_key].append(v)
            by_lesson[v.lesson_id]["nodes"].add(v.node_type)

        for lesson_id in sorted(by_lesson.keys()):
            info = by_lesson[lesson_id]
            print(f"\n📌 {lesson_id}: {info['count']} 个违规")
            print(f"   违规类型: {', '.join(sorted(info['nodes']))}")
            print("   涉及文件:")
            for file_path, violations in sorted(info["files"].items()):
                print(f"     - {Path(file_path).name} ({len(violations)} 处)")

        print("\n" + "-" * 70)
        print("⚠️  需要修复的课程:")
        for lesson_id in sorted(by_lesson.keys()):
            boundary = LESSON_BOUNDARIES.get(lesson_id)
            print(f"\n   【{lesson_id}】{boundary.name if boundary else ''}")
            info = by_lesson[lesson_id]
            print(f"   违规统计: {info['count']} 处越界")
            print(f"   越界类型: {', '.join(sorted(info['nodes']))}")
    else:
        print("\n✅ 未发现语法越界！所有 exercises 符合知识点边界定义。")

    print("\n" + "=" * 70)
    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
