import pygame as pg
from . import FPS


class Escena():
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        pass


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.logo = pg.image.load("resources/images/arkanoid_name.png")

    def bucle_principal(self):
        game_over = False
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    game_over = True

            self.pantalla.fill((80, 80, 255))
            self.pantalla.blit(self.logo, (140, 140))

            pg.display.flip()


class Partida(Escena):
    pass


class Records(Escena):
    pass
