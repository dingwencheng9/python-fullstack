"""Exercise 1: Celery Task"""

from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379")


@app.task
def process_data(data: dict) -> dict:
    """Process data task"""
    result = data.get("value", 0) * 2
    return {"status": "success", "result": result}


def test():
    # Just verify task is defined
    assert process_data.name == "process_data"
    print("PASS: Celery task defined")


if __name__ == "__main__":
    test()
