import pygame as pg
from pygame.sprite import Sprite
from . import ANCHO, ALTO, FPS


class Raqueta(Sprite):
    disfraces = ["electric00.png", "electric01.png", "electric02.png"]

    def __init__(self, **kwargs):
        self.imagenes = []
        for nombre in self.disfraces:
            self.imagenes.append(pg.image.load(f"resources/images/{nombre}"))
        self.imagen_activa = 0

        self.tiempo_transcurrido = 0
        self.tiempo_hasta_cambio_disfraz = 1000 // FPS * 1

        self.image = self.imagenes[self.imagen_activa]
        self.rect = self.image.get_rect(**kwargs)

    def update(self, dt):
        if pg.key.get_pressed()[pg.K_LEFT] and not self.rect.left <= 0:
            self.rect.x -= 7

        if pg.key.get_pressed()[pg.K_RIGHT] and not self.rect.right >= ANCHO:
            self.rect.x += 7

        self.tiempo_transcurrido += dt
        if self.tiempo_transcurrido >= self.tiempo_hasta_cambio_disfraz:
            self.imagen_activa += 1
            if self.imagen_activa >= len(self.imagenes):
                self.imagen_activa = 0

            self.tiempo_transcurrido = 0

        self.image = self.imagenes[self.imagen_activa]


class Bola(Sprite):
    disfraces = "ball1.png"

    def __init__(self, **kwargs):
        self.image = pg.image.load(f"resources/images/{self.disfraces}")
        self.rect = self.image.get_rect(**kwargs)
        self.delta_x = 7
        self.delta_y = 7
        self.viva = True
        self.posicion_inicial = kwargs

    def update(self, dt):
        self.rect.x += self.delta_x
        if self.rect.x <= 0 or self.rect.right >= ANCHO:
            self.delta_x *= -1

        self.rect.y += self.delta_y
        if self.rect.y <= 0:
            self.delta_y *= -1

        if self.rect.bottom >= ALTO:
            self.viva = False
            self.rect = self.image.get_rect(**self.posicion_inicial)

    def comprobar_colision(self, otro):
        if self.rect.right >= otro.rect.left and self.rect.left <= otro.rect.right and \
           self.rect.bottom >= otro.rect.top and self.rect.top <= otro.rect.bottom:
            self.delta_y *= -1
