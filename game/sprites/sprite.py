from pygame import sprite, Surface, transform
from config import conf
from random import random, choice as random_choice


class Sprite(sprite.Sprite):
    DROP_CHANCE = 1

    def __init__(
        self,
        models: list[Surface],
        y_speed: float,
        animation_speed: float,
        is_on_edges=True,
    ) -> None:
        sprite.Sprite.__init__(self)

        self.models = models
        self.model_index = 0
        self.animation_speed = animation_speed
        self.y_speed = y_speed
        self.is_on_edges = is_on_edges

        self.rect = self.current_model.get_rect()

        self.rect.y = -self.rect.height * 2
        self.rect.x = self.__set_x_pos()

    @property
    def current_model(self):
        return self.models[int(self.model_index)]

    @property
    def side(self):
        # This property shows that the sprite is
        # on which side, the right or
        # the left. If we cut the screen in half
        # then the sides are obvious
        if conf.PLATFORM_WIDTH <= self.rect.x <= conf.SCREEN_WIDTH / 2:
            return "left"
        elif (
            conf.SCREEN_WIDTH / 2
            < self.rect.x
            <= conf.SCREEN_WIDTH - conf.PLATFORM_WIDTH
        ):
            return "right"
        else:
            return None

    @staticmethod
    def generate_random_x_pos():
        return (
            random() * (conf.SCREEN_WIDTH - conf.PLATFORM_WIDTH * 2)
            + conf.PLATFORM_WIDTH
        )

    def __set_x_pos(self):
        # If the sprite is on the edges
        if self.is_on_edges:
            # then pick a position between the
            # right pos or the left pos coordinates

            right_pos = conf.SCREEN_WIDTH - conf.PLATFORM_FLOOR_WIDTH - self.rect.width

            left_pos = conf.PLATFORM_FLOOR_WIDTH

            x_pos = random_choice([left_pos, right_pos])
        else:
            # otherwise generate a random x position
            x_pos = self.generate_random_x_pos()

        return x_pos

    def __update_rect(self):
        # This method will change the model rect
        # and set the previous coordinates
        # to the new rect coordinates

        prev_x = self.rect.x
        prev_y = self.rect.y
        self.rect = self.current_model.get_rect()

        # If it's on the edges then the x must be set from the
        # new rect width so we need to call __set_x_pos method
        # otherwise we set the new_x to the previous x position
        self.rect.x = prev_x

        self.rect.y = prev_y

    def update(self, game_speed: float):
        self.rect.y += game_speed + self.y_speed

    def draw(self, surface: Surface):
        surface.blit(
            transform.flip(
                self.current_model,
                self.side == "right",
                False,
            ),
            self.rect,
        )

    def change_animation(self):
        # If there is more than one image for the sprite
        # and the animation speed is non-zero
        if self.animation_speed > 0 and len(self.models) > 1:
            # increase the model_index by animation_speed
            self.model_index += self.animation_speed

            # and if the index reaches the last element
            # in the models list
            if self.model_index >= len(self.models):
                # reset the index
                self.model_index = 0

            # and then update model rect
            self.__update_rect()
