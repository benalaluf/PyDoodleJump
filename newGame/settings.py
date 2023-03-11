# -*- coding: utf-8 -*-
import pygame.image
from pygame.font import SysFont
from pygame import init


class Theme():
    def __init__(self):
        self.theme = 'r'

    def setTheme(self, theme):
        self.theme = theme
        print('theme set to', theme)

    def getTheme(self):
        return self.theme


init()
# ==================================

# Window Settings
XWIN, YWIN = 640, 1024  # Resolution
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2  # Center
DISPLAY = (XWIN, YWIN)
FLAGS = 0  # Fullscreen, resizeable...
FPS = 60  # Render frame rate

# Theme
instant = Theme()
theme = instant.getTheme()

# Player
PLAYER_SIZE = (60, 58)
BULLET_SIZE = (15, 15)

BULLET_SPEED = 60
PLAYER_MAX_SPEED = 15
PLAYER_JUMPFORCE = 15
PLAYER_SPRING_JUMPFORCE = 50
PLAYER_TRAMP_JUMPFORCE = 40
GRAVITY = .45
# allimages
PLATFORM_SIZE = (80, 20)
TRAMP_SIZE = (45, 20)
SPRING_SIZE = (20, 17)


def setTheme(t):
    global theme
    theme = t



BACKGROUND = pygame.image.load(f'images/{theme}/background.png')
PLAYER_IMAGE_RIGHT = pygame.transform.scale(pygame.image.load(f"images/{theme}/doodle_r.png"), PLAYER_SIZE)
PLAYER_IMAGE_JUMP_RIGHT = pygame.transform.scale(pygame.image.load(f"images/{theme}/doodle_jump.png"), PLAYER_SIZE)
PLAYER_IMAGE_LEFT = pygame.transform.flip(PLAYER_IMAGE_RIGHT, True, False)
PLAYER_IMAGE_JUMP_LEFT = pygame.transform.flip(PLAYER_IMAGE_JUMP_RIGHT, True, False)
MONSTER_IMAGE = pygame.image.load('images/monster.png')
PLAYER_IMAGE_SHOOT = pygame.transform.scale(pygame.image.load(f"images/shoot_player.png"), (40, 80))
BULLET_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/bullet.png"), BULLET_SIZE)
PLATFORM_BASE_IMAGE = pygame.transform.scale(pygame.image.load(f"images/r/baseplatform.png"), PLATFORM_SIZE)
PLATFORM_BREAKABLE_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/breakableplatform.png"),
                                                  PLATFORM_SIZE)
PLATFORM_MOVEABLE_IMGAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/moveplatform.png"),
                                                  PLATFORM_SIZE)
PLATFORM_SPRING_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/spring.png"), SPRING_SIZE)
PLATFORM_SPRING_OPEN_IMAGE = pygame.image.load(f"images/{theme}/spring opend.png")
PLATFORM_TRAMP_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/trampolin.png"), TRAMP_SIZE)

def loadTheme():
    global BACKGROUND, PLAYER_IMAGE_RIGHT, PLAYER_IMAGE_JUMP_RIGHT, PLAYER_IMAGE_LEFT, PLAYER_IMAGE_JUMP_LEFT
    global MONSTER_IMAGE, PLAYER_IMAGE_SHOOT, BULLET_IMAGE, PLATFORM_BASE_IMAGE, PLATFORM_BREAKABLE_IMAGE
    global PLATFORM_MOVEABLE_IMGAGE, PLATFORM_SPRING_IMAGE, PLATFORM_SPRING_OPEN_IMAGE, PLATFORM_TRAMP_IMAGE
    BACKGROUND = pygame.image.load(f'images/{theme}/background.png')
    PLAYER_IMAGE_RIGHT = pygame.transform.scale(pygame.image.load(f"images/{theme}/doodle_r.png"), PLAYER_SIZE)
    PLAYER_IMAGE_JUMP_RIGHT = pygame.transform.scale(pygame.image.load(f"images/{theme}/doodle_jump.png"), PLAYER_SIZE)
    PLAYER_IMAGE_LEFT = pygame.transform.flip(PLAYER_IMAGE_RIGHT, True, False)
    PLAYER_IMAGE_JUMP_LEFT = pygame.transform.flip(PLAYER_IMAGE_JUMP_RIGHT, True, False)
    MONSTER_IMAGE = pygame.image.load('images/monster.png')
    PLAYER_IMAGE_SHOOT = pygame.transform.scale(pygame.image.load(f"images/shoot_player.png"), (40, 80))
    BULLET_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/bullet.png"), BULLET_SIZE)
    PLATFORM_BASE_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/baseplatform.png"), PLATFORM_SIZE)
    PLATFORM_BREAKABLE_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/breakableplatform.png"),
                                                      PLATFORM_SIZE)
    PLATFORM_MOVEABLE_IMGAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/moveplatform.png"),
                                                      PLATFORM_SIZE)
    PLATFORM_SPRING_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/spring.png"), SPRING_SIZE)
    PLATFORM_SPRING_OPEN_IMAGE = pygame.image.load(f"images/{theme}/spring opend.png")
    PLATFORM_TRAMP_IMAGE = pygame.transform.scale(pygame.image.load(f"images/{theme}/trampolin.png"), TRAMP_SIZE)


# Platforms


PLATFORM_DISTANCE_GAP = (30, 120)
MAX_PLATFORM_NUMBER = 35
SPRING_SPAWN_CHANCE = 30
TRAMP_SPAWN_CHANCE = 30
BREAKABLE_PLATFORM_CHANCE = 15
MOVEABLE_PLATFORM_CHANCE = 10

SPRING_IMAGES = (PLATFORM_SPRING_IMAGE, PLATFORM_SPRING_OPEN_IMAGE)
TRAMP_IMAGES = (PLATFORM_TRAMP_IMAGE, PLATFORM_TRAMP_IMAGE)

# Fonts
LARGE_FONT = SysFont("arial-bold", 100)
SMALL_FONT = SysFont("arial-bold", 50)

# Menu
MENU_FONT = "arial-bold"
MENU_TEXT_COLOR = "white"
GRAY = [30, 30, 30]
