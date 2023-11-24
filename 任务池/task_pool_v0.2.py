# coding:utf-8

'''
进一步完善 Task 类，以支持任务存储、任务分配、任务优先级管理、任务跟踪，并为其提供外接算法的功能
'''

import heapq
import threading
import time

class Task:
    def __init__(self, description, priority, algorithm=None):
        self.description = description
        self.priority = priority
        self.status = "Pending"
        self.assignee = None
        self.created_at = time.time()
        self.algorithm = algorithm

    def assign(self, assignee):
        self.assignee = assignee
        self.status = "Assigned"

    def complete(self):
        self.status = "Completed"

    def apply_algorithm(self):
        if self.algorithm:
            self.algorithm.execute(self)

# 外接算法的接口
class Algorithm:
    def execute(self, task):
        pass

class PriorityAlgorithm(Algorithm):
    def execute(self, task):
        # 优先级算法示例：根据任务创建时间和优先级进行排序
        task.priority_score = task.priority + (time.time() - task.created_at) / 1000

# 任务池类
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
        # return task.priority
        if self.algorithm:
            
            # return self.algorithm.execute(task)
            return task.priority
        else:
            return task.priority

    def display_tasks(self):
        with self.lock:
            for _, task in sorted(self.tasks, key=lambda x: x[0]):
                print(f'Description: {task.description}, Priority: {task.priority}, Status: {task.status}, Assignee: {task.assignee}')


# 示例用法
if __name__ == "__main__":
    # 创建一个任务池，并使用优先级算法
    priority_algorithm = PriorityAlgorithm()
    task_pool = TaskPool(algorithm=priority_algorithm)

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