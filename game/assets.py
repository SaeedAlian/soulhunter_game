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

# Explosion
EXPLOSION_MODELS: list[Surface] = []

for i in range(1, 8):
    EXPLOSION_MODELS.append(
        transform.scale(
            image.load(f"assets/environment/explosion/{i}.png"),
            (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
        )
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

for i in range(1, 14):
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
        (conf.PLAYER_WIDTH, conf.PLAYER_HEIGHT),
    )
]

for i in range(1, 6):
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

for i in range(1, 13):
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

# Bringer of Death
BRINGER_OF_DEATH_MAIN_MODELS: list[Surface] = []
BRINGER_OF_DEATH_DEATH_MODELS: list[Surface] = []


for i in range(1, 9):
    BRINGER_OF_DEATH_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/bringer_of_death/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )


for i in range(1, 12):
    BRINGER_OF_DEATH_DEATH_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/bringer_of_death/death/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )

# Hellhound
HELLHOUND_MAIN_MODELS: list[Surface] = []

for i in range(1, 12):
    HELLHOUND_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/hellhound/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )

# Ooze
OOZE_MAIN_MODELS = [
    transform.rotate(
        transform.scale(
            image.load(f"assets/sprites/ooze/1.png"),
            (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
        ),
        -90,
    )
]

# Worm
WORM_MAIN_MODELS = [
    transform.rotate(
        transform.scale(
            image.load(f"assets/sprites/worm/1.png"),
            (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
        ),
        -90,
    )
]

# Ghost
GHOST_MAIN_MODELS = [
    transform.rotate(
        transform.scale(
            image.load(f"assets/sprites/ghost/1.png"),
            (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
        ),
        -90,
    )
]

# Golem
GOLEM_MAIN_MODELS: list[Surface] = []

for i in range(1, 5):
    GOLEM_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/golem/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )

# Bat
BAT_MAIN_MODELS: list[Surface] = []

for i in range(1, 5):
    BAT_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/bat/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )

# Cacodemon
CACODEMON_MAIN_MODELS: list[Surface] = []
CACODEMON_DEATH_MODELS: list[Surface] = []


for i in range(1, 14):
    CACODEMON_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/cacodemon/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )


for i in range(1, 9):
    CACODEMON_DEATH_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/cacodemon/death/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )

# Sorcerer
SORCERER_MAIN_MODELS: list[Surface] = []

for i in range(1, 9):
    SORCERER_MAIN_MODELS.append(
        transform.rotate(
            transform.scale(
                image.load(f"assets/sprites/sorcerer/{i}.png"),
                (conf.ENEMY_WIDTH, conf.ENEMY_HEIGHT),
            ),
            -90,
        )
    )
