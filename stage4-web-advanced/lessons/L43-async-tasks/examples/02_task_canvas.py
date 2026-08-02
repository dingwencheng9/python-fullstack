"""Example 2: Celery Task Canvas (Chain, Group, Chord)"""

from celery import Celery, group, chord, chain as celery_chain

app = Celery("tasks", broker="redis://localhost:6379/0")


# Define tasks
@app.task
def fetch_data(source: str):
    """Fetch data from source."""
    return {"source": source, "data": [1, 2, 3]}


@app.task
def process_data(data: dict):
    """Process fetched data."""
    return {"processed": [x * 2 for x in data["data"]]}


@app.task
def save_result(result: dict):
    """Save result to storage."""
    return {"saved": True, "result": result}


@app.task
def send_alert(message: str):
    """Send notification."""
    return {"alert_sent": True, "message": message}


# Task chains
def pipeline_chain():
    """Sequential pipeline: fetch -> process -> save."""
    return celery_chain(fetch_data.s("api://source"), process_data.s(), save_result.s())


def parallel_with_callback():
    """Parallel processing with callback when all complete."""
    return chord(
        group(fetch_data.s("source1"), fetch_data.s("source2"), fetch_data.s("source3")),
        send_alert.s("All sources processed"),
    )


def complex_workflow():
    """Complex workflow with multiple branches."""
    return celery_chain(
        # Step 1: Fetch initial data
        fetch_data.s("primary"),
        # Step 2: Process and branch to parallel tasks
        chord(
            group(
                process_data.s(),
                save_result.s(),
            ),
            send_alert.s("Processing complete"),
        ),
    )


if __name__ == "__main__":
    # Execute chains
    result = pipeline_chain().apply_async()
    print(f"Chain result: {result.get(timeout=30)}")

    # Execute parallel with callback
    result = parallel_with_callback().apply_async()
    print(f"Chord result: {result.get(timeout=30)}")
