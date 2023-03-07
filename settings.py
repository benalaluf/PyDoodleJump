# -*- coding: utf-8 -*-
import pygame.image
from pygame.font import SysFont
from pygame import init

init()
# ==================================

# Window Settings
XWIN, YWIN = 650, 950  # Resolution
HALF_XWIN, HALF_YWIN = XWIN / 2, YWIN / 2  # Center
DISPLAY = (XWIN, YWIN)
FLAGS = 1  # Fullscreen, resizeable...
FPS = 80  # Render frame rate

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 50)
LIGHT_GREEN = (30, 144, 255)
ANDROID_GREEN = (164, 198, 57)
FOREST_GREEN = (87, 189, 68)

# Player
PLAYER_SIZE = (70,68 )
PLAYER_IMAGE_RIGHT = "images/lik-right@2x.png"
PLAYER_IMAGE_LEFT = "images/lik-left@2x.png"
PLAYER_COLOR = ANDROID_GREEN
PLAYER_MAX_SPEED = 15
PLAYER_JUMPFORCE = 15
PLAYER_SPRING_JUMPFORCE = 50
PLAYER_TRAMP_JUMPFORCE = 40
GRAVITY = .4

# Platforms
PLATFORM_COLOR = FOREST_GREEN
PLATFORM_COLOR_LIGHT = LIGHT_GREEN
PLATFORM_BASE_IMAGE = "images/baseplatform.png"
PLATFORM_BREAKABLE_IMAGE = "images/breakableplatform.png"
PLATFORM_SPRING_IMAGE = "images/spring.png"
PLATFORM_SPRING_OPEN_IMAGE = "images/spring opend.png"
PLATFORM_TRAMP_IMAGE = "images/trampolin.png"
PLATFORM_SIZE = (85, 23)
PLATFORM_DISTANCE_GAP = (40, 210)
MAX_PLATFORM_NUMBER = 15
SPRING_SPAWN_CHANCE = 15
TRAMP_SPAWN_CHANCE = 20
BREAKABLE_PLATFORM_CHANCE = 12

# Fonts
LARGE_FONT = SysFont("arial-bold", 128)
SMALL_FONT = SysFont("", 60)
