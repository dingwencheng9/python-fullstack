"""

from __future__ import annotations

练习 6：PEP 750 t-string 实战 — 写一个安全的 shell 命令构造器

⚠️ 需要 Python 3.14+。运行：python3.14 stage2-engineering/lessons/L21-python313-experience/exercises/exercise_06_tstring_shell_safe.py

背景：
    用户输入的字符串如果直接拼进 shell 命令，会造成命令注入：
        evil = "; rm -rf /"
        os.system(f"ls {evil}")    # 灾难
    本练习要求：用 t-string + 自定义渲染器，把用户输入转义为安全 shell argv。
"""

from __future__ import annotations

import sys

# ============================================================================
# 任务 1：把 Template 转为 subprocess 友好的 argv 列表
# ============================================================================

# TODO: 实现 to_argv(template) -> list[str]
#   - template 是 t-string 返回的 Template 对象
#   - 静态片段（template.strings）直接 shlex.split
#   - 插值（template.interpolations）作为单个 argv 元素，原样保留（不切分、不转义到 shell 字符串）
#   - 最终返回的列表可以直接传给 subprocess.run
#
# 示例输入：t"ls -la {user_path}"，user_path = "; rm -rf /"
# 期望输出：["ls", "-la", "; rm -rf /"]   ← 危险字符作为单个参数，不会被 shell 解释


def to_argv(template) -> list[str]:
    """请实现"""
    raise NotImplementedError


# ============================================================================
# 任务 2：实现一个调试用的 to_shell_string(template) -> str
# ============================================================================

# TODO: 把 Template 转回 shell 字符串形式，但对插值用 shlex.quote 转义
#   仅作日志/调试展示，不要传给 os.system
#
# 示例：t"ls -la {path}"，path = "my dir"
# 期望：'ls -la my\\ dir'   或 "ls -la 'my dir'"


def to_shell_string(template) -> str:
    raise NotImplementedError


# ============================================================================
# 自检
# ============================================================================


def main() -> None:
    if sys.version_info < (3, 14):
        print("⚠️ 本练习需要 Python 3.14+，当前", sys.version_info[:3])
        return

    # 用 exec 推迟 t-string 解析，避免 3.13 的语法错误
    test_code = """
evil_path = "; rm -rf /"
tmpl = t"ls -la {evil_path}"
argv = to_argv(tmpl)
print(f"  Task 1: argv = {argv}")
expected_evil_in_argv = "; rm -rf /" in argv
print(f"           危险字符是否作为单个 argv 元素: {'✅' if expected_evil_in_argv else '❌'}")
print(f"           是否避免被 shell 切分: {'✅' if len(argv) >= 2 else '❌'}")

shell_str = to_shell_string(tmpl)
print(f"  Task 2: shell string = {shell_str!r}")
print(f"           危险字符已转义: {'✅' if '/' not in shell_str.split()[-1].rstrip(chr(39)) else '❌'}")
"""
    try:
        exec(test_code, globals())
    except NotImplementedError:
        print("  ⏳ 任务待实现")


if __name__ == "__main__":
    main()
