"""
example_06_python314_tstring.py — PEP 750 模板字符串（Python 3.14+）

PEP 750 在 Python 3.14 引入"t-string"（template strings），是 f-string 的安全
替代品。t-string 不立即拼接，而是返回 Template 对象，供后续按需求处理：
SQL 参数化、HTML 转义、shell 命令转义、i18n 翻译……

f-string 的痛点：
    user = "'; DROP TABLE users; --"
    sql = f"SELECT * FROM users WHERE name = '{user}'"  # ⚠️ SQL 注入

t-string 的解法：
    sql = t"SELECT * FROM users WHERE name = {user}"   # 返回 Template
    # 由专门的格式化函数把 Template 转成参数化 SQL
    cursor.execute(*safe_sql(sql))                      # 安全

运行要求：
    python3.14 example_06_python314_tstring.py

教学要点：
    1. t-string 与 f-string 语法几乎相同，差别只是前缀 t/f
    2. t"..." 返回 Template 对象（含 strings 元组 + interpolations 列表）
    3. 应用场景：SQL、HTML、shell、日志结构化、i18n

⚠️ 安全说明：
    本文件使用 exec() 仅用于教学演示 Python 3.14 t-string 语法特性。
    exec() 在生产环境中禁止使用，会导致任意代码执行（RCE）漏洞。
    实际代码应直接使用 t-string 字面量（Python 3.14+），无需 exec()。
"""

from __future__ import annotations

import sys


def demo_tstring_basics() -> None:
    """t-string 基础结构"""
    print("=" * 70)
    print("演示 1：t-string 返回 Template 对象")
    print("=" * 70)

    if sys.version_info < (3, 14):
        print("  ⚠️ 需要 Python 3.14+，当前", sys.version_info[:3])
        return

    # 注意：t-string 是语法层特性，旧版本无法解析这一行
    # 我们通过 exec 推迟编译，让旧版本也能加载本文件
    code = """
from string.templatelib import Template

name = "Alice"
balance = 100
tmpl = t"Hi {name}, your balance is {balance}"

print(f"  类型：{type(tmpl).__name__}")
print(f"  strings：{tmpl.strings}")
print(f"  interpolations：")
for interp in tmpl.interpolations:
    print(f"    expression={interp.expression!r}, value={interp.value!r}")
print()
"""
    # ⚠️ 反模式（教学演示 Python 3.14 t-string 语法）
    # 生产环境禁止使用 exec()，会导致任意代码执行（RCE）漏洞
    exec(code)


def demo_safe_sql() -> None:
    """t-string 实战：安全的参数化 SQL"""
    print("=" * 70)
    print("演示 2：t-string 实战 — 防 SQL 注入")
    print("=" * 70)

    if sys.version_info < (3, 14):
        print("  ⚠️ 需要 Python 3.14+，跳过")
        return

    code = '''
from string.templatelib import Template


def safe_sql(template: Template) -> tuple[str, list]:
    """把 t-string 转成参数化 SQL（占位符 + 参数列表）"""
    parts = []
    params = []
    for i, segment in enumerate(template.strings):
        parts.append(segment)
        if i < len(template.interpolations):
            parts.append("?")
            params.append(template.interpolations[i].value)
    return "".join(parts), params


# 危险输入：包含 SQL 元字符
user_input = "Alice' OR '1'='1"
user_id = 42

sql_template = t"SELECT * FROM users WHERE name = {user_input} AND id = {user_id}"
sql_string, params = safe_sql(sql_template)

print(f"  危险输入：{user_input!r}")
print(f"  生成的 SQL（安全）：{sql_string}")
print(f"  参数列表（独立传递）：{params}")
print(f"  ✅ 用户输入永远不会拼进 SQL 字符串")
print()
'''
    # ⚠️ 反模式（教学演示 Python 3.14 t-string 语法）
    # 生产环境禁止使用 exec()，会导致任意代码执行（RCE）漏洞
    # 本示例在受控环境下演示 Python 3.14 t-string 特性
    exec(code)


def demo_safe_html() -> None:
    """t-string 实战：HTML 转义"""
    print("=" * 70)
    print("演示 3：t-string 实战 — HTML 自动转义")
    print("=" * 70)

    if sys.version_info < (3, 14):
        print("  ⚠️ 需要 Python 3.14+，跳过")
        return

    import html as html_module

    code = """
from string.templatelib import Template


def safe_html(template):
    parts = []
    for i, segment in enumerate(template.strings):
        parts.append(segment)
        if i < len(template.interpolations):
            value = str(template.interpolations[i].value)
            parts.append(html_module.escape(value))
    return "".join(parts)


user_comment = "<script>alert('XSS')</script>"
page_template = t"<div>用户评论：{user_comment}</div>"
print(f"  原始 t-string 插值：{user_comment!r}")
print(f"  安全 HTML 输出：{safe_html(page_template)}")
print(f"  ✅ <script> 被自动转义为 &lt;script&gt;")
print()
"""
    # ⚠️ 反模式（教学演示 Python 3.14 t-string 语法）
    # 生产环境禁止使用 exec()，会导致任意代码执行（RCE）漏洞
    exec(code, {"html_module": html_module})


def demo_diff_with_fstring() -> None:
    """t-string 和 f-string 的对比"""
    print("=" * 70)
    print("演示 4：t-string vs f-string 关键差异")
    print("=" * 70)

    if sys.version_info < (3, 14):
        print("  ⚠️ 需要 Python 3.14+，跳过")
        return

    code = """
name = "Alice"

# f-string：立即拼接为字符串
f_result = f"Hi {name}"
print(f"  f-string 类型：{type(f_result).__name__} -> {f_result!r}")

# t-string：返回 Template 对象，延迟处理
t_result = t"Hi {name}"
print(f"  t-string 类型：{type(t_result).__name__}")
print(f"  t-string 可以被序列化、传递、按目标格式渲染")
print()
print("  使用建议：")
print("    - 立即输出文本 → f-string")
print("    - 文本走向不可信通道（SQL/HTML/shell）→ t-string + 专用格式化")
"""
    # ⚠️ 反模式（教学演示 Python 3.14 t-string 语法）
    # 生产环境禁止使用 exec()，会导致任意代码执行（RCE）漏洞
    exec(code)


def main() -> None:
    print(f"\nPython 版本：{sys.version_info[:3]}\n")
    demo_tstring_basics()
    demo_safe_sql()
    demo_safe_html()
    demo_diff_with_fstring()


if __name__ == "__main__":
    main()
