from pygame import Surface, transform
from config import conf
from .assets import (
    PLAYER_RUN_MODELS,
    PLAYER_ATTACK_MODELS,
    PLAYER_JUMP_MODELS,
    PLAYER_SHIELD_EFFECTS,
    PLAYER_HIT_EFFECTS,
)


class Player:
    def __init__(self, jump_speed: float) -> None:
        self.__jump_speed = jump_speed
        self.model_index = 0
        self.shield_effect_index = 0
        self.hit_effect_index = 0
        self.model_index = 0
        self.is_jumping = False
        self.is_attacking = False
        self.is_shielded = False
        self.is_sprinting = False
        self.is_hit = False
        self.lives = 3
        self.jump_dir = None
        self.angle = 90
        self.shield_effects = PLAYER_SHIELD_EFFECTS
        self.hit_effects = PLAYER_HIT_EFFECTS

        # Set the player position
        self.rect = self.current_model.get_rect()
        self.right_pos = conf.SCREEN_WIDTH - conf.PLATFORM_FLOOR_WIDTH - self.rect.width

        self.left_pos = conf.PLATFORM_FLOOR_WIDTH

        self.rect.y = conf.PLAYER_Y_POS
        self.rect.x = self.right_pos

    @property
    def models(self):
        if self.is_attacking:
            return PLAYER_ATTACK_MODELS
        elif self.is_jumping:
            return PLAYER_JUMP_MODELS
        else:
            return PLAYER_RUN_MODELS

    @property
    def current_model(self):
        return self.models[int(self.model_index)]

    @property
    def current_hit_effect(self):
        return self.hit_effects[int(self.hit_effect_index)]

    @property
    def current_shield_effect(self):
        return self.shield_effects[int(self.shield_effect_index)]

    @property
    def side(self):
        # This property shows that the player is
        # on which side of platforms, the right or
        # the left
        if self.rect.x <= self.left_pos:
            return "left"
        elif self.rect.x >= self.right_pos:
            return "right"
        else:
            return "center"

    @property
    def jump_speed(self):
        return self.__jump_speed * 2 if self.is_sprinting else self.__jump_speed

    def jump(self, to_left: bool, to_right: bool):
        # If we are on the left side and want to
        # jump to left or the opposite, we cannot do it
        if not (
            (to_left and self.side == "left") or (to_right and self.side == "right")
        ):
            self.is_jumping = True
            self.model_index = 0
            self.angle = 0

            # Setting the jump direction
            if to_left:
                self.jump_dir = "left"
            elif to_right:
                self.jump_dir = "right"
            else:
                self.jump_dir = None

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.model_index = 0

    def disable_attack(self):
        if self.is_attacking:
            self.is_attacking = False
            self.model_index = 0

    def disable_jump(self):
        if self.is_jumping:
            self.is_jumping = False
            self.model_index = 0
            self.jump_dir = None
            self.angle = 90

    def shield(self):
        self.is_shielded = True

    def disable_shield(self):
        self.is_shielded = False

    def hit(self):
        if not self.is_shielded:
            self.is_hit = True
            self.lives -= 1

    def sprint(self):
        self.is_sprinting = True
        self.shield()

    def disable_sprint(self):
        self.is_sprinting = False
        self.disable_shield()

    def update(self, new_jump_speed: float = None):
        if new_jump_speed is not None:
            self.__jump_speed = new_jump_speed

        # If the player is jumping
        if self.is_jumping:
            # and the jump direction is left and he is
            # not on the left side
            if self.jump_dir == "left" and self.side != "left":
                # then move left
                self.rect.x -= self.jump_speed

            # or the jump direction is right and he is
            # not on the right side
            elif self.jump_dir == "right" and self.side != "right":
                # then move right
                self.rect.x += self.jump_speed

            # otherwise
            else:
                self.disable_jump()

    def draw(self, surface: Surface):
        # Draw player model
        surface.blit(
            transform.flip(
                transform.rotate(self.current_model, self.angle),
                self.side == "left" or self.jump_dir == "left",
                False,
            ),
            self.rect,
        )

        # Draw shield effect
        if self.is_shielded:
            surface.blit(self.current_shield_effect, self.rect)

        # Draw hit effect
        if self.is_hit:
            surface.blit(self.current_hit_effect, self.rect)

    def change_animation(self, current_game_speed: float):
        # If there is more than one image on the player
        # models then
        if len(self.models) > 1:
            # increase the model_index by a factor of
            # game speed
            self.model_index += (
                conf.PLAYER_ATTACK_SPEED
                if self.is_attacking
                else current_game_speed / 10
            )

            # and if the index reaches the last element
            # in the models list
            if self.model_index >= len(self.models):
                # disable attacking if he is attacking
                # because the attacking animation is finished
                if self.is_attacking:
                    self.disable_attack()

                # otherwise reset the index
                else:
                    self.model_index = 0

        # These two blocks is for changing the hit
        # effect and shield effect images
        # and the algorithm is based on the player
        # models in the previous block

        if self.is_hit and len(self.hit_effects) > 1:
            self.hit_effect_index += 0.2

            if self.hit_effect_index >= len(self.hit_effects):
                self.hit_effect_index = 0
                self.is_hit = False

        if self.is_shielded and len(self.shield_effects) > 1:
            self.shield_effect_index += 0.1

            if self.shield_effect_index >= len(self.shield_effects):
                self.shield_effect_index = 0
