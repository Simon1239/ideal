# coding:utf-8

"""
优化任务分发机制
"""

import queue
import threading
import time
import random

class Task:
    def __init__(self, description, priority) -> None:
        self.description = description
        self.priority = priority
        self.status = "Pending"
        self.assignee = None

    def assign(self, assignee):
        self.assignee = assignee
        self.status = "Assigned"

    def complete(self):
        self.status = "Completed"

def worker(task_queue):
    while True:
        task = task_queue.get()
        print(task)
        if task is None:
            break
        # 模拟任务处理
        time.sleep(random.uniform(0.1, 0.5))
        task.complete()

def task_scheduler(task_queue, tasks):
    for task in tasks:
        task_queue.put(task)

if __name__ == "__main__":
    task_queue = queue.Queue()
    tasks = [Task(f"Task {i}", priority=random.randint(1,5)) for i in range(10)]

    # 启动任务调度线程
    scheduler_thread = threading.Thread(target=task_scheduler, args=(task_queue, tasks))
    scheduler_thread.start()

    # 启动多个工作者线程
    num_workers = 3
    worker_threads = [threading.Thread(target=worker, args=(task_queue,)) for _ in range(num_workers)]

    for thread in worker_threads:
        thread.start()

    # 等待任务调度线程和工作者线程完成
    scheduler_thread.join()
    for _ in range(num_workers):
        task_queue.put(None)
    for thread in worker_threads:
        thread.join()

    print("All task completed.")