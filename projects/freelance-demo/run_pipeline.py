"""Freelance Demo · 数据分析阶段封装。

from __future__ import annotations

把项目 1 的爬取 JSON 直接喂给项目 3 的分析管道，
输出一份 Markdown 报告。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Freelance Demo · 数据分析包装")
    parser.add_argument("--input", required=True, help="项目 1 输出的 JSON 文件")
    parser.add_argument("--output", required=True, help="Markdown 报告输出路径")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"❌ 输入文件不存在: {in_path}", file=sys.stderr)
        sys.exit(1)

    if not in_path.is_file():
        print(f"❌ 输入路径不是文件: {in_path}", file=sys.stderr)
        sys.exit(1)

    # 验证输出目录可写
    out_path = Path(args.output).resolve()
    out_dir = out_path.parent
    if not out_dir.exists():
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"❌ 无法创建输出目录 {out_dir}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        from pipeline.report import generate_markdown_report

        result_path = generate_markdown_report(in_path, str(out_path))
        print(f"✅ 报告已生成: {result_path}")
    except ImportError as e:
        print(f"❌ 导入失败（请确保 PYTHONPATH 包含 project 3）: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 报告生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
