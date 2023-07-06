import pygame, sys
from . import assets
from config import conf
from .player import Player
from .sprites.sprite import Sprite
from .sprites.obstacles import obstacles
from .sprites.items import items
from .sprites.enemies import enemies
from random import choices as random_choices, randint


class Game:
    SPRITES = pygame.sprite.Group()
    MAXIMUM_SPRITES = 1
    SPRITE_DISTANCE_FACTOR = conf.MAX_SPRITES_DISTANCE_FACTOR
    SPRITE_CLASSES: list[Sprite] = items + obstacles + enemies
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
        # If the sprites on the screen was less than
        # the maximum value
        if len(self.SPRITES) < self.MAXIMUM_SPRITES:
            # we will set the add sprite flag to true
            can_add_sprite = True

            # and if there is a sprite
            if self.SPRITES:
                last_sprite = self.SPRITES.sprites()[-1]

                # and if there is not enough space after the
                # last sprite, we won't spawn another sprite,
                # and the distance factor will be calculated with
                # a random value between current distance factor
                # and maximum distance factor
                if last_sprite.y + last_sprite.height < last_sprite.height * randint(
                    int(self.SPRITE_DISTANCE_FACTOR), conf.MAX_SPRITES_DISTANCE_FACTOR
                ):
                    can_add_sprite = False

            # Add sprite if we can
            if can_add_sprite:
                self.spawn_sprite()

        # Loop through all sprites
        for sprite in self.SPRITES:
            # Draw, update and animate
            sprite.draw(self.surface)
            sprite.update(self.speed)
            sprite.change_animation()

            # If the sprite went out of the screen
            # we will delete the sprite and remove it
            if sprite.y > conf.SCREEN_HEIGHT + conf.PLATFORM_HEIGHT:
                sprite.kill()

        # Increase max sprites on screen value
        if self.MAXIMUM_SPRITES < conf.MAX_SPRITES_ON_SCREEN:
            self.MAXIMUM_SPRITES += conf.SPRITES_ON_SCREEN_INCREMENT_FACTOR

        # Decrease sprite distance factor value
        if self.SPRITE_DISTANCE_FACTOR > conf.MIN_SPRITES_DISTANCE_FACTOR:
            self.SPRITE_DISTANCE_FACTOR -= conf.SPRITES_DISTANCE_DECREMENT_FACTOR

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
