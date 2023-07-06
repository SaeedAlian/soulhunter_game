from pygame import font as pygame_font, Surface


class Text:
    def __init__(
        self,
        font: pygame_font.Font,
        x: float,
        y: float,
        texts: list[str],
        color: tuple[int],
        centerized: bool = False,
        inverse_y_position: bool = False,
        margin_between_texts: float = 20,
    ) -> None:
        # If the texts are inversely positioned
        # we need to reverse the texts list, so
        # it'll render accurately
        if inverse_y_position:
            texts.reverse()

        self.text_surfaces = [font.render(text, True, color) for text in texts]
        self.centerized = centerized
        self.inverse_y_position = inverse_y_position
        self.margin_between_texts = margin_between_texts

        self.text_rects = self.__create_rects(x, y)

    def __create_rects(
        self,
        x: float,
        y: float,
    ):
        text_rects = []

        # Loop through all of surfaces
        for i, surface in enumerate(self.text_surfaces):
            # Get the rect
            rect = surface.get_rect()

            # If we want to inversely set position of the texts
            # we will decrease the default y position by the factor
            # of text rect height and margin between texts multiplied
            # by the index of text surface, otherwise we will increase
            # the default y position by that factor
            y_pos = (
                y - (i * (rect.height + self.margin_between_texts))
                if self.inverse_y_position
                else y + (i * (rect.height + self.margin_between_texts))
            )

            # If texts are centerized
            if self.centerized:
                # we will set the center
                rect.center = (x, y_pos)

            # otherwise
            else:
                # we will set the x and y values
                rect.x = x
                rect.y = y_pos

            # then append the rect to text_rects
            text_rects.append(rect)

        return text_rects

    def update_pos(self, x: float, y: float):
        self.text_rects = self.__create_rects(x, y)

    def draw(self, surface: Surface):
        for i in range(len(self.text_surfaces)):
            surface.blit(self.text_surfaces[i], self.text_rects[i])
