import pygame
from config.conf import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.game import Game


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Soul Hunter")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        game.get_events()
        game.update_screen()
        game.update_music()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
