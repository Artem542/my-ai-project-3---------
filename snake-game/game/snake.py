from pygame import Vector2


class Snake:
    def __init__(self, x: int, y: int):
        self.positions = [Vector2(x, y)]
        self.direction = Vector2(1, 0)
        self.next_direction = Vector2(1, 0)
        self.grow_pending = 0

    @property
    def head(self) -> Vector2:
        return self.positions[0]

    def change_direction(self, direction: Vector2):
        if direction.length() == 0:
            return
        if self.direction.x != 0 and direction.x != 0:
            return
        if self.direction.y != 0 and direction.y != 0:
            return
        self.next_direction = direction

    def move(self):
        self.direction = self.next_direction
        new_head = self.head + self.direction
        self.positions.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()

    def grow(self):
        self.grow_pending += 1

    def check_collision(self, width: int, height: int) -> bool:
        head = self.head
        if head.x < 0 or head.x >= width or head.y < 0 or head.y >= height:
            return True
        for pos in self.positions[1:]:
            if pos == head:
                return True
        return False