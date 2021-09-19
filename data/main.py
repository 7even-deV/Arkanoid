from . import __author__
from .manager import *
from .scenes import Menu, Game, Record


class Main():
    def __init__(self):
        self.scenes = [Menu(screen), Game(screen), Record(screen)]

    def run(self):
        i = 0
        while True:
            scene_caption(i)
            scene_music(i)
            self.scenes[i].main_loop()

            if self.scenes[i].turnback:
                i -= 1
                self.scenes[i].turnback = False
            else:
                i += 1

            if i == len(self.scenes) or i < 0:
                i = 0

    def __del__(self):
        print(__author__)
