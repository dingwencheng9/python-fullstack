"""Tests for Celery Tasks module."""

import pytest

pytest.importorskip("celery", reason="celery 未安装；可选依赖")
from solutions.solution_01_celery import (  # noqa: E402
    process_with_retry,
    send_notification,
    create_processing_chain,
    create_batch_processing,
)


class TestCeleryTasks:
    """Test Celery task definitions."""

    def test_task_creation(self):
        """Test that tasks are properly defined."""
        assert process_with_retry.name == "process_with_retry"
        assert process_with_retry.max_retries == 3

    def test_notification_task(self):
        """Test notification task."""
        assert send_notification.name == "send_notification"

    def test_chain_creation(self):
        """Test creating a task chain."""
        chain = create_processing_chain({"value": 10})
        # Chain is a celery chain object
        assert chain is not None

    def test_batch_creation(self):
        """Test creating batch processing."""
        items = [{"value": 1}, {"value": 2}, {"value": 3}]
        batch = create_batch_processing(items)
        # Group should contain multiple tasks
        assert batch is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
