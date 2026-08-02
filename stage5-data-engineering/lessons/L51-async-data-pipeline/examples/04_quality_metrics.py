"""L52 示例：数据质量、schema drift 与指标。"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def load_solution_module():
    base = Path(__file__).resolve().parents[1]
    path = base / "solutions" / "04_production_pipeline.py"
    spec = importlib.util.spec_from_file_location("l52_production_pipeline", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


async def main() -> None:
    module = load_solution_module()
    records = [
        {"id": 1, "value": 10},
        {"id": 2, "value": "oops"},
        {"id": 3},
    ]

    with TemporaryDirectory() as tmpdir:
        pipeline = module.ProductionPipeline.default(
            checkpoint_path=Path(tmpdir) / "checkpoint.json",
            sink_path=Path(tmpdir) / "sink.jsonl",
        )
        metrics = await pipeline.run(records)
        print("metrics:", metrics.snapshot())
        print("dlq:", [(record.key, record.error_type) for record in pipeline.dlq.records])


if __name__ == "__main__":
    asyncio.run(main())
