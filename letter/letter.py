import random

import pygame
from pygame.sprite import Sprite

from utils.constants import *
from utils.helpers import *


class Letter(Sprite):
    def __init__(self, ):
        super(Letter, self).__init__()
        self.key = random.choice(list(LETTERS_UPPER))
        self.image = pygame.image.load(LETTERS_UPPER[self.key]).convert_alpha()
        self.image = scale_image(self.image, 70)
        self.rect = self.image.get_rect(
            center=(
                random.randint(WIDTH + 20, WIDTH + 200),
                random.randint(150, HEIGHT - 50),
            )
        )
        self.speed = random.randint(LETTER_SPEED_MIN, LETTER_SPEED_MIN)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
