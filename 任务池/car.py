# coding:utf-8

class Car:
    def __init__(self) -> None:
        self.engine_running = False
        self.speed = 0
        self.direction = "straight"
        self.brake_pedal = False
        self.accelerator_pedal = False
        self.gear = "P" # P for Park
        self.headlights_on = False

    def start_engine(self):
        self.engine_running = True

    def stop_engine(self):
        self.engine_running = False
        self.speed = 0
        self.direction = "straight"
        self.brake_pedal = False
        self.accelerator_pedal = False
        self.gear = "P"

    def accelerate(self):
        if self.engine_running and self.gear != "P":
            self.speed += 5

    def brake(self):
        if self.speed > 0:
            self.speed -= 5
        else:
            self.speed = 0

    def turn_left(self):
        self.direction = "left"

    def turn_right(self):
        self.direction = "right"

    def straighten(self):
        self.direction = "straight"

    def shift_gear(self, gear):
        self.gear = gear

    def turn_on_headlights(self):
        self.headlights_on = True

    def turn_off_headlights(self):
        self.headlights_on = False

# 实例用法
car = Car()
car.start_engine()
car.accelerate()
car.turn_left()
car.brake()
car.turn_on_headlights()

print(f"Engine Running: {car.engine_running}")
print(f"Speed: {car.speed} km/h")
print(f"Direction: {car.direction}")
print(f"Headlights On: {car.headlights_on}")

