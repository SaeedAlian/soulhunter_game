from .sprite import Sprite
from pygame import Surface
from config import conf
from ..assets import (
    DOUBLE_BLOCK_MODEL,
    SINGLE_BLOCK_MODEL,
    SPIKE_MODELS,
    DEAD_BUSH_MODEL,
)


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


class Spike(Obstacle):
    DROP_CHANCE = conf.SPIKE_DROP_CHANCE

    def __init__(self):
        super().__init__(SPIKE_MODELS, 0.1)


class DeadBush(Obstacle):
    DROP_CHANCE = conf.DEAD_BUSH_DROP_CHANCE

    def __init__(self):
        super().__init__([DEAD_BUSH_MODEL])


obstacles = [SingleBlock, DoubleBlock, Spike, DeadBush]
