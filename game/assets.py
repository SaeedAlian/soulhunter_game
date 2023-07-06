import sys

from pygame import image, transform
from config import sizes

# Append root path to file
sys.path.append("../")

# Backgrounds
GAME_BG = transform.scale(
    image.load("assets/ui/game_bg.png"), (sizes.SCREEN_WIDTH, sizes.SCREEN_HEIGHT)
)
MENU_BG = transform.scale(
    image.load("assets/ui/menu_bg.png"), (sizes.SCREEN_WIDTH, sizes.SCREEN_HEIGHT)
)

# Game objects
PLATFORM = transform.scale(
    transform.rotate(image.load("assets/environment/ground/1.png"), -90),
    (sizes.PLATFORM_WIDTH, sizes.PLATFORM_HEIGHT),
)
