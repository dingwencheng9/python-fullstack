"""

from __future__ import annotations

练习 6 参考答案：PEP 750 t-string 安全 shell
"""

from __future__ import annotations

import shlex
import sys


def to_argv(template) -> list[str]:
    """把 t-string Template 转成 subprocess argv 列表

    原则：
    - 静态片段（template.strings）按 shell 词法切分
    - 插值（template.interpolations）作为单个 argv 元素，原样保留
    - 这样危险字符无论是空格、分号、`、$ 都不会被 shell 解释
    """
    argv: list[str] = []
    pending = ""

    for i, segment in enumerate(template.strings):
        # 静态片段按 shell 词法切分（处理空格、引号等）
        # 但末尾如果没有空白，要和下一个插值粘连
        if segment:
            tokens = shlex.split(segment)
            # 判断 segment 是否以空白结束 — 如果是，最后一个 token 独立
            # 如果不是，最后一个 token 要和下一个插值粘连（暂存到 pending）
            if not segment[-1].isspace() and tokens and i < len(template.interpolations):
                argv.extend(pending + t for t in tokens[:-1]) if pending else argv.extend(tokens[:-1])
                pending = (pending + tokens[-1]) if pending else tokens[-1]
            else:
                if pending:
                    argv.append(pending)
                    pending = ""
                argv.extend(tokens)

        # 插值原样追加（关键：不切分、不解释为 shell 元字符）
        if i < len(template.interpolations):
            value = str(template.interpolations[i].value)
            if pending:
                # 与前一个 token 粘连
                argv.append(pending + value)
                pending = ""
            else:
                argv.append(value)

    if pending:
        argv.append(pending)

    return argv


def to_shell_string(template) -> str:
    """渲染为 shell 字符串形式，插值用 shlex.quote 转义"""
    parts = []
    for i, segment in enumerate(template.strings):
        parts.append(segment)
        if i < len(template.interpolations):
            parts.append(shlex.quote(str(template.interpolations[i].value)))
    return "".join(parts)


def main() -> None:
    if sys.version_info < (3, 14):
        print("⚠️ 需要 Python 3.14+")
        return

    code = """
print("Python:", sys.version_info[:3])

# 测试 1：危险路径
evil_path = "; rm -rf /"
tmpl = t"ls -la {evil_path}"
argv = to_argv(tmpl)
print(f"  argv = {argv}")
assert argv == ["ls", "-la", "; rm -rf /"], f"unexpected: {argv}"
print("  ✅ Task 1 通过：危险字符作为单个 argv 元素")

# 测试 2：shell 字符串渲染
shell_str = to_shell_string(tmpl)
print(f"  shell string = {shell_str!r}")
assert "rm -rf" not in shell_str.split("ls -la ")[1] or shell_str.count("'") >= 2
print("  ✅ Task 2 通过：危险字符已转义")
"""
    exec(code, globals())


if __name__ == "__main__":
    main()
