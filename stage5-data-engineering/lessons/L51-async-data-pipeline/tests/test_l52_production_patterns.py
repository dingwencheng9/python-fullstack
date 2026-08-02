"""L52 生产级数据管道模式测试。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def load_pipeline_module() -> ModuleType:
    lesson_dir = Path(__file__).resolve().parents[1]
    path = lesson_dir / "solutions" / "04_production_pipeline.py"
    spec = importlib.util.spec_from_file_location("l52_production_pipeline", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def pipeline_module() -> ModuleType:
    return load_pipeline_module()


@pytest.mark.asyncio
async def test_checkpoint_resume_and_idempotent_sink(tmp_path: Path, pipeline_module: ModuleType):
    records = [{"id": i, "value": i * 10} for i in range(5)]
    checkpoint_path = tmp_path / "checkpoint.json"
    sink_path = tmp_path / "sink.jsonl"

    first_run = pipeline_module.ProductionPipeline.default(checkpoint_path, sink_path)
    await first_run.run(records[:3])

    assert pipeline_module.JsonCheckpointStore(checkpoint_path).load() == 2
    assert [row["key"] for row in first_run.sink.rows] == ["0", "1", "2"]

    second_run = pipeline_module.ProductionPipeline.default(checkpoint_path, sink_path)
    await second_run.run(records)

    assert pipeline_module.JsonCheckpointStore(checkpoint_path).load() == 4
    assert [row["key"] for row in second_run.sink.rows] == ["0", "1", "2", "3", "4"]

    third_run = pipeline_module.ProductionPipeline.default(checkpoint_path, sink_path)
    await third_run.run(records)
    assert [row["key"] for row in third_run.sink.rows] == ["0", "1", "2", "3", "4"]


@pytest.mark.asyncio
async def test_schema_drift_goes_to_dead_letter_queue(tmp_path: Path, pipeline_module: ModuleType):
    records = [
        {"id": 1, "value": 10},
        {"id": 2, "value": "bad"},
        {"id": 3},
    ]
    pipeline = pipeline_module.ProductionPipeline.default(
        checkpoint_path=tmp_path / "checkpoint.json",
        sink_path=tmp_path / "sink.jsonl",
    )

    metrics = await pipeline.run(records)

    assert metrics.processed == 1
    assert metrics.failed == 2
    assert metrics.success_rate == pytest.approx(1 / 3)
    assert [record.error_type for record in pipeline.dlq.records] == ["TypeError", "ValueError"]
    assert [row["key"] for row in pipeline.sink.rows] == ["1"]


@pytest.mark.asyncio
async def test_duplicate_key_is_skipped_without_failure(tmp_path: Path, pipeline_module: ModuleType):
    checkpoint_path = tmp_path / "checkpoint.json"
    sink_path = tmp_path / "sink.jsonl"
    pipeline = pipeline_module.ProductionPipeline.default(checkpoint_path, sink_path)

    await pipeline.process_one(pipeline_module.PipelineItem(0, "same", {"id": 1, "value": 10}))
    await pipeline.process_one(pipeline_module.PipelineItem(1, "same", {"id": 1, "value": 99}))

    assert pipeline.metrics.processed == 1
    assert pipeline.metrics.duplicate_skipped == 1
    assert pipeline.metrics.failed == 0
    assert len(pipeline.sink.rows) == 1
    assert pipeline.sink.rows[0]["value_doubled"] == 20


def test_metrics_snapshot_contains_operational_fields(pipeline_module: ModuleType):
    metrics = pipeline_module.PipelineMetrics(processed=9, failed=1, retried=2, duplicate_skipped=3)
    snapshot = metrics.snapshot()

    assert snapshot["processed"] == 9
    assert snapshot["failed"] == 1
    assert snapshot["retried"] == 2
    assert snapshot["duplicate_skipped"] == 3
    assert snapshot["success_rate"] == 0.9
    assert snapshot["throughput"] >= 0
