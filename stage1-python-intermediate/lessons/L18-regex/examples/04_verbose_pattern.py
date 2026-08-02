"""L16 示例 4：re.VERBOSE 模式 - 可维护的长正则表达式。

re.VERBOSE（也写作 re.X）允许在正则表达式中添加空白字符和注释，
大幅提升复杂正则的可读性和可维护性。
"""

from __future__ import annotations

import re


def demo_basic_verbose() -> None:
    """演示 re.VERBOSE 的基本用法。"""
    print("=== re.VERBOSE 基础 ===")

    # 传统写法：一行搞定，难以阅读
    pattern_compact = r"^\w+[\.-]?\w*@\w+\.\w{2,}$"
    emails = ["user@example.com", "john.doe@company.co.uk", "invalid", "@nodomain"]

    print("紧凑模式:")
    for email in emails:
        print(f"  {email}: {bool(re.match(pattern_compact, email))}")

    # VERBOSE 模式：格式化后易于理解
    pattern_verbose = re.compile(
        r"""
        ^                          # 字符串开头
        \w+                        # 用户名（字母数字下划线）
        [\.-]?\w*                  # 可选的中间名分隔符
        @                          # @ 符号
        \w+                        # 域名
        \.                         # 点号
        \w{2,}                     # 顶级域名（至少2个字符）
        $                          # 字符串结尾
        """,
        re.VERBOSE,
    )

    print("\nVERBOSE 模式:")
    for email in emails:
        print(f"  {email}: {bool(pattern_verbose.match(email))}")


def demo_complex_pattern() -> None:
    """演示复杂正则使用 VERBOSE 的优势。"""
    print("\n=== 复杂正则：HTTP 请求行解析 ===")

    # 不使用 VERBOSE：难以阅读和调试
    # pattern = r'^(GET|POST|PUT|DELETE|PATCH)\s+(/[\w/{}?-]*)\s+HTTP/(\d+\.\d+)$'

    # 使用 VERBOSE：清晰展示 HTTP 请求格式
    http_request = re.compile(
        r"""
        ^                              # 开始
        (GET|POST|PUT|DELETE|PATCH)   # HTTP 方法
        \s+                            # 空格分隔
        (                              # 路径组开始
          /                             # 路径以 / 开头
          (?:[\w{}/?=&%-]+/?)*         # 路径段（可包含参数）
        )                              # 路径组结束
        \s+                            # 空格分隔
        HTTP/                          # HTTP 版本前缀
        (\d+\.\d+)                     # 版本号
        $                              # 结束
        """,
        re.VERBOSE,
    )

    requests = [
        "GET /api/users HTTP/1.1",
        "POST /api/users?name=test HTTP/1.0",
        "DELETE /api/users/123 HTTP/2.0",
        "GET  HTTP/1.1",  # 无路径
        "INVALID /path HTTP/1.1",  # 无效方法
        "GET /api HTTP/INVALID",  # 无效版本
    ]

    print("测试 HTTP 请求:")
    for req in requests:
        match = http_request.match(req)
        if match:
            print(f"  ✓ {req}")
            print(f"    方法: {match.group(1)}, 路径: {match.group(2)}, 版本: {match.group(3)}")
        else:
            print(f"  ✗ {req}")


def demo_inline_flags_with_verbose() -> None:
    """演示 VERBOSE 模式中嵌入内联标志。"""
    print("\n=== VERBOSE + 内联标志 ===")

    # 在注释中添加 (?i) 等内联标志
    phone_pattern = re.compile(
        r"""
        ^                          # 开始
        (?:\+86)?                   # 可选的国家代码 (?i: 不区分大小写，但数字不需要)
        \s*                        # 可选空格
        (?:1[3-9]\d)               # 手机号段（130-199）
        [\s-]?                     # 可选分隔符
        \d{4}                      # 前4位
        [\s-]?                     # 可选分隔符
        \d{4}                      # 后4位
        $                          # 结束
        """,
        re.VERBOSE,
    )

    phones = [
        "13812345678",
        "+86 138 1234 5678",
        "138-1234-5678",
        "12345678901",  # 非法号段
    ]

    print("测试手机号:")
    for phone in phones:
        print(f"  {'✓' if phone_pattern.match(phone) else '✗'} {phone}")


def main() -> None:
    """运行全部 re.VERBOSE 示例。"""
    demo_basic_verbose()
    demo_complex_pattern()
    demo_inline_flags_with_verbose()
    print("\n💡 提示: re.VERBOSE 让复杂正则表达式可读、可维护、可测试！")


if __name__ == "__main__":
    main()
