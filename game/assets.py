import sys

from pygame import image, transform, Surface
from config import conf

# Append root path to file
sys.path.append("../")

# Backgrounds
GAME_BG = transform.scale(
    image.load("assets/ui/game_bg.png"), (conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT)
)
MENU_BG = transform.scale(
    image.load("assets/ui/menu_bg.png"), (conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT)
)

# Game objects
PLATFORM = transform.scale(
    transform.rotate(image.load("assets/environment/ground/1.png"), -90),
    (conf.PLATFORM_WIDTH, conf.PLATFORM_HEIGHT),
)

# Player models
PLAYER_RUN_MODELS: list[Surface] = []
PLAYER_ATTACK_MODELS: list[Surface] = []
PLAYER_JUMP_MODELS = [
    transform.scale(
        image.load(f"assets/sprites/player/jump/1.png"),
        (conf.PLAYER_WIDTH, conf.PLAYER_HEIGHT),
    )
]

for i in range(1, 7):
    PLAYER_RUN_MODELS.append(
        transform.scale(
            image.load(f"assets/sprites/player/run/{i}.png"),
            (conf.PLAYER_WIDTH, conf.PLAYER_HEIGHT),
        )
    )

for i in range(1, 7):
    PLAYER_ATTACK_MODELS.append(
        transform.scale(
            image.load(f"assets/sprites/player/attack/{i}.png"),
            (conf.PLAYER_WIDTH, conf.PLAYER_HEIGHT),
        )
    )

# Player effects
PLAYER_HIT_EFFECTS: list[Surface] = []
PLAYER_SHIELD_EFFECTS: list[Surface] = [
    transform.scale(
        image.load(f"assets/sprites/player/shield/1.png"),
        (conf.PLAYER_WIDTH * 1.5, conf.PLAYER_HEIGHT * 1.5),
    )
]

for i in range(1, 4):
    PLAYER_HIT_EFFECTS.append(
        transform.scale(
            image.load(f"assets/sprites/player/hit/{i}.png"),
            (conf.PLAYER_WIDTH, conf.PLAYER_HEIGHT),
        )
    )

# Block models
SINGLE_BLOCK_MODEL = transform.scale(
    transform.rotate(image.load("assets/environment/block/single.png"), -90),
    (conf.BLOCK_WIDTH, conf.BLOCK_HEIGHT),
)
DOUBLE_BLOCK_MODEL = transform.scale(
    image.load("assets/environment/block/double.png"),
    (conf.BLOCK_WIDTH * 2, conf.BLOCK_HEIGHT),
)

# Spike models
SPIKE_MODELS: list[Surface] = []

for i in range(1, 7):
    SPIKE_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/environment/spikes/{i}.png"),
                (conf.SPIKE_WIDTH, conf.SPIKE_HEIGHT),
            ),
            -90,
        )
    )

# Dead bush
DEAD_BUSH_MODEL = transform.rotate(
    transform.scale(
        image.load("assets/environment/dead_bush/1.png"),
        (conf.DEAD_BUSH_WIDTH, conf.DEAD_BUSH_HEIGHT),
    ),
    -90,
)

# Coin
COIN_MODELS: list[Surface] = []

for i in range(1, 9):
    COIN_MODELS.append(
        transform.scale(
            image.load(f"assets/items/coin/{i}.png"),
            (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
        )
    )

# Coin bag
COIN_BAG_MODEL = transform.scale(
    image.load(f"assets/items/coin_bag/1.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)

# Emerald
EMERALD_MODEL = transform.scale(
    image.load(f"assets/items/emerald/1.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)

# Ruby
RUBY_MODEL = transform.scale(
    image.load(f"assets/items/ruby/1.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)

# Sapphire
SAPPHIRE_MODEL = transform.scale(
    image.load(f"assets/items/sapphire/1.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)

# Sprint item
SPRINT_ITEM_MODEL = transform.scale(
    image.load(f"assets/items/sprint/1.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)

# Heart
FULL_HEART_MODEL = transform.scale(
    image.load(f"assets/items/heart/full.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)
EMPTY_HEART_MODEL = transform.scale(
    image.load(f"assets/items/heart/empty.png"),
    (conf.ITEM_WIDTH, conf.ITEM_HEIGHT),
)
