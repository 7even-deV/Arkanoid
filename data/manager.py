import pygame as pg
import pickle
from .settings import *


pg.init()
clock = pg.time.Clock()
time = pg.time.get_ticks()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(CAPTION[0])

# Load music and sounds
pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()

pg.mixer.music.load(f"resources/audio/{SCENE_MUSIC[0]}.wav")
pg.mixer.music.set_volume(0.5)
pg.mixer.music.play(-1, 0.0, 1000)

select_fx = pg.mixer.Sound('resources/audio/select.wav')
select_fx.set_volume(0.5)
game_run_fx = pg.mixer.Sound('resources/audio/game_run.wav')
game_run_fx.set_volume(0.5)
pause_fx = pg.mixer.Sound('resources/audio/pause.wav')
pause_fx.set_volume(0.5)
knock_fx = pg.mixer.Sound('resources/audio/knock.wav')
knock_fx.set_volume(0.5)
break_fx = pg.mixer.Sound('resources/audio/break.wav')
break_fx.set_volume(0.5)
limit_fx = pg.mixer.Sound('resources/audio/limit.wav')
limit_fx.set_volume(0.5)
win_fx = pg.mixer.Sound('resources/audio/win.wav')
win_fx.set_volume(0.5)
game_over_fx = pg.mixer.Sound('resources/audio/game_over.wav')
game_over_fx.set_volume(0.5)


def scene_caption(index):
    pg.display.set_caption(CAPTION[index])


def scene_music(index):
    pg.mixer.music.load(f"resources/audio/{SCENE_MUSIC[index]}.wav")
    if index == len(SCENE_MUSIC) - 1:
        pg.mixer.music.play(1, 0.0, 1000)
    else:
        pg.mixer.music.play(-1, 0.0, 1000)


def volume(vol=0):
    return round(pg.mixer.music.get_volume() + vol, 1)


def screen_size(resize):
    WIDTH = SCREEN_SIZE[resize][1]
    HEIGHT = SCREEN_SIZE[resize][0]
    pg.display.set_mode((WIDTH, HEIGHT))


def timer(timeout, *cooldown, **events):
    return Timer(timeout, *cooldown, **events).update()


class Timer:

    def __init__(self, timeout, *cooldown, **events):
        self.timeout = timeout * 1000
        self.cooldown = cooldown
        self.events = events
        self.start_time = 0
        self.current_time = 0
        self.counter = 0
        self.aux = 1

    def update(self):
        active_timer = countdown = True

        while active_timer:
            if countdown:
                self.start_time = self.current_time = pg.time.get_ticks()
                countdown = False

            self.current_time = pg.time.get_ticks()
            if self.aux == self.current_time // 1000:
                self.aux += 1
                print(self.current_time)

            if self.current_time - self.start_time > self.timeout:
                active_timer = False
                self.return_events()

    def return_events(self):
        for key, value in self.events.items():
            if isinstance(key, str):
                if key == "on":
                    value
                elif key == "off":
                    value()
