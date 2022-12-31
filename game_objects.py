import pygame as pg
from random import randrange

from settings import *

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100  # milliseconds
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.directions[pg.K_UP]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_DOWN and self.directions[pg.K_DOWN]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
            if event.key == pg.K_LEFT and self.directions[pg.K_LEFT]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
            if event.key == pg.K_RIGHT and self.directions[pg.K_RIGHT]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size // 2, WINDOW_SIZE - self.size // 2, self.size)] * 2

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > WINDOW_SIZE:
            self.game.new_game()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'white', segment) for segment in self.segments]


class Food:
    def __init__(self, game):
        self.game = game
        self.size = TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()
        self.blink_rate = 300
        self.time = 0
        self.is_blinking = False

    def update(self):
        self.time += pg.time.Clock().tick(FPS)
        if self.time > self.blink_rate:
            self.is_blinking = not self.is_blinking
            self.time = 0

    def draw(self):
        if not self.is_blinking:
            pg.draw.rect(self.game.screen, 'dimgray', self.rect)
