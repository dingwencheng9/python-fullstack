"""L16 示例 3：前瞻、后顾与否定环视。"""

from __future__ import annotations

import re


def demo_positive_lookahead() -> None:
    """演示正向前瞻：匹配后面跟 GB 的数字。"""
    text = "内存 16GB，硬盘 512GB，价格 999USD"
    print("=== 正向前瞻 ===")
    print(re.findall(r"\d+(?=GB)", text))


def demo_negative_lookahead() -> None:
    """演示否定前瞻：排除 tmp 文件。"""
    files = "app.py app.tmp test.py cache.tmp"
    print("\n=== 否定前瞻 ===")
    print(re.findall(r"\b(?!\w+\.tmp\b)\w+\.\w+", files))


def demo_lookbehind() -> None:
    """演示正向后顾和否定后顾。"""
    prices = "价格 $19.99，折扣 $5.00，库存 20"
    escaped = r"a,b\,c,d"
    print("\n=== 后顾 ===")
    print(re.findall(r"(?<=\$)\d+(?:\.\d{2})?", prices))
    print([match.start() for match in re.finditer(r"(?<!\\),", escaped)])


def demo_password_strength() -> None:
    """演示密码强度校验。"""
    pattern = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")
    passwords = ["Passw0rd!", "password", "PASSWORD1", "Short1!"]
    print("\n=== 密码强度 ===")
    for password in passwords:
        print(password, bool(pattern.fullmatch(password)))


def main() -> None:
    """运行全部环视示例。"""
    demo_positive_lookahead()
    demo_negative_lookahead()
    demo_lookbehind()
    demo_password_strength()


if __name__ == "__main__":
    main()
