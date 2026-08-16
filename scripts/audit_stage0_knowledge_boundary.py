#!/usr/bin/env python3
"""
Stage 0 知识点越界全面审查脚本
检测语法越界、类型注解越界、术语越界
"""

import ast
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

# 知识点边界定义
KNOWLEDGE_BOUNDARY = {
    "L01": {
        "allowed": [
            "print", "input", "int", "float", "str", "bool", "None", "complex", "bytes",
            "type", "help", "dir", "repr",
            "f-string", "escape", "raw-string",
            "variable_assignment", "type_annotation_variable",
            "type_conversion",  # int(), float(), str(), bool()
            "immutable_concept",  # int/str 不可变
        ],
        "forbidden_syntax": [
            "If", "Elif", "Else",  # if/elif/else
            "For", "While", "Break", "Continue",  # 循环
            "FunctionDef", "AsyncFunctionDef",  # def 函数
            "ClassDef",  # class 类
            "List", "Dict", "Set", "Tuple",  # 复合数据类型
            "ListComp", "DictComp", "SetComp", "GeneratorExp",  # 推导式
            "Try", "ExceptHandler", "Raise", "With",  # 异常/上下文
            # 允许 import（用于 from typing import 未来可能需要的注解）
            "Lambda",  # lambda
            "Match", "Case",  # match-case
            "Assert",  # assert
        ],
        "forbidden_type_annotations": [
            # 仅禁止小写泛型注解
            r"list\[", r"dict\[", r"set\[", r"tuple\[",
        ],
        "forbidden_terms": [
            "循环", "if 语句", "条件判断", "分支",
            "函数", "def", "方法", "参数",
            "类", "class", "对象", "面向对象",
            "列表", "字典", "集合", "元组",
            "异常", "try", "except", "捕获",
            "推导式", "列表推导",
        ],
    },
    "L02": {
        "allowed": [
            "If", "Elif", "Else",
            "For", "While", "Break", "Continue",
            "Match", "Case",
            "Enumerate", "Zip",
            "BinOp", "UnaryOp", "Compare", "BoolOp",
            "BitAnd", "BitOr", "BitXor", "Invert", "LShift", "RShift",
            "FunctionDef",  # 允许函数定义（exercises 需要学员实现）
        ],
        "forbidden_syntax": [
            "AsyncFunctionDef",
            "ClassDef",
            "ListComp", "DictComp", "SetComp",
            "Try", "ExceptHandler", "Raise", "With",
            "Lambda",
            # 注意：不禁止 Import/ImportFrom，因为 import 是 Python 基础语法
        ],
        "forbidden_type_annotations": [
            r"list\[", r"dict\[", r"set\[", r"tuple\[",  # 泛型注解（小写）
            r"List\[", r"Dict\[", r"Set\[", r"Tuple\[",  # 泛型注解（大写）
            # 注意：typing.List 等不应在 L02 使用
        ],
        "forbidden_terms": [
            "函数定义", "def", "方法",
            "类", "class", "对象",
            "列表", "字典", "集合", "元组",
            "异常处理", "try", "except",
        ],
    },
    "L03": {
        "allowed": [
            # L03 核心：列表、元组、字典、集合
            "List", "Dict", "Set", "Tuple",
            "ListComp", "DictComp", "SetComp", "GeneratorExp",
            "Subscript",  # lst[0], d["key"]
            "Call",  # .append(), .pop(), .get()
            # L03 允许循环遍历
            "For", "While", "Break", "Continue",
        ],
        "forbidden_syntax": [
            # FunctionDef 在 exercises 中是允许的（学员需要实现函数）
            # 但 FunctionDef 可能在某些 examples 中越界
            "AsyncFunctionDef",
            "ClassDef",
            "Try", "ExceptHandler", "Raise", "With",
            "Lambda",
            # 允许 Import（用于 from typing import List）
        ],
        "forbidden_type_annotations": [
            # 仅禁止小写泛型注解 list[...]（Python 3.9+ 特性）
            # 大写 List[...] 使用 from typing import List 是允许的
        ],
        "forbidden_terms": [
            "函数定义", "def",
            "类定义", "class",
            "异常", "try", "except",
        ],
    },
    "L04": {
        "allowed": [
            "FunctionDef", "AsyncFunctionDef",  # 函数是 L04 核心
            "Lambda",
            "Import", "ImportFrom",
            "arguments",  # 默认参数, *args, **kwargs
        ],
        "forbidden_syntax": [
            "ClassDef",
            "Try", "ExceptHandler", "Raise", "With",  # 异常处理是 L06 内容
            "ListComp", "DictComp", "SetComp",  # 推导式是 L03 内容
        ],
        "forbidden_type_annotations": [],
        "forbidden_terms": [
            "类定义", "class",
            "异常处理", "try", "except",
        ],
    },
    "L05": {
        "allowed": [
            "pdb", "breakpoint", "traceback",
            "sys.last_traceback",
        ],
        "forbidden_syntax": [
            "ClassDef",
        ],
        "forbidden_type_annotations": [],
        "forbidden_terms": [
            "类定义", "class",
        ],
    },
    "L06": {
        "allowed": [
            "Try", "ExceptHandler", "Raise",
            "With", "WithItem",
        ],
        "forbidden_syntax": [
            "ClassDef",
        ],
        "forbidden_type_annotations": [],
        "forbidden_terms": [
            "类定义", "class",
        ],
    },
    "L07": {
        "allowed": [
            "ClassDef",
            "FunctionDef",  # 实例方法
            "With",
        ],
        "forbidden_syntax": [],
        "forbidden_type_annotations": [],
        "forbidden_terms": [],
    },
    "L08": {
        "allowed": [
            "ClassDef",
            "FunctionDef",
            "Import", "ImportFrom",
        ],
        "forbidden_syntax": [],
        "forbidden_type_annotations": [],
        "forbidden_terms": [],
    },
    "L09": {
        "allowed": [
            "ClassDef",
            "FunctionDef",
            "Import", "ImportFrom",
            "Try", "ExceptHandler",  # 文件操作中的异常处理
            "With",
            "Call",  # open(), pathlib
        ],
        "forbidden_syntax": [],
        "forbidden_type_annotations": [],
        "forbidden_terms": [],
    },
}

# 课程顺序
LESSON_ORDER = ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "P01"]


@dataclass
class Violation:
    """违规记录"""
    lesson: str
    file_path: str
    line_number: int
    violation_type: str  # syntax/annotation/term
    code_snippet: str
    description: str
    severity: str = "HIGH"


@dataclass
class AuditResult:
    """审查结果"""
    total_files: int = 0
    violations: list[Violation] = field(default_factory=list)
    files_by_lesson: dict = field(default_factory=dict)

    def add_violation(self, v: Violation):
        self.violations.append(v)

    def get_by_lesson(self, lesson: str) -> list[Violation]:
        return [v for v in self.violations if v.lesson == lesson]

    def summary(self) -> dict:
        """生成摘要"""
        by_type = {}
        by_severity = {}
        by_lesson = {}

        for v in self.violations:
            by_type[v.violation_type] = by_type.get(v.violation_type, 0) + 1
            by_severity[v.severity] = by_severity.get(v.severity, 0) + 1
            by_lesson[v.lesson] = by_lesson.get(v.lesson, 0) + 1

        return {
            "total_files": self.total_files,
            "total_violations": len(self.violations),
            "by_type": by_type,
            "by_severity": by_severity,
            "by_lesson": by_lesson,
        }


def extract_lesson_from_path(path: Path) -> str | None:
    """从文件路径提取课程编号"""
    path_str = str(path)
    for lesson in LESSON_ORDER:
        if lesson in path_str:
            return lesson
    return None


def detect_syntax_violations(content: str, path: Path) -> list[Violation]:
    """检测语法越界"""
    violations = []
    lesson = extract_lesson_from_path(path)
    if not lesson or lesson not in KNOWLEDGE_BOUNDARY:
        return violations

    boundary = KNOWLEDGE_BOUNDARY[lesson]
    forbidden = boundary.get("forbidden_syntax", [])

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return violations

    lines = content.split("\n")

    class SyntaxVisitor(ast.NodeVisitor):
        def visit(self, node):
            node_type = type(node).__name__
            if node_type in forbidden:
                line_no = getattr(node, "lineno", 0)
                snippet = lines[line_no - 1].strip() if line_no <= len(lines) else ""

                # 处理 ClassDef 特殊逻辑
                if "ClassDef" in forbidden and node_type == "ClassDef":
                    if lesson in ["L01", "L02", "L03", "L04", "L05", "L06"]:
                        violations.append(Violation(
                            lesson=lesson,
                            file_path=str(path),
                            line_number=line_no,
                            violation_type="syntax",
                            code_snippet=snippet[:80],
                            description=f"课程 {lesson} 禁止使用 class 定义类",
                            severity="CRITICAL"
                        ))
                elif node_type in forbidden:
                    violations.append(Violation(
                        lesson=lesson,
                        file_path=str(path),
                        line_number=line_no,
                        violation_type="syntax",
                        code_snippet=snippet[:80],
                        description=f"课程 {lesson} 禁止使用 {node_type}",
                        severity="HIGH"
                    ))

            self.generic_visit(node)

    SyntaxVisitor().visit(tree)
    return violations


def detect_annotation_violations(content: str, path: Path) -> list[Violation]:
    """检测类型注解越界"""
    violations = []
    lesson = extract_lesson_from_path(path)
    if not lesson or lesson not in KNOWLEDGE_BOUNDARY:
        return violations

    boundary = KNOWLEDGE_BOUNDARY[lesson]
    forbidden_patterns = boundary.get("forbidden_type_annotations", [])

    if not forbidden_patterns:
        return violations

    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        for pattern in forbidden_patterns:
            if re.search(pattern, line):
                # 检查是否是注释（# 后的内容）
                comment_pos = line.find("#")
                match_pos = re.search(pattern, line).start()
                if comment_pos != -1 and comment_pos < match_pos:
                    continue  # 跳过注释中的内容

                violations.append(Violation(
                    lesson=lesson,
                    file_path=str(path),
                    line_number=i,
                    violation_type="annotation",
                    code_snippet=line.strip()[:80],
                    description=f"课程 {lesson} 禁止使用泛型类型注解 {pattern}",
                    severity="HIGH"
                ))

    return violations


def detect_term_violations(content: str, path: Path) -> list[Violation]:
    """检测文档中的术语越界"""
    violations = []
    lesson = extract_lesson_from_path(path)
    if not lesson or lesson not in KNOWLEDGE_BOUNDARY:
        return violations

    boundary = KNOWLEDGE_BOUNDARY[lesson]
    forbidden_terms = boundary.get("forbidden_terms", [])

    if not forbidden_terms:
        return violations

    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # 跳过代码块
        if line.strip().startswith("```"):
            continue
        if line.strip().startswith("#"):
            continue  # 跳过注释

        for term in forbidden_terms:
            # 简单匹配（忽略大小写）
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            matches = pattern.findall(line)
            if matches:
                violations.append(Violation(
                    lesson=lesson,
                    file_path=str(path),
                    line_number=i,
                    violation_type="term",
                    code_snippet=line.strip()[:80],
                    description=f"课程 {lesson} 中出现禁止术语 '{term}'",
                    severity="MEDIUM"
                ))

    return violations


def audit_file(path: Path) -> list[Violation]:
    """审计单个文件"""
    violations = []

    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return violations

    violations.extend(detect_syntax_violations(content, path))
    violations.extend(detect_annotation_violations(content, path))

    # lesson.md 和 README.md 检查术语
    if path.suffix == ".md":
        violations.extend(detect_term_violations(content, path))

    return violations


def audit_lesson(lesson_path: Path) -> list[Violation]:
    """审计整个课程目录"""
    violations = []

    # 扫描教学核心文件：examples/、exercises/、lesson.md、README.md
    # 注意：tests/ 和 solutions/ 不在审查范围内（CI 系统使用）
    patterns = ["examples/**/*.py", "exercises/**/*.py", "lesson.md", "README.md"]
    for pattern in patterns:
        for file_path in lesson_path.glob(pattern):
            # 排除 __pycache__ 和 .venv
            if "__pycache__" in str(file_path) or ".venv" in str(file_path):
                continue
            violations.extend(audit_file(file_path))

    return violations


def generate_report(result: AuditResult) -> str:
    """生成审查报告"""
    summary = result.summary()

    report = []
    report.append("# Stage 0 知识点越界全面审查报告")
    report.append("")
    report.append("## 执行摘要")
    report.append("")
    report.append("| 指标 | 数值 |")
    report.append("|------|------|")
    report.append(f"| 审查文件总数 | {summary['total_files']} |")
    report.append(f"| 发现违规数 | {summary['total_violations']} |")
    report.append("")
    report.append("### 按违规类型分布")
    report.append("")
    for t, count in sorted(summary["by_type"].items(), key=lambda x: -x[1]):
        report.append(f"- **{t}**: {count} 个")
    report.append("")
    report.append("### 按严重程度分布")
    report.append("")
    for s in ["CRITICAL", "HIGH", "MEDIUM"]:
        count = summary["by_severity"].get(s, 0)
        report.append(f"- **{s}**: {count} 个")
    report.append("")
    report.append("### 按课程分布")
    report.append("")
    for lesson in LESSON_ORDER:
        count = summary["by_lesson"].get(lesson, 0)
        if count > 0:
            report.append(f"- **{lesson}**: {count} 个违规")
    report.append("")

    # 按课程详细列出违规
    report.append("## 违规详情")
    report.append("")

    for lesson in LESSON_ORDER:
        lesson_violations = result.get_by_lesson(lesson)
        if not lesson_violations:
            continue

        report.append(f"### {lesson}")
        report.append("")

        # 按文件分组
        by_file = {}
        for v in lesson_violations:
            by_file.setdefault(v.file_path, []).append(v)

        for file_path, file_violations in by_file.items():
            rel_path = Path(file_path).relative_to(Path("/Users/nexo/python-fullstack/stage0-python-basics"))
            report.append(f"#### `{rel_path}`")
            report.append("")
            report.append("| 行号 | 类型 | 严重 | 代码片段 | 说明 |")
            report.append("|------|------|------|----------|------|")
            for v in sorted(file_violations, key=lambda x: x.line_number):
                snippet = v.code_snippet.replace("|", "\\|")[:50]
                report.append(f"| {v.line_number} | {v.violation_type} | {v.severity} | `{snippet}` | {v.description} |")
            report.append("")

    return "\n".join(report)


def scan_lesson_files(lesson_dir: Path) -> list[tuple]:
    """扫描课程目录，返回需要审计的文件列表"""
    files = []
    patterns = ["examples/**/*.py", "exercises/**/*.py", "lesson.md", "README.md"]
    for pattern in patterns:
        for file_path in lesson_dir.glob(pattern):
            if "__pycache__" in str(file_path) or ".venv" in str(file_path):
                continue
            files.append(file_path)
    return files


def main():
    base_path = Path("/Users/nexo/python-fullstack/stage0-python-basics/lessons")
    result = AuditResult()

    print("🔍 开始 Stage 0 知识点越界审查...")
    print("📋 审查范围: examples/, exercises/, lesson.md, README.md")
    print("⚠️  排除范围: tests/, solutions/ (CI 系统使用)")
    print()

    for lesson_dir in sorted(base_path.iterdir()):
        if not lesson_dir.is_dir():
            continue

        lesson_name = lesson_dir.name

        # 使用新函数获取文件列表
        for file_path in scan_lesson_files(lesson_dir):
            result.total_files += 1
            violations = audit_file(file_path)

            for v in violations:
                result.add_violation(v)

                # 打印进度
                if v.severity == "CRITICAL":
                    icon = "🚨"
                elif v.severity == "HIGH":
                    icon = "⚠️"
                else:
                    icon = "📝"
                print(f"  {icon} [{lesson_name}] {file_path.name}:{v.line_number} - {v.violation_type}")

    print()
    print(f"📊 审查完成: {result.total_files} 个文件, {len(result.violations)} 个违规")
    print()

    # 生成报告
    report = generate_report(result)

    # 保存报告
    report_path = Path("/Users/nexo/python-fullstack/docs/stage0-audit-report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(f"📄 报告已保存至: {report_path}")

    # 打印摘要
    summary = result.summary()
    print()
    print("=== 摘要 ===")
    print(f"总违规: {summary['total_violations']}")
    print(f"CRITICAL: {summary['by_severity'].get('CRITICAL', 0)}")
    print(f"HIGH: {summary['by_severity'].get('HIGH', 0)}")
    print(f"MEDIUM: {summary['by_severity'].get('MEDIUM', 0)}")

    return 0 if len(result.violations) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
