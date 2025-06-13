import random

class SnakeGame:
    def __init__(self, width=640, height=480, speed=20):
        self.width = width
        self.height = height
        self.speed = speed
        self.snake = [[100, 50]]
        self.direction = 'RIGHT'
        self.food = self.spawn_food()
        self.score = 0

    def spawn_food(self):
        return [random.randrange(0, self.width, 20), random.randrange(0, self.height, 20)]

    def move(self):
        x, y = self.snake[0]
        if self.direction == 'UP':
            y -= self.speed
        elif self.direction == 'DOWN':
            y += self.speed
        elif self.direction == 'LEFT':
            x -= self.speed
        elif self.direction == 'RIGHT':
            x += self.speed

        new_head = [x, y]
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        return (
            head in self.snake[1:] or
            head[0] < 0 or head[0] > self.width or
            head[1] < 0 or head[1] > self.height
        )
