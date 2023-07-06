from pygame import Surface, transform, mouse


class Button:
    def __init__(
        self,
        x: float,
        y: float,
        icon: Surface,
        sizes: tuple[float] = (),
        centerized: bool = False,
    ) -> None:
        self.centerized = centerized

        # If there is no sizing just use the default icon size
        self.icon = (
            transform.scale(icon, (sizes[0], sizes[1]))
            if sizes and sizes[0] and sizes[1]
            else icon
        )

        self.icon_rect = self.icon.get_rect()

        self.__set_pos(x, y)

    def __set_pos(self, x: float = None, y: float = None):
        # If it's centerized set the x and y to rect centerx and rect centery
        if self.centerized:
            if x:
                self.icon_rect.centerx = x

            if y:
                self.icon_rect.centery = y

        # otherwise set the x and y to rect x and rect y
        else:
            if x:
                self.icon_rect.x = x

            if y:
                self.icon_rect.y = y

    def change_icon(self, new_icon: Surface):
        # Save previous position
        prev_x = self.icon_rect.centerx if self.centerized else self.icon_rect.x
        prev_y = self.icon_rect.centery if self.centerized else self.icon_rect.y

        # Set new icon based on previous width and height
        self.icon = transform.scale(
            new_icon, (self.icon_rect.width, self.icon_rect.height)
        )
        self.icon_rect = self.icon.get_rect()

        # Set the position on new rect
        self.__set_pos(prev_x, prev_y)

    def change_size(self, new_width: float = None, new_height: float = None):
        # Save previous position
        prev_x = self.icon_rect.x
        prev_y = self.icon_rect.y

        # Set width and height (if there is no new size set it to previous size)
        width = new_width if new_width is not None else self.icon_rect.width
        height = new_height if new_height is not None else self.icon_rect.height

        # Rescale the icon
        self.icon = transform.scale(self.icon, (width, height))
        self.icon_rect = self.icon.get_rect()

        # Set the position on new rect
        self.__set_pos(prev_x, prev_y)

    def change_pos(self, new_x: float = None, new_y: float = None):
        self.__set_pos(new_x, new_y)

    def is_hovering(self):
        mouse_pos = mouse.get_pos()

        # If icon rect is colliding with
        # mouse position we will return true
        if self.icon_rect.collidepoint(mouse_pos):
            return True

        # otherwise we will return false
        return False

    def is_clicked(self):
        # If user is hovering on button
        # and clicking the left mouse button
        # we will return true
        if self.is_hovering() and mouse.get_pressed()[0]:
            return True

        # otherwise we will return false
        return False

    def draw(self, surface: Surface):
        surface.blit(self.icon, self.icon_rect)
