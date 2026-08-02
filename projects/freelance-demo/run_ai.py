"""Freelance Demo · AI 问答阶段封装。

from __future__ import annotations

启动项目 2 的 FastAPI 服务，并在启动时把项目 1 的爬取数据
自动导入向量库，让客户能立刻向"刚抓到的网站内容"提问。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

import uvicorn
from app.main import app
from app.routes.documents import get_rag_service

DEFAULT_WORKSPACE = "default"


def preload_documents(json_path: Path) -> int:
    """把项目 1 的爬虫输出导入项目 2 默认 workspace 的 RAG 服务。"""
    try:
        rag_service = get_rag_service(DEFAULT_WORKSPACE)
    except Exception as e:
        print(f"❌ RAG 服务初始化失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        content_bytes = json_path.read_text(encoding="utf-8")
        data = json.loads(content_bytes)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {json_path}", file=sys.stderr)
        print(f"   {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"❌ 文件读取失败: {json_path}", file=sys.stderr)
        print(f"   {e}", file=sys.stderr)
        sys.exit(1)

    pages = data if isinstance(data, list) else data.get("pages", [])

    count = 0
    for page in pages:
        title = page.get("title") or page.get("url") or "untitled"
        content = page.get("text") or page.get("content") or ""
        source = page.get("url") or "scraped"
        if content.strip():
            try:
                asyncio.run(rag_service.ingest(title, content, source))
                count += 1
            except Exception as e:
                print(f"⚠️  文档导入失败（跳过）: {title[:50]} - {e}", file=sys.stderr)
                continue
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Freelance Demo · AI 问答启动")
    parser.add_argument("--documents", help="项目 1 输出的 JSON（启动时自动导入）")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.documents:
        path = Path(args.documents).resolve()
        if not path.exists():
            print(f"❌ 文档文件不存在: {path}", file=sys.stderr)
            print("   提示: 请先运行爬虫阶段生成 scraped.json", file=sys.stderr)
            sys.exit(1)

        if not path.is_file():
            print(f"❌ 路径不是文件: {path}", file=sys.stderr)
            sys.exit(1)

        n = preload_documents(path)
        print(f"📚 已导入 {n} 份文档到 RAG 向量库")

    print("")
    print(f"🌐 访问 http://{args.host}:{args.port}")
    print(f"📘 API 文档 http://{args.host}:{args.port}/docs")
    print("按 Ctrl+C 停止")
    print("")

    try:
        uvicorn.run(app, host=args.host, port=args.port, log_level="info")
    except KeyboardInterrupt:
        print("\n✅ AI 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务启动失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
