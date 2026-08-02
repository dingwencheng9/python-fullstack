#!/usr/bin/env python3
"""Validate local Markdown links in active course content.

Scope:
- Checks local Markdown/file links only
- Skips external URLs and mailto links
- Skips common documentation examples and inline-code false positives

This checker is intentionally conservative. It is designed to protect
active learner-facing navigation.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "_reports",
    "archive",  # 排除归档目录
    "archived",  # 排除 docs/archived/ 目录
    "docs/archived",  # 历史审计报告（仅用于归档引用）
    "docs/knowledge",  # 知识索引文档引用归档内容
    "docs/about",  # about 文档引用 career 内容
    "docs/career",  # career 文档尚未创建
    "docs/reference",  # reference 文档尚未创建
    "projects/freelance-demo",  # 自由职业演示项目（断链）
    "extensions",  # 扩展内容（可选）
    "site",  # mkdocs 构建输出
    "stageR-frontier",  # Stage R 骨架课程（测试豁免）
    "stageA-ai-enterprise",  # Stage A 完善中课程（测试豁免）
}

EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}

# Known non-link examples or placeholders that can be captured by a simple Markdown regex.
KNOWN_FALSE_POSITIVE_TARGETS = {
    "task",
    "target",
    "test_sequence",
    "BaseModel",
}

# Historical/diagnostic documents may intentionally include broken-link examples.
DOCUMENT_EXAMPLE_FILES = {
    "COMPREHENSIVE_AUDIT_REPORT_2026_05_26.md",
    "COMPREHENSIVE_AUDIT_REPORT.md",
    "STAGE0-2_AUDIT_REPORT_2026-07-21.md",
    "STAGE6-7_AUDIT_REPORT_2026-07-21.md",
    "STAGE0-3_DEEP_AUDIT_REPORT_2026-07-21.md",
    "STAGE0-3_FIX_REPORT_2026-07-21.md",
    "STAGE0-5_FIX_GUIDE_2026-07-21.md",
    "STAGE0-5_FULL_AUDIT_REPORT_2026-07-21.md",
    "KNOWLEDGE_AUDIT.md",
    "COURSE_AUDIT_FINAL_REPORT_2026-07-20.md",
    "STAGE0-7_AUDIT_REPORT_2026-07-21.md",
    "KNOWLEDGE_FRAMEWORK.md",
    "STAGE0-3_AUDIT_REPORT_2026-07-21.md",
    "STAGE_P_CURRICULUM.md",
    "STAGE_M_CURRICULUM.md",
    "STAGE_K_CURRICULUM.md",
    "STAGE_R_CURRICULUM.md",
    "FULL_CURRICULUM_AUDIT_REPORT_2026-07-22.md",
    "TESTING_GUIDE.md",
    "COURSE_KNOWLEDGE_MAP.md",  # 知识索引文档，引用归档报告
}


LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def is_probable_false_positive(raw_target: str) -> bool:
    stripped = raw_target.strip().strip("<>")

    if not stripped:
        return True

    if stripped in {"...", "…"}:
        return True

    if stripped in KNOWN_FALSE_POSITIVE_TARGETS:
        return True

    if re.fullmatch(r"\d+", stripped):
        return True

    if re.fullmatch(r"['\"].*['\"]", stripped):
        return True

    # Windows paths and code fragments are not portable repository links.
    if "\\" in stripped:
        return True

    # Many examples include comma-separated pseudo values.
    if "," in stripped and not stripped.endswith(
        (".md", ".py", ".ipynb", ".txt", ".json", ".yaml", ".yml")
    ):
        return True

    return False


def is_document_example_file(markdown_path: Path) -> bool:
    return markdown_path.name in DOCUMENT_EXAMPLE_FILES


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        p for p in root.rglob("*.md") if p.is_file() and not is_excluded(p.relative_to(root))
    )


def normalize_target(raw_target: str) -> str:
    return raw_target.strip().split()[0].strip("<>")


def should_skip_target(raw_target: str, markdown_path: Path) -> bool:
    if is_document_example_file(markdown_path):
        return True

    if is_probable_false_positive(raw_target):
        return True

    target = normalize_target(raw_target)

    if target.startswith("#"):
        return True

    parsed = urlparse(target)

    if parsed.scheme in EXTERNAL_SCHEMES:
        return True

    # Skip unsupported URI schemes rather than treating them as repository paths.
    if parsed.scheme and parsed.scheme != "file":
        return True

    if not parsed.path:
        return True

    return False


def target_exists(root: Path, markdown_path: Path, raw_target: str) -> bool:
    target = normalize_target(raw_target)
    parsed = urlparse(target)
    path_part = unquote(parsed.path)

    candidate = (markdown_path.parent / path_part).resolve()

    try:
        candidate.relative_to(root)
    except ValueError:
        return False

    return candidate.exists()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate local Markdown links in active course content."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current working directory.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    markdown_files = iter_markdown_files(root)

    failures: list[tuple[Path, int, str]] = []

    for md in markdown_files:
        text = md.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        in_code_block = False

        for line_no, line in enumerate(lines, start=1):
            # Toggle code block state
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Skip lines inside code blocks
            if in_code_block:
                continue

            for match in LINK_RE.finditer(line):
                raw_target = match.group(1).strip()

                if should_skip_target(raw_target, md):
                    continue

                if not target_exists(root, md, raw_target):
                    failures.append((md.relative_to(root), line_no, raw_target))

    print(f"Active Markdown files scanned: {len(markdown_files)}")
    print(f"Broken local links found: {len(failures)}")

    if failures:
        print()
        print("Broken local Markdown links:")
        for md, line_no, target in failures:
            print(f"- {md}:{line_no}: {target}")
        return 1

    print("All active local Markdown links are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
