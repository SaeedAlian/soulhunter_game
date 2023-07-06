import pygame
from config.sizes import SCREEN_WIDTH, SCREEN_HEIGHT
from config.game import FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Soul Hunter")
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
