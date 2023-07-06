import pygame, sys
from . import assets
from config import conf


class Game:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.speed = conf.GAME_SPEED

        """
          This variable can move the platforms in
          the y direction with the game speed
        """
        self._platform_move_y = 0

    def draw_menu(self):
        pass

    def draw_platforms(self):
        # increase the y factor by the game speed
        self._platform_move_y += self.speed

        if self._platform_move_y >= conf.PLATFORM_HEIGHT:
            self._platform_move_y = 0

        for y in range(-conf.PLATFORM_HEIGHT, conf.SCREEN_HEIGHT, conf.PLATFORM_HEIGHT):
            # Right platform
            self.surface.blit(
                pygame.transform.flip(assets.PLATFORM, flip_x=True, flip_y=False),
                (conf.SCREEN_WIDTH - conf.PLATFORM_WIDTH, y + self._platform_move_y),
            )

            # Left platform
            self.surface.blit(
                assets.PLATFORM,
                (0, y + self._platform_move_y),
            )

    def draw_game_bg(self):
        self.surface.blit(assets.GAME_BG, (0, 0))

    def update_screen(self):
        self.draw_game_bg()
        self.draw_platforms()

    def get_events(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
