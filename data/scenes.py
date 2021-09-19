from .manager import *
from .sprites import Paddle, Ball, Tile, Canvas


class Scene():

    score = SCORE
    level = LEVEL
    turnback = False

    def __init__(self, screen):
        self.screen = screen
        self.clock = clock
        self.highscore = self.load_data()

    def load_data(self):
        try:
            with open(file="highscore", mode='rb') as file:
                highscore = pickle.load(file)
        except: highscore = HIGHSCORE

        if self.score > highscore:
            highscore = self.score
            self.new_highscore = True
        else: self.new_highscore = False

        with open(file=HS_FILE, mode='wb') as file:
            pickle.dump(highscore, file)

        return highscore


class Menu(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.logo = pg.image.load("resources/images/arkanoid_logo.png")

        self.text_score = Canvas(size=24, center=True, y=HEIGHT//2.6, color=BLACK, letter_f=FONTS[1])
        self.text_highscore = Canvas(size=24, center=True, y=HEIGHT//2.3, color=BLACK, letter_f=FONTS[1])
        self.text_play = Canvas(size=44, center=True, y=HEIGHT//1.7, color=GREEN)
        self.text_level = Canvas(size=34, center=True, y=HEIGHT//1.5, color=BLACK)
        self.text_exit = Canvas(size=34, center=True, y=HEIGHT//1.22, color=RED)

        self.text_play.text = "Press <SPC> to Play"
        self.text_exit.text = "Press <ESC> to Exit"

        self.text_group = pg.sprite.Group()
        self.text_group.add(self.text_score, self.text_highscore, self.text_play, self.text_level, self.text_exit)

        self.resize = RESIZE

    def main_loop(self):
        highscore = self.load_data()
        resize = self.resize
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()

                    if event.key == pg.K_SPACE:
                        run = False

                    if event.key == pg.K_UP:
                        if Scene.level < 20:
                            Scene.level += 1
                        else: Scene.level = 1
                        select_fx.play()

                    if event.key == pg.K_DOWN:
                        if Scene.level > 1:
                            Scene.level -= 1
                        else: Scene.level = 20
                        select_fx.play()

                    if event.key == pg.K_LEFT:
                        if resize > 0:
                            resize -= 1
                        else: resize = len(SCREEN_SIZE) -1
                        screen_size(resize)
                        select_fx.play()

                    if event.key == pg.K_RIGHT:
                        if resize < len(SCREEN_SIZE) -1:
                            resize += 1
                        else : resize = 0
                        screen_size(resize)
                        select_fx.play()

            self.text_score.text = f"Score:  {Scene.score}"
            self.text_highscore.text = f"Highscore:  {highscore}"
            self.text_level.text = f"Press <UP or DOWN> to Level:  {Scene.level}"

            self.screen.fill(SILVER)
            self.screen.blit(self.logo, ((WIDTH-LOGO)//2, (WIDTH-LOGO)//2))
            self.text_group.update(FPS)
            self.text_group.draw(self.screen)

            pg.display.flip()


class Game(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.background = pg.image.load("resources/images/background.jpg")
        self.player = Paddle(midbottom=(WIDTH // 2, HEIGHT - 15))
        self.ball = Ball(center=(self.player.rect.x + self.player.rect.w//2, self.player.rect.y - 30))

        self.paused = Canvas(size=80, center=True, y=HEIGHT//3, color=RED)
        self.vol_browse = Canvas(center=True, y=HEIGHT//2, color=YELLOW)

        self.text_lives = Canvas(size=26, color=YELLOW)
        self.text_level = Canvas(size=26, center=True, color=LIME)
        self.text_score = Canvas(size=26, right_text=True, color=RED)
        self.view_lives = Canvas(y=40, letter_f=FONTS[1])
        self.view_level = Canvas(y=40, center=True, letter_f=FONTS[1])
        self.view_score = Canvas(y=40, right=True, letter_f=FONTS[1])

        self.settings = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.all = pg.sprite.Group()

    def reset(self):
        self.lives = 2
        self.points = 0
        self.next_level()

    def next_level(self):
        self.lives += 1

        self.tiles.empty()
        self.all.empty()

        self.ball.reset()
        self.player.reset()

        for row in range(Scene.level):
            for column in range(6):
                tile = Tile(column * 90 + 30, row * 30 + 90)
                self.tiles.add(tile)

        self.all.add(self.tiles, self.ball, self.player,
        self.text_lives, self.text_level, self.text_score,
        self.view_lives, self.view_level, self.view_score)

        self.settings.add(self.paused, self.vol_browse)

    def main_loop(self):
        highscore = self.load_data()
        Scene.turnback = False
        self.reset()
        game_run_fx.play()

        vol = volume()
        pause = False
        run = True
        while run:
            tick = self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False

                    if event.key == pg.K_SPACE:
                        if pause:
                            pause = False
                        else: pause = True
                        pause_fx.play()

                    if event.key == pg.K_UP and volume() < 1.0:
                        vol = volume(+ 0.1)
                        pg.mixer.music.set_volume(vol)
                        select_fx.play()

                    if event.key == pg.K_DOWN and volume() > 0.0:
                        vol = volume(- 0.1)
                        pg.mixer.music.set_volume(vol)
                        select_fx.play()

                    if event.key == pg.K_RETURN:
                        Scene.turnback = True
                        run = False

            self.paused.text = "P A U S E"

            if vol == 0.0 or vol == 1.0:
                self.vol_browse.color = ORANGE
            else: self.vol_browse.color = YELLOW
            self.vol_browse.text = f"Press <UP or DOWN> to vol:  {vol}"

            self.text_lives.text = "Lives"
            self.text_level.text = "~ level ~"
            if self.points > highscore:
                self.text_score.x = WIDTH-200
                self.text_score.text = "New  Highscore"
            else: self.text_score.text = f"{highscore}  Score"
            self.view_lives.text = self.lives
            self.view_level.text = Scene.level
            self.view_score.text = self.points
            if not pause:
                self.all.update(tick)
            self.settings.update(tick)

            self.ball.check_collision(self.player, knock_fx)

            collided = pg.sprite.spritecollide(self.ball, self.tiles, True)
            if len(collided) > 0:
                self.ball.dy *= -1
                self.points += len(collided) * 10
                break_fx.play()
            elif len(self.tiles) == 0:
                if Scene.level < 20:
                    Scene.level += 1
                self.ball.speed += 1
                self.player.speed += 1
                self.next_level()
                win_fx.play()

            if not self.ball.is_live:
                self.lives -= 1
                self.ball.is_live = True
                self.player.reset()
                timer(2, on=game_over_fx.play())

                if self.lives == 0:
                    run = False

                if self.ball.speed and self.player.speed > 0:
                    self.ball.speed -= 1
                    self.player.speed -= 1

            width = self.background.get_width()
            height = self.background.get_height()
            for scroll_x in range(2):
                for scroll_y in range(2):
                    self.screen.blit(self.background, ((scroll_x * width - self.ball.rect.x * 0.2), (scroll_y * height - self.ball.rect.y * 0.2)))

            self.all.draw(self.screen)
            if pause:
                self.settings.draw(self.screen)

            pg.display.flip()

        Scene.score = self.points


class Record(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        self.logo = pg.image.load("resources/images/game_over.png")

        self.text_score = Canvas(size=24, center=True, y=HEIGHT//2.6, letter_f=FONTS[1])
        self.text_highscore = Canvas(size=24, center=True, y=HEIGHT//2.3, letter_f=FONTS[1])
        self.text_continue = Canvas(size=44, center=True, y=HEIGHT//1.7, color=GREEN)
        self.text_replay = Canvas(size=40, center=True, y=HEIGHT//1.5, color=YELLOW)
        self.text_exit = Canvas(size=34, center=True, y=HEIGHT//1.22, color=RED)

        self.text_continue.text = "Press <SPC> to Continue"
        self.text_replay.text = "Press <ENTER> to Menu"
        self.text_exit.text = "Press <ESC> to Exit"

        self.text_group = pg.sprite.Group()
        self.text_group.add(self.text_score, self.text_highscore, self.text_replay, self.text_continue, self.text_exit)

    def main_loop(self):
        highscore = self.load_data()
        Scene.turnback = False
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()

                    if event.key == pg.K_SPACE:
                        Scene.turnback = True
                        run = False

                    if event.key == pg.K_RETURN:
                        run = False

            self.text_score.text = f"Score:  {Scene.score}"
            if self.new_highscore:
                self.text_highscore.text = "NEW HIGHSCORE"
            else: self.text_highscore.text = f"Highscore:  {highscore}"

            self.screen.fill(BLACK)
            self.screen.blit(self.logo, ((WIDTH-LOGO)//2, (WIDTH-LOGO)//2))
            self.text_group.update(FPS)
            self.text_group.draw(self.screen)
            pg.display.flip()
