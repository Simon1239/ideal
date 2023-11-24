# coding:utf-8

"""
定义了一个 Task 类，包含了任务的基本属性和方法，以及各种状态的转换。
"""

class Task:
    def __init__(self, name, execution_time) -> None:
        self.name = name
        self.execution_time = execution_time
        self.status = "Pending"

    def assign(self):
        self.status = "Assigned"

    def start(self):
        self.status = "Runing"

    def complete(self):
        self.status = "Completed"

    def pause(self):
        self.status = "Pauses"

    def cancel(self):
        self.status = "Cancelled"

    def fail(self):
        self.status = "Failed"

    def wait(self):
        self.status = "Waiting"

    def display_status(self):
        print(f"Task {self.name} is {self.status}")

# 示例用法
if __name__ == "__main__":
    task = Task("ProjectX_Task1", execution_time=5)

    task.display_status()  # 输出: Task ProjectX_Task1 is Pending

    task.assign()
    task.display_status()  # 输出: Task ProjectX_Task1 is Assigned

    task.start()
    task.display_status()  # 输出: Task ProjectX_Task1 is Running

    # 模拟任务执行
    task.wait()
    task.display_status()  # 输出: Task ProjectX_Task1 is Waiting

    # 模拟任务失败
    task.fail()
    task.display_status()  # 输出: Task ProjectX_Task1 is Failed

    # 模拟任务被取消
    task.cancel()
    task.display_status()  # 输出: Task ProjectX_Task1 is Cancelled

    # 模拟任务完成
    task.complete()
    task.display_status()  # 输出: Task ProjectX_Task1 is Completed



