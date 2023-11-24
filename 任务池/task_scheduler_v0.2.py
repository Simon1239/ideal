# coding:utf-8

"""
先来先服务、最短作业优先、优先级调度、轮转调度、多级队列调度、最高响应比优先和多处理器调度算法的基本实现
"""

import queue
import threading
import time
from collections import deque

class Task:
    def __init__(self, name, execution_time, priority=0) -> None:
        self.name = name
        self.execution_time = execution_time
        self.status = "Pending"
        self.priority = priority
        self.arrival_time = time.time()

    def execute(self):
        time.sleep(self.execution_time)
        self.status = "Completed"

class FCFS_Scheduler:
    def __init__(self) -> None:
        self.task_queue = queue.Queue()

    def add_task(self, task):
        self.task_queue.put(task)
    
    def start_schedule(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            task.status = "Runing"
            task.execute()

class SJF_Scheduler:
    def __init__(self) -> None:
        self.task_queue = queue.PriorityQueue()

    def add_task(self, task):
        self.task_queue.put((task.execution_time, task))
    
    def start_schedule(self):
        while not self.task_queue.empty():
            _, task = self.task_queue.get()
            task.status = "Runing"
            task.execute()

class Priority_Scheduler:
    def __init__(self) -> None:
        self.task_queue = queue.PriorityQueue()

    def add_task(self, task):
        self.task_queue.put((-task.priority, task))

    def start_schdule(self):
        while not self.task_queue.empty():
            _, task = self.task_queue.get()
            task.status = "Runing"
            task.execute()

class RoundRobin_Scheduler:
    def __init__(self, time_slice=1) -> None:
        self.task_queue = queue.Queue()
        self.time_slice = time_slice

    def add_task(self, task):
        self.task_queue.put(task)

    def start_schedule(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            task.status = "Runing"
            start_time = time.time()
            while time.time() - start_time < self.time_slice and task.status != "Completed":
                task.execute()
            if task.status != "Completed":
                self.task_queue.put(task)

class MultiLevelQueue_Scheduler:
    def __init__(self, queues) -> None:
        self.queues = queues

    def add_task(self, task, queue_index=0):
        self.queues[queue_index].append(task)

    def start_schedule(self):
        for queue in self.queues:
            for task in queue:
                task.status = "Runing"


class HRRN_Scheduler:
    def __init__(self) -> None:
        self.task_queue = []

    def add_task(self, task):
        self.task_queue.append(task)

    def start_schedule(self):
        self.task_queue.sort(key=lambda task: task.execution_time / (time.time() - task.arrival_time))
        for task in self.task_queue:
            task.status = "Runing"
            task.execute()

class MultiProcessor_Scheduler:
    def __init__(self, num_processors) -> None:
        self.num_processors = num_processors
        self.task_queues = [queue.Queue() for _ in range(num_processors)]
        self.processors = [threading.Thread(target=self.processor_schedule, args=(i,)) for i in range(num_processors)]

    def add_task(self, task):
        shortest_queue = min(self.task_queues, key=lambda q: q.qsize())
        shortest_queue.put(task)

    def processor_schedule(self, processor_index):
        while True:
            task = self.task_queues[processor_index].get()
            task.status = "Runing"
            task.execute()

    def start_schedule(self):
        for processor in self.processors:
            processor.start()

# 示例用法
if __name__ == "__main__":
    task1 = Task("Task 1", execution_time=2)
    task2 = Task("Task 2", execution_time=3)
    task3 = Task("Task 3", execution_time=1)

    fcfs_scheduler = FCFS_Scheduler()
    fcfs_scheduler.add_task(task1)
    fcfs_scheduler.add_task(task2)
    fcfs_scheduler.add_task(task3)
    fcfs_scheduler.start_schedule()

    sjf_scheduler = SJF_Scheduler()
    sjf_scheduler.add_task(task1)
    sjf_scheduler.add_task(task2)
    sjf_scheduler.add_task(task3)
    sjf_scheduler.start_schedule()

    priority_scheduler = Priority_Scheduler()
    # priority_scheduler.add_task(task1)
    # priority_scheduler.add_task(task2)
    # priority_scheduler.add_task(task3)
    # priority_scheduler.start_schedule()

    round_robin_scheduler = RoundRobin_Scheduler(time_slice=1)
    round_robin_scheduler.add_task(task1)
    round_robin_scheduler.add_task(task2)
    round_robin_scheduler.add_task(task3)
    round_robin_scheduler.start_schedule()

    multi_level_queue_scheduler = MultiLevelQueue_Scheduler(queues=[[], []])
    multi_level_queue_scheduler.add_task(task1, queue_index=0)
    multi_level_queue_scheduler.add_task(task2, queue_index=1)
    multi_level_queue_scheduler.start_schedule()

    hrrn_scheduler = HRRN_Scheduler()
    hrrn_scheduler.add_task(task1)
    hrrn_scheduler.add_task(task2)
    hrrn_scheduler.add_task(task3)
    hrrn_scheduler.start_schedule()

    multi_processor_scheduler = MultiProcessor_Scheduler(num_processors=2)
    multi_processor_scheduler.add_task(task1)
    multi_processor_scheduler.add_task(task2)
    multi_processor_scheduler.add_task(task3)
    multi_processor_scheduler.start_schedule()
        
