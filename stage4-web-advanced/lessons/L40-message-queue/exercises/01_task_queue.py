"""练习 1: 实现任务队列。

from __future__ import annotations

实现 Queue 类：
- enqueue(task) -> task_id
- dequeue() -> Task | None
- get_result(task_id) -> Task | None
"""

from typing import Any

# ========================================
# 📝 练习：实现内存任务队列
#
# 🎯 目标：理解任务队列的基本原理和实现
#
# 📌 要求：
# 1. 实现 Task 类存储任务信息
# 2. 实现 TaskQueue 类管理任务队列
# 3. 支持任务入队（enqueue）
# 4. 支持任务出队（dequeue）
# 5. 支持通过 ID 查询任务结果
# 6. 记录任务状态（pending, processing, completed）
#
# 💡 实现提示：
# - 使用 deque 实现 FIFO 队列
# - 使用 uuid4() 生成唯一任务 ID
# - 使用字典存储任务 ID 到任务的映射
# - 任务状态：pending → processing → completed
#
# ✅ 验收标准：
# - 任务按 FIFO 顺序处理
# - 任务 ID 唯一
# - 状态转换正确
# - 可以查询任务结果
# ========================================


class Task:
    """任务对象

    Attributes:
        task_id: 任务唯一标识
        data: 任务数据
        status: 任务状态（pending, processing, completed）
        result: 任务结果

    Examples:
        >>> task = Task("test_data")
        >>> task.status
        'pending'
        >>> task.data
        'test_data'
    """

    def __init__(self, data: Any) -> None:
        """初始化任务

        Args:
            data: 任务数据
        """
        # 👉 TODO: 初始化任务属性
        # self.task_id: str = str(uuid4())
        # self.data: Any = data
        # self.status: str = "pending"
        # self.result: Any = None
        raise NotImplementedError

    def __repr__(self) -> str:
        """字符串表示"""
        return f"Task(id={self.task_id[:8]}, status={self.status})"


class TaskQueue:
    """任务队列

    管理任务的入队、出队和状态查询。

    Examples:
        >>> queue = TaskQueue()
        >>> task_id = queue.enqueue("task1")
        >>> task = queue.dequeue()
        >>> task.data
        'task1'
    """

    def __init__(self) -> None:
        """初始化任务队列"""
        # 👉 TODO: 初始化队列和任务字典
        # self._queue: deque[str] = deque()  # 存储任务 ID
        # self._tasks: dict[str, Task] = {}  # 任务 ID -> Task 映射
        raise NotImplementedError

    def enqueue(self, data: Any) -> str:
        """任务入队

        Args:
            data: 任务数据

        Returns:
            任务 ID

        Examples:
            >>> queue = TaskQueue()
            >>> task_id = queue.enqueue("my_task")
            >>> isinstance(task_id, str)
            True
            >>> len(task_id) > 0
            True
        """
        # 👉 TODO: 实现任务入队
        # 1. 创建 Task 对象
        # 2. 将任务 ID 添加到队列
        # 3. 将任务存储到字典
        # 4. 返回任务 ID
        #
        # 示例代码：
        # task = Task(data)
        # self._queue.append(task.task_id)
        # self._tasks[task.task_id] = task
        # return task.task_id
        raise NotImplementedError

    def dequeue(self) -> Task | None:
        """任务出队

        Returns:
            任务对象，如果队列为空返回 None

        Examples:
            >>> queue = TaskQueue()
            >>> queue.enqueue("task1")
            '...'
            >>> task = queue.dequeue()
            >>> task.data
            'task1'
            >>> task.status
            'processing'
        """
        # 👉 TODO: 实现任务出队
        # 1. 检查队列是否为空
        # 2. 如果为空，返回 None
        # 3. 从队列取出任务 ID: self._queue.popleft()
        # 4. 获取任务对象
        # 5. 更新任务状态为 "processing"
        # 6. 返回任务对象
        #
        # 示例代码：
        # if not self._queue:
        #     return None
        # task_id = self._queue.popleft()
        # task = self._tasks[task_id]
        # task.status = "processing"
        # return task
        raise NotImplementedError

    def get_result(self, task_id: str) -> Task | None:
        """查询任务结果

        Args:
            task_id: 任务 ID

        Returns:
            任务对象，如果不存在返回 None

        Examples:
            >>> queue = TaskQueue()
            >>> task_id = queue.enqueue("task1")
            >>> task = queue.get_result(task_id)
            >>> task.data
            'task1'
        """
        # 👉 TODO: 实现任务查询
        # return self._tasks.get(task_id)
        raise NotImplementedError

    def complete_task(self, task_id: str, result: Any) -> None:
        """标记任务完成

        Args:
            task_id: 任务 ID
            result: 任务结果

        Examples:
            >>> queue = TaskQueue()
            >>> task_id = queue.enqueue("task1")
            >>> queue.complete_task(task_id, "result1")
            >>> task = queue.get_result(task_id)
            >>> task.status
            'completed'
            >>> task.result
            'result1'
        """
        # 👉 TODO: 实现任务完成
        # 1. 获取任务对象
        # 2. 更新状态为 "completed"
        # 3. 保存结果
        #
        # 示例代码：
        # task = self._tasks.get(task_id)
        # if task:
        #     task.status = "completed"
        #     task.result = result
        raise NotImplementedError

    def size(self) -> int:
        """获取队列长度

        Returns:
            队列中待处理的任务数

        Examples:
            >>> queue = TaskQueue()
            >>> queue.enqueue("task1")
            '...'
            >>> queue.size()
            1
        """
        # 👉 TODO: 返回队列长度
        # return len(self._queue)
        raise NotImplementedError


if __name__ == "__main__":
    print("=" * 60)
    print("📬 任务队列练习")
    print("=" * 60)

    print("\n💡 完成上述类后，取消下面的注释测试：")
    print()

    # # 创建任务队列
    # queue = TaskQueue()
    #
    # # 入队任务
    # print("✅ 入队任务:")
    # task_ids = []
    # for i in range(3):
    #     task_id = queue.enqueue(f"task_{i}")
    #     task_ids.append(task_id)
    #     print(f"  入队: task_{i}, ID: {task_id[:8]}...")
    #
    # print(f"\n📊 队列大小: {queue.size()}")
    #
    # # 出队任务
    # print("\n✅ 出队任务:")
    # for _ in range(3):
    #     task = queue.dequeue()
    #     if task:
    #         print(f"  出队: {task.data}, 状态: {task.status}")
    #         # 模拟处理任务
    #         queue.complete_task(task.task_id, f"result_{task.data}")
    #
    # print(f"\n📊 队列大小: {queue.size()}")
    #
    # # 查询任务结果
    # print("\n✅ 查询任务结果:")
    # for task_id in task_ids:
    #     task = queue.get_result(task_id)
    #     if task:
    #         print(f"  任务 {task.data}:")
    #         print(f"    状态: {task.status}")
    #         print(f"    结果: {task.result}")

    print("\n" + "=" * 60)
    print("📚 关键要点:")
    print("   - FIFO 队列保证任务顺序")
    print("   - 使用唯一 ID 跟踪任务")
    print("   - 状态转换: pending → processing → completed")
    print("=" * 60)
