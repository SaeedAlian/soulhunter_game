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
