# Soulhunter the game

## Requirements

- Python 3.8 (or above)
- Pygame 2.4.0

## Getting started

<b>Make sure that you have python3.8 (or above) installed.</b>

First clone or download the repository, then run the command below inside the project directory :

`pip install -r requirements.txt`

When the installation is finished run this command to start the game :

`python3 main.py`

## Code explaination

- `Config` module contains all constant variables.

The whole game contains a `Game` class which consists of four main components :

- Player
- Sprites
- Database
- UI

### Player

[Player](./game/player.py) class represents the main character.
It contains the player controls and drawing methods, position and ability properties.

### Sprites

[Sprite](./game/sprites/sprite.py) class represents the objects and sprites on the game.
It contains drawing methods, position properties and also impact property for showing that a sprite is impacted or not.

#### Sprite categories

- Enemies
- Items
- Obstacles

[Enemies](./game/sprites/enemies.py) can be attacked and killed by the player and if the player impacts with them without attacking, player will lose health.
[Items](./game/sprites/items.py) can be obtained by the player for gaining some ability or coins.
[Obstacles](./game/sprites/obstacles.py) will hit the player if they impact the player and must be passed by the player.

### Database

[Database](./db/db.py) will save every `record` of game, and will tell if there is a `highscore` reach or not.
It has [ًRecord](./db//record.py) class which represents the record entity model of database.
The [Database](./db/db.py) is using `CSV` files to save the data.

### UI

The UI component consists of three classes :

- [Button](./game/ui/button.py)
- [Text](./game/ui/text.py)
- [Prompt](./game/ui/prompt.py)

All of them are used to create an UI to showing the player.

### Game class

[Game](./game/game.py) class is the main class of project and will use the previous components to maintain the game.

## License

Soulhunter is licensed under MIT. See the [LICENSE](LICENSE) file for more information.

## ENJOY !
