import pygame.font


class Button():

    def __init__(self, settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.toolbar_rect = pygame.Rect(
            settings.screen_width-settings.toolbar_width, 0, settings.toolbar_width, settings.screen_height)

        # Set the dimensions and properties of the button.
        self.width, self.height = 100, 50
        self.button_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 30, self.width, self.height)
        self.rect.centerx = self.toolbar_rect.centerx

        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
