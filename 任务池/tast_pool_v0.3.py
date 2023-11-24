# coding:utf-8
"""
如果一个任务由多个子任务（段子任务）组成，我们可以对 Task 类进行一些修改，以支持管理子任务。
"""

import heapq
import threading
import time

class SubTask:
    def __init__(self, description) -> None:
        self.description = description
        self.status = "Pending"

    def complete(self):
        self.status = "Completed"

class Task:
    def __init__(self, description, priority, algorithm=None) -> None:
        self.description = description
        self.priority = priority
        self.status = "Pending"
        self.assignee = None
        self.created_at = time.time()
        self.algorithm = algorithm
        self.subtasks = []

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def assign(self, assignee):
        self.assignee = assignee
        self.status = "Assigned"

    def complete(self):
        for subtask in self.subtasks:
            subtask.complete()
        self.status = "Completed"

    def apply_algorithm(self):
        if self.algorithm:
            self.algorithm.execute(self)

class PriorityAlgorithm:
    def execute(self, task):
        # 优先级算法示例：根据任务创建时间和优先级进行排序
        return task.priority + (time.time() - task.created_at) / 1000

class TaskPool:
    def __init__(self, algorithm=None):
        self.tasks = []
        self.lock = threading.Lock()
        self.algorithm = algorithm

    def add_task(self, task):
        with self.lock:
            heapq.heappush(self.tasks, (self._get_priority_score(task), task))

    def get_task(self):
        with self.lock:
            if self.tasks:
                _, task = heapq.heappop(self.tasks)
                return task

    def assign_task(self, assignee):
        task = self.get_task()
        if task:
            task.assign(assignee)
            return task

    def complete_task(self, task):
        task.complete()

    def _get_priority_score(self, task):
        if self.algorithm:
            return self.algorithm.execute(task)
        else:
            return task.priority

    def display_tasks(self):
        with self.lock:
            for _, task in sorted(self.tasks, key=lambda x: x[0]):
                print(f"Description: {task.description}, Priority: {task.priority}, Status: {task.status}, Assignee: {task.assignee}, Subtasks: {len(task.subtasks)}")

# 示例用法
if __name__ == "__main__":
    # 创建一个任务池，并使用优先级算法
    priority_algorithm = PriorityAlgorithm()
    task_pool = TaskPool(algorithm=priority_algorithm)

    # 添加任务
    task1 = Task("Project X", priority=2)
    task1.add_subtask(SubTask("Implement Feature A"))
    task1.add_subtask(SubTask("Write Tests for Feature A"))

    task2 = Task("Project Y", priority=1)
    task2.add_subtask(SubTask("Fix Bug in Module B"))

    task_pool.add_task(task1)
    task_pool.add_task(task2)

    # 分配任务
    assignee1 = "User A"
    assigned_task1 = task_pool.assign_task(assignee1)

    # 完成任务
    task_pool.complete_task(assigned_task1)

    # 显示任务状态
    task_pool.display_tasks()
