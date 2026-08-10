"""L51 生产级异步数据管道模式参考答案。

本文件刻意只使用 Python 标准库，方便在教学环境中稳定运行。它演示：
- schema 校验与 schema drift 捕获
- checkpoint / offset 断点续跑
- 幂等 sink，避免重复写入
- dead letter queue，记录不可恢复数据
- 基础 metrics，度量成功率与吞吐量
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import AsyncIterator, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Self

Record = dict[str, Any]


@dataclass(slots=True)
class PipelineItem:
    """管道中传递的标准数据项。"""

    offset: int
    key: str
    payload: Record


@dataclass(slots=True)
class DeadLetterRecord:
    """无法处理的数据记录。"""

    offset: int
    key: str
    error_type: str
    message: str
    payload: Record
    timestamp: float = field(default_factory=time.time)


@dataclass(slots=True)
class PipelineMetrics:
    """生产级管道最小指标集合。"""

    processed: int = 0
    failed: int = 0
    retried: int = 0
    duplicate_skipped: int = 0
    started_at: float = field(default_factory=time.perf_counter)

    @property
    def total(self) -> int:
        return self.processed + self.failed + self.duplicate_skipped

    @property
    def success_rate(self) -> float:
        attempts = self.processed + self.failed
        return self.processed / attempts if attempts else 1.0

    @property
    def throughput(self) -> float:
        elapsed = max(time.perf_counter() - self.started_at, 1e-9)
        return self.processed / elapsed

    def snapshot(self) -> dict[str, float | int]:
        """返回适合日志/监控系统采集的指标快照。"""
        return {
            "processed": self.processed,
            "failed": self.failed,
            "retried": self.retried,
            "duplicate_skipped": self.duplicate_skipped,
            "success_rate": round(self.success_rate, 4),
            "throughput": round(self.throughput, 4),
        }


class SchemaValidator:
    """轻量 schema 校验器。

    `required_fields` 描述字段名与期望类型。生产系统可替换为 Pydantic、Pandera
    或 Great Expectations；课程示例使用标准库以突出模式本身。
    """

    def __init__(self, required_fields: dict[str, type]) -> None:
        self.required_fields = required_fields

    def validate(self, payload: Record) -> None:
        for field_name, expected_type in self.required_fields.items():
            if field_name not in payload:
                raise ValueError(f"missing field: {field_name}")
            if not isinstance(payload[field_name], expected_type):
                actual = type(payload[field_name]).__name__
                expected = expected_type.__name__
                raise TypeError(f"field {field_name} expected {expected}, got {actual}")


class JsonCheckpointStore:
    """JSON checkpoint 存储，记录最后成功提交的 offset。"""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> int:
        if not self.path.exists():
            return -1
        data = json.loads(self.path.read_text())
        return int(data.get("last_committed_offset", -1))

    def save(self, offset: int) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"last_committed_offset": offset}, ensure_ascii=False))


class IdempotentJsonSink:
    """幂等 JSON sink。

    相同 key 只写一次，重复数据会被跳过。这里用内存索引 + JSONL 文件模拟数据库
    的唯一键约束；真实项目可映射到 UPSERT / MERGE / ON CONFLICT DO NOTHING。
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._seen_keys: set[str] = set()
        self._rows: list[Record] = []
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                self._rows.append(row)
                self._seen_keys.add(str(row["key"]))

    @property
    def rows(self) -> list[Record]:
        return self._rows.copy()

    async def write(self, item: PipelineItem) -> bool:
        """写入一条记录，返回是否实际写入。"""
        await asyncio.sleep(0)
        if item.key in self._seen_keys:
            return False
        row = {"offset": item.offset, "key": item.key, **item.payload}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._seen_keys.add(item.key)
        self._rows.append(row)
        return True


class DeadLetterQueue:
    """内存 dead letter queue。"""

    def __init__(self) -> None:
        self.records: list[DeadLetterRecord] = []

    def add(self, item: PipelineItem, error: Exception) -> None:
        self.records.append(
            DeadLetterRecord(
                offset=item.offset,
                key=item.key,
                error_type=type(error).__name__,
                message=str(error),
                payload=item.payload,
            )
        )

    def by_error_type(self, error_type: str) -> list[DeadLetterRecord]:
        return [record for record in self.records if record.error_type == error_type]


async def async_source(records: Iterable[Record], start_offset: int = 0) -> AsyncIterator[PipelineItem]:
    """把普通 iterable 包装成异步数据源。"""
    for offset, payload in enumerate(records):
        if offset < start_offset:
            continue
        await asyncio.sleep(0)
        yield PipelineItem(offset=offset, key=str(payload.get("id", offset)), payload=dict(payload))


class ProductionPipeline:
    """可恢复、可观测、幂等的异步数据管道。"""

    def __init__(
        self,
        checkpoint: JsonCheckpointStore,
        sink: IdempotentJsonSink,
        validator: SchemaValidator,
        dlq: DeadLetterQueue | None = None,
        metrics: PipelineMetrics | None = None,
    ) -> None:
        self.checkpoint = checkpoint
        self.sink = sink
        self.validator = validator
        self.dlq = dlq or DeadLetterQueue()
        self.metrics = metrics or PipelineMetrics()

    @classmethod
    def default(cls, checkpoint_path: str | Path, sink_path: str | Path) -> Self:
        return cls(
            checkpoint=JsonCheckpointStore(checkpoint_path),
            sink=IdempotentJsonSink(sink_path),
            validator=SchemaValidator({"id": int, "value": int}),
        )

    async def transform(self, item: PipelineItem) -> PipelineItem:
        self.validator.validate(item.payload)
        transformed = dict(item.payload)
        transformed["value_doubled"] = transformed["value"] * 2
        transformed["quality_status"] = "ok"
        return PipelineItem(offset=item.offset, key=item.key, payload=transformed)

    async def process_one(self, item: PipelineItem) -> None:
        try:
            transformed = await self.transform(item)
            inserted = await self.sink.write(transformed)
            if inserted:
                self.metrics.processed += 1
            else:
                self.metrics.duplicate_skipped += 1
            self.checkpoint.save(item.offset)
        except Exception as exc:
            self.metrics.failed += 1
            self.dlq.add(item, exc)

    async def run(self, records: Iterable[Record]) -> PipelineMetrics:
        start_offset = self.checkpoint.load() + 1
        async for item in async_source(records, start_offset=start_offset):
            await self.process_one(item)
        return self.metrics


async def demo() -> None:
    """运行一个可重复的端到端 demo。"""
    records = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": "schema-drift"},
        {"id": 4, "value": 40},
    ]
    with TemporaryDirectory() as tmpdir:
        pipeline = ProductionPipeline.default(
            checkpoint_path=Path(tmpdir) / "checkpoint.json",
            sink_path=Path(tmpdir) / "sink.jsonl",
        )
        metrics = await pipeline.run(records)
        print(metrics.snapshot())
        print([row["key"] for row in pipeline.sink.rows])
        print([record.error_type for record in pipeline.dlq.records])


if __name__ == "__main__":
    asyncio.run(demo())
