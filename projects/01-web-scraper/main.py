"""

from __future__ import annotations

Web Scraper 主入口
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from scraper.collector import Collector
from scraper.pipeline import Pipeline

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Web Scraper - 生产级合规网络爬虫")
    parser.add_argument("--url", required=True, help="起始URL")
    parser.add_argument("--max-pages", type=int, default=10, help="最大采集页面数")
    parser.add_argument("--delay", type=float, default=1.0, help="请求间隔(秒)")
    parser.add_argument("--timeout", type=int, default=10, help="请求超时(秒)")
    parser.add_argument("--output", required=True, help="输出文件路径(.json或.csv)")
    parser.add_argument("--no-robots", action="store_true", help="忽略 robots.txt")
    args = parser.parse_args()

    logger.info("开始采集: %s", args.url)
    logger.info("最大页面数: %s, 请求间隔: %ss", args.max_pages, args.delay)

    try:
        collector = Collector(
            delay=args.delay, timeout=args.timeout, respect_robots=not args.no_robots
        )
        results = collector.crawl(args.url, max_pages=args.max_pages)
    except Exception:
        logger.error("网络采集失败: %s", args.url, exc_info=True)
        print("❌ 采集失败，请检查网络连接或目标站点可访问性", file=sys.stderr)
        sys.exit(1)

    if not results:
        logger.warning("未采集到任何页面: %s", args.url)
        print("❌ 未采集到任何页面")
        return

    logger.info("采集完成: %d 个页面", len(results))

    try:
        pipeline = Pipeline()
        pipeline.save_batch(results)
    except Exception:
        logger.error("数据存储失败", exc_info=True)
        print("❌ 数据存储失败", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    try:
        if output_path.suffix.lower() == ".json":
            pipeline.export_json(output_path)
            # 导出 schema
            schema_path = output_path.with_name(f"{output_path.stem}_schema.json")
            schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "页面URL"},
                        "title": {"type": "string", "description": "页面标题"},
                        "text": {"type": "string", "description": "正文文本"},
                        "status_code": {"type": "integer", "description": "HTTP状态码"},
                        "fetch_time": {"type": "number", "description": "采集耗时(秒)"},
                        "word_count": {"type": "integer", "description": "正文词数"},
                        "extracted_date": {
                            "type": ["string", "null"],
                            "description": "提取的日期(YYYY-MM-DD)",
                        },
                    },
                    "required": ["url", "title", "text", "status_code", "fetch_time", "word_count"],
                },
            }
            schema_path.write_text(
                json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            logger.info("导出JSON Schema: %s", schema_path)

        elif output_path.suffix.lower() == ".csv":
            pipeline.export_csv(output_path)
        else:
            logger.error("不支持的输出格式: %s", output_path.suffix)
            print(f"❌ 不支持的输出格式: {output_path.suffix}", file=sys.stderr)
            sys.exit(1)
    except Exception:
        logger.error("文件导出失败: %s", output_path, exc_info=True)
        print(f"❌ 导出失败: {output_path}", file=sys.stderr)
        sys.exit(1)

    logger.info("导出完成: %s", output_path)

    try:
        stats = pipeline.analyze().iloc[0]
        print("\n📊 统计信息:")
        print(f"  总页面数: {stats['total_pages']}")
        print(f"  平均词数: {stats['avg_word_count']:.0f}")
        print(f"  平均采集耗时: {stats['avg_fetch_time']:.3f}s")
        print(f"  包含日期数: {stats['unique_dates']}")
    except Exception:
        logger.error("统计信息生成失败", exc_info=True)
        print("⚠️  统计信息生成失败，但数据已成功导出")


if __name__ == "__main__":
    main()
