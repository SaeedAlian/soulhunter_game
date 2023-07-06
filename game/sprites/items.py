from .sprite import Sprite
from pygame import Surface
from config import conf
from ..assets import (
    SAPPHIRE_MODEL,
    COIN_BAG_MODEL,
    COIN_MODELS,
    EMERALD_MODEL,
    FULL_HEART_MODEL,
    RUBY_MODEL,
    SPRINT_ITEM_MODEL,
)


class Item(Sprite):
    def __init__(
        self,
        models: list[Surface],
        animation_speed=0,
        is_on_edges=True,
    ):
        super().__init__(
            models, y_speed=0, animation_speed=animation_speed, is_on_edges=is_on_edges
        )


class Coin(Item):
    DROP_CHANCE = conf.COIN_DROP_CHANCE

    def __init__(self):
        self.count = 1
        super().__init__(COIN_MODELS, animation_speed=0.2)


class CoinBag(Item):
    DROP_CHANCE = conf.COIN_BAG_DROP_CHANCE

    def __init__(self):
        self.count = 10
        super().__init__([COIN_BAG_MODEL])


class Emerald(Item):
    DROP_CHANCE = conf.EMERALD_DROP_CHANCE

    def __init__(self):
        self.count = 20
        super().__init__([EMERALD_MODEL])


class Ruby(Item):
    DROP_CHANCE = conf.RUBY_DROP_CHANCE

    def __init__(self):
        self.count = 30
        super().__init__([RUBY_MODEL])


class Sapphire(Item):
    DROP_CHANCE = conf.SAPPHIRE_DROP_CHANCE

    def __init__(self):
        self.count = 25
        super().__init__([SAPPHIRE_MODEL])


class Health(Item):
    DROP_CHANCE = conf.HEALTH_DROP_CHANCE

    def __init__(self):
        super().__init__([FULL_HEART_MODEL])


class Sprint(Item):
    DROP_CHANCE = conf.SPRINT_DROP_CHANCE

    def __init__(self):
        super().__init__([SPRINT_ITEM_MODEL])
