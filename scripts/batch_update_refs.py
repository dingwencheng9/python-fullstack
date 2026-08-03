#!/usr/bin/env python3
"""批量更新课程编号引用"""
from pathlib import Path

# 定义替换规则
REPLACEMENTS = {
    # Stage 0 课程编号更新
    "L05": "L05",
    "L06-file-operations": "L06-file-operations",
    "L06-file": "L06-file",
    "L07-oop-basics": "L07-oop-basics",
    "L07-oop": "L07-oop",
    "L08-magic-methods": "L08-magic-methods",
    "L08-magic": "L08-magic",
    "L09-exceptions": "L09-exceptions",
    "L09-exception": "L09-exception",
    "L10-basics-project": "L10-basics-project",
    "L10-basics": "L10-basics",
    # Stage S 爬虫课程
    "S01": "S01",
    "S02": "S02",
    "S03": "S03",
    "S04": "S04",
    "S05": "S05",
    "S06": "S06",
    "S07": "S07",
    "S08": "S08",
    "S09": "S09",
    "stageS-web-scraping": "stageS-web-scraping",
    # 根目录文档
    "L01-L10": "L01-L10",
    "stageS": "stageS",
}

def update_file(filepath: Path) -> bool:
    """更新单个文件，返回是否修改"""
    try:
        content = filepath.read_text(encoding="utf-8")
        original = content

        for old, new in REPLACEMENTS.items():
            # 避免部分替换导致问题
            if old in content:
                content = content.replace(old, new)

        if content != original:
            filepath.write_text(content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    base = Path("/Users/nexo/python-fullstack")

    # 需要更新的目录
    dirs_to_scan = [
        base / "stage0-python-basics/lessons",
        base / "stageS-web-scraping",
        base,
        base / "docs/knowledge",
        base / "projects",
    ]

    updated_files = []
    for directory in dirs_to_scan:
        if not directory.exists():
            continue
        for pattern in ["*.md", "*.py"]:
            for filepath in directory.rglob(pattern):
                # 跳过 .venv 和 __pycache__
                if ".venv" in filepath.parts or "__pycache__" in filepath.parts:
                    continue
                if update_file(filepath):
                    updated_files.append(filepath)

    print("=== 更新完成 ===")
    print(f"共更新 {len(updated_files)} 个文件:")
    for f in sorted(updated_files):
        print(f"  - {f.relative_to(base)}")

if __name__ == "__main__":
    main()
