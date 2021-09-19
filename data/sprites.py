from .manager import *


class Paddle(pg.sprite.Sprite):
    sprite_list = []
    for img in range(3):
        sprite_list.append(f"paddle_{img}.png")

    def __init__(self, **kwargs):
        super().__init__()
        self.images = []
        for sprite in self.sprite_list:
            self.images.append(pg.image.load(f"resources/images/{sprite}"))
        self.current_img = 0

        self.time_elapsed = 0
        self.sprite_change_time = 1000 // FPS * 5

        self.init_pos = kwargs
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect(**kwargs)

        self.speed = 0

    def reset(self):
        self.rect = self.image.get_rect(**self.init_pos)

    def update(self, dt):
        if pg.key.get_pressed()[pg.K_LEFT] and not self.rect.left <= 0:
            self.rect.x -= 5 + self.speed

        if pg.key.get_pressed()[pg.K_RIGHT] and not self.rect.right >= WIDTH:
            self.rect.x += 5 + self.speed

        self.time_elapsed += dt
        if self.time_elapsed >= self.sprite_change_time:
            self.current_img += 1
            if self.current_img >= len(self.images):
                self.current_img = 0

            self.time_elapsed = 0

        self.image = self.images[self.current_img]


class Ball(pg.sprite.Sprite):
    sprite_list = []
    for img in range(5):
        sprite_list.append(f"ball_{img}.png")

    def __init__(self, **kwargs):
        super().__init__()
        self.images = []
        for sprite in self.sprite_list:
            self.images.append(pg.image.load(f"resources/images/{sprite}"))
        self.current_img = 0

        self.time_elapsed = 0
        self.sprite_change_time = 1000 // FPS * 5

        self.init_pos = kwargs
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect(**kwargs)

        self.speed = 0
        self.dx = 5
        self.dy = 5
        self.is_live = True

    def update(self, dt):
        self.rect.x += self.dx
        if self.rect.x <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1

        self.rect.y += self.dy
        if self.rect.y <= 0:
            self.dy *= -1

        if self.rect.bottom >= HEIGHT:
            self.dx = self.dy = 0

            if self.current_img == -1:
                self.current_img = 0
                self.is_live = False
                self.reset()
            else:
                self.time_elapsed += dt
                if self.time_elapsed >= self.sprite_change_time:
                    self.current_img += 1
                    if self.current_img >= len(self.images):
                        self.current_img = -1

                    self.time_elapsed = 0

        self.image = self.images[self.current_img]

    def reset(self):
        self.rect = self.image.get_rect(**self.init_pos)
        self.dx = 5 + self.speed
        self.dy = - (5 + self.speed)

    def check_collision(self, other, fx=None):
        if self.rect.right >= other.rect.left and self.rect.left <= other.rect.right and \
           self.rect.bottom >= other.rect.top and self.rect.top <= other.rect.bottom:
            self.dy *= -1
            fx.play()


class Tile(pg.sprite.Sprite):
    sprite = "tile_1.png"

    def __init__(self, x=5, y=5):
        super().__init__()
        self.image = pg.image.load(f"resources/images/{self.sprite}")
        self.rect = self.image.get_rect(x=x, y=y)


class Canvas(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()
        self._text = ""
        self.kwargs = kwargs

        self.x = self._keys('x') or self.is_right() or 20
        self.y = self._keys('y') or 10
        self.letter_f = self._keys('letter_f') or FONTS[0]
        self.size = self._keys('size') or 28
        self.color = self._keys('color') or (WHITE)

        self.font = pg.font.Font(
            f"resources/fonts/{self.letter_f}.ttf", self.size)
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def update(self, dt):
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.is_right_text()
        self.is_right()
        self.is_center()

    def _keys(self, key):
        return key in self.kwargs.keys() and self.kwargs[key]

    def is_right_text(self):
        if self._keys('right_text'):
            self.x = WIDTH - (20 + len(self.text) * 12)

    def is_right(self):
        if self._keys('right'):
            self.x = WIDTH - (20 + len(self.text) * 15)

    def is_center(self):
        if self._keys('center'):
            self.x = WIDTH // 2 - self.rect.w // 2

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
