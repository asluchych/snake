import pygame as pg
from random import randrange

vec2 = pg.math.Vector2

class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100  # milliseconds
        self.time = 0

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.direction = vec2(0, -self.size)
            if event.key == pg.K_DOWN:
                self.direction = vec2(0, self.size)
            if event.key == pg.K_LEFT:
                self.direction = vec2(-self.size, 0)
            if event.key == pg.K_RIGHT:
                self.direction = vec2(self.size, 0)

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)

    def update(self):
        self.move()

    def draw(self):
        pg.draw.rect(self.game.screen, 'white', self.rect)


class Food:
    def __init__(self, game):
        pass

    def draw(self):
        pass