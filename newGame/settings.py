# -*- coding: utf-8 -*-
import pygame.image
from pygame.font import SysFont
from pygame import init

init()
# ==================================

# Window Settings
XWIN, YWIN = 650, 1000  # Resolution
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2  # Center
DISPLAY = (XWIN, YWIN)
FLAGS = 0  # Fullscreen, resizeable...
FPS = 60  # Render frame rate

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 50)
LIGHT_GREEN = (30, 144, 255)
ANDROID_GREEN = (164, 198, 57)
FOREST_GREEN = (87, 189, 68)

# Player
PLAYER_SIZE = (60, 58)
BULLET_SIZE = (15,15)
PLAYER_IMAGE_RIGHT = pygame.transform.scale(pygame.image.load("../images/doodle_right.png"), PLAYER_SIZE)
PLAYER_IMAGE_LEFT = pygame.transform.scale(pygame.image.load("../images/doodle_left.png"), PLAYER_SIZE)
PLAYER_IMAGE_SHOOT = pygame.transform.scale(pygame.image.load("../images/shoot_player.png"), (40, 80))
BULLET_IMAGE = pygame.transform.scale(pygame.image.load("../images/bullet.png"), BULLET_SIZE)
BULLET_SPEED = 60
PLAYER_COLOR = ANDROID_GREEN
PLAYER_MAX_SPEED = 15
PLAYER_JUMPFORCE = 15
PLAYER_SPRING_JUMPFORCE = 50
PLAYER_TRAMP_JUMPFORCE = 40
GRAVITY = .45

# Platforms
PLATFORM_COLOR = FOREST_GREEN
PLATFORM_SIZE = (80, 20)
PLATFORM_COLOR_LIGHT = LIGHT_GREEN
PLATFORM_BASE_IMAGE = pygame.transform.scale(pygame.image.load("../images/baseplatform.png"), PLATFORM_SIZE)
PLATFORM_BREAKABLE_IMAGE = pygame.transform.scale(pygame.image.load("../images/breakableplatform.png"), PLATFORM_SIZE)
TRAMP_SIZE = (45, 20)
SPRING_SIZE = (20, 17)

PLATFORM_SPRING_IMAGE = pygame.transform.scale(pygame.image.load("../images/spring.png"), SPRING_SIZE)
PLATFORM_SPRING_OPEN_IMAGE = pygame.image.load("../images/spring opend.png")
PLATFORM_TRAMP_IMAGE = pygame.transform.scale(pygame.image.load("../images/trampolin.png"), TRAMP_SIZE)
PLATFORM_DISTANCE_GAP = (40, 150)
MAX_PLATFORM_NUMBER = 30
SPRING_SPAWN_CHANCE = 10
TRAMP_SPAWN_CHANCE = 12
BREAKABLE_PLATFORM_CHANCE = 12

# Fonts
LARGE_FONT = SysFont("arial-bold", 100)
SMALL_FONT = SysFont("arial-bold", 70)

# Menu
MENU_FONT = "arial-bold"
MENU_TEXT_COLOR = "white"
