#!/usr/bin/env python3
"""课程元数据验证脚本

用途：验证所有课程的元数据完整性和一致性
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys

# 添加 scripts 目录到路径以导入共享模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common.colors import print_error, print_info
from common.course_scanner import iter_all_lessons


@dataclass
class CourseMetadata:
    """课程元数据"""

    lesson_number: str | None = None
    stage: str | None = None
    duration: str | None = None
    difficulty: str | None = None
    has_standard_format: bool = False
    has_compact_format: bool = False


@dataclass
class ValidationIssue:
    """验证问题"""

    severity: str  # ERROR, WARNING, INFO
    lesson_dir: str
    issue_type: str
    message: str


class CourseMetadataValidator:
    """课程元数据验证器"""

    # 常量定义
    STANDARD_FORMAT_PATTERN = r"> \*\*课程编号\*\*:\s*L\d+"
    COMPACT_FORMAT_PATTERN = r"> \*\*编号\*\*:\s*L\d+\s*\|"
    LESSON_NUMBER_PATTERN = r"(L\d+)"
    METADATA_FIELDS = {
        "lesson_number": r"> \*\*课程编号\*\*:\s*(L\d+)",
        "stage": r"> \*\*所属阶段\*\*:\s*(.+)",
        "duration": r"> \*\*预计时长\*\*:\s*(.+)",
        "difficulty": r"> \*\*难度\*\*:\s*(.+)",
        "compact_lesson_number": r"> \*\*编号\*\*:\s*(L\d+)",
    }

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.issues: list[ValidationIssue] = []

    def extract_lesson_number_from_dirname(self, dirname: str) -> str | None:
        """从目录名提取课程编号（如 L19）"""
        try:
            match = re.match(self.LESSON_NUMBER_PATTERN, dirname)
            return match.group(1) if match else None
        except Exception as e:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=dirname,
                    issue_type="EXTRACTION_ERROR",
                    message=f"提取课程编号时发生错误: {e!s}",
                )
            )
            return None

    def extract_metadata_from_readme(self, readme_path: Path) -> CourseMetadata:
        """从 README 提取元数据"""
        metadata = CourseMetadata()

        try:
            if not readme_path.exists():
                return metadata

            # 使用上下文管理器安全读取文件
            with open(readme_path, encoding="utf-8") as file:
                content = file.read()

            # 检查标准格式
            if re.search(self.STANDARD_FORMAT_PATTERN, content):
                metadata.has_standard_format = True

                # 提取元数据字段
                for field, pattern in self.METADATA_FIELDS.items():
                    if field != "compact_lesson_number":
                        match = re.search(pattern, content)
                        if match:
                            setattr(metadata, field, match.group(1).strip())

            # 检查紧凑格式
            elif re.search(self.COMPACT_FORMAT_PATTERN, content):
                metadata.has_compact_format = True

                # 提取课程编号
                match = re.search(self.METADATA_FIELDS["compact_lesson_number"], content)
                if match:
                    metadata.lesson_number = match.group(1)

        except OSError as e:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=readme_path.parent.name,
                    issue_type="FILE_READ_ERROR",
                    message=f"读取 README 文件时发生错误: {e!s}",
                )
            )
        except Exception as e:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=readme_path.parent.name,
                    issue_type="UNEXPECTED_ERROR",
                    message=f"处理 README 文件时发生意外错误: {e!s}",
                )
            )

        return metadata

    def validate_lesson(self, lesson_dir: Path) -> None:
        """验证单个课程"""
        dirname = lesson_dir.name
        readme_path = lesson_dir / "README.md"

        # 提取目录编号
        dir_number = self.extract_lesson_number_from_dirname(dirname)
        if not dir_number:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=dirname,
                    issue_type="INVALID_DIRNAME",
                    message="目录名不符合规范（应为 LXX-name 格式）",
                )
            )
            return

        # 检查 README 是否存在
        try:
            if not readme_path.exists():
                self.issues.append(
                    ValidationIssue(
                        severity="ERROR",
                        lesson_dir=dirname,
                        issue_type="MISSING_README",
                        message="缺少 README.md 文件",
                    )
                )
                return
        except Exception as e:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=dirname,
                    issue_type="FILE_CHECK_ERROR",
                    message=f"检查 README 文件时发生错误: {e!s}",
                )
            )
            return

        # 提取元数据
        metadata = self.extract_metadata_from_readme(readme_path)

        # 检查是否有元数据
        if not metadata.has_standard_format and not metadata.has_compact_format:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=dirname,
                    issue_type="MISSING_METADATA",
                    message="缺少元数据块（无标准格式或紧凑格式）",
                )
            )
            return

        # 检查格式一致性
        if metadata.has_compact_format and not metadata.has_standard_format:
            self.issues.append(
                ValidationIssue(
                    severity="WARNING",
                    lesson_dir=dirname,
                    issue_type="FORMAT_INCONSISTENCY",
                    message="使用紧凑格式，建议统一为标准格式",
                )
            )

        # 检查编号一致性
        if metadata.lesson_number and metadata.lesson_number != dir_number:
            self.issues.append(
                ValidationIssue(
                    severity="ERROR",
                    lesson_dir=dirname,
                    issue_type="NUMBER_MISMATCH",
                    message=f"元数据编号 {metadata.lesson_number} 与目录编号 {dir_number} 不一致",
                )
            )

        # 检查元数据完整性
        if metadata.has_standard_format:
            if not metadata.stage:
                self.issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        lesson_dir=dirname,
                        issue_type="INCOMPLETE_METADATA",
                        message="缺少所属阶段信息",
                    )
                )
            if not metadata.duration:
                self.issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        lesson_dir=dirname,
                        issue_type="INCOMPLETE_METADATA",
                        message="缺少预计时长信息",
                    )
                )
            if not metadata.difficulty:
                self.issues.append(
                    ValidationIssue(
                        severity="WARNING",
                        lesson_dir=dirname,
                        issue_type="INCOMPLETE_METADATA",
                        message="缺少难度信息",
                    )
                )

    def validate_all_lessons(self) -> None:
        """验证所有课程（使用共享扫描器）"""
        for stage_dir, lesson_dir in iter_all_lessons(self.repo_root):
            self.validate_lesson(lesson_dir)

    def generate_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("=" * 70)
        report.append("课程元数据验证报告")
        report.append("=" * 70)
        report.append("")

        # 统计
        errors = [i for i in self.issues if i.severity == "ERROR"]
        warnings = [i for i in self.issues if i.severity == "WARNING"]
        infos = [i for i in self.issues if i.severity == "INFO"]

        report.append("📊 统计:")
        report.append(f"  总问题数: {len(self.issues)}")
        report.append(f"  🔴 错误 (ERROR): {len(errors)}")
        report.append(f"  🟡 警告 (WARNING): {len(warnings)}")
        report.append(f"  🔵 信息 (INFO): {len(infos)}")
        report.append("")

        # 按严重程度分组显示
        if errors:
            report.append("🔴 错误 (ERROR)")
            report.append("-" * 70)
            for issue in errors:
                report.append(f"  [{issue.lesson_dir}] {issue.issue_type}: {issue.message}")
            report.append("")

        if warnings:
            report.append("🟡 警告 (WARNING)")
            report.append("-" * 70)
            for issue in warnings:
                report.append(f"  [{issue.lesson_dir}] {issue.issue_type}: {issue.message}")
            report.append("")

        if infos:
            report.append("🔵 信息 (INFO)")
            report.append("-" * 70)
            for issue in infos:
                report.append(f"  [{issue.lesson_dir}] {issue.issue_type}: {issue.message}")
            report.append("")

        # 结论
        report.append("=" * 70)
        if not self.issues:
            report.append("✅ 验证通过！所有课程元数据格式正确。")
        elif errors:
            report.append(f"❌ 验证失败！发现 {len(errors)} 个错误需要修复。")
        else:
            report.append(f"⚠️ 验证通过，但有 {len(warnings)} 个警告建议处理。")
        report.append("=" * 70)

        return "\n".join(report)

    def get_exit_code(self) -> int:
        """获取退出码"""
        errors = [i for i in self.issues if i.severity == "ERROR"]
        return 1 if errors else 0


def main() -> None:
    """主函数"""
    try:
        # 获取仓库根目录
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent if script_dir.name == "scripts" else script_dir

        print_info(f"仓库根目录: {repo_root}")
        print_info("开始验证课程元数据...")
        print("")

        # 创建验证器并执行验证
        validator = CourseMetadataValidator(repo_root)
        validator.validate_all_lessons()

        # 生成并打印报告
        report = validator.generate_report()
        print(report)

        # 返回退出码
        sys.exit(validator.get_exit_code())
    except Exception as e:
        print_error(f"发生严重错误: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
