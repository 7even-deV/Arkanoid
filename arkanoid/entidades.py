import pygame as pg
from pygame.sprite import Sprite
from . import ANCHO, ALTO


class Raqueta(Sprite):
    disfraces = "electric00.png"

    def __init__(self, **kwargs):
        self.image = pg.image.load(f"resources/images/{self.disfraces}")
        self.rect = self.image.get_rect(**kwargs)

    def update(self):
        if pg.key.get_pressed()[pg.K_LEFT] and not self.rect.x <= 0:
            self.rect.x -= 7

        if pg.key.get_pressed()[pg.K_RIGHT] and not self.rect.x >= ANCHO - self.rect.w:
            self.rect.x += 7


class Bola(Sprite):
    disfraces = "ball1.png"

    def __init__(self, **kwargs):
        self.image = pg.image.load(f"resources/images/{self.disfraces}")
        self.rect = self.image.get_rect(**kwargs)
        self.dx = 7
        self.dy = 7

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.x + self.rect.w > ANCHO or self.rect.x < 0:
            self.dx *= -1
        if self.rect.y < 0:
            self.dy *= -1

class Tiles(Sprite):
    disfraces = "redTile.png"

    def __init__(self, **kwargs):
        self.image = pg.image.load(f"resources/images/{self.disfraces}")
        self.rect = self.image.get_rect(**kwargs)
