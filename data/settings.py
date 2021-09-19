# Standard screen resolutions
VGA  = (640, 480)   # SCREEN_SIZE[0]
SVGA = (800, 600)   # SCREEN_SIZE[1]
XGA  = (1024, 768)  # SCREEN_SIZE[2]
XVGA = (1280, 1024) # SCREEN_SIZE[3]

SCREEN_SIZE = (VGA, SVGA, XGA, XVGA)

# Game window
RESIZE = 1
WIDTH = SCREEN_SIZE[RESIZE][1]
HEIGHT = SCREEN_SIZE[RESIZE][0]

# Set framerate
FPS = 60

# Define caption & scene music
CAPTION = ('M e n u', 'G a m e', 'R e c o r d')
SCENE_MUSIC = ("music_menu", "music_game", "music_record")

# Define game variables
FONTS = ("CabinSketch", "Fixedsys500c", "LibreFranklin", "PoetsenOne-Regular")
LOGO = 500
LEVEL = 1

# Define highscore
HS_FILE = "highscore"
HIGHSCORE = 0
SCORE = 0

# Define colours (R, G, B)
BLACK = (0, 0, 0)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)

BROWN = (255, 192, 192)
MAROON = (128, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
GREEN = (0, 128, 0)
LIME = (0, 255, 0)
OLIVE = (128, 128, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
SKY = (0, 128, 255)
TEAL = (0, 128, 128)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
PINK = (255, 0, 255)
PURPLE = (128, 0, 128)
