"""
Python Free-threading 极限压测 - 算力释放实战
=============================================

本模块通过 CPU 密集型任务（Mandelbrot 分形渲染）对比单线程与多线程性能，
用真实的加速比数据粉碎"Python 多线程无用论"。

环境要求：
- 课程基线：Python 3.13t（PEP 703 试验性 free-threading 构建）
- 试验补充：Python 3.14t（PEP 779 官方支持的 free-threading 构建）

启动方式（标准）：
    python3.13t 01_free_threading_benchmark.py
    PYTHON_GIL=0 python3.13t 01_free_threading_benchmark.py    # 强制关闭 GIL
    python3.13t -X gil=0 01_free_threading_benchmark.py        # 等价写法

对照实验（保留 GIL）：
    PYTHON_GIL=1 python3.13t 01_free_threading_benchmark.py    # 在 t 构建上强开 GIL
    python3.13 01_free_threading_benchmark.py                  # 标准构建（永远有 GIL）

⚠️ 重要：`python3.13 --disable-gil` 这个命令不存在。`--disable-gil` 是
CPython configure 脚本的编译 flag，不是运行时参数。详见
docs/FREE_THREADING_TRUTH.md。

实验设计：
- 任务：Mandelbrot 集合计算（纯 CPU 密集型）
- 对比：1/2/4/8 线程性能
- 输出：加速比报告 + 效率分析

预期结果（无 GIL 模式）：
- 2 线程：1.9x 加速
- 4 线程：3.5-3.9x 加速
- 8 线程：6.5-7.5x 加速

作者：Python 3.13 全栈课程
"""

from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BenchmarkResult:
    """基准测试结果（不可变数据类）"""

    task_name: str
    gil_status: Literal["enabled", "disabled", "unknown"]
    num_threads: int
    duration: float
    speedup: float
    efficiency: float  # speedup / num_threads


def check_gil_status() -> Literal["enabled", "disabled", "unknown"]:
    """
    检测当前 Python 运行时的 GIL 状态

    Returns:
        "disabled": 无 GIL 模式（Python 3.13t / 3.14t free-threading 构建）
        "enabled": 传统 GIL 模式
        "unknown": 无法检测（Python < 3.13）
    """
    if hasattr(sys, "_is_gil_enabled"):
        return "disabled" if not sys._is_gil_enabled() else "enabled"
    return "unknown"


def mandelbrot_pixel(cx: float, cy: float, max_iter: int = 256) -> int:
    """
    计算单个像素的 Mandelbrot 集合迭代次数

    Args:
        cx: 复数实部
        cy: 复数虚部
        max_iter: 最大迭代次数

    Returns:
        迭代次数（未逃逸则返回 max_iter）
    """
    x, y = 0.0, 0.0

    for i in range(max_iter):
        x2, y2 = x * x, y * y
        if x2 + y2 > 4.0:
            return i
        x, y = x2 - y2 + cx, 2.0 * x * y + cy

    return max_iter


def mandelbrot_row(
    y: int,
    width: int,
    height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    max_iter: int,
) -> list[int]:
    """
    计算 Mandelbrot 集合的一行像素

    Args:
        y: 当前行号
        width: 图像宽度
        height: 图像高度
        x_min, x_max: X 轴范围
        y_min, y_max: Y 轴范围
        max_iter: 最大迭代次数

    Returns:
        该行所有像素的迭代次数列表
    """
    row: list[int] = []
    cy = y_min + (y / height) * (y_max - y_min)

    for x in range(width):
        cx = x_min + (x / width) * (x_max - x_min)
        row.append(mandelbrot_pixel(cx, cy, max_iter))

    return row


def mandelbrot_set_serial(
    width: int = 800,
    height: int = 600,
    max_iter: int = 256,
) -> list[list[int]]:
    """
    串行计算 Mandelbrot 集合（单线程基准）

    Args:
        width: 图像宽度
        height: 图像高度
        max_iter: 最大迭代次数

    Returns:
        二维迭代次数数组
    """
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.0, 1.0

    result: list[list[int]] = []
    for y in range(height):
        row = mandelbrot_row(y, width, height, x_min, x_max, y_min, y_max, max_iter)
        result.append(row)

    return result


def mandelbrot_set_parallel(
    width: int = 800,
    height: int = 600,
    max_iter: int = 256,
    num_threads: int = 4,
) -> list[list[int]]:
    """
    并行计算 Mandelbrot 集合（多线程）

    Args:
        width: 图像宽度
        height: 图像高度
        max_iter: 最大迭代次数
        num_threads: 线程数

    Returns:
        二维迭代次数数组
    """
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.0, 1.0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(mandelbrot_row, y, width, height, x_min, x_max, y_min, y_max, max_iter) for y in range(height)]

        result: list[list[int]] = [future.result() for future in futures]

    return result


def run_benchmark(
    width: int = 800,
    height: int = 600,
    max_iter: int = 256,
) -> list[BenchmarkResult]:
    """
    运行完整的基准测试套件

    Args:
        width: 图像宽度
        height: 图像高度
        max_iter: 最大迭代次数

    Returns:
        所有测试结果列表
    """
    gil_status = check_gil_status()
    results: list[BenchmarkResult] = []

    print(f"\n{'=' * 80}")
    print("Python Free-threading 极限压测（PEP 703 / PEP 779）")
    print(f"{'=' * 80}\n")
    print(f"GIL 状态: {gil_status.upper()}")
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"测试图像: {width}x{height} ({max_iter} 迭代)")
    print(f"\n{'=' * 80}\n")

    # 串行基准测试
    print("运行串行基准测试...")
    start = time.perf_counter()
    _ = mandelbrot_set_serial(width, height, max_iter)
    baseline_time = time.perf_counter() - start
    print(f"✓ 完成，耗时 {baseline_time:.3f}s\n")

    # 多线程测试
    thread_counts = [1, 2, 4, 8]

    for num_threads in thread_counts:
        print(f"运行 {num_threads} 线程测试...")
        start = time.perf_counter()

        if num_threads == 1:
            _ = mandelbrot_set_serial(width, height, max_iter)
        else:
            _ = mandelbrot_set_parallel(width, height, max_iter, num_threads)

        duration = time.perf_counter() - start
        speedup = baseline_time / duration
        efficiency = speedup / num_threads

        results.append(
            BenchmarkResult(
                task_name="Mandelbrot 分形",
                gil_status=gil_status,
                num_threads=num_threads,
                duration=duration,
                speedup=speedup,
                efficiency=efficiency,
            )
        )

        print(f"✓ 完成，耗时 {duration:.3f}s (加速比 {speedup:.2f}x)\n")

    return results


def print_report(results: list[BenchmarkResult]) -> None:
    """
    格式化输出基准测试报告

    Args:
        results: 测试结果列表
    """
    print(f"\n{'=' * 80}")
    print("性能报告")
    print(f"{'=' * 80}\n")

    # 表头
    print(f"{'线程数':<12} {'耗时(s)':<15} {'加速比':<15} {'效率':<15}")
    print("-" * 80)

    # 数据行
    for r in results:
        print(f"{r.num_threads:<12} {r.duration:<15.3f} {r.speedup:<15.2f}x {r.efficiency:<15.1%}")

    # 结论分析
    print(f"\n{'=' * 80}")
    print("结论")
    print(f"{'=' * 80}\n")

    gil_status = results[0].gil_status

    if gil_status == "disabled":
        best_speedup = max(r.speedup for r in results)
        best_threads = next(r.num_threads for r in results if r.speedup == best_speedup)

        print("✅ 无 GIL 模式检测成功")
        print(f"✅ 最佳加速比: {best_speedup:.2f}x ({best_threads} 线程)")
        print("✅ 多线程可以充分利用多核 CPU")
        print("\n推荐策略:")
        print("  - CPU 密集型任务使用多线程")
        print("  - 线程数 = CPU 核心数")
        print("  - 避免过度创建线程（开销增加）")

    elif gil_status == "enabled":
        print("⚠️  传统 GIL 模式检测")
        print("⚠️  多线程无法利用多核（加速比接近 1.0）")
        print("⚠️  CPU 密集型任务必须使用 multiprocessing")
        print("\n建议:")
        print("  - 切换到 free-threading 构建: python3.13t（试验性）或 python3.14t（PEP 779 官方支持）")
        print("  - 在 t 构建上强制关闭 GIL: PYTHON_GIL=0 python3.13t script.py")
        print("  - 完整说明: docs/FREE_THREADING_TRUTH.md")

    else:
        print("⚠️  无法检测 GIL 状态")
        print("⚠️  可能运行在 Python < 3.13 版本")
        print("\n建议:")
        print("  - 升级到 Python 3.13+")
        print("  - 安装 python3.13t（Free-Threading 版本）")

    print(f"\n{'=' * 80}\n")


def main() -> None:
    """主函数：运行基准测试并生成报告"""
    # 较小的测试（快速验证）
    # results = run_benchmark(width=400, height=300, max_iter=128)

    # 标准测试（完整基准）
    results = run_benchmark(width=800, height=600, max_iter=256)

    # 大规模测试（压力测试）
    # results = run_benchmark(width=1600, height=1200, max_iter=512)

    print_report(results)


if __name__ == "__main__":
    main()
