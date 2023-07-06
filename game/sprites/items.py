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
    SCORE_BOOST_ITEM_MODEL,
    SHIELD_ITEM_MODEL,
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

    def __init__(
        self, models: list[Surface] = COIN_MODELS, animation_speed=0.1, count=1
    ):
        self.count = count
        super().__init__(models, animation_speed=animation_speed)


class CoinBag(Coin):
    DROP_CHANCE = conf.COIN_BAG_DROP_CHANCE

    def __init__(self):
        super().__init__([COIN_BAG_MODEL], count=10, animation_speed=0)


class Emerald(Coin):
    DROP_CHANCE = conf.EMERALD_DROP_CHANCE

    def __init__(self):
        super().__init__([EMERALD_MODEL], count=20, animation_speed=0)


class Ruby(Coin):
    DROP_CHANCE = conf.RUBY_DROP_CHANCE

    def __init__(self):
        super().__init__([RUBY_MODEL], count=30, animation_speed=0)


class Sapphire(Coin):
    DROP_CHANCE = conf.SAPPHIRE_DROP_CHANCE

    def __init__(self):
        super().__init__([SAPPHIRE_MODEL], count=25, animation_speed=0)


class Health(Item):
    DROP_CHANCE = conf.HEALTH_DROP_CHANCE

    def __init__(self):
        super().__init__([FULL_HEART_MODEL])


class Sprint(Item):
    DROP_CHANCE = conf.SPRINT_DROP_CHANCE

    def __init__(self):
        super().__init__([SPRINT_ITEM_MODEL])


class ScoreBoost(Item):
    DROP_CHANCE = conf.SCORE_BOOST_DROP_CHANCE

    def __init__(self):
        super().__init__([SCORE_BOOST_ITEM_MODEL])


class Shield(Item):
    DROP_CHANCE = conf.SHIELD_DROP_CHANCE

    def __init__(self):
        super().__init__([SHIELD_ITEM_MODEL])


items = [Coin, CoinBag, Emerald, Ruby, Sapphire, Health, Sprint, ScoreBoost, Shield]
