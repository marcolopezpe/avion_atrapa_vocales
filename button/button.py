from pygame.sprite import Sprite

from utils.helpers import *


class Button(Sprite):
    def __init__(self, x, y, image, action):
        super(Button, self).__init__()
        self.surface = pygame.image.load(image).convert_alpha()
        self.surface = scale_image(self.surface, 200)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = self.rect.width
        self.h = self.rect.height
        self.action = action

    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
