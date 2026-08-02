"""Solution: Celery Task with Retry and Chain"""

from celery import Celery, chain, group

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_with_retry(self, data: dict) -> dict:
    """Task with automatic retry on failure."""
    try:
        # Simulate processing
        result = data.get("value", 0) * 2
        return {"status": "success", "result": result}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2**self.request.retries)


@app.task
def send_notification(user_id: str, message: str) -> dict:
    """Send notification task."""
    # Simulate sending
    print(f"Sending notification to {user_id}: {message}")
    return {"sent": True, "user_id": user_id}


@app.task
def log_result(data: dict) -> dict:
    """Log processing result."""
    print(f"Logging result: {data}")
    return {"logged": True}


def create_processing_chain(data: dict) -> chain:
    """Create a task chain: process -> notify -> log."""
    return chain(
        process_with_retry.s(data),
        send_notification.s("admin@example.com", "Processing complete"),
        log_result.s(),
    )


def create_batch_processing(items: list) -> group:
    """Create parallel processing for multiple items."""
    return group(process_with_retry.s(item) for item in items)


if __name__ == "__main__":
    # Example: Submit single chain
    result = create_processing_chain({"value": 10}).apply_async()
    print(f"Chain task ID: {result.id}")

    # Example: Submit batch
    batch_result = create_batch_processing([{"value": 1}, {"value": 2}, {"value": 3}]).apply_async()
    print(f"Batch task IDs: {batch_result.id}")
