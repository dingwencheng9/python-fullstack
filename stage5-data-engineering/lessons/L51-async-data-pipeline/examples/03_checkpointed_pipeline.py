"""L52 示例：checkpoint + 幂等写入。"""

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
    records = [{"id": i, "value": i * 10} for i in range(1, 6)]

    with TemporaryDirectory() as tmpdir:
        checkpoint = Path(tmpdir) / "checkpoint.json"
        sink = Path(tmpdir) / "sink.jsonl"

        first_run = module.ProductionPipeline.default(checkpoint, sink)
        await first_run.run(records[:3])

        second_run = module.ProductionPipeline.default(checkpoint, sink)
        await second_run.run(records)

        print("rows:", [row["key"] for row in second_run.sink.rows])
        print("checkpoint:", module.JsonCheckpointStore(checkpoint).load())


if __name__ == "__main__":
    asyncio.run(main())
