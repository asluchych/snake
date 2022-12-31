import sys
from game_objects import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('SNAKE')
        self.screen = pg.display.set_mode([WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self):
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, WINDOW_SIZE))
         for x in range(0, WINDOW_SIZE, TILE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (WINDOW_SIZE, y))
         for y in range(0, WINDOW_SIZE, TILE_SIZE)]

    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        self.snake.update()
        self.food.update()
        pg.display.flip()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.snake.draw()
        self.food.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # snake controls
            self.snake.control(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
