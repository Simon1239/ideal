# coding:utf-8

'''
实现一个包含任务存储、任务分配、优先级管理、状态跟踪、通知和提醒等功能的任务池，可以考虑使用类和数据结构来组织代码.
'''

import heapq
import threading
import time

class Task:
    def __init__(self, description, priority) -> None:
        self.description = description
        self.priority = priority
        self.status = 'Pending'
        self.assignee = None
        self.created_at = time.time()

    def assign(self, assigne):
        self.assign = assigne
        self.status = 'Assigned'

    def complete(self):
        self.status = 'Completed'

class TaskPool:
    def __init__(self) -> None:
        self.tasks = []
        self.lock = threading.Lock()

    def add_task(self, task):
        with self.lock:
            heapq.heappush(self.tasks, (task.priority, task))

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

    def display_tasks(self):
        with self.lock:
            for _, task in sorted(self.tasks, key=lambda x: x[0]):
                print(f'Description: {task.description}, Priority: {task.priority}, Status: {task.status}, Assignee: {task.assignee}')


if __name__ == "__main__":
    task_pool = TaskPool()

    # 添加任务
    task1 = Task("Task 1", priority=2)
    task2 = Task("Task 2", priority=1)
    task3 = Task("Task 3", priority=3)

    task_pool.add_task(task1)
    task_pool.add_task(task2)
    task_pool.add_task(task3)

    # 分配任务
    assignee1 = "User A"
    assignee2 = "User B"

    assigned_task1 = task_pool.assign_task(assignee1)
    assigned_task2 = task_pool.assign_task(assignee2)

    # 完成任务
    task_pool.complete_task(assigned_task1)
    task_pool.complete_task(assigned_task2)

    # 显示任务状态
    task_pool.display_tasks()