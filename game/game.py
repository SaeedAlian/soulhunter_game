import pygame, sys
from . import assets
from config import conf
from .player import Player
from .sprites.sprite import Sprite
from .sprites.obstacles import DoubleBlock, SingleBlock
from random import choices as random_choices, random


class Game:
    SPRITES = pygame.sprite.Group()
    MAXIMUM_SPRITES = 5
    SPRITE_DISTANCE_FACTOR = 7
    SPRITE_CLASSES: list[Sprite] = [SingleBlock, DoubleBlock]
    SPRITE_DROP_WEIGHTS: list[float] = [
        c.DROP_CHANCE if c.DROP_CHANCE else 1 for c in SPRITE_CLASSES
    ]

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.speed = conf.GAME_SPEED
        self.player_jump_speed = self.speed * conf.PLAYER_JUMP_SPEED_FACTOR
        self.player = Player(self.player_jump_speed)

        # This variable can move the platforms in
        # the y direction with the game speed
        self._platform_move_y = 0

    def increment_speed(self):
        if self.speed < conf.MAX_GAME_SPEED:
            self.speed += conf.GAME_SPEED_INCREMENT_FACTOR
            self.player_jump_speed = self.speed * conf.PLAYER_JUMP_SPEED_FACTOR

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

    def spawn_sprite(self):
        sprite = random_choices(self.SPRITE_CLASSES, self.SPRITE_DROP_WEIGHTS)[0]()

        self.SPRITES.add(sprite)

    def update_sprites(self):
        if len(self.SPRITES) < self.MAXIMUM_SPRITES:
            can_add_sprite = True

            for sprite in self.SPRITES:
                if sprite.rect.top < sprite.rect.height * self.SPRITE_DISTANCE_FACTOR:
                    can_add_sprite = False

            if can_add_sprite:
                self.spawn_sprite()

        for sprite in self.SPRITES:
            sprite.draw(self.surface)
            sprite.update(self.speed)
            sprite.change_animation()

            if sprite.rect.y > conf.SCREEN_HEIGHT + conf.PLATFORM_HEIGHT:
                sprite.kill()

    def draw_game_bg(self):
        self.surface.blit(assets.GAME_BG, (0, 0))

    def update_screen(self):
        # Update game screen
        self.draw_game_bg()
        self.draw_platforms()

        # Update player
        self.player.draw(self.surface)
        self.player.update(self.player_jump_speed)
        self.player.change_animation(self.speed)

        # Update sprites
        self.update_sprites()

        # Increment game speed
        self.increment_speed()

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
