import pygame as pg
from arkanoid import ALTO, ANCHO
from arkanoid.escenas import Portada

pg.init()


class Game():
    def __init__(self):
        pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.escenas = [Portada(pantalla)]

    def launch(self):
        self.escenas[0].bucle_principal()
        pg.quit()
