"""L17 示例 6: 矩阵测试报告模拟。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MatrixTestResult:
    python_version: str
    passed: int
    failed: int


def run_mock_matrix() -> list[MatrixTestResult]:
    """模拟矩阵测试运行结果。"""
    return [
        MatrixTestResult("3.12", passed=42, failed=0),
        MatrixTestResult("3.13", passed=42, failed=0),
    ]


if __name__ == "__main__":
    for r in run_mock_matrix():
        status = "✅" if r.failed == 0 else "❌"
        print(f"{status} Python {r.python_version}: {r.passed} passed, {r.failed} failed")
