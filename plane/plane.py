from pygame import Surface
from pygame.sprite import Sprite

from utils.helpers import *


class Plane(Sprite):
    def __init__(self):
        super(Plane, self).__init__()
        self.images = []
        self.image_index = 0
        self.image = None
        self.rect = None
        self.load_images()

    def load_images(self):
        for i in range(1, 3):
            plane_image = pygame.image.load(f'assets/images/avion/fly{i}.png').convert_alpha()
            plane_image = scale_image(plane_image, 150)
            self.images.append(plane_image)
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 200

    def update(self):
        self.rect.y += 4
        self.image_index += 0.2
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[int(self.image_index)]

    def fly_up(self):
        self.rect.y -= 8
