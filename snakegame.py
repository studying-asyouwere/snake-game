import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

font = pygame.font.Font('Roboto-Medium.ttf', 25)

BLOCK_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 110, 255)
RED = (200, 0, 0)

class SnakeGame:

    def __init__(self, w=560, h=480):
        self.w = w
        self.h = h

        # initialise display settings
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake game by Studying As You Were')

        # initialise game settings
        # direction
        self.direction = Direction.RIGHT
        # snake
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)
        ]
        # food
        self.food = None
        self._place_food()
        # clock
        self.clock = pygame.time.Clock()
        # score
        self.score = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        # 2. Move snake
        self._move_head(self.direction) # this updates the self.head position
        self.snake.insert(0, self.head)
        # 3. Decide if game over
        if self._is_collision() == True:
            game_over = True
            return game_over, self.score
        # 4. Replace food or just move
        if self.head == self.food: 
            self._place_food()
            self.score += 1
        else:
            self.snake.pop()
        # 5. Update UI and tick clock
        self._update_ui()
        self.clock.tick(2 * len(self.snake) + 1)
        # 6. Return game over and score
        game_over = False
        return game_over, self.score
    
    def _is_collision(self):
        if self.head.x < 0 or self.w - BLOCK_SIZE < self.head.x or self.head.y < 0 or self.h - BLOCK_SIZE < self.head.y:
            return True
        if self.head in self.snake[1:]:
            return True
    
    def _move_head(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y )
    
    def _update_ui(self):
        # fill window
        self.display.fill(BLACK)
        # draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 0.2 * BLOCK_SIZE, pt.y + 0.2 * BLOCK_SIZE, 0.6 * BLOCK_SIZE, 0.6 * BLOCK_SIZE))
        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        # update score
        text = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(text, [0.2 * BLOCK_SIZE, 0.2 * BLOCK_SIZE])
        # update ui
        pygame.display.flip()

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()
        if game_over == True:
            break

    print('Final Score: ' + str(score))
    pygame.quit()