"""示例 1: Celery 基础"""

from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")


@app.task(bind=True, max_retries=3)
def process_data(self, data_id: int):
    """处理数据任务"""
    try:
        # 模拟处理
        result = data_id * 2
        return {"status": "success", "result": result}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task
def send_notification(user_id: int, message: str):
    """发送通知任务"""
    print(f"通知用户 {user_id}: {message}")
    return {"sent": True}


@app.task
def cleanup_old_data():
    """清理旧数据任务"""
    print("清理过期数据...")
    return {"cleaned": 100}


# 使用示例
if __name__ == "__main__":
    # 异步调用
    result = process_data.delay(42)
    print(f"任务 ID: {result.id}")

    # 等待结果
    print(f"结果: {result.get(timeout=10)}")
