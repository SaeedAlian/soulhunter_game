### SIZES

# Screen
SCREEN_WIDTH = 680
SCREEN_HEIGHT = 984

# Player
PLAYER_WIDTH = 140
PLAYER_HEIGHT = 140
PLAYER_FOOT_MARGIN = 20

# Objects
PLATFORM_WIDTH = SCREEN_WIDTH / 4
PLATFORM_HEIGHT = SCREEN_HEIGHT // 3
PLATFORM_FLOOR_WIDTH = (
    PLATFORM_WIDTH - 3
)  # Platform width without counting the empty width
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 70
SPIKE_WIDTH = 70
SPIKE_HEIGHT = 70
DEAD_BUSH_WIDTH = 180
DEAD_BUSH_HEIGHT = 70
ITEM_WIDTH = 28
ITEM_HEIGHT = 28
ENEMY_WIDTH = 90
ENEMY_HEIGHT = 90


### GAME OPTIONS

# Speeds
FPS = 120
GAME_SPEED = 4
MAX_GAME_SPEED = 6
GAME_SPEED_INCREMENT_FACTOR = 0.001
PLAYER_JUMP_SPEED_FACTOR = 1.5
PLAYER_ATTACK_SPEED = 0.15
PLAYER_HIT_ANIMATION_SPEED = 0.1
PLAYER_SHIELD_ANIMATION_SPEED = 0.1
PLAYER_RUN_ANIMATION_SPEED = 0.03
EXPLOSION_ANIMATION_SPEED = 0.3

# Options
PLAYER_Y_POS = SCREEN_HEIGHT - (SCREEN_HEIGHT / 4)
MAX_SPRITES_ON_SCREEN = 4
MIN_SPRITES_DISTANCE_FACTOR = 5
MAX_SPRITES_DISTANCE_FACTOR = 12
SPRITES_ON_SCREEN_INCREMENT_FACTOR = 0.005
SPRITES_DISTANCE_DECREMENT_FACTOR = 0.002

# Sprite drop chances
SINGLE_BLOCK_DROP_CHANCE = 2
DOUBLE_BLOCK_DROP_CHANCE = 1.8
SPIKE_DROP_CHANCE = 1.6
DEAD_BUSH_DROP_CHANCE = 1.7
ENEMY_DROP_CHANCE = 1.78
COIN_DROP_CHANCE = 0.8
COIN_BAG_DROP_CHANCE = 0.5
EMERALD_DROP_CHANCE = 0.25
RUBY_DROP_CHANCE = 0.15
SAPPHIRE_DROP_CHANCE = 0.2
HEALTH_DROP_CHANCE = 0.05
SPRINT_DROP_CHANCE = 0.1
