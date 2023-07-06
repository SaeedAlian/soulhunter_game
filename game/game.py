import pygame, sys
from . import assets
from config import conf
from .player import Player


class Game:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.speed = conf.GAME_SPEED
        self.player_jump_speed = self.speed * 2
        self.player = Player(self.player_jump_speed)

        # This variable can move the platforms in
        # the y direction with the game speed
        self._platform_move_y = 0

    def draw_menu(self):
        pass

    def draw_platforms(self):
        # Increase the y factor by the game speed
        self._platform_move_y += self.speed

        # but we need to reset the platform_move_y
        # variable to 0 because if the platform_move_y
        # becomes greater than the platform height it will
        # overlap the previous drawings of
        # platform so we need to reset this to 0
        if self._platform_move_y >= conf.PLATFORM_HEIGHT:
            self._platform_move_y = 0

        # Draw side blocks :
        # we will start the y position from
        # the negative of platform height
        # and increase it by platform height
        # itself until we reach screen height
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
        # Update game screen
        self.draw_game_bg()
        self.draw_platforms()

        # Update player
        self.player.draw(self.surface)
        self.player.update()
        self.player.change_animation(self.speed)

    def get_events(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RIGHT:
                        self.player.jump(to_right=True, to_left=False)

                    case pygame.K_LEFT:
                        self.player.jump(to_right=False, to_left=True)

                    case pygame.K_SPACE:
                        self.player.attack()
