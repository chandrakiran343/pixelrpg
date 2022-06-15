import pygame,sys
from settings import *
from debug import debug
from level import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Zelda")
        self.level = level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(fps)

if __name__ == '__main__':
    game = Game()
    game.run()
            