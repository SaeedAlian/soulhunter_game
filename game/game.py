import pygame, sys


class Game:
    def __init__(self) -> None:
        pass

    def get_events(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
