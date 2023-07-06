from .sprite import Sprite
from pygame import Surface, transform
from config import conf
from ..assets import (
    BRINGER_OF_DEATH_MAIN_MODELS,
    BRINGER_OF_DEATH_DEATH_MODELS,
    HELLHOUND_MAIN_MODELS,
    EXPLOSION_MODELS,
    OOZE_MAIN_MODELS,
    WORM_MAIN_MODELS,
    BAT_MAIN_MODELS,
    GOLEM_MAIN_MODELS,
    GHOST_MAIN_MODELS,
    CACODEMON_DEATH_MODELS,
    CACODEMON_MAIN_MODELS,
    SORCERER_MAIN_MODELS,
)


class Enemy(Sprite):
    DROP_CHANCE = conf.ENEMY_DROP_CHANCE

    def __init__(
        self,
        main_models: list[Surface],
        death_models: list[Surface] = [],
        y_speed=0,
        animation_speed=0,
        death_animation_speed=0,
    ):
        self.is_dead = False
        self.death_model_index = 0
        self.main_models = main_models
        self.has_death_model = bool(len(death_models))
        self.death_models = death_models if self.has_death_model else EXPLOSION_MODELS
        self.death_animation_speed = (
            death_animation_speed
            if self.has_death_model
            else conf.EXPLOSION_ANIMATION_SPEED
        )

        super().__init__(
            self.main_models,
            y_speed=y_speed,
            animation_speed=animation_speed,
        )

    @property
    def current_death_model(self):
        return self.death_models[int(self.death_model_index)]

    def __draw_death_model(self, surface: Surface):
        surface.blit(
            transform.flip(
                self.current_death_model,
                self.side == "right",
                False,
            ),
            (self.x, self.y),
        )

    def die(self):
        self.is_dead = True
        self.y_speed = 0

    def draw(self, surface: Surface):
        # If the enemy is dead
        if self.is_dead:
            # and if it doesn't have special
            # death model, then draw the enemy itself
            if not self.has_death_model:
                super().draw(surface)

            # then draw its death models
            self.__draw_death_model(surface)

        # otherwise
        else:
            # draw it normally
            super().draw(surface)

    def change_animation(self):
        # If the enemy is dead
        if self.is_dead:
            # do the animations on death models
            if self.death_animation_speed > 0 and len(self.death_models) > 1:
                self.death_model_index += self.death_animation_speed

                if self.death_model_index >= len(self.death_models) - 1:
                    # and kill the enemy from sprite group
                    # when the death animation is finished
                    self.kill()
                    self.death_model_index = 0

        # otherwise
        else:
            # do the default animation
            super().change_animation()


class BringerOfDeath(Enemy):
    def __init__(self):
        super().__init__(
            BRINGER_OF_DEATH_MAIN_MODELS,
            BRINGER_OF_DEATH_DEATH_MODELS,
            y_speed=0,
            animation_speed=0.1,
            death_animation_speed=0.2,
        )


class Hellhound(Enemy):
    def __init__(self):
        super().__init__(HELLHOUND_MAIN_MODELS, y_speed=0.5, animation_speed=0.1)


class Ooze(Enemy):
    def __init__(self):
        super().__init__(OOZE_MAIN_MODELS)


class Worm(Enemy):
    def __init__(self):
        super().__init__(WORM_MAIN_MODELS)


class Ghost(Enemy):
    def __init__(self):
        super().__init__(GHOST_MAIN_MODELS)


class Bat(Enemy):
    def __init__(self):
        super().__init__(BAT_MAIN_MODELS, y_speed=0.6, animation_speed=0.1)


class Golem(Enemy):
    def __init__(self):
        super().__init__(GOLEM_MAIN_MODELS, animation_speed=0.1)


class Cacodemon(Enemy):
    def __init__(self):
        super().__init__(
            CACODEMON_MAIN_MODELS,
            CACODEMON_DEATH_MODELS,
            y_speed=0.1,
            animation_speed=0.1,
            death_animation_speed=0.4,
        )


class Sorcerer(Enemy):
    def __init__(self):
        super().__init__(SORCERER_MAIN_MODELS, animation_speed=0.06)


enemies = [
    BringerOfDeath,
    Hellhound,
    Ooze,
    Worm,
    Ghost,
    Bat,
    Golem,
    Cacodemon,
    Sorcerer,
]
