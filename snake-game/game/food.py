from pygame import Vector2
import random


class Food:
    def __init__(self):
        self.position = Vector2(0, 0)

    def respawn(self, occupied: list[Vector2], width: int, height: int):
        while True:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            pos = Vector2(x, y)
            if pos not in occupied:
                self.position = pos
                break