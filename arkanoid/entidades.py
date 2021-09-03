import pygame as pg
from pygame.sprite import Sprite


class Raqueta(Sprite):
    disfraces = "electric00.png"

    def __init__(self, **kwargs):
        self.image = pg.image.load(f"resources/images/{self.disfraces}")
        self.rect = self.image.get_rect(**kwargs)

    def update(self):
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.rect.x -= 5

        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.rect.x += 5
