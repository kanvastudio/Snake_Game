"""
=========================================================
🐍 SNAKE GAME LOGIC (CLASSIC GRID VERSION)
=========================================================
- Pure logic (no UI code here)
- Handles movement, food, collision, score
=========================================================
"""

WIDTH = 20
HEIGHT = 20


class SnakeGame:
    def __init__(self, speed=0.2, wall_collision=True):

        # movement speed (seconds per tick)
        self.base_speed = speed
        self.speed = speed

        # initial snake (3 segments = classic snake feel)
        self.snake = [
            (10, 10),
            (9, 10),
            (8, 10),
        ]

        # initial movement direction
        self.direction = (1, 0)

        # food position
        self.food = (5, 5)

        # game state
        self.score = 0
        self.game_over = False

        # wall mode (kill or wrap)
        self.wall_collision = wall_collision

    def step(self):
        """
        Executes ONE game tick:
        - move snake
        - check collisions
        - handle food
        """

        head = self.snake[0]

        new_x = head[0] + self.direction[0]
        new_y = head[1] + self.direction[1]

        # -------------------------
        # WALL LOGIC
        # -------------------------
        if self.wall_collision:
            new_head = (new_x, new_y)

            if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
                self.game_over = True
                return
        else:
            new_head = (new_x % WIDTH, new_y % HEIGHT)

        # -------------------------
        # SELF COLLISION
        # -------------------------
        if new_head in self.snake:
            self.game_over = True
            return

        # move snake
        self.snake.insert(0, new_head)

        # -------------------------
        # FOOD LOGIC
        # -------------------------
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def spawn_food(self):
        """Spawn food in empty cell"""
        import random

        while True:
            pos = (
                random.randint(1, WIDTH - 2),
                random.randint(1, HEIGHT - 2),
            )
            if pos not in self.snake:
                self.food = pos
                return