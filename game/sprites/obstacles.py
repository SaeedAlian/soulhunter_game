from .sprite import Sprite
from pygame import Surface
from config import conf
from random import randint
from ..assets import DOUBLE_BLOCK_MODEL, SINGLE_BLOCK_MODEL


class Obstacle(Sprite):
    def __init__(
        self,
        models: list[Surface],
        animation_speed=0,
        is_on_edges=True,
    ):
        super().__init__(
            models, y_speed=0, animation_speed=animation_speed, is_on_edges=is_on_edges
        )


class SingleBlock(Obstacle):
    DROP_CHANCE = conf.SINGLE_BLOCK_DROP_CHANCE

    def __init__(self):
        super().__init__([SINGLE_BLOCK_MODEL])


class DoubleBlock(Obstacle):
    DROP_CHANCE = conf.DOUBLE_BLOCK_DROP_CHANCE

    def __init__(self):
        super().__init__([DOUBLE_BLOCK_MODEL])
