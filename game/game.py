import pygame, sys
from . import assets
from config import conf
from .player import Player
from .sprites.sprite import Sprite
from .sprites.obstacles import obstacles
from .sprites.items import items, Coin, Sprint, Health, Shield, ScoreBoost
from .sprites.enemies import enemies, Enemy
from .ui.button import Button
from .ui.text import Text
from .ui.prompt import Prompt
from db.db import DB
from db.record import Record
from random import choices as random_choices, randint


class Game:
    SPRITES = pygame.sprite.Group()
    MAXIMUM_SPRITES = 1
    SPRITE_DISTANCE_FACTOR = conf.MAX_SPRITES_DISTANCE_FACTOR
    SPRITE_CLASSES: list[Sprite] = items + obstacles + enemies
    SPRITE_DROP_WEIGHTS: list[float] = [
        c.DROP_CHANCE if c.DROP_CHANCE else 1 for c in SPRITE_CLASSES
    ]

    SPRINT_DISABLE_EVENT = pygame.USEREVENT + 1
    SHIELD_DISABLE_EVENT = pygame.USEREVENT + 2
    SCORE_BOOST_DISABLE_EVENT = pygame.USEREVENT + 3

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.speed = conf.GAME_SPEED
        self.is_started = False
        self.is_paused = False
        self.is_game_over = False
        self.is_reached_high_score = False
        self.coins = 0
        self.kills = 0
        self.score = 0
        self.is_score_boosted = False
        self.is_muted = False

        self.player = Player(self.player_jump_speed)

        self.db = DB(conf.DB_FILEPATH)

        # This variable can move the platforms in
        # the y direction with the game speed
        self.__platform_move_y = 0

        # This variable is for saving speed
        # before performing a sprint action
        # and reset the speed to it after
        # the sprint action has finished
        self.__speed_before_sprint = None

        # Load and play the main menu theme
        self.load_and_play_music(conf.MAIN_MENU_THEME_PATH)

    @property
    # is_running shows that the game is not over or paused
    def is_running(self):
        return not self.is_game_over and not self.is_paused

    @property
    # is_playing shows that the game is not in
    # main menu or paused or over
    def is_playing(self):
        return self.is_started and self.is_running

    @property
    def player_jump_speed(self):
        return self.speed * conf.PLAYER_JUMP_SPEED_FACTOR

    @property
    def active_ability_icons(self):
        icons = []

        if self.is_score_boosted:
            icons.append(assets.SCORE_BOOST_ITEM_MODEL)

        if self.player.is_shielded and not self.player.is_sprinting:
            icons.append(assets.SHIELD_ITEM_MODEL)

        if self.player.is_sprinting:
            icons.append(assets.SPRINT_ITEM_MODEL)

        return icons

    def __shield_event(self, duration: int):
        self.player.shield()
        pygame.time.set_timer(self.SHIELD_DISABLE_EVENT, duration)

    def __sprint_event(self, duration: int):
        self.player.sprint()
        pygame.time.set_timer(self.SPRINT_DISABLE_EVENT, duration)

    def __score_boost_event(self, duration: int):
        self.active_score_boost()
        pygame.time.set_timer(self.SCORE_BOOST_DISABLE_EVENT, duration)

    def __draw_game_stats_ui(
        self,
        font: pygame.font.Font,
        text: str,
        icon: pygame.Surface,
        position: tuple[float],
    ):
        text_surface = font.render(text, True, conf.GAME_STATS_TEXT_COLOR)

        icon_rect = icon.get_rect()
        text_rect = text_surface.get_rect()

        icon_rect.center = (position[0] + icon_rect.width, position[1])

        text_rect.center = (
            icon_rect.centerx + (icon_rect.width * 1.1),
            icon_rect.centery,
        )

        self.surface.blit(icon, icon_rect)
        self.surface.blit(text_surface, text_rect)

    def __draw_ability_icon(self, icon: pygame.Surface, position: tuple[float]):
        icon_rect = icon.get_rect()
        icon_rect.center = (position[0] - icon_rect.width, position[1])

        self.surface.blit(
            pygame.transform.scale(
                icon, (conf.GAME_STATS_ICON_SIZE, conf.GAME_STATS_ICON_SIZE)
            ),
            icon_rect,
        )

    def load_and_play_music(self, music_path: str):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loops=-1)

    def update_speed(self):
        # Increase the speed by the sprint factor
        # if the player is sprinting until it reaches
        # the sprint maximum value
        if self.player.is_sprinting:
            if self.speed < conf.PLAYER_SPRINT_MAX_SPEED:
                self.speed += conf.PLAYER_SPRINT_INCREMENT_FACTOR

        # If the speed before sprint is not null and
        # the game speed is greater than the speed before
        # sprint, then decrease the speed by the sprint factor
        elif (
            self.__speed_before_sprint is not None
            and self.speed > self.__speed_before_sprint
        ):
            self.speed -= conf.PLAYER_SPRINT_INCREMENT_FACTOR

        # otherwise we are in the normal situation and
        # will increase speed by the game speed increment factor
        elif self.speed < conf.MAX_GAME_SPEED:
            # and also set the __speed_before_sprint to None
            # to prevent decreasing of the game speed
            # in the previous if check
            self.__speed_before_sprint = None
            self.speed += conf.GAME_SPEED_INCREMENT_FACTOR

    def increment_score(self, count=1):
        self.score += count * 2 if self.is_score_boosted else count

    def increment_coins(self, count=1):
        self.coins += count * 2 if self.is_score_boosted else count

    def increment_kill(self, count=1):
        self.kills += count

    def active_score_boost(self):
        self.is_score_boosted = True

    def deactive_score_boost(self):
        self.is_score_boosted = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def game_over(self):
        # Save record
        new_record = Record(score=self.score, kills=self.kills, coins=self.coins)

        self.db.add_record(new_record)

        # Check for higher record
        # If there is no higher record then it is a high score
        if not self.db.is_there_any_higher_records(new_record):
            self.is_reached_high_score = True

        self.is_game_over = True

    def reset(self):
        self.coins = 0
        self.kills = 0
        self.score = 0
        self.is_started = False
        self.is_paused = False
        self.is_game_over = False
        self.is_reached_high_score = False
        self.speed = conf.GAME_SPEED
        self.__platform_move_y = 0
        self.__speed_before_sprint = None

        self.deactive_score_boost()
        self.player.reset(self.player_jump_speed)
        self.SPRITES.empty()

        self.MAXIMUM_SPRITES = 1
        self.SPRITE_DISTANCE_FACTOR = conf.MAX_SPRITES_DISTANCE_FACTOR

    def start(self):
        self.reset()
        self.is_started = True
        self.load_and_play_music(conf.GAME_THEME_PATH)

    def finish(self):
        self.is_started = False
        self.load_and_play_music(conf.MAIN_MENU_THEME_PATH)

    def quit(self):
        pygame.quit()
        sys.exit()

    def toggle_mute(self):
        self.is_muted = not self.is_muted

    def shield_action(self):
        # Active shield action
        self.__shield_event(conf.SHIELD_ACTION_DURATION_IN_MS)

    def score_boost_action(self):
        # Active score boost
        self.__score_boost_event(conf.SCORE_BOOST_ACTION_DURATION_IN_MS)

    def sprint_action(self):
        # Active sprint action
        self.__speed_before_sprint = self.speed
        self.__sprint_event(conf.SPRINT_ACTION_DURATION_IN_MS)
        self.__shield_event(conf.SPRINT_ACTION_DURATION_IN_MS + 5000)

    def draw_main_menu(self):
        font = pygame.font.Font(None, conf.MAIN_MENU_FONT_SIZE)

        # Draw background
        self.surface.blit(assets.MENU_BG, (0, 0))

        # Set x center position
        x_center_pos = conf.SCREEN_WIDTH / 2

        # Set logo rect position
        logo_rect = assets.LOGO.get_rect()
        logo_rect.center = (x_center_pos, conf.SCREEN_HEIGHT / 7)

        # Draw logo
        self.surface.blit(assets.LOGO, logo_rect)

        # Set play button
        play_btn = Button(
            x=x_center_pos,
            y=logo_rect.y + logo_rect.height + 80,
            sizes=(150, 150),
            icon=assets.PLAY_BUTTON,
            centerized=True,
        )

        play_btn.draw(self.surface)

        if play_btn.is_clicked():
            self.start()

        # Set sound button
        sound_btn = Button(
            x=x_center_pos,
            y=play_btn.icon_rect.y + play_btn.icon_rect.height + 60,
            sizes=(75, 75),
            icon=assets.DEACTIVE_SOUND_BUTTON
            if self.is_muted
            else assets.ACTIVE_SOUND_BUTTON,
            centerized=True,
        )

        sound_btn.draw(self.surface)

        if sound_btn.is_clicked():
            self.toggle_mute()

        # Set guide text
        guide_text = Text(
            font=font,
            x=x_center_pos,
            y=conf.SCREEN_HEIGHT - 50,
            color=conf.MAIN_MENU_TEXT_COLOR,
            centerized=True,
            inverse_y_position=True,
            texts=[
                "Move to sides with arrow keys",
                "Attack with spacebar",
                "Pause with P",
                "Toggle mute with M",
            ],
        )

        guide_text.draw(self.surface)

    def draw_pause_prompt(self):
        # Define buttons
        resume_btn = Button(x=0, y=0, icon=assets.PLAY_BUTTON, centerized=True)

        sound_btn = Button(
            x=0,
            y=0,
            icon=assets.DEACTIVE_SOUND_BUTTON
            if self.is_muted
            else assets.ACTIVE_SOUND_BUTTON,
            centerized=True,
        )

        exit_btn = Button(x=0, y=0, icon=assets.HOME_BUTTON, centerized=True)

        # Create prompt
        prompt = Prompt(
            assets.PROMPT_PAUSE_TITLE,
            buttons=[resume_btn, sound_btn, exit_btn],
            texts=["Press P to continue"],
        )

        # Draw prompt
        prompt.draw(self.surface)

        # Button events
        if resume_btn.is_clicked():
            self.resume()

        if sound_btn.is_clicked():
            self.toggle_mute()

        if exit_btn.is_clicked():
            self.finish()

    def draw_game_over_prompt(self):
        # Define buttons
        retry_btn = Button(x=0, y=0, icon=assets.RETRY_BUTTON, centerized=True)

        exit_btn = Button(x=0, y=0, icon=assets.HOME_BUTTON, centerized=True)

        # Create prompt
        prompt = Prompt(
            title=assets.PROMPT_NEW_HIGH_SCORE_TITLE
            if self.is_reached_high_score
            else assets.PROMPT_YOU_LOST_TITLE,
            buttons=[retry_btn, exit_btn],
            texts=[
                "YOU HAVE REACHED A HIGH SCORE !"
                if self.is_reached_high_score
                else "You are lost !",
                f"Your score : {self.score}",
                "Press R to retry",
                "Press ESC to exit",
            ],
        )

        # Draw prompt
        prompt.draw(self.surface)

        # Button events
        if retry_btn.is_clicked():
            self.start()

        if exit_btn.is_clicked():
            self.finish()

    def draw_platforms(self):
        # Increase the y factor by the game speed
        self.__platform_move_y += self.speed

        # but we need to reset the platform_move_y
        # variable to 0 because if the platform_move_y
        # becomes greater than the platform height it will
        # overlap the previous drawings of
        # platform so we need to reset this to 0
        if self.__platform_move_y >= conf.PLATFORM_HEIGHT:
            self.__platform_move_y = 0

        # Draw side blocks :
        # we will start the y position from
        # the negative of platform height
        # and increase it by platform height
        # itself until we reach screen height
        for y in range(-conf.PLATFORM_HEIGHT, conf.SCREEN_HEIGHT, conf.PLATFORM_HEIGHT):
            # Right platform
            self.surface.blit(
                pygame.transform.flip(assets.PLATFORM, flip_x=True, flip_y=False),
                (conf.SCREEN_WIDTH - conf.PLATFORM_WIDTH, y + self.__platform_move_y),
            )

            # Left platform
            self.surface.blit(
                assets.PLATFORM,
                (0, y + self.__platform_move_y),
            )

    def spawn_sprite(self):
        sprite = random_choices(self.SPRITE_CLASSES, self.SPRITE_DROP_WEIGHTS)[0]()

        self.SPRITES.add(sprite)

    def update_sprites(self):
        # If the sprites on the screen was less than
        # the maximum value
        if len(self.SPRITES) < self.MAXIMUM_SPRITES:
            # we will set the add sprite flag to true
            can_add_sprite = True

            # and if there is a sprite
            if self.SPRITES:
                last_sprite = self.SPRITES.sprites()[-1]

                # and if there is not enough space after the
                # last sprite, we won't spawn another sprite,
                # and the distance factor will be calculated with
                # a random value between current distance factor
                # and maximum distance factor
                if last_sprite.y + last_sprite.height < last_sprite.height * randint(
                    int(self.SPRITE_DISTANCE_FACTOR), conf.MAX_SPRITES_DISTANCE_FACTOR
                ):
                    can_add_sprite = False

            # Add sprite if we can
            if can_add_sprite:
                self.spawn_sprite()

        # Loop through all sprites
        for sprite in self.SPRITES:
            # Draw, update and animate
            sprite.draw(self.surface)
            sprite.update(self.speed)
            sprite.change_animation()

            # Collision check
            if self.player.collision_rect.colliderect(sprite.rect):
                # If player attacked an enemy
                if self.player.is_attacking and isinstance(sprite, Enemy):
                    # increment the score and kills if wasn't dead
                    if not sprite.is_dead:
                        self.increment_score(conf.ENEMY_KILL_SCORE)
                        self.increment_kill()

                    # and kill the enemy
                    sprite.die()

                # If player got a coin
                elif isinstance(sprite, Coin):
                    # increment the coins by the coin count
                    self.increment_coins(sprite.count)
                    # and remove the sprite
                    sprite.kill()

                # If player got a sprint item
                elif isinstance(sprite, Sprint):
                    # and player was not sprinting
                    if not self.player.is_sprinting:
                        # do the sprint action
                        self.sprint_action()
                        # and remove the sprite
                        sprite.kill()

                # If player got a sprint item
                elif isinstance(sprite, ScoreBoost):
                    # and game was not score boosted
                    if not self.is_score_boosted:
                        # do the score boost action
                        self.score_boost_action()
                        # and remove the sprite
                        sprite.kill()

                # If player got a sprint item
                elif isinstance(sprite, Shield):
                    # and player was not shielded
                    if not self.player.is_shielded:
                        # do the shield action
                        self.shield_action()
                        # and remove the sprite
                        sprite.kill()

                # If player got an health item
                elif isinstance(sprite, Health):
                    # heal
                    self.player.heal()
                    # and remove the sprite
                    sprite.kill()

                # If player is shielded or got hit or the sprite is impacted
                elif (
                    self.player.is_shielded or self.player.is_hit or sprite.is_impacted
                ):
                    # do nothing
                    pass

                # Player got hit by an obstacle or enemy
                else:
                    # we will hit the player
                    self.player.hit()
                    # impacted the sprite
                    sprite.impact()

                    # and if the lives were less than 1
                    if self.player.lives < 1:
                        # game is over
                        self.game_over()

            # If the sprite went out of the screen
            # we will delete the sprite and remove it
            # and also increase the score
            if sprite.y > conf.SCREEN_HEIGHT + conf.PLATFORM_HEIGHT:
                sprite.kill()
                self.increment_score(conf.OBSTACLE_PASSING_SCORE)

        # Increase max sprites on screen value
        if self.MAXIMUM_SPRITES < conf.MAX_SPRITES_ON_SCREEN:
            self.MAXIMUM_SPRITES += conf.SPRITES_ON_SCREEN_INCREMENT_FACTOR

        # Decrease sprite distance factor value
        if self.SPRITE_DISTANCE_FACTOR > conf.MIN_SPRITES_DISTANCE_FACTOR:
            self.SPRITE_DISTANCE_FACTOR -= conf.SPRITES_DISTANCE_DECREMENT_FACTOR

    def draw_game_bg(self):
        self.surface.blit(assets.GAME_BG, (0, 0))

    def draw_stats_ui(self):
        font = pygame.font.Font(None, conf.GAME_STATS_ICON_SIZE)

        stats = [
            {
                "text": str(self.player.lives),
                "icon": assets.LIVES_STATS_ICON,
            },
            {
                "text": str(self.kills),
                "icon": assets.KILLS_STATS_ICON,
            },
            {
                "text": str(self.score),
                "icon": assets.SCORE_STATS_ICON,
            },
            {
                "text": str(self.coins),
                "icon": assets.COINS_STATS_ICON,
            },
        ]

        x_pos = 5
        y_starting_pos = conf.SCREEN_HEIGHT - conf.GAME_STATS_ICON_SIZE

        for i, stat in enumerate(stats):
            self.__draw_game_stats_ui(
                font=font,
                text=stat["text"],
                icon=stat["icon"],
                position=(
                    x_pos,
                    y_starting_pos + (-i * conf.GAME_STATS_ICON_SIZE * 1.3),
                ),
            )

    def draw_ability_icon(self):
        # This method will draw the ability icons that are activated

        x_pos = conf.SCREEN_WIDTH - conf.GAME_STATS_ICON_SIZE - 5
        y_starting_pos = conf.SCREEN_HEIGHT - conf.GAME_STATS_ICON_SIZE

        for i, icon in enumerate(self.active_ability_icons):
            self.__draw_ability_icon(
                icon, (x_pos, y_starting_pos + (-i * conf.GAME_STATS_ICON_SIZE * 1.3))
            )

    def draw_pause_button(self):
        pause_btn = Button(x=10, y=10, icon=assets.PAUSE_BUTTON, sizes=(65, 65))

        pause_btn.draw(self.surface)

        if pause_btn.is_clicked():
            self.pause()

    def update_screen(self):
        if not self.is_started:
            self.draw_main_menu()

        elif self.is_game_over:
            self.draw_game_over_prompt()

        elif self.is_paused:
            self.draw_pause_prompt()

        else:
            # Update game screen
            self.draw_game_bg()
            self.draw_platforms()

            # Update player
            self.player.draw(self.surface)
            self.player.update(self.player_jump_speed)
            self.player.change_animation(self.speed)

            # Update sprites
            self.update_sprites()

            # Update game speed
            self.update_speed()

            # Draw stats UI
            self.draw_stats_ui()
            self.draw_ability_icon()

            # Draw pause button
            self.draw_pause_button()

    def update_music(self):
        if self.is_muted or self.is_game_over:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def get_events(self):
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == self.SHIELD_DISABLE_EVENT:
                self.player.disable_shield()

            if event.type == self.SCORE_BOOST_DISABLE_EVENT:
                self.is_score_boosted = False

            if event.type == self.SPRINT_DISABLE_EVENT:
                self.player.disable_sprint()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_m:
                        self.toggle_mute()

                if not self.is_started:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.quit()

                        case pygame.K_SPACE:
                            self.start()
                elif self.is_paused:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.finish()

                        case pygame.K_p:
                            self.resume()
                elif self.is_game_over:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.finish()

                        case pygame.K_r:
                            self.start()
                else:
                    match event.key:
                        case pygame.K_RIGHT:
                            self.player.jump(to_right=True, to_left=False)

                        case pygame.K_LEFT:
                            self.player.jump(to_right=False, to_left=True)

                        case pygame.K_SPACE:
                            self.player.attack()

                        case pygame.K_p:
                            self.pause()

            if event.type == pygame.KEYUP:
                if self.is_playing:
                    match event.key:
                        case pygame.K_SPACE:
                            self.player.disable_attack()
