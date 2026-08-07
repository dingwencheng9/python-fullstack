#!/usr/bin/env python3
"""
AST 精确修复脚本 - Stage 0 exercises 知识点越界
将 def 函数体替换为 pass 语句（模板型练习）
"""

import ast
from pathlib import Path


class FunctionTemplateRewriter(ast.NodeTransformer):
    """将函数体替换为 pass 语句"""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """转换函数定义"""
        # 检查是否有文档字符串
        has_docstring = (
            len(node.body) > 0 and
            isinstance(node.body[0], ast.Expr) and
            isinstance(node.body[0].value, ast.Constant) and
            isinstance(node.body[0].value.value, str)
        )

        # 构建新函数体
        new_body = [node.body[0]] if has_docstring else []

        # 添加 pass 语句
        pass_stmt = ast.Pass()
        if has_docstring and len(node.body) > 0:
            pass_stmt.lineno = node.body[0].lineno + 1
            pass_stmt.col_offset = node.body[0].col_offset + 4
        else:
            pass_stmt.lineno = node.lineno + 1
            pass_stmt.col_offset = node.col_offset + 4

        new_body.append(pass_stmt)

        # 创建新函数节点
        new_node = ast.FunctionDef(
            lineno=node.lineno,
            col_offset=node.col_offset,
            name=node.name,
            args=node.args,
            body=new_body,
            decorator_list=list(node.decorator_list),
            returns=node.returns,
            type_comment=node.type_comment,
        )
        ast.copy_location(new_node, node)

        return new_node

    def visit_async_function_def(self, node: ast.AsyncFunctionDef) -> ast.FunctionDef:
        """将异步函数转换为同步函数（移除 async def 中的 async 关键字）"""
        # 创建同步版本的函数定义
        new_node = ast.FunctionDef(
            lineno=node.lineno,
            col_offset=node.col_offset,
            name=node.name,
            args=node.args,
            body=node.body,
            decorator_list=list(node.decorator_list),
            returns=node.returns,
            type_comment=node.type_comment,
        )
        ast.copy_location(new_node, node)
        return new_node

    # 别名：AsyncFunctionDef 也使用相同的转换逻辑
    visit_AsyncFunctionDef = visit_async_function_def  # noqa: N815


def fix_file_ast(file_path: Path) -> bool:
    """使用 AST 修复文件"""
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        print(f"  ⚠️ 语法错误: {e}")
        return False

    # 检查是否有需要修复的函数
    has_functions = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        for node in ast.walk(tree)
    )

    if not has_functions:
        return False

    # 转换
    rewriter = FunctionTemplateRewriter()
    new_tree = rewriter.visit(tree)
    ast.fix_missing_locations(new_tree)

    # 生成代码
    try:
        new_source = ast.unparse(new_tree)
    except Exception as e:
        print(f"  ⚠️ AST unparse 失败: {e}")
        return False

    if new_source != source:
        file_path.write_text(new_source, encoding="utf-8")
        return True
    return False


def main():
    stage0 = Path("/Users/nexo/python-fullstack/stage0-python-basics/lessons")

    # 需要修复的文件
    files_to_fix = [
        # L02: def 函数越界
        ("L02-operators-control", "01_arithmetic_conditions.py"),
        ("L02-operators-control", "02_logical_operators.py"),
        ("L02-operators-control", "03_bitwise_operations.py"),
        ("L02-operators-control", "04_loops.py"),
        ("L02-operators-control", "05_match_case.py"),
        ("L02-operators-control", "06_comprehensive.py"),
        # L03: def 函数越界
        ("L03-data-structures", "01_exercise.py"),
        ("L03-data-structures", "02_exercise.py"),
        ("L03-data-structures", "03_exercise.py"),
    ]

    print("=" * 60)
    print("🔧 Stage 0 exercises 知识点越界修复 (AST 版本)")
    print("=" * 60)

    fixed_count = 0
    for lesson_dir, filename in files_to_fix:
        file_path = stage0 / lesson_dir / "exercises" / filename
        if not file_path.exists():
            print(f"  ⚠️ 跳过 {file_path} (不存在)")
            continue

        if fix_file_ast(file_path):
            print(f"  ✅ 已修复 [{lesson_dir}] {filename}")
            fixed_count += 1
        else:
            print(f"  ⚪ 无需修改 [{lesson_dir}] {filename}")

    print(f"\n✅ 共修复 {fixed_count} 个文件")


if __name__ == "__main__":
    main()
