import pygame
from config.sizes import SCREEN_WIDTH, SCREEN_HEIGHT
from config.game import FPS
from game.game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Soul Hunter")
    clock = pygame.time.Clock()

    game = Game()

    while True:
        game.get_events()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
