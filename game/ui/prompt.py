from pygame import Surface, font as pygame_font, transform
from .button import Button
from .text import Text
from config import conf
from .. import assets


class Prompt:
    def __init__(
        self,
        title: Surface,
        texts: list[str] = [],
        buttons: list[Button] = [],
        button_spacing: float = None,
        button_size: float = None,
    ) -> None:
        font = pygame_font.Font(None, conf.PROMPT_FONT_SIZE)

        self.title = title
        self.title_rect = title.get_rect()

        self.buttons = buttons
        self.button_spacing = (
            button_spacing if button_spacing else conf.PROMPT_WIDTH / 18
        )
        self.button_size = button_size if button_size else conf.PROMPT_WIDTH / 6

        self.text_component = (
            Text(
                font=font,
                texts=texts,
                centerized=True,
                color=conf.PROMPT_TEXT_COLOR,
                x=0,
                y=0,
            )
            if texts
            else []
        )

        board_height = self.__calculate_board_height()

        self.board = transform.scale(
            assets.PROMPT_BOARD, (conf.PROMPT_WIDTH, board_height)
        )

        self.board_rect = self.board.get_rect()
        self.board_rect.center = (conf.SCREEN_WIDTH / 2, conf.SCREEN_HEIGHT / 2)

        self.__calculate_rect_positions()

    def __calculate_board_height(self):
        board_height = conf.PROMPT_HEIGHT  # Set default value for board height

        # Increase the board height by each text height
        if self.text_component:
            for text_rect in self.text_component.text_rects:
                board_height += (
                    text_rect.height + self.text_component.margin_between_texts
                )

        return board_height

    def __calculate_rect_positions(self):
        # Set title rect center
        self.title_rect.center = (
            self.board_rect.centerx,
            self.board_rect.centery - self.board_rect.height / 2,
        )

        # Set texts position
        if self.text_component:
            self.text_component.update_pos(
                self.board_rect.centerx,
                self.title_rect.centery + self.title_rect.height,
            )

        # Set buttons positions
        buttons_y_pos = (
            self.board_rect.centery
            + self.board_rect.height / 2
            - self.board_rect.height / 4
        )

        # this variable is for button container width
        # and if there is just one btn it will become 0
        button_container_width = (self.button_size + self.button_spacing) * (
            len(self.buttons) - 1
        )

        # and we will loop through the buttons
        for i, button in enumerate(self.buttons):
            # and set x position to beginning of button container
            # by using board centerx minus half of the container width
            # because we want to centerize the button container and then
            # we will increase it by a factor of button spacing and button size
            # multiplied by the button index
            # in this case if we just have one button it will centerize
            # otherwise buttons will align themselves in the center of prompt
            x_pos = (self.board_rect.centerx - button_container_width / 2) + i * (
                self.button_spacing + self.button_size
            )

            # reset the button sizes
            button.change_size(self.button_size, self.button_size)

            # set the button position
            button.change_pos(new_x=x_pos, new_y=buttons_y_pos)

    def draw(self, surface: Surface):
        surface.blit(self.board, self.board_rect)
        surface.blit(self.title, self.title_rect)

        for btn in self.buttons:
            btn.draw(surface)

        if self.text_component:
            self.text_component.draw(surface)
