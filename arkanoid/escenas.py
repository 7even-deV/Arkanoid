import pygame as pg
from . import FPS, ANCHO, ALTO
from .entidades import Raqueta, Bola, Tiles


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
        fuente = pg.font.Font("resources/fonts/CabinSketch-Bold.ttf", 45)
        self.textito = fuente.render(
            "Pulsa <SPC> para comenzar", True, (0, 0, 0))
        self.anchoTexto = self.textito.get_width()

    def bucle_principal(self):
        game_over = False
        while not game_over:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    exit()

                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        game_over = True

            self.pantalla.fill((80, 80, 255))
            self.pantalla.blit(self.logo, (140, 140))
            self.pantalla.blit(
                self.textito, ((ANCHO - self.anchoTexto) // 2, 640))
            pg.display.flip()


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fondo = pg.image.load("resources/images/background.jpg")
        self.player = Raqueta(midbottom=(ANCHO//2, ALTO - 15))
        self.bola = Bola(midbottom=(ANCHO//2, ALTO//2))
        self.tiles = Tiles(midbottom=(ANCHO//2, ALTO//4))
        self.lives = 3
        self.score = 0
        self.can_points = True

    def collisions(self):
        if self.bola.rect.y + self.bola.rect.h > self.player.rect.y\
            and self.bola.rect.x > self.player.rect.x and self.bola.rect.x + self.bola.rect.w < self.player.rect.x + self.player.rect.w:
            self.bola.dy *= -1

        if self.bola.rect.y + self.bola.rect.h > ALTO:
            if self.lives >= 0:
                self.lives -= 1
                self.bola.rect.midbottom = ANCHO//2, ALTO//2
            else:
                self.bola.rect.midbottom = ANCHO//2, ALTO//2

        if self.bola.rect.y < self.tiles.rect.y + self.tiles.rect.h and self.bola.rect.y + self.bola.rect.h > self.tiles.rect.y\
            and self.bola.rect.x < self.tiles.rect.x + self.tiles.rect.w and self.bola.rect.x + self.bola.rect.w > self.tiles.rect.x:
            if self.can_points:
                self.score += 10
                self.can_points = False
        else: self.can_points = True

    def ui(self):
        if self.lives >= 0:
            fuente = pg.font.Font("resources/fonts/LibreFranklin-VariableFont_wght.ttf", 25)
            self.UI = fuente.render(f"Lives: {self.lives}  |  Score: {self.score}", True, (255, 255, 255))
        else:
            fuente = pg.font.Font("resources/fonts/CabinSketch-Bold.ttf", 45)
            self.UI = fuente.render("G A M E   O V E R", True, (255, 0, 0))

        self.anchoUI = self.UI.get_width()

        self.pantalla.blit(self.UI, ((ANCHO - self.anchoUI)//2, 40))

    def bucle_principal(self):
        game_over = False
        while not game_over:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    exit()

            self.player.update()
            if self.lives >= 0:
                self.bola.update()
            self.collisions()

            self.pantalla.blit(self.fondo, (0, 0))
            self.pantalla.blit(self.player.image, self.player.rect)
            self.pantalla.blit(self.bola.image, self.bola.rect)
            self.pantalla.blit(self.tiles.image, self.tiles.rect)
            self.ui()
            pg.display.flip()


class Records(Escena):
    def bucle_principal(self):
        print("soy records")
